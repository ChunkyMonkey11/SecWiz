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