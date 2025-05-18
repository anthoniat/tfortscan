// src/components/ResultsDisplay.js
import React from 'react';
import { Link } from 'react-router-dom';

// Helper to render boolean results nicely (keep as is)
const renderResult = (value) => {
    if (typeof value === 'boolean') {
        return value ?
          <span className="badge bg-danger">Detected / Present</span> :
          <span className="badge bg-success">Not Detected / Missing</span>;
      }
      if (value === 'Error requesting URL') {
        return <span className="badge bg-warning text-dark">Error Checking</span>;
      }
      if (value === null || value === undefined) {
        return <span className="badge bg-secondary">N/A</span>;
      }
      if (Array.isArray(value) && value.length === 0) {
          return <span className="text-muted">None found</span>;
      }
      if (Array.isArray(value)) {
           return <span>{value.join(', ')}</span>;
      }
      return <span>{JSON.stringify(value)}</span>;
};

// Helper to map backend keys to user-friendly names (keep as is)
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
};

function ResultsDisplay({ data }) {
    if (!data || data.message === "nothing to view" || !data.results) {
        return null;
    }

    const results = data.results;
    const errors = data.errors;

    const mainResultKeys = Object.keys(results).filter(key =>
        !key.endsWith('_details') && key !== 'ip_address'
    );

    const sqliFormDetails = results.sqli_details;
    const xssDetails = results.xss_details;

    const showDetailsSection = (sqliFormDetails && sqliFormDetails.length > 0) || xssDetails;

    return (
        // Added results-card class
        <div className="card mt-4 results-card">
            <div className="card-header">
                Scan Results
            </div>
            <div className="card-body">
                {/* Error Display */}
                {errors && (
                    <div className="alert alert-warning">
                        <strong>Note:</strong> Some errors occurred during the scan: {JSON.stringify(errors)}
                    </div>
                )}

                {/* Main Results Table */}
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
                                {key === "Scan Ports" ? (
                                    <td>
                                        {Array.isArray(results[key]) && results[key].length > 0
                                            ? results[key].join(', ')
                                            : (Array.isArray(results[key]) ? <span className="text-muted">None found</span> : renderResult(results[key]))
                                        }
                                        {results['ip_address'] && ` (IP: ${results['ip_address']})`}
                                    </td>
                                ) : (
                                     <td>{renderResult(results[key])}</td>
                                )}
                            </tr>
                        ))}
                    </tbody>
                </table>

                {/* Check Details Section - Wrapped in a div with check-details-section class */}
                {showDetailsSection && (
                    <div className="check-details-section"> {/* Added class wrapper */}
                        {/* <hr />  Removed HR as section styling provides separation */}
                        <h5>Check Details:</h5>

                        {/* SQLi Detailed Form Info */}
                        {sqliFormDetails && sqliFormDetails.length > 0 && (
                            <div className="mb-3">
                                <strong>SQL Injection Potential Forms Found:</strong>
                                {sqliFormDetails.map((form, index) => (
                                    <div key={index} className="card mt-2 mb-2 shadow-sm">
                                       <div className="card-body" style={{ fontSize: '0.9em' }}>
                                            <p className="card-title" style={{ marginBottom: '5px' }}><strong>Form {index + 1}:</strong></p>
                                            <p style={{ margin: '2px 0' }}> Action URL: <code>{form.action || '(None Specified)'}</code></p>
                                            <p style={{ margin: '2px 0' }}> Method: <code>{form.method || 'GET'}</code></p>
                                            <p style={{ margin: '2px 0' }}> Input Fields:</p>
                                            {form.inputs && form.inputs.length > 0 ? (
                                                <ul style={{ margin: '2px 0 2px 15px', paddingLeft: '15px', listStyleType: 'disc' }}>
                                                    {form.inputs.map((input, i) => (
                                                        <li key={i}>
                                                            <code>{input.name || '(No Name)'}</code> (Type: <code>{input.type || 'text'}</code>)
                                                        </li>
                                                    ))}
                                                </ul>
                                            ) : (
                                                <em style={{ marginLeft: '15px' }}> No input fields identified within this form.</em>
                                            )}
                                       </div>
                                    </div>
                                ))}
                            </div>
                        )} {/* Closing div for SQLi details */}

                        {/* XSS Details */}
                        {xssDetails && (
                            <div>
                                <p><small><strong>XSS Details:</strong> {xssDetails}</small></p>
                            </div>
                        )} {/* Closing div for XSS details */}

                    </div> /* Closing check-details-section div */
                )} {/* Closing outer conditional block for details */}


                {/* Next Steps / Solutions Section - Wrapped in a div with next-steps-section class */}
                <div className="next-steps-section"> {/* Added class wrapper */}
                    <hr/>
                    <h5>Next Steps / Solutions</h5>
                    <p>Review the results above. For detected vulnerabilities or
                       missing security headers, consult security best practices:</p>
                     <ul>
                        <li>
                            <strong>SQL Injection:</strong> Use parameterized queries
                            or prepared statements. Validate and sanitize all user input. Implement
                            least privilege database access. (<Link to="/info/sql">Learn
                            more</Link>)
                        </li>
                        <li>
                            <strong>XSS:</strong> Implement strict Content Security
                            Policy (CSP). Contextually encode output data (HTML, JS, CSS). Validate and
                            sanitize user input. Use modern web frameworks with built-in XSS
                            protection. (<Link to="/info/xss">Learn more</Link>)
                        </li>
                        <li>
                            <strong>Open Ports:</strong> Ensure only necessary ports
                            are open to the public internet. Use firewalls to restrict access.
                        </li>
                        <li>
                            <strong>Security Headers:</strong> Implement missing
                            headers like HSTS, CSP, X-Frame-Options, X-Content-Type-Options to mitigate
                            various attacks. (<Link to="/info/headers">Learn more</Link>)
                        </li>
                     </ul>
                </div> {/* Closing next-steps-section div */}

            </div> {/* Closing card-body */}
        </div> /* Closing results-card div */
    );
}

export default ResultsDisplay;