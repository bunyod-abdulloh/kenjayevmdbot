import aiohttp


async def check_cas(user_id: int) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.cas.chat/check?user_id={user_id}"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                data = await resp.json()
                return data.get("ok", False)
    except Exception:
        return False
