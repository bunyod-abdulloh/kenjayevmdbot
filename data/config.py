from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
BOT_ID = env.int("BOT_ID")
ADMIN_GROUP = env.int("ADMIN_GROUP")
IP = env.str("IP")

MAX_ATTEMPTS = env.int("MAX_ATTEMPTS")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")
REDIS_DB = env.int("REDIS_DB")
CAPTCHA_TTL = env.int("CAPTCHA_TTL")
PENDING_REQUEST_TTL = env.int("PENDING_REQUEST_TTL")
JOIN_REQUEST_COOLDOWN = env.int("JOIN_REQUEST_COOLDOWN")
FAILED_CAPTCHA_LIMIT = env.int("FAILED_CAPTCHA_LIMIT")
FAILED_CAPTCHA_BAN_TTL = env.int("FAILED_CAPTCHA_BAN_TTL")


WEBHOOK_HOST = env.str("WEBHOOK_HOST")
WEBHOOK_PATH = env.str("WEBHOOK_PATH")
WEBAPP_HOST = env.str("WEBAPP_HOST")
WEBAPP_PORT = env.int("WEBAPP_PORT")
