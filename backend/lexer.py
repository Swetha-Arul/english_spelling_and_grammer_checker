import re


TOKEN_PATTERN = re.compile(r"([A-Za-z]+(?:'[A-Za-z]+)?)|(\d+(?:\.\d+)?)|([^\w\s])|(\s+)")


def tokenize(text: str) -> list[dict]:
    tokens = []
    index = 0

    for match in TOKEN_PATTERN.finditer(text):
        value = match.group(0)
        token_type = "unknown"

        if match.group(1):
          token_type = "word"
        elif match.group(2):
          token_type = "number"
        elif match.group(3):
          token_type = "punctuation"
        elif match.group(4):
          token_type = "whitespace"

        tokens.append(
            {
                "type": token_type,
                "value": value,
                "index": index,
                "start": match.start(),
                "end": match.end(),
            }
        )
        index += 1

    return tokens


def summarize_tokens(tokens: list[dict]) -> dict:
    summary = {"word": 0, "number": 0, "punctuation": 0, "whitespace": 0, "unknown": 0}
    for token in tokens:
        summary[token["type"]] = summary.get(token["type"], 0) + 1
    return summary
