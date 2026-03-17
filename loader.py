from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from redis import Redis

from data import config
from data.config import REDIS_HOST, REDIS_PORT, REDIS_DB

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    # password=REDIS_PASSWORD,
    decode_responses=True,  # string qaytarsin
)
dp = Dispatcher(bot, storage=storage)
