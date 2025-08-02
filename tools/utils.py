"""
utils.py contains all utilities used in main script.

Functions written here should be functions that serve a quick purpose such as checks or validation. 
"""

import re
from urllib.parse import urlparse, urlunparse


def extract_status_urls(gobuster_output: str, base_url: str) -> list[str]:
    """
    Extracts clean full URLs (without port) for 200 and 301 status responses from Gobuster output.
    """
    urls = []

    parsed_base = urlparse(base_url)


    base = urlunparse((parsed_base.scheme, parsed_base.hostname, "", "", "", ""))

    for line in gobuster_output.splitlines():
        if "(Status: 200)" not in line and "(Status: 301)" not in line:
            continue

        # If it's a redirect line
        redirect = re.search(r'\[--> (https?://[^\]]+)\]', line)
        if redirect:
            redirected_url = redirect.group(1)
            parsed_redirect = urlparse(redirected_url)
            clean_url = urlunparse((parsed_redirect.scheme, parsed_redirect.hostname, parsed_redirect.path, "", "", ""))
            urls.append(clean_url)
            continue

        # If it's a normal path match
        match = re.match(r'^(\S+)\s+\(Status:\s*(?:200|301)\)', line)
        if match:
            path = match.group(1)
            urls.append(f"{base}{path}")


    return urls