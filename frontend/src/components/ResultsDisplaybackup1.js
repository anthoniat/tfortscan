import { Link } from 'react-router-dom';
import React from 'react';

// Helper to render boolean results nicely
const renderResult = (value) => {
    if (typeof value === 'boolean') {
        return value ?
            <span className="badge bg-danger">Detected / Present</span> :
            <span className="badge bg-success">Not Detected / Missing</span>;
    }
     if (value === 'Error requesting URL') {
         return <span className="badge bg-warning text-dark">Error Checking</span>;
     }
     // Handle other types if needed (e.g., strings, numbers)
     if (value === null || value === undefined){
         return <span className="badge bg-secondary">N/A</span>;
     }
     // Default rendering for non-boolean (like port list)
     return <span>{JSON.stringify(value)}</span>;
};


// Helper to map backend keys to user-friendly names
const resultLabels = {
    "Check if the link is valid or not": "Link Validity Check",
    "Vulnerabilities Test": "Vulnerability Scan Status",
    "SQL Injection Test": "SQL Injection Potential",
    "XSS Test": "XSS Potential (Reflected)",
    "Scan Ports": "Open Ports Found",
    "Header of x-frame": "X-Frame-Options Header",
    "Header of hsts": "Strict-Transport-Security (HSTS) Header",
    "Header of policy": "Content-Security-Policy Header",
    "Header of xxss": "X-XSS-Protection Header",
    "Header of nonsnif": "X-Content-Type-Options (nosniff) Header",
    // Internal details keys - maybe hide or display differently
    "sqli_details": "SQLi Check Details",
    "xss_details": "XSS Check Details",
};

function ResultsDisplay({ data }) {
   // Handle the "nothing to view" message explicitly if needed,
   // although ScanPage handles the main display for this now.
   if (!data || data.message === "nothing to view" || !data.results) {
     return null; // Don't render anything if no results or specific message handled above
   }

   const results = data.results;
   const errors = data.errors;

   // Filter out detail keys for the main table
   const mainResultKeys = Object.keys(results).filter(key => !key.endsWith('_details'));


   return (
     <div className="card mt-4">
       <div className="card-header">
         Scan Results
       </div>
       <div className="card-body">
         {errors && (
             <div className="alert alert-warning">
                 <strong>Note:</strong> Some errors occurred during the scan: {JSON.stringify(errors)}
             </div>
         )}
          <table className="table table-striped table-hover">
             <thead>
                 <tr>
                     <th>Check</th>
                     <th>Result</th>
                 </tr>
             </thead>
             <tbody>
                 {mainResultKeys.map(key => (
                     <tr key={key}>
                         <td>{resultLabels[key] || key}</td>
                         {/* Special rendering for port list */}
                         {key === "Scan Ports" ? (
                             <td>
                                 {Array.isArray(results[key]) && results[key].length > 0
                                     ? results[key].join(', ')
                                     : (Array.isArray(results[key]) ? <span className="text-muted">None found</span> : renderResult(results[key]))
                                 }
                                 {/* Show IP if available */}
                                 {results['ip_address'] && ` (IP: ${results['ip_address']})`}
                             </td>
                         ) : (
                             <td>{renderResult(results[key])}</td>
                         )}
                     </tr>
                 ))}
             </tbody>
         </table>

          {/* Display details if they exist */}
         {(results.sqli_details || results.xss_details) && (
             <>
                 <hr />
                 <h5>Check Details:</h5>
                 {results.sqli_details && <p><small><strong>SQLi:</strong> {results.sqli_details}</small></p>}
                 {results.xss_details && <p><small><strong>XSS:</strong> {results.xss_details}</small></p>}
             </>
          )}

         {/* Post Condition: The User read testing result, and solution */}
         <hr/>
         <h5>Next Steps / Solutions</h5>
         <p>Review the results above. For detected vulnerabilities or missing security headers, consult security best practices:</p>
         <ul>
             <li><strong>SQL Injection:</strong> Use parameterized queries or prepared statements. Validate and sanitize all user input. Implement least privilege database access. (<Link to="/info/sql">Learn more</Link>)</li>
             <li><strong>XSS:</strong> Implement strict Content Security Policy (CSP). Contextually encode output data (HTML, JS, CSS). Validate and sanitize user input. Use modern web frameworks with built-in XSS protection. (<Link to="/info/xss">Learn more</Link>)</li>
             <li><strong>Open Ports:</strong> Ensure only necessary ports are open to the public internet. Use firewalls to restrict access.</li>
             <li><strong>Security Headers:</strong> Implement missing headers like HSTS, CSP, X-Frame-Options, X-Content-Type-Options to mitigate various attacks. (<Link to="/info/headers">Learn more</Link>)</li>
         </ul>
       </div>
     </div>
   );
}

export default ResultsDisplay;