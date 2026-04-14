from backend.corrector import apply_corrections
from backend.lexer import summarize_tokens, tokenize
from backend.parser import analyze_grammar
from backend.spell_checker import analyze_spelling
from backend.utils import split_sentences


def analyze_text(text: str) -> dict:
    tokens = tokenize(text)
    spelling_issues = analyze_spelling(tokens)
    grammar_issues = analyze_grammar(text)

    return {
        "inputText": text,
        "correctedText": apply_corrections(text, spelling_issues),
        "summary": {
            "characterCount": len(text),
            "wordCount": sum(1 for token in tokens if token["type"] == "word"),
            "sentenceCount": len(split_sentences(text)),
            "misspellingCount": len(spelling_issues),
            "grammarIssueCount": len(grammar_issues),
        },
        "compilerPipeline": [
            {
                "phase": "Lexical Analysis",
                "description": "Breaks input into words, numbers, punctuation, and whitespace tokens.",
                "result": summarize_tokens(tokens),
            },
            {
                "phase": "Spelling Validation",
                "description": "Checks word tokens against a dictionary and proposes edit-distance corrections.",
                "result": {"flaggedWords": len(spelling_issues)},
            },
            {
                "phase": "Grammar Checking",
                "description": "Applies lightweight parsing rules for punctuation, capitalization, repeated words, and article agreement.",
                "result": {"flaggedRules": len(grammar_issues)},
            },
        ],
        "tokens": [
            {"type": token["type"], "value": token["value"], "position": token["index"]}
            for token in tokens
            if token["type"] != "whitespace"
        ][:80],
        "spellingIssues": spelling_issues,
        "grammarIssues": grammar_issues,
        "parseTreeHint": {"root": "Document", "children": ["Sentence", "TokenStream", "ValidationRules"]},
    }
