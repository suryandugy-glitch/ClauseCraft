import re

BOUNDARY = re.compile(
    r"\n[ \t]*(?=\d+[.)]\s|[a-z][.)]\s|(?:section|clause|article)\s+(?:\d+|[ivxlcdm]+)\b)"
    r"|\n[ \t]*\n+",
    re.I,
)


def split_into_clauses(text: str):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [" ".join(part.split()) for part in BOUNDARY.split(text) if part.strip()]
