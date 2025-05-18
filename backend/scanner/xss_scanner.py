# WARNING: Basic XSS check. Real detection is much more complex.
# This looks for simple reflections of basic script tags in non-standard places.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from .utils import make_request

def check_xss_potential(url):
    """
    Performs a *very basic* check for reflected XSS by injecting a simple
    payload into URL parameters if they exist.
    """
    is_vulnerable = False
    details = "No obvious reflection found or no parameters to test."
    test_payload = "<script>alert('ToniaVulnXSS')</script>"
    encoded_payload = requests.utils.quote(test_payload) # URL-encode the payload

    original_response = make_request(url)
    if not original_response:
        return {"XSS Test": False, "details": "Could not fetch original URL."}

    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if not query_params:
        # Try finding forms and testing their inputs (more complex)
        # For now, if no URL params, report as likely not vulnerable via this method
        details = "No URL parameters found to test for reflected XSS."
        return {"XSS Test": False, "details": details}

    # Test each parameter
    for param in query_params:
        # Create a copy of params to modify
        test_params = parse_qs(parsed_url.query)
        # Inject payload (replace existing value)
        test_params[param] = [encoded_payload] # Use the encoded payload here

        # Rebuild the URL with the injected parameter
        test_query = urlencode(test_params, doseq=True)
        test_url_parts = list(parsed_url)
        test_url_parts[4] = test_query # Index 4 is the query string
        test_url = urlunparse(test_url_parts)

        print(f"Testing XSS with URL: {test_url}") # For debugging
        test_response = make_request(test_url)

        if test_response and test_response.text:
            # Check if the *exact* payload string appears unescaped in the response HTML
            # This is a weak check, real XSS can be much subtler
            if test_payload in test_response.text:
                 # Basic check passed - needs further investigation
                # Check if it's inside a safe context (like a <textarea> or properly escaped)
                # Using BeautifulSoup to see if the <script> tag exists as a tag (not just text)
                try:
                    soup = BeautifulSoup(test_response.text, 'lxml')
                    scripts = soup.find_all('script')
                    found_in_script_tag = any('ToniaVulnXSS' in str(s) for s in scripts)

                    if found_in_script_tag:
                         is_vulnerable = True
                         details = f"Potential reflected XSS found in parameter '{param}'. Payload '{test_payload}' reflected in response's script tags."
                         print(details) # For debugging
                         break # Found one, no need to check others for this basic scan
                    elif test_payload in test_response.text:
                         # Reflected as text, maybe less severe but still notable
                         is_vulnerable = True # Still flag as potential
                         details = f"Potential reflected XSS found in parameter '{param}'. Payload '{test_payload}' reflected as plain text in response."
                         print(details) # For debugging
                         break

                except Exception as e:
                    print(f"Error parsing response for XSS check: {e}")


    if not is_vulnerable and details == "No obvious reflection found or no parameters to test.":
         details = "No simple reflected XSS found in URL parameters."


    return {"XSS Test": is_vulnerable, "details": details}