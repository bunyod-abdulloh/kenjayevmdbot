from aiogram import types

from loader import dp
from utils.anti_link import detect_link_reason


@dp.message_handler(
    is_regular_member=True,
    content_types=types.ContentTypes.ANY
)
async def anti_link_handler(message: types.Message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    # service xabarlarni o'tkazamiz
    if message.new_chat_members or message.left_chat_member:
        return

    reason = detect_link_reason(message)
    if not reason:
        return

    try:
        await message.delete()
    except Exception:
        return
