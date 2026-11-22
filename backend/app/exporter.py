from jinja2 import Environment

TEMPLATE = Environment(autoescape=True).from_string("""
<!doctype html>
<html lang="en">
<meta charset="utf-8">
<title>ClauseCraft by Cellar | Report</title>
<style>
body {max-width: 56rem; margin: 2rem auto; padding: 0 1rem; font: 1rem/1.55 system-ui;}
li {margin-bottom: 1rem;}
</style>
<h1>ClauseCraft by Cellar</h1>
<p>Document: {{ report.filename }}</p>
<p>Keyword flags identify clauses for closer review.</p>
<ol>
{% for clause in report.original_clauses %}
<li>
<p>{{ clause }}</p>
{% if report.risk_scores[loop.index0] > 0.7 %}<strong>Review flag</strong>{% endif %}
{% if report.plain_clauses %}<p>{{ report.plain_clauses[loop.index0] }}</p>{% endif %}
</li>
{% endfor %}
</ol>
</html>
""")


def render_report(report):
    return TEMPLATE.render(report=report)
