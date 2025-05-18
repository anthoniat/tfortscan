from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3 # Import SQLite library
import datetime # To record timestamp

# Import scanner functions
from scanner.utils import validate_and_normalize_url
from scanner.header_scanner import check_security_headers
from scanner.port_scanner import check_common_ports
from scanner.sqli_scanner import check_sqli_potential # Basic check
from scanner.xss_scanner import check_xss_potential  # Basic check

app = Flask(__name__)
CORS(app)

DATABASE = 'scanner_history.db' # Database file name

# --- Database Initialization ---
def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        print("Initializing database...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT NOT NULL,
                scan_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_link_valid BOOLEAN,
                vulnerabilities_test_ran BOOLEAN,
                sqli_potential BOOLEAN,
                xss_potential BOOLEAN,
                open_ports TEXT, -- Store as JSON string
                header_x_frame BOOLEAN,
                header_hsts BOOLEAN,
                header_policy BOOLEAN,
                header_xxss BOOLEAN,
                header_nonsnif BOOLEAN,
                scan_errors TEXT, -- Store as JSON string or simple text
                details TEXT -- Store as JSON string (e.g., sqli/xss details)
            )
        ''')
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()

# --- Function to save scan results ---
def save_scan_to_db(target_url, results, errors):
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Prepare data for insertion - use .get() for safety
        # Convert potentially complex data (lists, dicts) to JSON strings
        open_ports_json = json.dumps(results.get("Scan Ports", []))
        errors_json = json.dumps(errors) if errors else None
        details_data = {
            "sqli": results.get("sqli_details"),
            "xss": results.get("xss_details")
        }
        details_json = json.dumps({k: v for k, v in details_data.items() if v is not None}) # Only include non-null details


        cursor.execute('''
            INSERT INTO scan_results (
                target_url, is_link_valid, vulnerabilities_test_ran,
                sqli_potential, xss_potential, open_ports,
                header_x_frame, header_hsts, header_policy, header_xxss, header_nonsnif,
                scan_errors, details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            target_url,
            results.get("Check if the link is valid or not", False),
            results.get("Vulnerabilities Test", False),
            results.get("SQL Injection Test", None), # Allow NULL if not run/error
            results.get("XSS Test", None),          # Allow NULL if not run/error
            open_ports_json,
            results.get("Header of x-frame", None),
            results.get("Header of hsts", None),
            results.get("Header of policy", None),
            results.get("Header of xxss", None),
            results.get("Header of nonsnif", None),
            errors_json,
            details_json
        ))
        conn.commit()
        print(f"Successfully saved scan results for {target_url} to database.")

    except sqlite3.Error as e:
        print(f"Database error while saving scan for {target_url}: {e}")
        # Optionally rollback if needed, but commit happens only on success here
    finally:
        if conn:
            conn.close()


@app.route('/')
def index():
    return "Tonia Vuln Scanner Backend is running!"

@app.route('/api/scan', methods=['POST'])
def handle_scan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    target_url_raw = data.get('url')

    if not target_url_raw:
        return jsonify({"error": "URL is required"}), 400

    # Step 3 (Backend): Validate Link
    target_url = validate_and_normalize_url(target_url_raw)
    if not target_url:
        # Prepare response for invalid link
        response_data = {
            "message": "nothing to view",
            "results": None,
            "error": "Invalid URL format provided."
        }
        # Also save this attempt to the DB (optional, but can be useful)
        # save_scan_to_db(target_url_raw, {"Check if the link is valid or not": False}, {"Validation": "Invalid URL format provided."})
        return jsonify(response_data), 400

    print(f"Received scan request for: {target_url}")

    # Step 6: Pass link to python functions for processing
    results = {}
    errors = {}

    try:
        # --- Functional Requirement: Check if link is valid ---
        initial_request_check = validate_and_normalize_url(target_url_raw) is not None
        results["Check if the link is valid or not"] = initial_request_check # Functional Requirement

        if initial_request_check:
             # --- Security Requirements ---
            print("Checking Headers...")
            results.update(check_security_headers(target_url))

            print("Checking Ports...")
            # Ensure check_common_ports returns a dictionary compatible with results.update()
            port_results = check_common_ports(target_url)
            if isinstance(port_results, dict):
                results.update(port_results)
            else:
                errors["PortScanFormat"] = "Unexpected port scan result format"


            print("Checking SQLi Potential...")
            sqli_result = check_sqli_potential(target_url)
            results["SQL Injection Test"] = sqli_result.get("SQL Injection Test", False)
            if 'details' in sqli_result: results["sqli_details"] = sqli_result['details']

            print("Checking XSS Potential...")
            xss_result = check_xss_potential(target_url)
            results["XSS Test"] = xss_result.get("XSS Test", False)
            if 'details' in xss_result: results["xss_details"] = xss_result['details']

            # --- Combined Vulnerabilities Test ---
            results["Vulnerabilities Test"] = True
        else:
             results["Vulnerabilities Test"] = False
             errors["Validation"] = "Initial URL validation failed."

    except Exception as e:
        print(f"Error during scanning process for {target_url}: {e}")
        errors["ScanProcessError"] = str(e)
        results["Vulnerabilities Test"] = False # Mark as Fail if scan crashes

    # --- Save results to database ---
    # We save regardless of scan success/failure to have a record
    save_scan_to_db(target_url, results, errors)

    # Step 7: Send result via API to frontend
    response_data = {
        "message": "Scan completed",
        "results": results,
        "errors": errors if errors else None
    }
    print(f"Sending results: {json.dumps(response_data, indent=2)}") # Log the response
    return jsonify(response_data)

# --- Optional: Add endpoint to view history (Example) ---
@app.route('/api/scans/history', methods=['GET'])
def get_scan_history():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row # Return rows as dict-like objects
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scan_results ORDER BY scan_timestamp DESC LIMIT 50") # Get latest 50
        scans = cursor.fetchall()
        # Convert Row objects to dictionaries for JSON serialization
        scan_history = [dict(scan) for scan in scans]
        return jsonify(scan_history)
    except sqlite3.Error as e:
        print(f"Database error fetching history: {e}")
        return jsonify({"error": "Failed to retrieve scan history", "details": str(e)}), 500
    finally:
        if conn:
            conn.close()

# --- Main Execution ---
if __name__ == '__main__':
    init_db() # Initialize DB when app starts
    app.run(debug=True, port=5000)