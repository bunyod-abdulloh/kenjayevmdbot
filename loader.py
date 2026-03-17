from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from redis import Redis

from data import config
from data.config import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD
from utils.db_api.admins_db import AdminsDB
from utils.db_api.create_tables import Database
from utils.db_api.groups_db import GroupsDB
from utils.db_api.referrals_db import ReferralsDB
from utils.db_api.users_db import UsersDB

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
db = Database()
udb = UsersDB(db)
refdb = ReferralsDB(db)
admdb = AdminsDB(db)
grpdb = GroupsDB(db)
