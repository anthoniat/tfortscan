// src/pages/InfoHeadersPage.js
import React from 'react';

function InfoHeadersPage() {
  // Content based on security headers checked
  return (
    <div className="info-page-container">
      <h2>About Security Headers</h2>
      <hr/>

      <h4>What are Security Headers?</h4>
      <p>
        HTTP security headers are directives web applications can use to configure security defenses in web browsers. They help mitigate attacks like Cross-Site Scripting (XSS), clickjacking, information disclosure, and more.
      </p>

      <h4>Common Security Headers Checked:</h4>
      <ul>
        <li>
          <strong>X-Frame-Options:</strong> Prevents your site from being embedded in an iframe on other sites, mitigating clickjacking attacks. Common values are `DENY` or `SAMEORIGIN`.
        </li>
        <li>
          <strong>Strict-Transport-Security (HSTS):</strong> Tells browsers to only communicate with the server over HTTPS, preventing protocol downgrade attacks and cookie hijacking.
        </li>
         <li>
            <strong>Content-Security-Policy (CSP):</strong> A powerful header that defines allowed sources for content (scripts, styles, images, etc.), effectively preventing many types of injection attacks, including XSS.
         </li>
        <li>
          <strong>X-Content-Type-Options:</strong> Usually set to `nosniff`. Prevents browsers from trying to guess (MIME-sniff) the content type of a resource if it differs from the declared `Content-Type` header, which can help prevent certain XSS vectors.
        </li>
         <li>
            <strong>X-XSS-Protection:</strong> An older header largely superseded by CSP. It instructs browsers to enable their built-in reflective XSS filters. Often set to `1; mode=block`. While deprecated, its presence can still offer some protection in older browsers.
        </li>
      </ul>

       <h4>How to Implement Them:</h4>
       <p>
         These headers are typically configured on your web server (like Nginx, Apache) or within your web application framework (like Flask, Express, etc.). Consult the documentation for your specific server/framework.
       </p>

        <p className="text-muted mt-4">Note: Implementing security headers correctly is crucial for web application security.</p>
    </div>
  );
}

export default InfoHeadersPage;