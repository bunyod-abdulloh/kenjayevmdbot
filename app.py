from aiogram import executor
import middlewares, filters, handlers

from data.config import WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_HOST
from loader import dp, bot
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

allowed_updates = ["message", "callback_query", "chat_join_request"]


async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)

    except Exception as e:
        print(f"SET DEFAULT COMMANDS ERROR: {e}")

    try:
        await on_startup_notify(dispatcher)

    except Exception as e:
        print(f"ON STARTUP ERROR: {e}")

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            allowed_updates=allowed_updates
        )
    except Exception as e:
        print(f"SET WEBHOOK_URL ERROR: {e}")


async def on_shutdown(dispatcher):
    # webhookni o‘chirib qo‘yamiz
    await bot.delete_webhook()


if __name__ == "__main__":
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
