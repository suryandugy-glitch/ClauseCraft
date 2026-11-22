// frontend/src/App.jsx
import { useState, useEffect } from 'react';
import Upload from './components/Upload';
import ClauseViewer from './components/ClauseViewer';
import Flowchart from './components/Flowchart';

function App() {
  const [contractData, setContractData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(() => localStorage.getItem('darkMode') === 'true');
  const [sourceFile, setSourceFile] = useState(null);

  // Persist dark‑mode choice
  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
  }, [darkMode]);

  const toggleDark = () => {
    setDarkMode(!darkMode);
    localStorage.setItem('darkMode', String(!darkMode));
  };

  const handleUpload = async (file) => {
    setLoading(true);
    setError(null);
    setContractData(null);
    setSourceFile(null);
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
      setSourceFile(file);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    if (!sourceFile) return;
    try {
      const formData = new FormData();
      formData.append('file', sourceFile);
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

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header with theme toggle */}
      <header className="bg-card/80 backdrop-blur-sm p-4 flex items-center justify-between border-b border-muted/20">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-primary">ClauseCraft by Cellar</h1>
          <p className="text-muted">Review clauses, permissions, and obligations</p>
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
        <p className="mb-3">Upload a text-based PDF up to 5 MB. Use a sample document for this public demo. Keyword flags are a guide for further review.</p>
        <Upload onUpload={handleUpload} loading={loading} />
        {error && <p role="alert" className="mt-3 text-red-700">{error}</p>}

        {contractData && (
          <>
            <ClauseViewer
              originalClauses={contractData.original_clauses}
              plainClauses={contractData.plain_clauses}
              aiEnabled={contractData.ai_enabled}
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