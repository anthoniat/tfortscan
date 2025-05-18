# backend/scanner/sqli_scanner.py
import requests
from bs4 import BeautifulSoup
# Make sure urljoin is imported
from urllib.parse import urljoin, urlparse
from .utils import make_request
import json # Import json for potential future use if needed, not strictly required here

def check_sqli_potential(url):
    """
    Performs a *very basic* check for potential SQLi entry points by
    identifying HTML forms and their details. Does NOT attempt injection.
    Returns a dictionary containing a boolean test result and details
    about the forms found.
    """
    potential_forms = [] # Store details of forms found
    details_message = "No forms found or error during request." # Default message

    response = make_request(url)
    if not response or not response.text:
        return {
            "SQL Injection Test": False,
            # Keep sqli_details consistent, return empty list or specific message
            "sqli_details": [] # Or you could return [{"error": details_message}]
            # "error_message": details_message # Or add a specific error field
        }

    try:
        soup = BeautifulSoup(response.text, 'lxml') # Use lxml if installed
        forms = soup.find_all('form')

        if forms:
            details_message = f"Found {len(forms)} form(s) which might be potential SQLi entry points."
            for form in forms:
                # Get form action URL, resolve relative paths
                action = form.get('action')
                # Resolve action URL relative to the base URL
                absolute_action = urljoin(url, action) if action else url

                # Get form method (default to GET if not specified)
                method = form.get('method', 'get').upper()

                # Find all input fields within the form
                inputs = []
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    input_name = input_tag.get('name')
                    # Include inputs even if they don't have a name, as they might be manipulated
                    # if input_name: # Optional: only include inputs with names
                    input_type = input_tag.get('type', 'text') # Default type if not input or missing
                    if input_tag.name == 'textarea':
                         input_type = 'textarea'
                    elif input_tag.name == 'select':
                         input_type = 'select'

                    inputs.append({
                        'name': input_name or '(No Name)',
                        'type': input_type
                    })

                potential_forms.append({
                    'action': absolute_action,
                    'method': method,
                    'inputs': inputs
                })

            # Return True if forms are found, along with the structured details
            return {
                "SQL Injection Test": True,
                "sqli_details": potential_forms
            }
        else:
            details_message = "No standard HTML forms found on the page."
            # Return False, indicate no forms found in details
            return {
                "SQL Injection Test": False,
                "sqli_details": [] # Return empty list when no forms found
                # "info_message": details_message # Or add an info field
            }

    except Exception as e:
        details_message = f"Error parsing HTML: {e}"
        print(details_message)
        # Return False on error, include error details
        return {
            "SQL Injection Test": False,
            "sqli_details": [], # Return empty list on error
            "error_message": details_message # Add a specific error field
        }