from tools.portScanner import scan_ports

addr_to_scan = input("Please enter a hostname or an IP to scan: ").strip()

# testphp.vulnweb.com

scan_ports(addr_to_scan)