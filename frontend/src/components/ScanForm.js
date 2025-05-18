import React, { useState } from 'react';

function ScanForm({ onSubmit, isLoading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent default form submission
    onSubmit(url); // Pass the URL up to the parent (ScanPage)
  };

  return (
    <form onSubmit={handleSubmit} className="mb-3">
      <div className="input-group">
        <span className="input-group-text">URL:</span>
        <input
          type="text"
          className="form-control"
          placeholder="example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)} // Use Case Step 1: User enter link
          required // Basic HTML5 validation
          disabled={isLoading}
        />
        <button
          type="submit"
          className="btn btn-primary" // Use Case Step 2: User presses the "scan" button
          disabled={isLoading}
        >
          {isLoading ? 'Scanning...' : 'Scan'}
        </button>
      </div>
    </form>
  );
}

export default ScanForm;