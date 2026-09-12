// frontend/src/App.jsx
import { useState, useEffect } from 'react';
import Upload from './components/Upload';
import ClauseViewer from './components/ClauseViewer';
import Flowchart from './components/Flowchart';
import RiskBadge from './components/RiskBadge';

function App() {
  const [contractData, setContractData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [reportReady, setReportReady] = useState(false);

  // Persist dark‑mode choice
  useEffect(() => {
    const saved = localStorage.getItem('darkMode');
    if (saved !== null) setDarkMode(saved === 'true');
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const toggleDark = () => {
    setDarkMode(!darkMode);
    localStorage.setItem('darkMode', String(!darkMode));
  };

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    setReportReady(false);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const resp = await fetch('/api/process', { method: 'POST', body: formData });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || 'Upload failed');
      }
      const data = await resp.json();
      setContractData(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!contractData) return;
    try {
      const formData = new FormData();
      // We need to send the original PDF bytes again.
      // For simplicity we’ll reconstruct a dummy file – in a real app you’d store the
      // original bytes client‑side or call the backend with the filename.
      // Here we just call the endpoint with a placeholder file; the backend will
      // re‑process using the filename we stored in contractData.
      const dummyBlob = new Blob([JSON.stringify({ filename: contractData.filename })], {
        type: 'application/json'
      });
      formData.append('file', dummyBlob);
      const resp = await fetch('/api/export', { method: 'POST', body: formData });
      if (!resp.ok) throw new Error('Export failed');
      const blob = await resp.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${contractData.filename}_report.html`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (e) {
      alert('Could not generate report: ' + e.message);
    }
  };

  if (error) {
    return (
      <div className="p-6 bg-error/10 text-error rounded-md">
        <p>Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header with theme toggle */}
      <header className="bg-card/80 backdrop-blur-sm p-4 flex items-center justify-between border-b border-muted/20">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-primary">ClauseCraft</h1>
          <p className="text-muted">Turn legalese into clarity in seconds</p>
        </div>
        <button
          onClick={toggleDark}
          className="p-2 rounded hover:bg-muted/20 focus-visible"
          aria-label="Toggle dark mode"
        >
          {darkMode ? '☀️ Light' : '🌙 Dark'}
        </button>
      </header>

      <main className="flex-1 p-4">
        <Upload onUpload={handleUpload} loading={loading} />

        {contractData && (
          <>
            <ClauseViewer
              originalClauses={contractData.original_clauses}
              plainClauses={contractData.plain_clauses}
              riskScores={contractData.risk_scores}
              onExport={handleExport}
            />
            <Flowchart
              clauses={contractData.original_clauses}
              triplesPerClause={contractData.triples_per_clause}
              riskScores={contractData.risk_scores}
            />
          </>
        )}
      </main>

      {/* Footer with download button (only show after processing) */}
      {contractData && (
        <footer className="p-4 bg-card/80 backdrop-blur-sm border-t border-muted/20">
          <button
            onClick={handleExport}
            disabled={loading}
            className="w-full px-4 py-2 bg-accent text-white rounded hover:bg-accent-dark focus-visible"
          >
            {loading ? 'Preparing report…' : '📥 Download HTML Report'}
          </button>
        </footer>
      )}
    </div>
  );
}

export default App;