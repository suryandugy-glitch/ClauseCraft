import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from app import clause_splitter, deontic, donut, exporter, negotiation, rewriter, risk_scorer

load_dotenv()
app = FastAPI(title="ClauseCraft by Cellar", docs_url=None, redoc_url=None)
MAX_PDF_BYTES = 5 * 1024 * 1024


def ai_enabled():
    return bool(os.getenv("ANTHROPIC_API_KEY") and os.getenv("ANTHROPIC_MODEL"))


@app.get("/health")
def health():
    return {"status": "ok"}


def analyze_pdf(contents, filename):
    try:
        lines, _ = donut.extract_text_and_layout(contents)
    except RuntimeError as error:
        raise HTTPException(400, "Could not read this PDF") from error
    clauses = clause_splitter.split_into_clauses("\n".join(lines))
    if not clauses:
        raise HTTPException(400, "No readable clauses found. Use a PDF with selectable text.")
    if len(clauses) > 100 or sum(map(len, clauses)) > 60_000:
        raise HTTPException(400, "This document is too long. Use a shorter excerpt.")
    return {
        "filename": filename,
        "original_clauses": clauses,
        "plain_clauses": rewriter.rewrite_clauses(clauses) if ai_enabled() else None,
        "triples_per_clause": deontic.extract_deontic_triples(clauses),
        "risk_scores": risk_scorer.score_clauses(clauses),
        "ai_enabled": ai_enabled(),
    }


async def analyze_upload(file):
    if not (file.filename or "").lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    contents = await file.read(MAX_PDF_BYTES + 1)
    if len(contents) > MAX_PDF_BYTES:
        raise HTTPException(413, "Use a PDF of 5 MB or less")
    try:
        return await run_in_threadpool(analyze_pdf, contents, file.filename)
    except RuntimeError as error:
        raise HTTPException(502, "The analysis provider could not complete this request") from error


@app.post("/process", include_in_schema=False)
@app.post("/api/process")
async def process_contract(file: UploadFile = File(...)):
    return await analyze_upload(file)


@app.post("/export", include_in_schema=False)
@app.post("/api/export")
async def export_contract(file: UploadFile = File(...)):
    data = await analyze_upload(file)
    return HTMLResponse(
        exporter.render_report(data),
        headers={"Content-Disposition": 'attachment; filename="clausecraft-report.html"'},
    )


class NegotiationRequest(BaseModel):
    clause: str = Field(min_length=1, max_length=6_000)


@app.post("/negotiate", include_in_schema=False)
@app.post("/api/negotiate")
def negotiate_clause(payload: NegotiationRequest):
    if not ai_enabled():
        raise HTTPException(503, "AI suggestions are disabled on this deployment")
    try:
        return {"suggestion": negotiation.suggest_reword(payload.clause)}
    except RuntimeError as error:
        raise HTTPException(502, "The suggestion provider could not complete this request") from error


site = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if site.is_dir():
    app.mount("/", StaticFiles(directory=site, html=True), name="frontend")
