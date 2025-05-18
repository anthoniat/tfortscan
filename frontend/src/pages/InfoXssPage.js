// src/pages/InfoXssPage.js
import React from 'react';

function InfoXssPage() {
  // Standard information about Cross-Site Scripting (XSS)
  return (
    <div className="info-page-container">
      <h2>About Cross-Site Scripting (XSS)</h2>
      <hr/>

      <h4>What is Cross-Site Scripting (XSS)?</h4>
      <p>
        Cross-Site Scripting (XSS) is a type of security vulnerability typically found in web applications. XSS attacks enable attackers to inject client-side scripts (usually JavaScript) into web pages viewed by other users. When the victim views the compromised page, the malicious script executes within their browser, allowing the attacker to bypass access controls, steal session cookies, deface websites, or redirect the user to malicious sites.
      </p>

      <h4>How does it work?</h4>
      <p>
        XSS vulnerabilities occur when a web application uses input from a user within the output it generates without validating or encoding it. An attacker can then supply malicious script content which the application includes in the page sent to a victim's browser. Common types include:
      </p>
      <ul>
          <li><strong>Reflected XSS:</strong> The malicious script comes from the victim's current HTTP request (e.g., in a URL parameter) and is reflected back by the server into the page content.</li>
          <li><strong>Stored XSS (Persistent XSS):</strong> The malicious script is permanently stored on the target server (e.g., in a database, message forum, comment field) and is served to any user who views the stored content.</li>
          <li><strong>DOM-based XSS:</strong> The vulnerability exists in the client-side code (JavaScript) itself. The script modifies the Document Object Model (DOM) environment in the victim's browser using unsafe user input, causing the script to execute.</li>
      </ul>


      <h4>Ways to Prevent XSS:</h4>
      <ul>
        <li>
          <strong>Encode Output Data:</strong> This is the most crucial defense. Encode data based on the context it's being placed into (HTML body, HTML attributes, JavaScript data, CSS). Use libraries designed for contextual output encoding (e.g., OWASP ESAPI, framework-specific functions like those in React for JSX).
        </li>
        <li>
          <strong>Validate and Sanitize User Input:</strong> Treat all input as untrusted. Validate input based on expected format, length, and characters (use allow-lists). Sanitize input by removing or neutralizing potentially dangerous characters/tags, but rely more heavily on output encoding.
        </li>
        <li>
            <strong>Implement Content Security Policy (CSP):</strong> Define a strict CSP header to tell the browser which sources of content (scripts, styles, images) are legitimate. This can drastically reduce the impact of XSS even if an injection occurs.
        </li>
        <li>
            <strong>Use Secure Frameworks:</strong> Modern web frameworks (like React, Angular, Vue) often have built-in protections against XSS (like automatic output encoding in JSX). Understand and leverage these features correctly.
        </li>
        <li>
            <strong>Set HTTPOnly Cookie Flag:</strong> Prevent JavaScript from accessing sensitive session cookies by setting the `HttpOnly` attribute on them.
        </li>
         <li>
            <strong>Scan Regularly:</strong> Regularly scan your web applications for XSS and other vulnerabilities using automated tools and manual testing.
        </li>
      </ul>
        <p className="text-muted mt-4">Note: Preventing XSS requires a combination of these techniques applied diligently throughout the application.</p>
    </div>
  );
}

export default InfoXssPage;