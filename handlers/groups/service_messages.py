from aiogram import types

from loader import dp


@dp.message_handler(
    lambda message: message.new_chat_members or message.left_chat_member,
    content_types=types.ContentTypes.ANY
)
async def delete_service_messages(message: types.Message):
    try:
        await message.delete()
    except Exception as e:
        pass


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome_new_members(message: types.Message):
    for user in message.new_chat_members:
        if user.is_bot:
            continue

        try:
            await message.answer(
                text="🎉 Xush kelibsiz!\n\n"
                     "Guruh qoidalariga amal qiling."
            )
        except Exception as e:
            pass
