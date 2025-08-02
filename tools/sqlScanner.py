from tools.parmScanner import fetch_forms_inputs
import re
import subprocess
import os
from config.config import sqlMap, sqlMapOutPut



urls = ['http://testphp.vulnweb.com/login.php']
path = sqlMap
output_file = sqlMapOutPut

def summarize_sqlmap_output(output):
    results = []

    # Split on each occurrence of injection results block
    injection_blocks = output.split("sqlmap identified the following injection point(s)")
    for block in injection_blocks[1:]:  # skip first non-matching part
        summary = {}

        # URL and method
        url_match = re.search(r"URL:\n(GET|POST) ([^\n]+)", block)
        if url_match:
            summary["Method"] = url_match.group(1)
            summary["URL"] = url_match.group(2)

        # Vulnerable parameter
        param_match = re.search(r"Parameter: (\w+) \((POST|GET)\)", block)
        if param_match:
            summary["Parameter"] = param_match.group(1)

        # DBMS
        dbms_match = re.search(r"back-end DBMS: (.+)", block)
        if dbms_match:
            summary["DBMS"] = dbms_match.group(1).strip()

        # Tech
        tech_match = re.search(r"web application technology: (.+)", block)
        if tech_match:
            summary["Tech"] = tech_match.group(1).strip()

        # OS
        os_match = re.search(r"web server operating system: (.+)", block)
        if os_match:
            summary["OS"] = os_match.group(1).strip()

        # Injections
        injections = []
        pattern = re.compile(r"Type: (.*?)\n\s+Title: (.*?)\n\s+Payload: (.*?)\n", re.DOTALL)
        for match in pattern.finditer(block):
            injections.append({
                "Type": match.group(1).strip(),
                "Title": match.group(2).strip(),
                "Payload": match.group(3).strip()
            })
        summary["Injections"] = injections

        results.append(summary)

    # Print all summaries
    for i, result in enumerate(results, 1):
        print(f"\n Target {i} Summary:")
        print(f"• URL: {result.get('URL')}")
        print(f"• Method: {result.get('Method')}")
        print(f"• OS: {result.get('OS')}")
        print(f"• Tech: {result.get('Tech')}")
        print(f"• DBMS: {result.get('DBMS')}")
        print(f"• Vulnerable Parameter: {result.get('Parameter')}")
        print(f"• Total Injections: {len(result['Injections'])}\n")

        for inj in result["Injections"]:
            print(f"\033[96m  • {inj['Type']} - {inj['Title']}\033[0m")
            print(f"\033[92m    Payload: {inj['Payload']}\033[0m\n")


def sqlScanner(urls):
    for url in urls:
        forms_data = fetch_forms_inputs(url)
        print("Starting Sql Scanner..")
        for form in forms_data:
            data_payload = "&".join(f"{param}=1" for param in form['params'])
            if form['method'] == 'get':
                target_url = f"{form['url']}?{data_payload}"
                print(f"sqlmap -u '{target_url}'")
                sqlmap_command = [
                    "python", path,
                    "-u", target_url
                ]
            else:
                print(f"sqlmap -u '{form['url']}' --data='{data_payload}'")
                sqlmap_command = [
                    "python", path,
                    "-u", form['url'],
                    "--data", data_payload
                ]
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    process = subprocess.Popen(
                        sqlmap_command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True
                    )
                    for line in process.stdout:
                        print(line, end="")  # Show in terminal
                        f.write(line)  # Save to file
                    process.wait()
                    with open(output_file, "r", encoding="utf-8") as f:
                        output = f.read()
                    summarize_sqlmap_output(output)
            except Exception as e:
                print(f"[!] Error running sqlmap: {e}")
