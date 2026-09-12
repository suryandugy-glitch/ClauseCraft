// frontend/src/components/ClauseViewer.jsx
import { useState } from 'react';

function ClauseViewer({ originalClauses, plainClauses, riskScores, onExport }) {
  const [viewMode, setViewMode] = useState('sideBySide'); // sideBySide or plainOnly
  const [copyFeedback, setCopyFeedback] = useState({}); // idx -> bool
  const [negotiationOpen, setNegotiationOpen] = useState(false);
  const [negotiationClause, setNegotiationClause] = useState('');
  const [negotiationSuggestion, setNegotiationSuggestion] = useState('');

  const toggleView = () => {
    setViewMode(viewMode === 'sideBySide' ? 'plainOnly' : 'sideBySide');
  };

  const copyToClipboard = async (text, idx) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopyFeedback(prev => ({ ...prev, [idx]: true }));
      setTimeout(() => setCopyFeedback(prev => ({ ...prev, [idx]: false })), 1500);
    } catch (err) {
      console.warn('Copy failed', err);
    }
  };

  const openNegotiation = (clause) => {
    setNegotiationClause(clause);
    setNegotiationOpen(true);
    // Call backend negotiation endpoint
    fetch('/api/negotiate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clause })
    })
      .then(r => r.json())
      .then(data => setNegotiationSuggestion(data.suggestion || ''))
      .catch(err => {
        console.error(err);
        setNegotiationSuggestion('[Error fetching suggestion]');
      });
  };

  const closeNegotiation = () => {
    setNegotiationOpen(false);
    setNegotiationClause('');
    setNegotiationSuggestion('');
  };

  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-3">Contract Analysis</h2>
      <div className="flex items-center justify-between mb-2">
        <span className="text-muted">View mode:</span>
        <button
          onClick={toggleView}
          className="px-3 py-1 bg-muted/20 rounded-md text-sm hover:bg-muted/30 focus-visible"
        >
          {viewMode === 'sideBySide' ? 'Plain English Only' : 'Side-by-Side'}
        </button>
      </div>

      {viewMode === 'sideBySide' ? (
        <div className="grid gap-4 md:grid-cols-2">
          {/* Original */}
          <div>
            <h3 className="font-medium mb-2">Original Legalese</h3>
            {originalClauses.map((clause, idx) => (
              <div key={idx} className="mb-4 p-3 bg-card border border-muted rounded-md shadow-sm">
                <p className="text-sm text-primary">{clause}</p>
                {riskScores[idx] > 0.7 && (
                  <span className="ml-2 inline-flex items-center px-2 py-0.5 bg-error/10 text-error rounded">
                    High Risk
                  </span>
                )}
              </div>
            ))}
          </div>
          {/* Plain English */}
          <div>
            <h3 className="font-medium mb-2">Plain English Summary</h3>
            {plainClauses.map((clause, idx) => (
              <div key={idx} className="mb-4 p-3 bg-card border border-muted rounded-md shadow-sm relative">
                <p className="text-sm text-primary">{clause}</p>
                {riskScores[idx] > 0.7 && (
                  <span className="ml-2 inline-flex items-center px-2 py-0.5 bg-error/10 text-error rounded">
                    High Risk
                  </span>
                )}
                {/* Copy button */}
                <button
                  onClick={() => copyToClipboard(clause, idx)}
                  className="absolute right-2 top-2 p-1 text-xs bg-muted/20 rounded hover:bg-muted/30 focus-visible"
                  aria-label="Copy plain English"
                >
                  {copyFeedback[idx] ? '✔️ Copied' : '📋'}
                </button>
                {/* Negotiation trigger (only for high‑risk) */}
                {riskScores[idx] > 0.7 && (
                  <button
                    onClick={() => openNegotiation(clause)}
                    className="mt-2 w-full text-left text-xs bg-accent/10 text-accent rounded hover:bg-accent/20 focus-visible"
                  >
                    Suggest fairer wording ⚖️
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div>
          <h3 className="font-medium mb-2">Plain English Summary</h3>
          {plainClauses.map((clause, idx) => (
            <div key={idx} className="mb-4 p-3 bg-card border border-muted rounded-md shadow-sm relative">
              <p className="text-sm text-primary">{clause}</p>
              {riskScores[idx] > 0.7 && (
                <span className="ml-2 inline-flex items-center px-2 py-0.5 bg-error/10 text-error rounded">
                  High Risk
                </span>
              )}
              <button
                onClick={() => copyToClipboard(clause, idx)}
                className="absolute right-2 top-2 p-1 text-xs bg-muted/20 rounded hover:bg-muted/30 focus-visible"
                aria-label="Copy plain English"
              >
                {copyFeedback[idx] ? '✔️ Copied' : '📋'}
              </button>
              {riskScores[idx] > 0.7 && (
                <button
                  onClick={() => openNegotiation(clause)}
                  className="mt-2 w-full text-left text-xs bg-accent/10 text-accent rounded hover:bg-accent/20 focus-visible"
                >
                  Suggest fairer wording ⚖️
                </button>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Negotiation Modal */}
      {negotiationOpen && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-card rounded-lg p-6 w-full max-w-md shadow-xl">
            <h3 className="text-lg font-semibold mb-3">Suggested Re‑wording</h3>
            <p className="text-muted mb-4">Original:</p>
            <blockquote className="p-3 bg-muted/10 rounded mb-4">{negotiationClause}</blockquote>
            <p className="text-muted mb-2">Fairer version:</p>
            <p className="font-medium text-accent">{negotiationSuggestion}</p>
            <div className="mt-4 flex justify-end">
              <button
                onClick={closeNegotiation}
                className="px-4 py-2 bg-muted rounded hover:bg-muted/20 focus-visible"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ClauseViewer;