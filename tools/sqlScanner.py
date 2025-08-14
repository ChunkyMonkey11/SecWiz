from tools.parmScanner import fetch_forms_inputs
import re
import subprocess
import os
import time
from datetime import datetime
from config.config import sqlMap, sqlMapOutPut

urls = ['http://testphp.vulnweb.com/login.php']
path = sqlMap
output_file = sqlMapOutPut

def summarize_sqlmap_output(output):
    """Parse sqlmap output to extract vulnerability information"""
    results = []
    injection_blocks = output.split("sqlmap identified the following injection point(s)")
    for block in injection_blocks[1:]:
        summary = {}
        url_match = re.search(r"URL:\n(GET|POST) ([^\n]+)", block)
        if url_match:
            summary["Method"] = url_match.group(1)
            summary["URL"] = url_match.group(2)
        param_match = re.search(r"Parameter: (\w+) \((POST|GET)\)", block)
        if param_match:
            summary["Parameter"] = param_match.group(1)
        dbms_match = re.search(r"back-end DBMS: (.+)", block)
        if dbms_match:
            summary["DBMS"] = dbms_match.group(1).strip()
        tech_match = re.search(r"web application technology: (.+)", block)
        if tech_match:
            summary["Tech"] = tech_match.group(1).strip()
        os_match = re.search(r"web server operating system: (.+)", block)
        if os_match:
            summary["OS"] = os_match.group(1).strip()
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
    return results

