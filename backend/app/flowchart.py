# backend/app/flowchart.py
def generate_mermaid(clauses, triples_per_clause, risk_scores):
    """
    Generate Mermaid.js flowchart syntax from clauses, their deontic triples, and risk scores.
    Returns a string containing the Mermaid definition.
    """
    # Helper to determine node color based on triples and risk score
    def node_color(triples, risk):
        has_obligation = any(t['modality'] == 'obligation' for t in triples)
        has_permission = any(t['modality'] == 'permission' for t in triples)
        has_prohibition = any(t['modality'] == 'prohibition' for t in triples)
        high_risk = risk > 0.7
        if has_prohibition or high_risk:
            return "#F44336"  # red
        elif has_obligation:
            return "#2196F3"  # blue
        elif has_permission:
            return "#4CAF50"  # green
        else:
            return "#9E9E9E"  # gray

    lines = []
    lines.append("flowchart LR")
    # Add nodes
    for i, (clause, triples, risk) in enumerate(zip(clauses, triples_per_clause, risk_scores)):
        node_id = f"clause{i}"
        # Truncate clause for display
        display = clause.strip()
        if len(display) > 60:
            display = display[:57] + "..."
        # Escape quotes for Mermaid
        display = display.replace('"', '\\"')
        color = node_color(triples, risk)
        # Tooltip: show full clause and risk score (we'll expose via data-id in the SVG)
        tooltip = f"Clause: {clause}\\nRisk: {risk:.2f}"
        tooltip = tooltip.replace('"', '\\"')
        lines.append(f'    {node_id}["{display}"]')
        lines.append(f'    style {node_id} fill:{color},stroke:#333,stroke-width:1px')
        # Attach a data-id attribute so the frontend can read it later
        # Mermaid lets us add arbitrary HTML-like attributes via a comment trick,
        # but we'll instead store the id in the node label via a zero‑width Unicode char.
        # For simplicity we rely on the frontend extracting the node id from the
        # generated SVG (the node id is exactly the string we used above).
    # Add edges between consecutive nodes
    for i in range(len(clauses) - 1):
        lines.append(f'    clause{i} --> clause{i+1}')
    return "\n".join(lines)