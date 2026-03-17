from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import (
    ADMIN_GROUP,
    PENDING_REQUEST_TTL,
    JOIN_REQUEST_COOLDOWN,
)
from utils.captcha_redis import (
    save_pending_request,
    has_join_cooldown,
    set_join_cooldown,
    get_join_cooldown_ttl,
    is_temp_banned,
    get_temp_ban_ttl,
)
from utils.cas import check_cas


async def handle_join_request(request: types.ChatJoinRequest, bot, redis_client):
    user = request.from_user
    group_id = request.chat.id

    if group_id != ADMIN_GROUP:
        return

    if user.is_bot:
        await bot.decline_chat_join_request(group_id, user.id)

        return

    if await check_cas(user.id):
        await bot.decline_chat_join_request(group_id, user.id)

        return

    if is_temp_banned(redis_client, user.id):
        ban_ttl = get_temp_ban_ttl(redis_client, user.id)
        await bot.decline_chat_join_request(group_id, user.id)
        try:
            await bot.send_message(
                chat_id=request.user_chat_id,
                text=(
                    "🚫 Siz vaqtincha bloklangansiz.\n\n"
                    f"Qayta urinish uchun taxminan {ban_ttl} soniya kuting."
                )
            )
        except Exception:
            pass
        return

    if has_join_cooldown(redis_client, user.id):
        cooldown = get_join_cooldown_ttl(redis_client, user.id)
        await bot.decline_chat_join_request(group_id, user.id)
        try:
            await bot.send_message(
                chat_id=request.user_chat_id,
                text=(
                    "⏳ Juda tez-tez join request yuboryapsiz.\n\n"
                    f"{cooldown} soniyadan keyin qayta urinib ko'ring."
                )
            )
        except Exception:
            pass
        return

    set_join_cooldown(redis_client, user.id, JOIN_REQUEST_COOLDOWN)
    save_pending_request(redis_client, user.id, group_id, ttl=PENDING_REQUEST_TTL)

    bot_info = await bot.get_me()
    deep_link = f"https://t.me/{bot_info.username}?start={user.id}"

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="🤖 Tekshiruvdan o'tish",
            url=deep_link
        )
    )

    try:
        await bot.send_message(
            chat_id=request.user_chat_id,
            text=(
                f"👋 Salom, {user.full_name}!\n\n"
                "Guruhga kirish uchun tekshiruvdan o'ting.\n"
                "Quyidagi tugmani bosing:"
            ),
            reply_markup=keyboard
        )
    except Exception as e:
        pass
