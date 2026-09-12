// frontend/src/components/Flowchart.jsx
import { useEffect, useRef, useState } from 'react';

function Flowchart({ clauses, triplesPerClause, riskScores }) {
  const mermaidRef = useRef(null);
  const tooltipRef = useRef(null);
  const [showTooltip, setShowTooltip] = useState(false);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [tooltipContent, setTooltipContent] = useState('');

  // Helper to decide colour (same logic as before)
  const nodeColor = (triples, risk) => {
    const hasObl = triples.some(t => t.modality === 'obligation');
    const hasPerm = triples.some(t => t.modality === 'permission');
    const hasPro = triples.some(t => t.modality === 'prohibition');
    const highRisk = risk > 0.7;
    if (hasPro || highRisk) return '#F44336'; // red
    if (hasObl) return '#2196F3'; // blue
    if (hasPerm) return '#4CAF50'; // green
    return '#9E9E9E'; // gray
  };

  useEffect(() => {
    if (!clauses || clauses.length === 0) return;

    // Build Mermaid syntax (identical to backend version)
    const generateMermaid = (cList, tList, rList) => {
      const lines = ['flowchart LR'];
      cList.forEach((clause, i) => {
        const nodeId = `clause${i}`;
        const display = clause.length > 60 ? clause.slice(0, 57) + '...' : clause;
        const escaped = display.replace(/"/g, '\\"');
        const color = nodeColor(tList[i] || [], rList[i] || 0);
        lines.push(`    ${nodeId}["${escaped}"]`);
        lines.push(`    style ${nodeId} fill:${color},stroke:#333,stroke-width:1px`);
      });
      for (let i = 0; i < cList.length - 1; i++) {
        lines.push(`    clause${i} --> clause${i+1}`);
      }
      return lines.join('\n');
    };

    const mermaidSyntax = generateMermaid(clauses, triplesPerClause, riskScores);

    // Initialise Mermaid
    if (window.mermaid) {
      window.mermaid.initialize({ startOnLoad: true, theme: 'variables' });
      window.mermaid.render('flowchartSVG', mermaidSyntax, (svgCode) => {
        mermaidRef.current.innerHTML = svgCode;
        // Add mouse‑over listeners to each <g> representing a node
        const svg = mermaidRef.current.querySelector('svg');
        if (!svg) return;
        svg.addEventListener('mousemove', (e) => {
          const target = e.target;
          const nodeG = target.closest('.node');
          if (!nodeG) {
            setShowTooltip(false);
            return;
          }
          const nodeId = nodeG?.getAttribute('data-id') ?? '';
          const match = nodeId.match(/clause(\d+)/);
          if (!match) {
            setShowTooltip(false);
            return;
          }
          const idx = Number(match[1]);
          const risk = riskScores[idx] ?? 0;
          const modalityList = triplesPerClause[idx] ?? [];
          const hasOb = modalityList.some(t => t.modality === 'obligation');
          const hasPer = modalityList.some(t => t.modality === 'permission');
          const hasPro = modalityList.some(t => t.modality === 'prohibition');
          let modTxt = '';
          if (hasOb) modTxt += 'Obligation • ';
          if (hasPer) modTxt += 'Permission • ';
          if (hasPro) modTxt += 'Prohibition • ';
          modTxt = modTxt.slice(0, -3) || '—';
          const tip = `Clause ${idx + 1}\n${modTxt}\nRisk: ${risk.toFixed(2)}`;
          setTooltipContent(tip);
          setTooltipPos({ x: e.pageX + 8, y: e.pageY + 8 });
          setShowTooltip(true);
        });
        svg.addEventListener('mouseleave', () => setShowTooltip(false));
      });
    }
  }, [clauses, triplesPerClause, riskScores]);

  // Loading skeleton placeholder
  const renderSkeleton = () => (
    <div className="h-40 w-full bg-card rounded-md">
      <div className="h-4 w-2/3 mx-auto my-2 skeleton rounded"></div>
      <div className="h-4 w-1/2 mx-auto my-2 skeleton rounded"></div>
      <div className="h-4 w-3/4 mx-auto my-2 skeleton rounded"></div>
    </div>
  );

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-3">Contract Flowchart</h2>
      <div className="relative">
        {!clauses || clauses.length === 0 ? renderSkeleton() : (
          <div
            ref={mermaidRef}
            className="w-full h-[400px] bg-card border border-muted rounded-md"
            // Mermaid will inject an SVG here
          />
        )}
        {/* Custom tooltip */}
        {showTooltip && (
          <div
            ref={tooltipRef}
            className={`absolute left-[${tooltipPos.x}px] top-[${tooltipPos.y}px] bg-muted/90 text-muted text-sm px-3 py-1 rounded max-w-xs break-words z-50`}
          >
            {tooltipContent}
          </div>
        )}
      </div>
      <div className="mt-2 flex flex-wrap gap-3 text-xs text-muted">
        <span>🟢 Permission &nbsp;🔵 Obligation &nbsp;🔴 Prohibition/High Risk</span>
        <span>Nodes appear in contract order.</span>
      </div>
    </div>
  );
}

export default Flowchart;