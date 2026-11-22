"""Identify common obligation, permission, and prohibition phrases."""
import re

MODALS = re.compile(
    r"\b(?:(?P<prohibition>(?:shall|must|may|can) not|cannot|prohibited from|forbidden to)"
    r"|(?P<obligation>shall|must|required to|obligated to|has to)"
    r"|(?P<permission>may|can|permitted to|allowed to))\b", re.I
)


def extract_deontic_triples(clauses):
    return [[{"modality": match.lastgroup, "text": match.group(), "sentence": clause}
             for match in MODALS.finditer(clause)] for clause in clauses]
