import subprocess

# Example: run sqlmap to identify databases
target_url = "http://example.com/vulnerable?id=1"

command = ["python", "../ExternalTools/sqlmap/sqlmap.py", "-u", target_url, "--dbs"]

try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("SQLMap Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print(f"Error running SQLMap: {e}")
    print(e.stderr)