# backend/app/clause_splitter.py
import re

def split_into_clauses(text: str):
    """
    Split contract text into clauses using heuristics:
    - Look for common clause starters (e.g., "Section", "Clause", "Article", numbered lists)
    - Also split on double newline as a fallback.
    Returns a list of clause strings.
    """
    # Normalise whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Patterns that often start a clause
    pattern = r'(?=\n(?:\d+\.|[A-Z]\.|Section\s+\d+|Clause\s+\d+|Article\s+[IVXLCDM]+|[a-z]\)))'

    clauses = re.split(pattern, text, flags=re.IGNORECASE)

    # If the split didn't work (no matches), fallback to double newline
    if len(clauses) == 1:
        clauses = [c.strip() for c in text.split('\n\n') if c.strip()]

    # Clean up each clause
    cleaned = []
    for clause in clauses:
        clause = clause.strip()
        if clause:
            cleaned.append(clause)

    return cleaned