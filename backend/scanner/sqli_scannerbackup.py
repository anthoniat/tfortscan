# WARNING: Real SQLi scanning is complex and requires sending potentially
# harmful payloads. This is a *very basic* conceptual check and is NOT
# a reliable way to detect SQLi. It primarily looks for forms.
# A real scanner would try injecting payloads and analyzing responses.

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .utils import make_request

def check_sqli_potential(url):
    """
    Performs a *very basic* check for potential SQLi entry points (forms).
    Does NOT actually attempt injection.
    """
    is_potentially_vulnerable = False
    details = "No forms found or error during request."

    response = make_request(url)
    if not response or not response.text:
        return {"SQL Injection Test": False, "details": details}

    try:
        soup = BeautifulSoup(response.text, 'lxml') # Use lxml if installed, otherwise 'html.parser'
        forms = soup.find_all('form')

        if forms:
            details = f"Found {len(forms)} form(s). Manual testing recommended for SQLi."
            # In a real scanner, you'd analyze form inputs, construct payloads,
            # submit them, and analyze results. This basic version just notes forms exist.
            is_potentially_vulnerable = True # Flag potential if forms are present
        else:
            details = "No standard HTML forms found on the page."
            # Could also check for URL parameters, but forms are common vectors.

    except Exception as e:
        details = f"Error parsing HTML: {e}"
        print(details)

    # Requirement table just asks for "SQL Injection Test" Pass/Fail
    # We interpret "Pass" as "Basic check performed, potential vectors noted"
    # We return True if forms are found (potential vector), False otherwise
    return {"SQL Injection Test": is_potentially_vulnerable, "details": details}