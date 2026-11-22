<img src="frontend/public/cellar-logo.png" width="64" height="64" alt="ClauseCraft logo">

# ClauseCraft by Cellar

[Launch ClauseCraft](https://cellar-clausecraft.onrender.com/) · [Report an issue](https://github.com/suryandugy-glitch/ClauseCraft/issues)

Upload a sample PDF with selectable text. Review the clauses in document order and download the HTML report.


Upload a text-based PDF to split it into clauses, find common obligations,
permissions, and prohibitions, and flag keywords for closer review. The app
shows clauses in document order and exports an HTML report.

The public demo accepts text-based PDFs up to 5 MB. Use sample contracts.
Keyword flags are informational and should be reviewed in context.

## Run locally

Build the frontend with Node.js 22, then start the API with Python 3.11.

    cd frontend
    npm ci
    npm run build
    cd ../backend
    python -m pip install -r requirements.txt
    python -m uvicorn app.main:app --port 8000

Open http://localhost:8000. For frontend development, run npm run dev in a
separate terminal and leave the API running on port 8000.

## Deploy on Render

The root render.yaml creates one free Docker web service. The API serves the
frontend from the same origin and reports health at /health.

AI features are optional and off by default. Enable them only in a deployment
where users have agreed that document text may be sent to Anthropic. Set
ANTHROPIC_API_KEY and ANTHROPIC_MODEL in that deployment's environment.
