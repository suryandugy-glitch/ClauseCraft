# backend/app/exporter.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import jinja2

router = APIRouter()

TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ClauseCraft Report – {{ filename }}</title>
<style>
  body {font-family: system-ui, sans-serif; margin:2rem; line-height:1.5; color:#222;}
  h1, h2 {color:#0d47a1;}
  .clause {margin:1rem 0; padding:1rem; border-left:4px solid #0d47a1; background:#f5f5f5;}
  .risk-high {border-left-color:#d32f2f; background:#ffebee;}
  .mermaid {text-align:center; margin:2rem 0;}
  a {color:#0d47a1;}
</style>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
</head>
<body>
<h1>ClauseCraft – Contract Summary</h1>
<p><strong>File:</strong> {{ filename }}</p>

<h2>Plain‑English Summary</h2>
{% for clause, plain, risk in clauses %}
<div class="clause {% if risk > 0.7 %}risk-high{% endif %}">
  <strong>Clause {{ loop.index }}:</strong> {{ clause }}<br>
  <em>Plain English:</em> {{ plain }}
  {% if risk > 0.7 %}<span style="color:#d32f2f;"> (High Risk)</span>{% endif %}
</div>
{% endfor %}

<h2>Flowchart</h2>
<div class="mermaid">
{{ mermaid_syntax | safe }}
</div>

<script>
  mermaid.initialize({startOnLoad:true,theme:'variables'});
</script>
</body>
</html>
"""

def render_report(filename, clauses, plain_clauses, mermaid_syntax):
    """Return an HTML string ready to be streamed back."""
    template = jinja2.Template(TEMPLATE_STR)
    # Pair each clause with its plain version; risk scores are not needed for the template,
    # but we keep the same shape as the caller expects.
    return template.render(
        filename=filename,
        clauses=list(zip(clauses, plain_clauses, [0]*len(clauses))),  # dummy risk for template
        mermaid_syntax=mermaid_syntax
    )