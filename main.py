from tools.nmap_scan import perform_scan
from tools.utils import is_valid_ipv4,is_valid_hostname
from tools.gobuster_scan import run_gobuster_scan

addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()


# testphp.vulnweb.com

if is_valid_ipv4(addr_to_scan):

    # Collect the URLS To scan with Gobuster
    urls_for_gobuster = perform_scan(addr_to_scan)

    # Run Gobuster Scan on the URLS collected
    run_gobuster_scan(urls_for_gobuster)
    
elif is_valid_hostname(addr_to_scan):

    # Collect the URLS To scan with Gobuster
    urls_for_gobuster = perform_scan(addr_to_scan)

    # Run Gobuster Scan on the URLS collected 
    run_gobuster_scan(urls_for_gobuster)

