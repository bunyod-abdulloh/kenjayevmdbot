import re
from typing import Optional

from aiogram import types

# Domen ko‘rinishlari
DOMAIN_RE = re.compile(
    r"\b(?:[a-z0-9-]+\.)+(?:com|net|org|info|biz|io|ai|ru|uz|me|tv|cc|ly|app|dev|shop|site|online|store|co)\b",
    re.IGNORECASE
)

# Oddiy URL lar
URL_RE = re.compile(
    r"(https?://\S+|www\.\S+)",
    re.IGNORECASE
)

# Telegram linklari
TG_LINK_RE = re.compile(
    r"(?:https?://)?(?:t\.me|telegram\.me|telegram\.dog)/[^\s]+",
    re.IGNORECASE
)

# Yashirin ko‘rinishlar: t me / telegram me / telegram dog
BROKEN_TG_RE = re.compile(
    r"\b(?:t\s*\.?\s*me|telegram\s*\.?\s*(?:me|dog))\s*/?\s*[a-z0-9_+/-]+\b",
    re.IGNORECASE
)

# @username
USERNAME_RE = re.compile(
    r"(?<![A-Za-z0-9_])@[A-Za-z][A-Za-z0-9_]{3,31}\b"
)

# joinchat yoki + invite
INVITE_RE = re.compile(
    r"\b(?:joinchat/|\+[A-Za-z0-9_-]{10,})",
    re.IGNORECASE
)

# dot / nuqta bilan yozilgan domenlar
OBFUSCATED_DOMAIN_RE = re.compile(
    r"\b[a-z0-9-]+\s*(?:\.|dot|nuqta)\s*[a-z0-9-]+\s*(?:\.|dot|nuqta)\s*[a-z]{2,}\b",
    re.IGNORECASE
)

# oddiy ikki bo‘lak domen: example dot com
OBFUSCATED_SIMPLE_DOMAIN_RE = re.compile(
    r"\b[a-z0-9-]+\s*(?:\.|dot|nuqta)\s*(?:com|net|org|info|biz|io|ai|ru|uz|me|tv|cc|ly|app|dev|shop|site|online|store|co)\b",
    re.IGNORECASE
)

# reklamaga o‘xshash iboralar
PROMO_WORDS_RE = re.compile(
    r"\b(obuna\s*bo['’]ling|kanalimiz|kanalga\s*kiring|gruppaga\s*kiring|guruhga\s*kiring|link|ssilka|havola)\b",
    re.IGNORECASE
)


def normalize_text(text: str) -> str:
    text = text.lower()

    replacements = {
        " dot ": ".",
        " nuqta ": ".",
        "(dot)": ".",
        "[dot]": ".",
        " h t t p s ": " https ",
        " h t t p ": " http ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # t me -> t.me
    text = re.sub(r"\bt\s+me\b", "t.me", text, flags=re.IGNORECASE)
    text = re.sub(r"\btelegram\s+me\b", "telegram.me", text, flags=re.IGNORECASE)
    text = re.sub(r"\btelegram\s+dog\b", "telegram.dog", text, flags=re.IGNORECASE)

    return text


def extract_message_text(message: types.Message) -> str:
    parts = []

    if message.text:
        parts.append(message.text)

    if message.caption:
        parts.append(message.caption)

    return "\n".join(parts).strip()


def message_has_link_entities(message: types.Message) -> bool:
    entities = []

    if message.entities:
        entities.extend(message.entities)

    if message.caption_entities:
        entities.extend(message.caption_entities)

    for entity in entities:
        if entity.type in {"url", "text_link", "mention"}:
            return True

    return False


def is_forwarded_message(message: types.Message) -> bool:
    return bool(
        message.forward_from
        or message.forward_from_chat
        or message.forward_sender_name
        or message.forward_date
    )


def detect_link_reason(message: types.Message) -> Optional[str]:
    raw_text = extract_message_text(message)
    normalized = normalize_text(raw_text) if raw_text else ""

    # Telegram entity ichida yashirin link bo‘lsa
    if message_has_link_entities(message):
        return "entity_link"

    if raw_text:
        if URL_RE.search(raw_text):
            return "url"

        if TG_LINK_RE.search(raw_text):
            return "telegram_link"

        if USERNAME_RE.search(raw_text):
            return "username"

        if INVITE_RE.search(raw_text):
            return "invite"

        if DOMAIN_RE.search(raw_text):
            return "domain"

    if normalized:
        if BROKEN_TG_RE.search(normalized):
            return "broken_telegram_link"

        if OBFUSCATED_DOMAIN_RE.search(normalized):
            return "obfuscated_domain"

        if OBFUSCATED_SIMPLE_DOMAIN_RE.search(normalized):
            return "obfuscated_simple_domain"

        # promo so'z + domen yoki username ko‘rinishi
        if PROMO_WORDS_RE.search(normalized):
            if DOMAIN_RE.search(normalized) or USERNAME_RE.search(normalized) or "t.me" in normalized:
                return "promo_link"

    return None
