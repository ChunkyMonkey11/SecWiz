from tools.portScanner import scan_ports
from tools.utils import is_valid_ipv4,is_valid_hostname
from tools.gobuster_scan import run_gobuster_scan

addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()


# testphp.vulnweb.com

if is_valid_ipv4(addr_to_scan):
    scan_ports(addr_to_scan)