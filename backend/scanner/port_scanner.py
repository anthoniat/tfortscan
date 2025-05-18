import socket
from .utils import get_domain_from_url

def check_common_ports(url, ports_to_check=None, timeout=1):
    """Checks if common web ports are open on the target domain."""
    if ports_to_check is None:
         # ports_to_check = [80, 443, 8080, 21, 22, 23, 25, 53, 110] # Example common ports
         ports_to_check = [80, 443, 8080, 21, 22, 23, 25, 53, 110] # Start simple, based on example/common use
         # The example screenshot showed just port 80 for pinterest.com.
         # You could make this configurable or focus on the most relevant ones.

    domain = get_domain_from_url(url)
    if not domain:
        return {"open_ports": [], "error": "Invalid domain"}

    open_ports = []
    results = {}
    try:
        ip_address = socket.gethostbyname(domain) # Resolve domain to IP
        results['ip_address'] = ip_address # Good info to have
        for port in ports_to_check:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result_code = sock.connect_ex((ip_address, port)) # connect_ex returns 0 on success
            if result_code == 0:
                open_ports.append(port)
            sock.close()
        results['open_ports'] = open_ports
    except socket.gaierror:
        results['open_ports'] = []
        results['error'] = f"Could not resolve domain: {domain}"
    except socket.error as e:
        results['open_ports'] = []
        results['error'] = f"Socket error: {e}"


    return {"Scan Ports": open_ports} # Return list of open ports found