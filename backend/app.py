# backend/app.py

# --- Core Flask Imports ---
# Ensure Flask, request, AND jsonify are imported
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# --- Standard Library Imports ---
import sqlite3  # <--- FIX for "Unresolved reference 'sqlite3'"
import datetime #

# --- Project-specific Imports ---
from scanner.utils import validate_and_normalize_url
from scanner.header_scanner import check_security_headers
from scanner.port_scanner import check_common_ports
# Ensure the SQLi scanner function IS imported
from scanner.sqli_scanner import check_sqli_potential # <--- FIX for "Unresolved reference 'check_sqli_potential'"
# Ensure the XSS scanner function IS imported
from scanner.xss_scanner import check_xss_potential

# --- Global Variables / Constants ---
app = Flask(__name__)
CORS(app) # Allow requests from React frontend (adjust origins in production)

# Define the database file name
DATABASE = 'scanner_history.db' # <--- FIX for "Unresolved reference 'DATABASE'"

# --- Database Initialization Function (Should be present from previous steps) ---
def init_db():
    conn = None
    try:
        # Use the defined DATABASE constant
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
                open_ports TEXT,
                header_x_frame BOOLEAN,
                header_hsts BOOLEAN,
                header_policy BOOLEAN,
                header_xxss BOOLEAN,
                header_nonsnif BOOLEAN,
                scan_errors TEXT,
                details TEXT
            )
        ''')
        conn.commit()
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()

# --- Database Saving Function (Use the corrected version from the previous response) ---
def save_scan_to_db(target_url, results, errors):
    conn = None
    try:
        # Use the defined DATABASE constant
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        open_ports_json = json.dumps(results.get("Scan Ports", []))
        errors_json = json.dumps(errors) if errors else None

        details_data = {
            "sqli": results.get("sqli_details"),
            "xss": results.get("xss_details")
        }
        details_json = json.dumps({k: v for k, v in details_data.items() if v})

        cursor.execute('''
            INSERT INTO scan_results (
                target_url, is_link_valid, vulnerabilities_test_ran,
                sqli_potential, xss_potential, open_ports,
                header_x_frame, header_hsts, header_policy, header_xxss,
                header_nonsnif,
                scan_errors, details
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            target_url,
            results.get("Check if the link is valid or not", False),
            results.get("Vulnerabilities Test", False),
            results.get("SQL Injection Test", False), # Use False default
            results.get("XSS Test", False),          # Use False default
            open_ports_json,
            results.get("Header of x-frame", False), # Use False default
            results.get("Header of hsts", False),    # Use False default
            results.get("Header of policy", False),  # Use False default
            results.get("Header of xxss", False),    # Use False default
            results.get("Header of nonsnif", False), # Use False default
            errors_json,
            details_json
        ))
        conn.commit()
        print(f"Successfully saved scan results for {target_url} to database.")

    except sqlite3.Error as e:
        print(f"Database error while saving scan for {target_url}: {e}")
    finally:
        if conn:
            conn.close()

# --- Flask Routes ---

@app.route('/')
def index():
    return "Tonia Vuln Scanner Backend is running!"

@app.route('/api/scan', methods=['POST'])
def handle_scan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400 # Ensure jsonify is imported

    data = request.get_json()
    target_url_raw = data.get('url')

    if not target_url_raw:
        return jsonify({"error": "URL is required"}), 400 # Ensure jsonify is imported

    target_url = validate_and_normalize_url(target_url_raw)

    results = {}
    errors = {}

    if not target_url:
        # Prepare specific response for invalid initial URL
        response_data_invalid = { # Define the variable before use
            "message": "nothing to view",
            "results": None,
            "error": "Invalid URL format provided."
        }
        # Optionally save invalid attempt
        # save_scan_to_db(target_url_raw, {"Check if the link is valid or not": False}, {"Validation": "Invalid URL format provided."})
        return jsonify(response_data_invalid), 400 # Use the defined variable

    print(f"Received scan request for: {target_url}")

    try:
        # Perform checks
        results["Check if the link is valid or not"] = True # If validation passed, it's valid structurally

        print("Checking Headers...")
        results.update(check_security_headers(target_url))

        print("Checking Ports...")
        port_results = check_common_ports(target_url)
        if isinstance(port_results, dict):
            results.update(port_results)
        else:
            errors["PortScanFormat"] = "Unexpected port scan result format"

        print("Checking SQLi Potential...")
        sqli_result = check_sqli_potential(target_url) # Use the imported function
        results["SQL Injection Test"] = sqli_result.get("SQL Injection Test", False)
        results["sqli_details"] = sqli_result.get("sqli_details", [])
        if sqli_result.get("error_message"):
             errors["SQLiError"] = sqli_result["error_message"]

        print("Checking XSS Potential...")
        xss_result = check_xss_potential(target_url) # Use the imported function
        results["XSS Test"] = xss_result.get("XSS Test", False)
        results["xss_details"] = xss_result.get("xss_details") # Assuming xss returns details string
        if xss_result.get("error_message"):
             errors["XSSError"] = xss_result["error_message"]


        # Mark main vulnerability test as ran successfully at this point
        results["Vulnerabilities Test"] = True

    except Exception as e:
        print(f"Error during scanning process for {target_url}: {e}")
        errors["ScanProcessError"] = str(e)
        results["Vulnerabilities Test"] = False # Mark as Fail if scan crashes

    # --- Define response_data before using it ---
    response_data = { # <--- FIX for "Unresolved reference 'response_data'"
        "message": "Scan completed",
        "results": results,
        "errors": errors if errors else None
    }

    print(f"Sending results: {json.dumps(response_data, indent=2)}")

    # Save results to database (regardless of scan success/failure)
    save_scan_to_db(target_url, results, errors)

    # Return the JSON response
    return jsonify(response_data) # <--- Use the defined response_data


# Optional History Endpoint (ensure imports/constants are available)
@app.route('/api/scans/history', methods=['GET'])
def get_scan_history():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE) # Use constant
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scan_results ORDER BY scan_timestamp DESC LIMIT 50")
        scans = cursor.fetchall()
        scan_history = [dict(scan) for scan in scans]
        return jsonify(scan_history) # Use imported jsonify
    except sqlite3.Error as e:
        print(f"Database error fetching history: {e}")
        return jsonify({"error": "Failed to retrieve scan history", "details": str(e)}), 500 # Use imported jsonify
    finally:
        if conn:
            conn.close()


# --- Main Execution ---
if __name__ == '__main__':
    init_db() # Initialize DB when app starts
    app.run(debug=True, port=5000)