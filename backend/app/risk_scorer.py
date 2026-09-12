# backend/app/risk_scorer.py
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
import numpy as np

# Load the Sentence-BERT model (small and fast)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Tiny training data for risk scoring (examples of high-risk and low-risk clauses)
# In a real project, you'd use a larger dataset like CUAD.
train_texts = [
    # High-risk clauses (label 1)
    "The Company may terminate this Agreement at any time, without cause, upon thirty (30) days' written notice.",
    "Customer shall indemnify and hold harmless the Company from any and all claims, liabilities, damages, losses, and expenses.",
    "This Agreement shall automatically renew for successive one-year terms unless either party provides written notice of non-renewal at least sixty (60) days prior to the end of the then-current term.",
    "The User agrees to bind their successors and assigns to the terms of this Agreement.",
    "Liability of the Company for any claim shall not exceed the total fees paid by the Customer under this Agreement.",
    # Low-risk clauses (label 0)
    "This Agreement shall be governed by the laws of the State of California.",
    "The Service Provider shall provide the Services in a professional and workmanlike manner.",
    "Either party may request a conference to discuss any issues arising under this Agreement.",
    "All invoices shall be paid within thirty (30) days of the invoice date.",
    "The parties agree to keep confidential all proprietary information disclosed during the term of this Agreement."
]
train_labels = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]  # 1 = high risk, 0 = low risk

# Encode the training texts
train_embeddings = model.encode(train_texts)

# Train a logistic regression classifier
clf = LogisticRegression(random_state=0, max_iter=1000)
clf.fit(train_embeddings, train_labels)

def score_clauses(clauses):
    """
    For each clause, compute the risk score (probability of being high-risk).
    Returns a list of floats between 0 and 1.
    """
    if not clauses:
        return []
    embeddings = model.encode(clauses)
    # Get probability of the positive class (high risk)
    probs = clf.predict_proba(embeddings)[:, 1]
    return probs.tolist()