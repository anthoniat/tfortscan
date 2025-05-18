import React from 'react';
import { Link } from 'react-router-dom';

// Add className="homepage-container" to the main div
// Add className="homepage-disclaimer" to the disclaimer paragraph
// Add className="learn-more-section" to the div containing the h2 and list group

function HomePage() {
  return (
    <div className="text-center homepage-container"> {/* Added class */}
      <h1 className="display-3 my-4">Welcome to Tonia Vuln Scanner</h1>
      {/* ... */}
      <p className="text-danger homepage-disclaimer"> {/* Added class */}
        <strong>Disclaimer:</strong> Only use this tool on websites you
        have explicit permission to test. Unauthorized scanning is illegal and
        unethical.
      </p>
      {/* ... */}
      <div className="learn-more-section"> {/* Added wrapper div and class */}
        <hr className="my-4"/>
        <h2>Learn More</h2>
        <div className="list-group w-50 mx-auto">
           <Link to="/info/sql" className="list-group-item list-group-item-action">SQL Injection Info</Link>
           <Link to="/info/xss" className="list-group-item list-group-item-action">Cross-Site Scripting (XSS) Info</Link>
           <Link to="/info/headers" className="list-group-item list-group-item-action">Security Headers Info</Link>
     </div>
      </div>
    </div>
  );
}
export default HomePage;