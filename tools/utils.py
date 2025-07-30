"""
utils.py contains all utilities used in main script.

Functions written here should be functions that serve a quick purpose such as checks or validation. 
"""

import re


# Function to validate ip address
def is_valid_ipv4(address):
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, address):
        return all(0 <= int(part) <= 255 for part in address.split('.'))
    return False

# Function to validate hostname
def is_valid_hostname(hostname):
    if len(hostname) > 253:
        return False

    if hostname[-1] == ".":
        hostname = hostname[:-1]  # Strip trailing dot (FQDN case)

    labels = hostname.split(".")
    valid = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)$")
    
    return all(valid.match(label) for label in labels)

def extract_status_urls(gobuster_output: str, base_url: str) -> list[str]:
    """
    Extracts URLs from Gobuster output with status 200 or 301.
    If a redirect is found, it returns the full redirect URL.
    Otherwise, it builds the full path using the base_url.
    """
    urls = []
    for line in gobuster_output.splitlines():
        if "Status: 301" in line or "Status: 200" in line:
            match = re.search(r'\[--> (https?://[^\]]+)\]', line)
            if match:
             urls.append(match.group(1))  # redirected URL like https://...
            else:
                path_match = re.match(r'^(/\S+)', line)
                if path_match:
                    urls.append(base_url.rstrip("/") + path_match.group(1))
            return urls