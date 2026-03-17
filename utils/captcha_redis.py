import json


def captcha_key(user_id: int) -> str:
    return f"captcha:{user_id}"


def pending_request_key(user_id: int) -> str:
    return f"pending_request:{user_id}"


def cooldown_key(user_id: int) -> str:
    return f"join_cooldown:{user_id}"


def failed_count_key(user_id: int) -> str:
    return f"captcha_failed_total:{user_id}"


def temp_ban_key(user_id: int) -> str:
    return f"captcha_temp_ban:{user_id}"


# ---------------- PENDING REQUEST ----------------

def save_pending_request(redis_client, user_id: int, group_id: int, ttl: int):
    redis_client.setex(pending_request_key(user_id), ttl, str(group_id))


def get_pending_request(redis_client, user_id: int):
    value = redis_client.get(pending_request_key(user_id))
    return int(value) if value else None


def delete_pending_request(redis_client, user_id: int):
    redis_client.delete(pending_request_key(user_id))


# ---------------- CAPTCHA ----------------

def save_captcha(redis_client, user_id: int, data: dict, ttl: int):
    redis_client.setex(captcha_key(user_id), ttl, json.dumps(data))


def get_captcha(redis_client, user_id: int):
    raw = redis_client.get(captcha_key(user_id))
    if not raw:
        return None
    return json.loads(raw)


def delete_captcha(redis_client, user_id: int):
    redis_client.delete(captcha_key(user_id))


def refresh_captcha(redis_client, user_id: int, data: dict, ttl: int):
    redis_client.setex(captcha_key(user_id), ttl, json.dumps(data))


# ---------------- JOIN REQUEST COOLDOWN ----------------

def has_join_cooldown(redis_client, user_id: int) -> bool:
    return redis_client.exists(cooldown_key(user_id)) == 1


def set_join_cooldown(redis_client, user_id: int, ttl: int):
    redis_client.setex(cooldown_key(user_id), ttl, "1")


def get_join_cooldown_ttl(redis_client, user_id: int) -> int:
    ttl = redis_client.ttl(cooldown_key(user_id))
    return max(ttl, 0)


# ---------------- FAILED CAPTCHA COUNT ----------------

def increment_failed_captcha(redis_client, user_id: int) -> int:
    return redis_client.incr(failed_count_key(user_id))


def get_failed_captcha_count(redis_client, user_id: int) -> int:
    value = redis_client.get(failed_count_key(user_id))
    return int(value) if value else 0


def reset_failed_captcha_count(redis_client, user_id: int):
    redis_client.delete(failed_count_key(user_id))


# ---------------- TEMP BAN ----------------

def set_temp_ban(redis_client, user_id: int, ttl: int):
    redis_client.setex(temp_ban_key(user_id), ttl, "1")


def is_temp_banned(redis_client, user_id: int) -> bool:
    return redis_client.exists(temp_ban_key(user_id)) == 1


def get_temp_ban_ttl(redis_client, user_id: int) -> int:
    ttl = redis_client.ttl(temp_ban_key(user_id))
    return max(ttl, 0)
