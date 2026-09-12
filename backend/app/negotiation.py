# backend/app/negotiation.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def suggest_reword(clause: str) -> str:
    """
    Very simple few‑shot call to Claude‑3‑Sonnet asking for a fairer wording.
    """
    prompt = f"""You are a legal‑tech assistant. Rewrite the following clause to be more balanced and user‑friendly while preserving the core intent.
Clause: "{ clause }"
Provide ONLY the rewritten clause, no extra text."""
    try:
        resp = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=150,
            temperature=0.2,
            system="You are a helpful assistant that rewrites legal clauses into fairer language.",
            messages=[{"role":"user","content":prompt}]
        )
        return resp.content[0].strip()
    except Exception as e:
        return f"[Error generating suggestion: {e}]"