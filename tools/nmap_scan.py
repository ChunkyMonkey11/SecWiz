import nmap3
import re
import json

# Function that validates if an Ip address is correct standard
def is_valid_ipv4(address):
    # Simple regex for IPv4 validation
    pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    if re.match(pattern, address):
        # Check each octet is between 0 and 255
        return all(0 <= int(part) <= 255 for part in address.split('.'))
    return False

# Intialize Scanner Object
scanner = nmap3.Nmap()

# Get address to scan
addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()

if is_valid_ipv4(addr_to_scan):
    """
    If the ip address is valid lets find open web ports running on this ip
    TO BE IMPLEMENTED

    NOTE TO SELF we need to construct the Ip into a valid passable URL for the next function 
    """
    pass
else:
    print(f"{addr_to_scan} is a hostname.")
    """
    if a hostname is provided we can pass this onto DIRB or Gobuster 
    TO BE IMPLEMENTED
    Question: How should this be passed onto DIRB or Gobuster is just knowing that this is a valid websever enough

    ANSWER: Construct a valid URL for the next function using the hostname
    """

result = scanner.scan_top_ports(addr_to_scan)

with open("nmap_scan_result.json", "w") as f:
    json.dump(result, f, indent=4)