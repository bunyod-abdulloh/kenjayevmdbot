from aiogram import types
from aiogram.dispatcher import FSMContext
from magic_filter import F

from loader import dp, bot, redis_client
from utils.captcha import send_captcha, handle_captcha_answer
from utils.captcha_redis import get_pending_request, delete_pending_request
from utils.join_requests import handle_join_request


@dp.message_handler(F.text == "/bekor", state="*")
async def bekor_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Jarayon bekor qilindi!")


@dp.chat_join_request_handler()
async def join_request_handler(request: types.ChatJoinRequest):
    await handle_join_request(request, bot, redis_client)


@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args()

    if args == str(user_id):
        group_id = get_pending_request(redis_client, user_id)

        if not group_id:
            await message.answer(
                "⚠️ Siz uchun aktiv join request topilmadi.\n\n"
                "Avval guruhga qayta join request yuboring."
            )
            return

        delete_pending_request(redis_client, user_id)
        await send_captcha(bot, redis_client, message.from_user, group_id)
        return

    await message.answer(
        "👋 Salom!\n\n"
        "Bu bot guruhga kirish uchun tekshiruv botidir.\n\n"
        "Avval join request yuboring."
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("captcha:"))
async def captcha_callback(callback: types.CallbackQuery):
    await handle_captcha_answer(callback, bot, redis_client)
