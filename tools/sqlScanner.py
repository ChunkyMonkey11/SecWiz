from tools.parmScanner import fetch_forms_inputs
import re
import subprocess
import os
from config.config import sqlMap, sqlMapOutPut

path = sqlMap
output_file = sqlMapOutPut

import re

def summarize_sqlmap_output(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    targets = re.split(r"\[\*\] starting @ .*?\n", content)[1:]  # كل تارجت لوحده

    for target in targets:
        url_match = re.search(r"URL:\s+GET\s+(.*?)\n", target)
        if not url_match:
            continue
        url = url_match.group(1).strip()
        print(f"\n🔗 URL: {url}")

        # استخراج الباراميترات القابلة للحقن
        vuln_blocks = re.findall(r"Parameter: (.*?) \(POST\)\n(.*?)---", target, re.DOTALL)
        if not vuln_blocks:
            print("  ⚠️ No injectable parameters found.")
            continue

        for param, details in vuln_blocks:
            print(f"  🧪 Parameter: {param.strip()}")
            types = re.findall(r"Type: (.*?)\n\s+Title: (.*?)\n", details)
            payloads = re.findall(r"Payload: (.*?)\n", details)
            for i, ((vtype, title), payload) in enumerate(zip(types, payloads), start=1):
                print(f"    {i}. Type: {vtype.strip()}")
                print(f"       Title: {title.strip()}")
                print(f"       Payload: {payload.strip()}")



def sqlScanner(urls):

    forms_data = fetch_forms_inputs(urls)
    print("Starting Sql Scanner..")
    for form in forms_data:
        data_payload = "&".join(f"{param}=1" for param in form['params'])
        if form['method'] == 'get':
            target_url = f"{form['url']}?{data_payload}"
            print(f"sqlmap -u '{target_url}'")
            sqlmap_command = [
                "python", path,
                "-u", target_url,
                "--batch"
            ]
        else:
            print(f"sqlmap -u '{form['url']}' --data='{data_payload}'")
            sqlmap_command = [
                "python", path,
                "-u", form['url'],
                "--data", data_payload,
                "--batch"
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

        except Exception as e:
            print(f"[!] Error running sqlmap: {e}")
    summarize_sqlmap_output(output_file)

