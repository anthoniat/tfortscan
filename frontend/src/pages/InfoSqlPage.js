import React from 'react';

function InfoSqlPage() {
  // Content based on Figure 4
  return (
    <div className="info-page-container"> {/* Added class */}
      <h2>About SQL Injection (SQLi)</h2>
      <hr/>

      <h4>What is SQL injection?</h4>
      <p>
        A SQL injection is a technique that attackers use to gain unauthorized access to a web application database by adding a string of malicious code to a database query.
      </p>

      <h4>How it's work?</h4>
      <p>
        SQL injection usually occurs when you ask a user for input, like their username/userid, and instead of a name/id, the user gives you an SQL statement that you will unknowingly run on your database.
      </p>

      <h4>Ways to Prevent SQL Injections:</h4>
      <ul>
        <li>
          <strong>Do not trust any user input:</strong> Treat all user input as untrusted. Any user input that is used in an SQL query introduces a risk of an SQL Injection.
        </li>
        <li>
          <strong>Use whitelists, not blacklists:</strong> Don't filter user input based on blacklists; attackers will almost always find a way to circumvent your blacklist. If possible, verify and filter user input using strict whitelists only.
        </li>
        <li>
            <strong>Input Validation and Sanitization:</strong> Strictly validate input formats (e.g., numbers, emails) and sanitize data by escaping special characters before including it in SQL queries.
        </li>
         <li>
            <strong>Use Parameterized Queries / Prepared Statements:</strong> This is the most effective defense. Database systems can distinguish between code and data, preventing injected code from being executed.
        </li>
        <li>
          <strong>Scan regularly:</strong> SQL Injections may be introduced by your developers or through external libraries/modules/software. You should regularly scan your web applications using a web vulnerability scanner.
        </li>
      </ul>
        <p className="text-muted mt-4">Note: The information provided here is a brief overview.</p>
    </div>
  );
}

export default InfoSqlPage;