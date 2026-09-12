// frontend/src/components/Upload.jsx
import { useState } from 'react';

function Upload({ onUpload, loading }) {
  const [file, setFile] = useState(null);
  const [dragOver, setDragOver] = useState(false);

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(true);
  };
  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
  };
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragOver(false);
    const dt = e.dataTransfer;
    const file = dt.files[0];
    if (file) setFile(file);
  };
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) setFile(file);
  };
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    onUpload(file);
  };

  return (
    <div
      className={`border-2 border-dashed border-muted rounded-lg p-6 text-center hover:border-muted/50 transition-colors
        ${dragOver ? 'bg-muted/5' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {dragOver ? (
        <p className="text-success font-medium">Release to upload</p>
      ) : (
        <>
          <p className="text-muted">Drag & drop a PDF contract here, or click to select</p>
          <input
            type="file"
            accept=".pdf"
            className="mt-4 block w-full text-sm text-muted file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-accent/10 file:text-accent hover:file:bg-accent/20"
            onChange={handleFileChange}
          />
        </>
      )}
      {file && (
        <p className="mt-2 text-sm text-muted truncate">
          Selected: {file.name}
        </p>
      )}
      {/* Loading skeleton */}
      {loading && (
        <div className="mt-4 flex items-center gap-3">
          <div className="h-4 w-20 skeleton rounded"></div>
          <span className="text-muted">Processing…</span>
        </div>
      )}
      <button
        onClick={handleSubmit}
        disabled={loading || !file}
        className="mt-4 w-full px-4 py-2 bg-accent text-white rounded hover:bg-accent-dark focus-visible"
      >
        {loading ? 'Analyzing…' : 'Analyze Contract'}
      </button>
    </div>
  );
}

export default Upload;