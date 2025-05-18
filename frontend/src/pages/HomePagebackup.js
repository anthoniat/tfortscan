import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="text-center">
      <h1 className="display-3 my-4">Welcome to Tonia Vuln Scanner</h1>
      <p className="lead">
        A simple tool to perform basic security checks on websites.
      </p>
       <p className="text-danger">
        <strong>Disclaimer:</strong> Only use this tool on websites you have explicit permission to test. Unauthorized scanning is illegal and unethical.
       </p>
      <Link to="/scan" className="btn btn-primary btn-lg mt-3">
        Start Scanning
      </Link>
       <hr className="my-4"/>
       <h2>Learn More</h2>
       <div className="list-group w-50 mx-auto">
           <Link to="/info/sql" className="list-group-item list-group-item-action">SQL Injection Info</Link>
           <Link to="/info/xss" className="list-group-item list-group-item-action">Cross-Site Scripting (XSS) Info</Link>
           <Link to="/info/headers" className="list-group-item list-group-item-action">Security Headers Info</Link>
       </div>
    </div>
  );
}

export default HomePage;