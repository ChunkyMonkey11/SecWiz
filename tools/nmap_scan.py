import nmap3
import re
import json


""" Takes the address and performs a scan for open ports on it then constructing Gobuster-compatible URLs """

def perform_scan(address):
    PORTS_TO_SCAN = [80, 443, 8080, 8443, 8000, 8888, 5000]
    port_list = ",".join(str(p) for p in PORTS_TO_SCAN)
    
    scanner = nmap3.Nmap()

    
    urls_for_gobuster = []

    # Perform version detection scan on selected ports
    print(f"Scanning {address} for web ports: {port_list}")
    result = scanner.nmap_version_detection(f"{address} -p {port_list}")

    # Extract host key from result (usually IP) # The use of next method comes from it grabing the first match that passes a filter
    host_key = next(k for k in result if k not in ["runtime", "stats", "task_results"])

    # Loop through ports and construct Gobuster-compatible URLs
    for port in result[host_key]["ports"]:
        if port["state"] == "open":
            port_num = port["portid"]
            service = port.get("service", {})
            service_name = service.get("name", "").lower()
            if service_name in ["http", "http-alt", "https", "https-alt"]:
                scheme = "https" if "https" in service_name else "http"
                urls_for_gobuster.append(f"{scheme}://{address}:{port_num}")

    # Save scan results
    with open("nmap_webport_scan.json", "w") as f:
        json.dump(result, f, indent=4)

    # Output Gobuster targets
    print("\nURLs ready for Gobuster:")
    for url in urls_for_gobuster:
        print(f"  • {url}")

    return urls_for_gobuster