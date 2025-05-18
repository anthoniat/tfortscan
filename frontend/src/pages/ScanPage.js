import React, { useState } from 'react';
import axios from 'axios';
import ScanForm from '../components/ScanForm';
import ResultsDisplay from '../components/ResultsDisplay';

// Define the backend API URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api/scan'; // Use environment variable or default

function ScanPage() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleScan = async (url) => {
    // Use Case Step 1 & 2 happen in ScanForm, this is Step 4 onwards
    setIsLoading(true);
    setError('');
    setResults(null); // Clear previous results

    // Basic frontend validation (non-empty)
    if (!url) {
        setError("Please enter a website URL.");
        setIsLoading(false);
        return;
    }

    // Ensure no trailing slash as per Figure 3 instruction (simple check)
    if (url.endsWith('/')) {
        url = url.slice(0, -1);
        // Optionally notify user? For now, just fix it.
    }


    try {
      // Step 4: Send via POST request
      const response = await axios.post(API_URL, { url: url });
      // Step 7: Receive result
      console.log("API Response:", response.data); // Log the response

      if (response.data && response.data.message === "nothing to view") {
         // Handle specific "invalid link" message from backend (Use Case Step 3)
         setError(response.data.error || "The provided link is not valid or reachable.");
         setResults({ message: "nothing to view" }); // Set a specific state for this
      } else if (response.data && response.data.results) {
         setResults(response.data); // Contains results and possibly errors object
         // Check if the backend reported errors during the scan
         if (response.data.errors) {
             const errorMessages = Object.values(response.data.errors).join('. ');
             setError(`Scan completed with errors: ${errorMessages}`);
         }
      } else {
          // Handle unexpected response format
          setError("Received an unexpected response from the server.");
          console.error("Unexpected response format:", response.data);
      }

    } catch (err) {
      console.error("API Call Error:", err);
      let errorMessage = "An error occurred while scanning.";
      if (err.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error("Error Response Data:", err.response.data);
        console.error("Error Response Status:", err.response.status);
        errorMessage = err.response.data?.error || `Server error: ${err.response.status}`;
        if (err.response.data?.message === "nothing to view") {
             setResults({ message: "nothing to view" });
             errorMessage = err.response.data?.error || "The provided link is not valid or reachable.";
        }

      } else if (err.request) {
        // The request was made but no response was received
        errorMessage = "Could not connect to the scanner service. Is the backend running?";
        console.error("Error Request:", err.request);
      } else {
        // Something happened in setting up the request that triggered an Error
        errorMessage = `Error setting up request: ${err.message}`;
      }
      setError(errorMessage);
      setResults(null); // Ensure results are cleared on error
    } finally {
      setIsLoading(false); // Stop loading indicator
    }
  };


  return (
    <div className="scan-page-container"> {/* Added class */}
      <h2>Security Vulnerability Scan</h2>
      <p>Enter the website URL (e.g., `example.com`, do not include trailing `/`).</p>
       <p className="text-danger small">
           <strong>Disclaimer:</strong> Only use this tool on websites you have explicit permission to test.
       </p>
      <ScanForm onSubmit={handleScan} isLoading={isLoading} />

      {isLoading && (
        <div className="d-flex justify-content-center my-3">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <span className="ms-2">Scanning...</span>
        </div>
      )}

      {error && (
        <div className="alert alert-danger mt-3" role="alert">
          {error}
        </div>
      )}

      {/* Step 8: User read security vulnerabilities testing result */}
      {results && <ResultsDisplay data={results} />}
       {/* Handle the specific "nothing to view" case based on Figure 3 */}
      {results?.message === "nothing to view" && !error && (
         <div className="alert alert-warning mt-3">
             Nothing to view. Please check the URL and ensure it is valid and accessible.
         </div>
      )}

    </div>
  );
}

export default ScanPage;