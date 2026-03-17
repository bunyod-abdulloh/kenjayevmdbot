from aiogram import executor

from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_HOST
from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands



WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)

    except Exception as e:
        pass

    try:
        await on_startup_notify(dispatcher)

    except Exception as e:
        pass

    try:
        await bot.set_webhook(WEBHOOK_URL)
    except Exception as e:
        pass


async def on_shutdown(dispatcher):
    # webhookni o‘chirib qo‘yamiz
    await bot.delete_webhook()

allowed_updates = ["message", "callback_query", "chat_join_request"]

if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        allowed_updates=allowed_updates,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
