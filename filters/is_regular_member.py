from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import bot, redis_client


class IsRegularMemberFilter(BoundFilter):
    key = "is_regular_member"

    def __init__(self, is_regular_member):
        self.is_regular_member = is_regular_member

    async def check(self, message: types.Message):
        if not message.from_user:
            return False

        if message.from_user.is_bot:
            return False

        chat_id = message.chat.id
        user_id = message.from_user.id

        cache_key = f"chat_member_status:{chat_id}:{user_id}"
        cached_status = redis_client.get(cache_key)

        if cached_status:
            result = cached_status in ["member", "restricted"]
            return result == self.is_regular_member

        try:
            member = await bot.get_chat_member(chat_id, user_id)
            status = member.status

            redis_client.setex(cache_key, 120, status)

            result = status in ["member", "restricted"]
            return result == self.is_regular_member

        except Exception as e:
            return False
