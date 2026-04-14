import re

from backend.utils import split_sentences


def analyze_grammar(text: str) -> list[dict]:
    issues = []

    for sentence in split_sentences(text):
        trimmed = sentence.strip()
        if not trimmed:
            continue

        if re.match(r"^[a-z]", trimmed):
            issues.append(
                {
                    "type": "capitalization",
                    "message": "Sentence should start with a capital letter.",
                    "excerpt": trimmed,
                    "suggestion": trimmed[0].upper() + trimmed[1:],
                }
            )

        if re.search(r"[A-Za-z0-9]$", trimmed):
            issues.append(
                {
                    "type": "punctuation",
                    "message": "Sentence may be missing ending punctuation.",
                    "excerpt": trimmed,
                    "suggestion": f"{trimmed}.",
                }
            )

    for match in re.finditer(r"\b([A-Za-z]+)\s+\1\b", text, flags=re.IGNORECASE):
        issues.append(
            {
                "type": "repeated-word",
                "message": f'Repeated word detected: "{match.group(1)}".',
                "excerpt": match.group(0),
                "suggestion": match.group(1),
            }
        )

    for match in re.finditer(r"\b(a|an)\s+([A-Za-z]+)", text, flags=re.IGNORECASE):
        article = match.group(1).lower()
        next_word = match.group(2)
        expected = "an" if re.match(r"^[aeiou]", next_word, flags=re.IGNORECASE) else "a"

        if article != expected:
            issues.append(
                {
                    "type": "article",
                    "message": f'Article agreement issue before "{next_word}".',
                    "excerpt": match.group(0),
                    "suggestion": f"{expected} {next_word}",
                }
            )

    for _match in re.finditer(r"(^|[\s(])i(?=[\s'\".,!?)]|$)", text):
        issues.append(
            {
                "type": "pronoun",
                "message": 'The pronoun "I" should be uppercase.',
                "excerpt": "i",
                "suggestion": "I",
            }
        )

    return issues
