import random

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import (
    MAX_ATTEMPTS,
    CAPTCHA_TTL,
    FAILED_CAPTCHA_LIMIT,
    FAILED_CAPTCHA_BAN_TTL,
)
from utils.captcha_redis import (
    save_captcha,
    get_captcha,
    delete_captcha,
    refresh_captcha,
    increment_failed_captcha,
    reset_failed_captcha_count,
    set_temp_ban,
)
from utils.math_captcha import generate_captcha


async def send_captcha(bot, redis_client, user: types.User, group_id: int):
    old_captcha = get_captcha(redis_client, user.id)
    if old_captcha and old_captcha.get("message_id"):
        try:
            await bot.delete_message(chat_id=user.id, message_id=int(old_captcha["message_id"]))
        except Exception:
            pass

    question, answer = generate_captcha()

    wrong_answers = set()
    while len(wrong_answers) < 3:
        fake = answer + random.randint(-10, 10)
        if fake > 0 and fake != answer:
            wrong_answers.add(fake)

    options = list(wrong_answers) + [answer]
    random.shuffle(options)

    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(
            text=str(opt),
            callback_data=f"captcha:{opt}"
        )
        for opt in options
    ]
    keyboard.add(*buttons)

    sent = await bot.send_message(
        chat_id=user.id,
        text=(
            f"👋 Salom, {user.full_name}!\n\n"
            f"Guruhga kirish uchun quyidagi savolga javob bering:\n\n"
            f"🧮 <b>{question}</b>\n\n"
            f"⚠️ {MAX_ATTEMPTS} ta noto'g'ri urinishdan so'ng shu request bekor qilinadi.\n"
            f"⏳ Captcha {CAPTCHA_TTL // 60} minut amal qiladi."
        ),
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    captcha_data = {
        "answer": answer,
        "attempts": 0,
        "group_id": group_id,
        "question": question,
        "message_id": sent.message_id,
    }
    save_captcha(redis_client, user.id, captcha_data, ttl=CAPTCHA_TTL)


async def handle_captcha_answer(callback: types.CallbackQuery, bot, redis_client):
    user_id = callback.from_user.id

    try:
        _, chosen_str = callback.data.split(":")
        chosen = int(chosen_str)
    except Exception:
        await callback.answer("⚠️ Noto'g'ri callback.", show_alert=True)
        return

    captcha_data = get_captcha(redis_client, user_id)

    if not captcha_data:
        await callback.answer(
            "⚠️ Captcha topilmadi yoki vaqti tugagan.",
            show_alert=True
        )
        try:
            await callback.message.edit_text(
                "⚠️ Captcha topilmadi yoki vaqti tugagan.\n\nQaytadan join request yuboring."
            )
        except Exception:
            pass
        return

    correct = int(captcha_data["answer"])
    attempts = int(captcha_data["attempts"])
    group_id = int(captcha_data["group_id"])

    if chosen == correct:
        delete_captcha(redis_client, user_id)
        reset_failed_captcha_count(redis_client, user_id)

        try:
            await bot.approve_chat_join_request(group_id, user_id)
        except Exception as e:
            await callback.answer("⚠️ Qabul qilishda xatolik yuz berdi.", show_alert=True)

            return

        await callback.message.edit_text(
            "✅ To'g'ri javob!\n\n"
            "Guruhga muvaffaqiyatli qo'shildingiz. Xush kelibsiz! 🎉"
        )
        await callback.answer()
        return

    attempts += 1
    remaining = MAX_ATTEMPTS - attempts

    if attempts >= MAX_ATTEMPTS:
        delete_captcha(redis_client, user_id)

        total_failed = increment_failed_captcha(redis_client, user_id)
        if total_failed >= FAILED_CAPTCHA_LIMIT:
            set_temp_ban(redis_client, user_id, FAILED_CAPTCHA_BAN_TTL)

        try:
            await bot.decline_chat_join_request(group_id, user_id)
        except Exception as e:
            pass

        text = (
            "❌ Urinishlar soni tugadi.\n\n"
            "Guruhga kirish rad etildi. Qaytadan urinib ko'ring."
        )

        if total_failed >= FAILED_CAPTCHA_LIMIT:
            text += (
                f"\n\n🚫 Siz vaqtincha bloklandingiz."
                f"\nTaxminan {FAILED_CAPTCHA_BAN_TTL // 60} minutdan keyin qayta urinib ko'ring."
            )

        await callback.message.edit_text(text)
        await callback.answer()
        return

    captcha_data["attempts"] = attempts
    refresh_captcha(redis_client, user_id, captcha_data, ttl=CAPTCHA_TTL)

    await callback.answer(
        f"❌ Noto'g'ri! Yana {remaining} ta urinish qoldi.",
        show_alert=True
    )
