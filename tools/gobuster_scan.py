import subprocess
from tools.utils import extract_status_urls
from config.config import wordList
from tools.sqlScanner import sqlScanner

def run_gobuster_scan(urls_for_go_buster):
    """
    Runs Gobuster on a list of URLs, extracts paths with status 200/301,
    and passes valid full URLs to sqlScanner().
    """
    successful_urls = []

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
            filtered_urls = extract_status_urls(p1.stdout, base_url=target_url)

            if filtered_urls:
                successful_urls.extend(filtered_urls)
                print(f"🔍 Found {len(filtered_urls)} accessible URLs.")
            else:
                print("⚠️  No matching 200/301 URLs found.")
        else:
            print("❌ Gobuster scan failed:")
            print(p1.stderr)

    if successful_urls:
        print("THESE ARE THE URLS TO SCAN", successful_urls)
        print("RUNNING SQL SCANNER")
        sqlScanner(successful_urls)