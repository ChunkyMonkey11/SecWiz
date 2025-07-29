from tools.nmap_scan import perform_scan
from tools.utils import is_valid_ipv4,is_valid_hostname

addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()

if is_valid_ipv4(addr_to_scan):
    urls_for_gobuster = perform_scan(addr_to_scan)
    
    # Pass the Urls to the run_gobuster_scan method 
    
elif is_valid_hostname(addr_to_scan):
    urls_for_gobuster = perform_scan(addr_to_scan)
    # Pass the Urls to the run_gobuster_scan method 

