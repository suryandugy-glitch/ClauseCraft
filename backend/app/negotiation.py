# backend/app/negotiation.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()


def suggest_reword(clause: str) -> str:
    """
    Very simple few‑shot call to Claude‑3‑Sonnet asking for a fairer wording.
    """
    prompt = f"""You are a legal‑tech assistant. Rewrite the following clause to be more balanced and user‑friendly while preserving the core intent.
Clause: "{ clause }"
Provide ONLY the rewritten clause, no extra text."""
    client = anthropic.Anthropic()
    try:
        resp = client.messages.create(
            model=os.environ["ANTHROPIC_MODEL"],
            max_tokens=150,
            temperature=0.2,
            system="You are a helpful assistant that rewrites legal clauses into fairer language.",
            messages=[{"role":"user","content":prompt}]
        )
        return resp.content[0].text.strip()
    except Exception as e:
        raise RuntimeError("Could not generate a suggestion") from e