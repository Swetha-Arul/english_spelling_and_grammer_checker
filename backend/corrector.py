import re

from backend.utils import split_sentences


def apply_corrections(text: str, spelling_issues: list[dict]) -> str:
    corrected = []
    cursor = 0

    for issue in sorted(spelling_issues, key=lambda item: item["start"]):
        corrected.append(text[cursor:issue["start"]])
        corrected.append(issue["suggestion"])
        cursor = issue["end"]

    corrected.append(text[cursor:])
    updated = "".join(corrected)
    updated = re.sub(r"\b([A-Za-z]+)\s+\1\b", r"\1", updated, flags=re.IGNORECASE)

    def article_fix(match: re.Match) -> str:
        article = match.group(1)
        next_word = match.group(2)
        expected = "an" if re.match(r"^[aeiou]", next_word, flags=re.IGNORECASE) else "a"
        return f"{expected.capitalize() if article[:1].isupper() else expected} {next_word}"

    updated = re.sub(r"\b(a|an)\s+([A-Za-z]+)", article_fix, updated, flags=re.IGNORECASE)
    updated = re.sub(r"(^|[\s(])i(?=[\s'\".,!?)]|$)", r"\1I", updated)

    rebuilt = []
    for sentence in split_sentences(updated):
        trimmed = sentence.strip()
        if not trimmed:
            continue
        capitalized = trimmed[0].upper() + trimmed[1:]
        rebuilt.append(capitalized if re.search(r"[.!?]$", capitalized) else f"{capitalized}.")

    return " ".join(rebuilt)
