from .utils import make_request

def check_security_headers(url):
    """Checks for common security headers."""
    headers_found = {
        'x-frame-options': False, # Prevents clickjacking
        'strict-transport-security': False, # HSTS - forces HTTPS
        'content-security-policy': False, # CSP - prevents XSS and data injection
        'x-content-type-options': False, # Prevents MIME type sniffing (often 'nosniff')
        'x-xss-protection': False # Deprecated by CSP, but still sometimes present
    }
    response = make_request(url)
    if not response:
        return {hdr: 'Error requesting URL' for hdr in headers_found}

    resp_headers = {k.lower(): v for k, v in response.headers.items()} # Case-insensitive check

    if 'x-frame-options' in resp_headers:
        headers_found['x-frame-options'] = True # Value could be DENY, SAMEORIGIN
    if 'strict-transport-security' in resp_headers:
        headers_found['strict-transport-security'] = True
    if 'content-security-policy' in resp_headers:
        headers_found['content-security-policy'] = True
    if 'x-content-type-options' in resp_headers and 'nosniff' in resp_headers['x-content-type-options'].lower():
         headers_found['x-content-type-options'] = True # Specifically check for 'nosniff'
    if 'x-xss-protection' in resp_headers:
         headers_found['x-xss-protection'] = True # Often '1; mode=block'

    # Match keys to the requirements table names
    return {
        'Header of x-frame': headers_found['x-frame-options'],
        'Header of hsts': headers_found['strict-transport-security'],
        'Header of policy': headers_found['content-security-policy'],
        'Header of xxss': headers_found['x-xss-protection'], # Corresponds to X-XSS-Protection
        'Header of nonsnif': headers_found['x-content-type-options'] # Corresponds to X-Content-Type-Options: nosniff
    }