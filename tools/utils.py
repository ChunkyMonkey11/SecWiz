"""
utils.py contains all utilities used in main script.

Functions written here should be functions that serve a quick purpose such as checks or validation. 
"""

import re
from urllib.parse import urlparse, urlunparse


def extract_status_urls(gobuster_output: str, base_url: str) -> list[str]:
    """
    Extracts URLs from Gobuster output with status 200 or 301.
    Strips any port number from base_url or redirect URLs.
    """
    urls: list[str] = []

    # parse base_url and rebuild without port
    pb = urlparse(base_url)
    base = urlunparse((pb.scheme, pb.hostname or pb.netloc, "", "", "", ""))

    for line in gobuster_output.splitlines():
        if "(Status: 200)" not in line and "(Status: 301)" not in line:
            continue

        # handle redirects
        redirect_match = re.search(r'\[--> (https?://[^\]]+)\]', line)
        if redirect_match:
            raw = redirect_match.group(1)
            pr = urlparse(raw)
            clean = urlunparse((pr.scheme, pr.hostname or pr.netloc, pr.path, "", "", ""))
            urls.append(clean)

            continue

        # handle normal hits
        path_match = re.match(r'^(\S+)\s+\(Status:\s*(?:200|301)\)', line)
        if path_match:
            path = path_match.group(1)
            urls.append(f"{base}{path}")


    return urls