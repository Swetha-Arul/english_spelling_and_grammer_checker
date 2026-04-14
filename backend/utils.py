import re


def normalize_word(word: str) -> str:
    return re.sub(r"^'+|'+$", "", word.lower())


def split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text)
    return [sentence.strip() for sentence in parts if sentence.strip()]
