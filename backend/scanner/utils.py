import requests
import urllib.parse
import socket

def validate_and_normalize_url(url_string):
    """
    Validates the URL format and ensures it has a scheme (http/https).
    Returns the normalized URL or None if invalid.
    """
    if not url_string:
        return None

    # Add scheme if missing (default to http)
    if not url_string.startswith(('http://', 'https://')):
        url_string = 'http://' + url_string

    try:
        parsed = urllib.parse.urlparse(url_string)
        # Basic check: scheme and netloc must exist
        if not parsed.scheme or not parsed.netloc:
            return None
        # Optional: More robust check (e.g., using regex or domain validation)
        return parsed.geturl()
    except ValueError:
        return None

def make_request(url, timeout=10):
    """Makes a GET request to the URL and returns the response object."""
    try:
        # Add a user-agent to mimic a browser slightly
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 ToniaVulnScanner/1.0'
        }
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        return response
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out for {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

def get_domain_from_url(url_string):
    """Extracts the domain name (netloc) from a URL."""
    try:
        parsed = urllib.parse.urlparse(url_string)
        return parsed.netloc
    except ValueError:
        return None