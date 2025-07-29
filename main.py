from tools.nmap_scan import perform_scan
from tools.utils import is_valid_ipv4,is_valid_hostname

addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()

if is_valid_ipv4(addr_to_scan):
    perform_scan(addr_to_scan)
    
elif is_valid_hostname(addr_to_scan):
    perform_scan(addr_to_scan)

# Now write gobuster file