import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.gobuster_scan import run_gobuster_scan


url_to_test = ["http://testphp.vulnweb.com:80"]
run_gobuster_scan(url_to_test)

