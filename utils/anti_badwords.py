import re
from typing import Optional

from utils.badwords import BAD_WORDS

WORD_RE = re.compile(r"[a-zA-Zа-яА-ЯёЁўқғҳʼ'`]+", re.UNICODE)


def normalize_text(text: str) -> str:
    text = text.lower()

    replacements = {
        "o‘": "o",
        "o'": "o",
        "g‘": "g",
        "g'": "g",
        "ʻ": "o",
        "ҳ": "х",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # harflarni cho‘zib yozish: jalaaab -> jalab
    text = re.sub(r"(.)\1{2,}", r"\1", text)

    return text


def detect_badword_reason(message_text: str) -> Optional[str]:
    if not message_text:
        return None

    text = normalize_text(message_text)

    words = WORD_RE.findall(text)

    for word in words:
        if word in BAD_WORDS:
            return word

    return None
