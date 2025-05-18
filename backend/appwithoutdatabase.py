from flask import Flask, request, jsonify
from flask_cors import CORS
import json # Import json module

# Import scanner functions
from scanner.utils import validate_and_normalize_url
from scanner.header_scanner import check_security_headers
from scanner.port_scanner import check_common_ports
from scanner.sqli_scanner import check_sqli_potential # Basic check
from scanner.xss_scanner import check_xss_potential  # Basic check

app = Flask(__name__)
CORS(app) # Allow requests from React frontend (adjust origins in production)

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

    # Step 3 (Backend): Validate Link (using our utility function)
    target_url = validate_and_normalize_url(target_url_raw)
    if not target_url:
         # Send back a specific structure frontend might expect for invalid link
        return jsonify({
            "message": "nothing to view", # As per use case scenario step 3
            "results": None,
            "error": "Invalid URL format provided."
        }), 400 # Bad Request

    print(f"Received scan request for: {target_url}") # Log the validated URL

    # Step 6: Pass link to python functions for processing
    results = {}
    errors = {}

    try:
        # --- Functional Requirement: Check if link is valid (already done implicitly by reaching here) ---
        # We add an explicit check result based on initial validation + request attempt
        initial_request_check = validate_and_normalize_url(target_url_raw) is not None
        results["Check if the link is valid or not"] = initial_request_check # Functional Requirement

        if initial_request_check:
             # --- Security Requirements ---
            print("Checking Headers...")
            results.update(check_security_headers(target_url))

            print("Checking Ports...")
            results.update(check_common_ports(target_url)) # Example: Check ports 80, 443

            print("Checking SQLi Potential...")
            sqli_result = check_sqli_potential(target_url)
            results["SQL Injection Test"] = sqli_result.get("SQL Injection Test", False)
            if 'details' in sqli_result: results["sqli_details"] = sqli_result['details']

            print("Checking XSS Potential...")
            xss_result = check_xss_potential(target_url)
            results["XSS Test"] = xss_result.get("XSS Test", False)
            if 'details' in xss_result: results["xss_details"] = xss_result['details']

            # --- Combined Vulnerabilities Test (Pass if basic checks done) ---
            # This can be a simple flag indicating scans were attempted
            results["Vulnerabilities Test"] = True # Mark as Pass (meaning tests were run)
        else:
             results["Vulnerabilities Test"] = False # Mark as Fail (link invalid)
             errors["Validation"] = "Initial URL validation failed."


    except Exception as e:
        print(f"Error during scanning: {e}")
        errors["ScanError"] = str(e)
        # Ensure main vulnerability test indicates failure if scan crashes
        results["Vulnerabilities Test"] = False


    # Step 7: After processing, result sent via API to frontend
    response_data = {
        "message": "Scan completed",
        "results": results,
        "errors": errors if errors else None
    }
    print(f"Sending results: {json.dumps(response_data, indent=2)}") # Log the response
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run on port 5000 typically