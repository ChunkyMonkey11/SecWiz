import socket
from config.config import PORTS
import ipaddress
import requests
from tools.gobuster_scan import run_gobuster_scan


def is_ip_address(input_string):
    try:
        ipaddress.ip_address(input_string)
        return True
    except ValueError:
        return False

def check_protocol(url_without_scheme):
    try:
        https_url = f"https://{url_without_scheme}"
        response = requests.head(https_url, allow_redirects=True, timeout=5)
        if response.status_code < 400: # Check for successful status codes
            return True
    except requests.exceptions.RequestException:
        pass
    try:
        http_url = f"http://{url_without_scheme}"
        response = requests.head(http_url, allow_redirects=True, timeout=5)
        if response.status_code < 400:
            return True
    except requests.exceptions.RequestException:
        pass

    return None


def scan_ports(target):
    if is_ip_address(target):
        print("Please Enter a valid Domain (example.com).")
        return
    print(f"Scanning ports http/s service on: {target}")
    target_url = []
    open_ports = []
    secured = None
    if target.__contains__('https://'):
        secured = True
        target = target.replace('https://', '')
    elif target.__contains__('http://'):
        secured = False
        target = target.replace('http://', '')
    if check_protocol(target):
        for port in PORTS:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} is open")
                open_ports.append(port)
            sock.close()
    if len(open_ports) >= 1:
        if secured:
            target_url.append(f"https://{target}")
            run_gobuster_scan(target_url)
        else:
            target_url.append(f"http://{target}")
            run_gobuster_scan(target_url)
    else:
        print("No ports open, please try another domain.")

# Test comment