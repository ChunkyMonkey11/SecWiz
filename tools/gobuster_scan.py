import sys
import os
# This affects the from statements below. Need to figure out what its doing. 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import subprocess
from tools.utils import extract_status_urls
from config.config import wordList
from tools.sqlScanner import sqlScanner

def run_gobuster_scan(urls_for_go_buster, isGUI):
    """
    Runs Gobuster on a list of URLs, extracts paths with status 200/301,
    and passes valid full URLs to sqlScanner().
    """
    accessible_urls = []
    all_urls = []
    protected_urls = []
    for target_url in urls_for_go_buster:
        print(f"\n🚀 Running Gobuster for: {target_url}") 
        p1 = subprocess.run(
            ["gobuster", "dir", "-u", target_url, "-w", wordList],
            shell=False,
            capture_output=True,
            text=True
        )

        print(p1.check_returncode)
        if p1.returncode == 0:
            print("✅ Gobuster scan successful.")
            filtered_urls = extract_status_urls(p1.stdout, base_url=target_url) #Filters for succesful URLS THAT CAN BE ACCESSED
            accessible_urls.extend(filtered_urls)
            
            if filtered_urls:
                if isGUI:
                    # print(isGUI) 
                    print(f"🔍 Found {len(filtered_urls)} accessible URLs.")
                    return{
                        'all_urls'       : all_urls, 
                        'accessible_urls': accessible_urls,
                        'protected_urls' : protected_urls
                    }
                else:
                    print(f"🔍 Found {len(filtered_urls)} accessible URLs.")
                    sqlScanner(filtered_urls)
            else:
                print("❌ Gobuster scan failed:")
                

# run_gobuster_scan(['http://testphp.vulnweb.com'],True) # Debug Statement