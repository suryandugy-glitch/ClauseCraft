# backend/app/rewriter.py
import anthropic
import os
import re
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set in environment")

client = anthropic.Anthropic(api_key=API_KEY)

# Few-shot examples for legalese -> plain English
FEW_SHOT_EXAMPLES = [
    {
        "legalese": "The Lessee shall not sublet the Premises without the prior written consent of the Lessor.",
        "plain": "You cannot sublet the place unless the landlord gives you written permission."
    },
    {
        "legalese": "This Agreement shall be governed by the laws of the State of New York.",
        "plain": "This agreement follows New York state law."
    },
    {
        "legalese": "The Service Provider shall indemnify the Client against any third-party claims.",
        "plain": "The service provider will cover any legal claims made by a third party."
    },
    {
        "legalese": "The Customer agrees to pay all fees within thirty (30) days of invoice date.",
        "plain": "You agree to pay all fees within 30 days of receiving an invoice."
    },
    {
        "legalese": "Either party may terminate this Agreement upon sixty (60) days' written notice to the other party.",
        "plain": "Either you or we can end this agreement by giving 60 days' written notice."
    }
]

def build_prompt(clauses):
    """
    Build a prompt for Claude with few-shot examples and the clauses to rewrite.
    We'll ask Claude to rewrite each clause in plain English, preserving the meaning.
    """
    prompt = "You are an expert at translating legal jargon into plain, everyday English. "
    prompt += "Rewrite each of the following legal clauses in clear, simple language. "
    prompt += "Keep the meaning exactly the same, but use words that a non-lawyer would understand.\n\n"
    prompt += "Examples:\n"
    for ex in FEW_SHOT_EXAMPLES:
        prompt += f'Legalese: "{ex["legalese"]}"\n'
        prompt += f'Plain: "{ex["plain"]}"\n\n'
    prompt += "Now rewrite these clauses:\n"
    for i, clause in enumerate(clauses, 1):
        prompt += f'{i}. "{clause}"\n'
    prompt += "\nProvide the rewritten clauses in the same order, each on a new line, without numbering or extra text."
    return prompt

def rewrite_clauses(clauses):
    """
    Send a request to Claude-3-Sonnet to rewrite the list of clauses.
    Returns a list of plain English strings in the same order.
    """
    prompt = build_prompt(clauses)
    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=500,
            temperature=0.2,
            system="You are a helpful assistant that rewrites legal clauses into plain English.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        # Extract the text from the response
        text = response.content[0].strip()
        # Split by newline and clean
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        # If we got the same number of lines as clauses, return them.
        # Otherwise, try to split by the pattern of numbering (if Claude added numbers)
        if len(lines) == len(clauses):
            return lines
        # Fallback: if Claude returned numbered list, strip the numbers
        cleaned = []
        for line in lines:
            # Remove leading numbers and dots (e.g., "1. ")
            line = re.sub(r'^\d+\.\s*', '', line)
            cleaned.append(line)
        if len(cleaned) == len(clauses):
            return cleaned
        # If still mismatch, return the original clauses as a last resort (but log warning)
        print(f"Warning: Claude returned {len(lines)} lines for {len(clauses)} clauses. Returning originals.")
        return clauses
    except Exception as e:
        raise RuntimeError(f"Failed to call Claude API: {str(e)}")