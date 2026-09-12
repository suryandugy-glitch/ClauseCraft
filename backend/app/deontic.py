# backend/app/deontic.py
import spacy
from spacy.matcher import Matcher

# Load the small English model
nlp = spacy.load("en_core_web_sm")

def extract_deontic_triples(clauses):
    """
    For each clause, extract triples (subject, modality, action) where modality is:
    - obligation: shall, must, required to, obligated to, has to
    - permission: may, permitted to, allowed to, can
    - prohibition: shall not, must not, prohibited from, forbidden to, may not
    Returns a list of list of triples (one list per clause).
    """
    matcher = Matcher(nlp.vocab)

    # Define patterns for each modality
    obligation_patterns = [
        [{"LEMMA": "shall"}],
        [{"LEMMA": "must"}],
        [{"LOWER": "required"}, {"LOWER": "to"}],
        [{"LOWER": "obligated"}, {"LOWER": "to"}],
        [{"LOWER": "has"}, {"LOWER": "to"}],
    ]
    permission_patterns = [
        [{"LEMMA": "may"}],
        [{"LOWER": "permitted"}, {"LOWER": "to"}],
        [{"LOWER": "allowed"}, {"LOWER": "to"}],
        [{"LEMMA": "can"}],
    ]
    prohibition_patterns = [
        [{"LEMMA": "shall"}, {"LOWER": "not"}],
        [{"LEMMA": "must"}, {"LOWER": "not"}],
        [{"LOWER": "prohibited"}, {"LOWER": "from"}],
        [{"LOWER": "forbidden"}, {"LOWER": "to"}],
        [{"LOWER": "may"}, {"LOWER": "not"}],
    ]

    # Add patterns to matcher with labels
    matcher.add("OBLIGATION", obligation_patterns)
    matcher.add("PERMISSION", permission_patterns)
    matcher.add("PROHIBITION", prohibition_patterns)

    results = []
    for clause in clauses:
        doc = nlp(clause)
        matches = matcher(doc)
        triples = []
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]  # Get string label
            # Extract the matched text
            matched_span = doc[start:end]
            modality = label.lower()
            # For this demo we simply record the modality and the full clause as the "action"
            triples.append({
                "modality": modality,
                "text": matched_span.text,
                "sentence": clause
            })
        results.append(triples)
    return results