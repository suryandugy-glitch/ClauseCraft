"""Keyword flags for clauses that may merit closer review."""
import re

REVIEW_PATTERNS = (
    re.compile(r"\bindemnif\w*\b|\bhold harmless\b", re.I),
    re.compile(r"\bautomat\w* renew\w*\b|\bauto-renew\w*\b", re.I),
    re.compile(r"\bwithout cause\b|\bsole discretion\b", re.I),
    re.compile(r"\blimitation of liability\b|\bliability.{0,50}\bshall not exceed\b", re.I),
    re.compile(r"\bwaiv\w*\b|\bunlimited liability\b", re.I),
)


def score_clauses(clauses):
    return [0.85 if any(pattern.search(clause) for pattern in REVIEW_PATTERNS)
            else 0.15 for clause in clauses]
