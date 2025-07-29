"""gobuster_scan.py contains code that performs the Web Directory/File Enummeration on the passed in http url"""
import subprocess

# So we will be using subprocess module to run our Gobuster commands within the terminal and collect its output.

# Let us now expierment with subprocess by having it list out all files in directory.

"""
shell=True vs shell=False

shell=True : The shell interprets the string as the whole string will be passed to the shell interpreter

shell=False : Expects a list, not a single string. Python tries to execute a literal program rather then a list of ["command", "arg1", "arg2"]
"""


def run_gobuster_scan(urls_for_go_buster):
    """ This method willt take in a list of urls and run a gobuster scan on each one 
        # It should later to a file write all the results with status code 200 or 301
    """
    for url in urls_for_go_buster:
        print(f"Running Gobuster for: {url}")
        
        p1 = subprocess.run(
            ["gobuster", "dir", "-u", url, "-w", "wordlist.txt"],
            shell=False,
            capture_output=True,
            text=True
        )

        if p1.returncode == 0:
            print("✅ Gobuster scan successful.")
            print(p1.stdout)
        else:
            print("❌ Gobuster scan failed:")
            print(p1.stderr)

urls_for_go_buster = ["http://scanme.org:80"]

