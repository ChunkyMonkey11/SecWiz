"""gobuster_scan.py contains code that performs the Web Directory/File Enumeration on the passed-in HTTP URL."""


import subprocess
from tools.utils import extract_status_urls
from config.config import wordList
from tools.sqlScanner import sqlScanner


def run_gobuster_scan(urls_for_go_buster):
    """
    Takes a list of URLs and runs a Gobuster scan on each.
    Extracts all results with status code 200 or 301 and writes only valid URLs to a file.
    """
    succesful_urls = []
    for target_url in urls_for_go_buster:
        print(f"\n🚀 Running Gobuster for: {target_url}")
        
        p1 = subprocess.run(
            ["gobuster", "dir", "-u", target_url, "-w", wordList],
            shell=False,
            capture_output=True,
            text=True
        )
        if p1.returncode == 0:
            print("✅ Gobuster scan successful.")

            # Extract 200/301 URLs using helper function extract_status_urls 
            filtered_urls = extract_status_urls(p1.stdout, base_url=target_url)
            
            if filtered_urls:
                succesful_urls.extend(filtered_urls)
                print(f"🔍 Found {len(filtered_urls)} accessible URLs.")
            else:
                print("⚠️  No matching 200/301 URLs found.")

        else:
            print("❌ Gobuster scan failed:")
            print(p1.stderr)

    # Write all extracted URLs to file
    if succesful_urls:
        print(f"THESE ARE THE URLS TO SCAN {succesful_urls}")

        print("RUNNING SQL SCANNER")
        sqlScanner(succesful_urls)