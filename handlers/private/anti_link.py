from aiogram import types

from loader import dp
from utils.anti_badwords import detect_badword_reason
from utils.anti_link import detect_link_reason


@dp.message_handler(
    is_regular_member=True,
    content_types=types.ContentTypes.ANY
)
async def moderation_handler(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    # service message skip
    if message.new_chat_members or message.left_chat_member:
        return

    text = (message.text or "") + "\n" + (message.caption or "")

    has_link = detect_link_reason(message)
    bad_word = detect_badword_reason(text)

    if not has_link and not bad_word:
        return

    try:
        await message.delete()
    except Exception:
        return

    # optional: warning
    try:
        if has_link:
            reason = "link yuborish taqiqlangan"
        else:
            reason = "haqoratli so‘z ishlatish mumkin emas"

        await message.answer(
            f"⚠️ {message.from_user.full_name}, {reason}."
        )
    except Exception:
        pass
