from backend.dictionary import WORDS
from backend.utils import normalize_word


def is_accepted_inflection(word: str) -> bool:
    if not word:
        return False

    variants = []
    if word.endswith("s") and len(word) > 3:
        variants.append(word[:-1])
    if word.endswith("es") and len(word) > 4:
        variants.append(word[:-2])
    if word.endswith("ed") and len(word) > 4:
        variants.append(word[:-2])
        variants.append(word[:-1])
    if word.endswith("ing") and len(word) > 5:
        variants.append(word[:-3])
        variants.append(f"{word[:-3]}e")
    if word.endswith("ly") and len(word) > 4:
        variants.append(word[:-2])

    return any(variant in WORDS for variant in variants)


def is_protected_word(word: str) -> bool:
    return word[:1].isupper() and word[1:].islower() and len(word) <= 3


def levenshtein_distance(source: str, target: str) -> int:
    rows = len(source) + 1
    cols = len(target) + 1
    table = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        table[row][0] = row
    for col in range(cols):
        table[0][col] = col

    for row in range(1, rows):
        for col in range(1, cols):
            cost = 0 if source[row - 1] == target[col - 1] else 1
            table[row][col] = min(
                table[row - 1][col] + 1,
                table[row][col - 1] + 1,
                table[row - 1][col - 1] + cost,
            )

    return table[-1][-1]


def suggest_spelling(word: str) -> str:
    normalized = normalize_word(word)
    if not normalized or normalized in WORDS or is_accepted_inflection(normalized) or is_protected_word(word):
        return word

    candidates = []
    for entry in WORDS:
        if abs(len(entry) - len(normalized)) > 2:
            continue
        if entry[0] != normalized[0]:
            continue

        distance = levenshtein_distance(normalized, entry)
        if distance <= 2:
            candidates.append((distance, entry))

    candidates.sort(key=lambda item: (item[0], item[1]))
    if not candidates:
        return word

    suggestion = candidates[0][1]
    return suggestion.capitalize() if word[:1].isupper() else suggestion


def analyze_spelling(tokens: list[dict]) -> list[dict]:
    misspellings = []

    for token in tokens:
        if token["type"] != "word":
            continue

        normalized = normalize_word(token["value"])
        if (
            not normalized
            or normalized in WORDS
            or is_accepted_inflection(normalized)
            or is_protected_word(token["value"])
        ):
            continue

        suggestion = suggest_spelling(token["value"])
        if not suggestion or suggestion.lower() == token["value"].lower():
            continue

        misspellings.append(
            {
                "word": token["value"],
                "suggestion": suggestion,
                "tokenIndex": token["index"],
                "start": token["start"],
                "end": token["end"],
            }
        )

    return misspellings