def run_sqlmap_automated(sqlmap_command, output_file, timeout=300):
    """
    Run sqlmap in automated mode without requiring manual input
    
    Args:
        sqlmap_command: List of command arguments for sqlmap
        output_file: Path to output file
        timeout: Maximum execution time in seconds
    
    Returns:
        tuple: (success: bool, output: str, error: str)
    """
    try:
        # Add automation flags to prevent manual input
        automated_command = sqlmap_command + [
            "--batch",           # Never ask for user input, use default behavior
            "--non-interactive", # Non-interactive mode
            "--random-agent",    # Use random user agent
            "--time-sec=3",      # Reduce time-based injection delay
            "--threads=1",       # Single thread for stability
            "--skip-waf",        # Skip WAF detection to speed up
            "--skip-heuristics", # Skip heuristic detection
            "--level=1",         # Basic level testing
            "--risk=1",          # Low risk level
            "--technique=BEUSTQ" # All SQL injection techniques
        ]
        
        print(f"🔍 Running automated sqlmap: {' '.join(automated_command)}")
        
        # Clear previous output
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("")
        
        # Run sqlmap with timeout
        start_time = time.time()
        process = subprocess.Popen(
            automated_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        output_lines = []
        while True:
            # Check timeout
            if time.time() - start_time > timeout:
                process.terminate()
                return False, "", f"Timeout after {timeout} seconds"
            
            # Read output line by line
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line:
                output_lines.append(line)
                print(line.rstrip())  # Print to console without extra newline
                
                # Write to file in real-time
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(line)
        
        # Wait for process to complete
        return_code = process.wait()
        output = ''.join(output_lines)
        
        if return_code == 0:
            return True, output, ""
        else:
            return False, output, f"sqlmap exited with code {return_code}"
            
    except subprocess.TimeoutExpired:
        process.terminate()
        return False, "", f"Process timeout after {timeout} seconds"
    except Exception as e:
        return False, "", f"Error running sqlmap: {str(e)}"

def sqlScanner(urls, isGUI):
    """
    Enhanced SQL injection scanner with full automation
    
    Args:
        urls: List of target URLs to scan
        isGUI: Boolean indicating if running in GUI mode
    
    Returns:
        List of vulnerability results for GUI mode
    """
    vulnerabilities = []
    scan_logs = []
    
    print("🚀 Starting Enhanced SQL Injection Scanner...")
    scan_logs.append(f"SQL Injection scan started at {datetime.now().isoformat()}")
    
    for url_index, url in enumerate(urls, 1):
        print(f"\n📋 Scanning URL {url_index}/{len(urls)}: {url}")
        scan_logs.append(f"Scanning URL: {url}")
        
        try:
            # Fetch forms and inputs from the target URL
            forms_data = fetch_forms_inputs(url)
            print(f"🔍 Found {len(forms_data)} forms to test")
            scan_logs.append(f"Found {len(forms_data)} forms to test")
            
            for form_index, form in enumerate(forms_data, 1):
                print(f"\n🔍 Testing form {form_index}/{len(forms_data)}")
                scan_logs.append(f"Testing form {form_index}: {form.get('url', 'Unknown URL')}")
                
                # Create test payload
                data_payload = "&".join(f"{param}=1" for param in form['params'])
                
                # Build sqlmap command based on form method
                if form['method'].lower() == 'get':
                    target_url = f"{form['url']}?{data_payload}"
                    sqlmap_command = [
                        "python", path,
                        "-u", target_url,
                        "--output-dir", os.path.dirname(output_file)
                    ]
                else:
                    sqlmap_command = [
                        "python", path,
                        "-u", form['url'],
                        "--data", data_payload,
                        "--output-dir", os.path.dirname(output_file)
                    ]
                
                # Run sqlmap in automated mode
                success, output, error = run_sqlmap_automated(sqlmap_command, output_file)
                
                if success:
                    # Parse results
                    parsed_results = summarize_sqlmap_output(output)
                    
                    if parsed_results:
                        print(f"✅ Found {len(parsed_results)} SQL injection vulnerabilities!")
                        scan_logs.append(f"Found {len(parsed_results)} SQL injection vulnerabilities in form {form_index}")
                        
                        for result in parsed_results:
                            result['source_url'] = url
                            result['form_index'] = form_index
                            vulnerabilities.append(result)
                    else:
                        print("✅ No SQL injection vulnerabilities found in this form")
                        scan_logs.append(f"No SQL injection vulnerabilities found in form {form_index}")
                else:
                    print(f"❌ Error during sqlmap execution: {error}")
                    scan_logs.append(f"Error in form {form_index}: {error}")
                    
        except Exception as e:
            error_msg = f"Error scanning URL {url}: {str(e)}"
            print(f"❌ {error_msg}")
            scan_logs.append(error_msg)
    
    # Final summary
    total_vulns = len(vulnerabilities)
    print(f"\n🏁 SQL Injection Scan Complete!")
    print(f"📊 Results: {total_vulns} vulnerabilities found across {len(urls)} URLs")
    scan_logs.append(f"Scan completed: {total_vulns} vulnerabilities found")
    
    if isGUI:
        # Return structured data for GUI
        return {
            'vulnerabilities': vulnerabilities,
            'scan_logs': scan_logs,
            'summary': {
                'total_urls': len(urls),
                'total_vulnerabilities': total_vulns,
                'scan_timestamp': datetime.now().isoformat()
            }
        }
    else:
        # Print detailed results for CLI
        if vulnerabilities:
            print(f"\n{'='*60}")
            print("🔍 DETAILED VULNERABILITY REPORT")
            print(f"{'='*60}")
            
            for i, vuln in enumerate(vulnerabilities, 1):
                print(f"\n🎯 Vulnerability {i}:")
                print(f"   URL: {vuln.get('URL', 'Unknown')}")
                print(f"   Method: {vuln.get('Method', 'Unknown')}")
                print(f"   Parameter: {vuln.get('Parameter', 'Unknown')}")
                print(f"   DBMS: {vuln.get('DBMS', 'Unknown')}")
                print(f"   Technology: {vuln.get('Tech', 'Unknown')}")
                print(f"   OS: {vuln.get('OS', 'Unknown')}")
                print(f"   Injection Types: {len(vuln.get('Injections', []))}")
                
                for inj in vuln.get('Injections', []):
                    print(f"     • {inj['Type']} - {inj['Title']}")
                    print(f"       Payload: {inj['Payload']}")
        
        return vulnerabilities

# Legacy function for backward compatibility
def sqlScanner_legacy(urls, isGUI):
    """Legacy sqlScanner function for backward compatibility"""
    return sqlScanner(urls, isGUI)


