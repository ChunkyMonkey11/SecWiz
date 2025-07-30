"""gobuster_scan.py contains code that performs the Web Directory/File Enumeration on the passed-in HTTP URL."""

import subprocess
from tools.utils import extract_status_urls

def run_gobuster_scan(urls_for_go_buster):
    """
    Takes a list of URLs and runs a Gobuster scan on each.
    Extracts all results with status code 200 or 301 and writes only valid URLs to a file.
    """
    all_matching_urls = []
    #
    for target_url in urls_for_go_buster:
        print(f"\n🚀 Running Gobuster for: {target_url}")
        
        p1 = subprocess.run(
            ["gobuster", "dir", "-u", target_url, "-w", "wordlist.txt"],
            shell=False,
            capture_output=True,
            text=True
        )

        print(p1.stdout)

        if p1.returncode == 0:
            print("✅ Gobuster scan successful.")

            # Extract 200/301 URLs using helper function extract_status_urls 
            filtered_urls = extract_status_urls(p1.stdout, base_url=target_url)

            if filtered_urls:
                all_matching_urls.extend(filtered_urls)
                print(f"🔍 Found {len(filtered_urls)} accessible URLs.")
            else:
                print("⚠️  No matching 200/301 URLs found.")

        else:
            print("❌ Gobuster scan failed:")
            print(p1.stderr)

    # Write all extracted URLs to file
    if all_matching_urls:
        with open("url.txt", "w") as f:
            for result_url in all_matching_urls:
                f.write(result_url + "\n")
        print(f"\n📄 Saved all {len(all_matching_urls)} filtered results to filtered_gobuster_results.txt")
    else:
        print("\n🚫 No valid URLs found in any scan.")

