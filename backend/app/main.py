# backend/app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses = JSONResponse, StreamingResponse
import uvicorn
import os
from dotenv import load_dotenv

# Import our local modules
from app import donut, clause_splitter, rewriter, deontic, risk_scorer, flowchart, exporter, negotiation

load_dotenv()
app = FastAPI(title="ClauseCraft API")

# -------------------------------------------------
# Existing /process endpoint (unchanged)
# -------------------------------------------------
@app.post("/process")
async def process_contract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    contents = await file.read()

    # 1️⃣ PDF → text (Donut replaced by PyMuPDF for simplicity)
    text_lines, _ = donut.extract_text_and_layout(contents)
    full_text = "\n".join(text_lines)

    # 2️⃣ Split into clauses
    clauses = clause_splitter.split_into_clauses(full_text)
    if not clauses:
        raise HTTPException(status_code=400, detail="No clauses found in the document")

    # 3️⃣ Rewrite each clause with Claude (few‑shot)
    plain_clauses = rewriter.rewrite_clauses(clauses)

    # 4️⃣ Extract deontic triples
    triples_per_clause = deontic.extract_deontic_triples(clauses)

    # 5️⃣ Risk scoring
    risk_scores = risk_scorer.score_clauses(clauses)

    # 6️⃣ Generate Mermaid flowchart syntax
    mermaid_syntax = flowchart.generate_mermaid(clauses, triples_per_clause, risk_scores)

    return JSONResponse(content={
        "filename": file.filename,
        "original_clauses": clauses,
        "plain_clauses": plain_clauses,
        "triples_per_clause": triples_per_clause,
        "risk_scores": risk_scores,
        "mermaid_syntax": mermaid_syntax
    })

# -------------------------------------------------
# New: Export endpoint – returns a downloadable HTML report
# -------------------------------------------------
@app.post("/export")
async def export_contract(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    contents = await file.read()

    # Re‑use the same pipeline as /process (duplication is fine for a hackathon)
    text_lines, _ = donut.extract_text_and_layout(contents)
    full_text = "\n".join(text_lines)
    clauses = clause_splitter.split_into_clauses(full_text)
    if not clauses:
        raise HTTPException(status_code=400, detail="No clauses found")
    plain_clauses = rewriter.rewrite_clauses(clauses)
    triples_per_clause = deontic.extract_deontic_triples(clauses)
    risk_scores = risk_scorer.score_clauses(clauses)
    mermaid_syntax = flowchart.generate_mermaid(clauses, triples_per_clause, risk_scores)

    html_str = exporter.render_report(file.filename, clauses, plain_clauses, mermaid_syntax)

    # Stream back as a downloadable file
    return StreamingResponse(
        iter([html_str.encode("utf-8")]),
        media_type="text/html",
        headers={"Content-Disposition": f'attachment; filename="{file.filename}_report.html"'}
    )

# -------------------------------------------------
# New: Negotiation suggestion (called from frontend)
# -------------------------------------------------
@app.post("/negotiate")
async def negotiate_clause(payload: dict):
    """
    Expects JSON: {"clause": "<original legalese>"}
    Returns: {"suggestion": "<fairer wording>"}
    """
    clause = payload.get("clause", "")
    if not clause:
        raise HTTPException(status_code=400, detail="Missing clause")
    suggestion = negotiation.suggest_reword(clause)
    return JSONResponse(content={"suggestion": suggestion})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)