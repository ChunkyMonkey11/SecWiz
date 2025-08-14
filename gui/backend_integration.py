"""
SecWiz GUI Backend Integration Module

This module provides a bridge between the GUI and the existing scanner tools.
It handles progress updates, result formatting, and error handling.
"""

import threading
import time
import socket
import subprocess
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime

# Import existing tools
from tools.portScanner import is_ip_address, check_protocol, scan_ports
from tools.gobuster_scan import run_gobuster_scan
from tools.sqlScanner import sqlScanner, summarize_sqlmap_output
from tools.parmScanner import fetch_forms_inputs
from tools.utils import extract_status_urls
from config.config import ports, wordList, sqlMap, sqlMapOutPut

class SecWizBackendIntegration:
    """Backend integration class for SecWiz GUI"""
    
    def __init__(self, progress_callback: Callable = None, result_callback: Callable = None):
        self.progress_callback = progress_callback
        self.result_callback = result_callback
        self.scan_results = {}
        self.is_scanning = False
        
    def update_progress(self, message: str, step: int = None, total_steps: int = None):
        """Update progress in GUI"""
        if self.progress_callback:
            self.progress_callback(message, step, total_steps)
            
    def update_results(self, scan_type: str, results: Dict[str, Any]):
        """Update results in GUI"""
        if self.result_callback:
            self.result_callback(scan_type, results)
            
    def run_full_scan(self, target: str) -> Dict[str, Any]:
        """Run complete vulnerability assessment"""
        self.is_scanning = True
        
        results = {
            'type': 'full',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'overview': {},
            'ports': {},
            'directories': {},
            'vulnerabilities': {},
            'logs': []
        }
        
        try:
            # STEP 1: Enhanced Port Scanning
            self.update_progress("🔍 Step 1/4: Enhanced Port Scanning...", 1, 4)
            port_results = scan_ports(target, True)
            results['ports'] = port_results
            results['logs'].append(f"Enhanced port scan completed: {len(port_results.get('open_ports', []))} ports analyzed")
            
            # Add risk assessment to logs
            risk_summary = port_results.get('risk_summary', {})
            if risk_summary:
                results['logs'].append(f"Risk assessment: {risk_summary.get('critical', 0)} critical, {risk_summary.get('high', 0)} high, {risk_summary.get('medium', 0)} medium, {risk_summary.get('low', 0)} low")

            """========================================================"""


            # STEP 2: Directory Enumeration WORKS WITH TOOLS FOLDER
            target_urls = port_results.get('target_urls')
            print(f"DEBUG TARGET_URLS : {target_urls}") #Debug statement
            dir_results = run_gobuster_scan(target_urls, isGUI=True) # How can this call urls and work. 
            results['directories'] = dir_results
            results['logs'].append(f"Empty Log after Directory Enumeration ")
            """ Uses run_gobuster_scan  WORKING"""
            print(f" DEBUG THIS IS WHAT GETS PASSED INTO SQLSCAN,\n {results['directories']['accessible_urls']}")

            "============================================================="
            


            # Step 3: Form Detection
            self.update_progress("📝 Step 3/4: Form Detection...", 3, 4)
            accessible_urls = results['directories'].get('accessible_urls', [])
            forms_found = []
            
            for url in accessible_urls:
                try:
                    forms = fetch_forms_inputs(url)
                    for form in forms:
                        form['source_url'] = url
                        forms_found.append(form)
                except Exception as e:
                    results['logs'].append(f"Error detecting forms on {url}: {str(e)}")
            
            results['vulnerabilities']['forms'] = forms_found
            results['logs'].append(f"Form detection completed: {len(forms_found)} forms found across {len(accessible_urls)} URLs")

            # Step 4: SQL Injection Testing
            self.update_progress("🗄️ Step 4/4: SQL Injection Testing...", 4, 4)
            accessible_urls_to_sql_scan = results['directories'].get('accessible_urls')
            if accessible_urls_to_sql_scan:
                print(f"🔍 Starting SQL injection scan on {len(accessible_urls_to_sql_scan)} URLs")
                sql_scan_results = sqlScanner(accessible_urls_to_sql_scan, True)
                
                # Handle new enhanced return structure
                if isinstance(sql_scan_results, dict):
                    # New enhanced structure
                    results['vulnerabilities']['sql_injection'] = sql_scan_results.get('vulnerabilities', [])
                    results['logs'].extend(sql_scan_results.get('scan_logs', []))
                    
                    # Add summary to logs
                    summary = sql_scan_results.get('summary', {})
                    if summary:
                        results['logs'].append(f"SQL injection scan completed: {summary.get('total_vulnerabilities', 0)} vulnerabilities found across {summary.get('total_urls', 0)} URLs")
                else:
                    # Legacy structure (list of vulnerabilities)
                    results['vulnerabilities']['sql_injection'] = sql_scan_results
                    results['logs'].append(f"SQL injection scan completed: {len(sql_scan_results)} vulnerabilities found")
            else:
                results['logs'].append("No accessible URLs found for SQL injection testing")
            # Create overview
            print(f"Will now be adding to results[overview] CURRENT results[overview] = = = = {results['overview']}")
            results['overview'] = self._create_overview(results) 
            
            self.update_progress("✅ Full scan completed successfully!", 4, 4)
            
        except Exception as e:
            results['logs'].append(f"Error during scan: {str(e)}")
            self.update_progress(f"❌ Error: {str(e)}")
            
        finally:
            self.is_scanning = False
            
            print(f"RESULTS IS {results}") 
        return results






























    def run_port_scan(self, target: str) -> Dict[str, Any]:
        """Run enhanced port scan only"""
        self.is_scanning = True
        results = {
            'type': 'port',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'all_ports': {},
            'open_ports_services': {},
            'logs': []
        }
        
        try:
            self.update_progress("🔍 Enhanced port scanning in progress...")
            port_results = scan_ports(target, True)
            print(port_results)
            
            # Enhanced port scan results
            results['all_ports'] = {
                'scanned_ports': ports,
                'open_ports': port_results.get('open_ports', []),
                'closed_ports': [p for p in ports if p not in port_results.get('open_ports', [])]
            }
            
            results['open_ports_services'] = {
                'open_ports': port_results.get('open_ports', []),
                'services': port_results.get('services', {}),
                'target_urls': port_results.get('target_urls', []),
                'risk_summary': port_results.get('risk_summary', {}),
                'scan_logs': port_results.get('scan_logs', [])
            }
            
            # Add enhanced logs
            risk_summary = port_results.get('risk_summary', {})
            if risk_summary:
                results['logs'].append(f"Enhanced port scan completed: {len(port_results.get('open_ports', []))} open ports found")
                results['logs'].append(f"Risk assessment: {risk_summary.get('critical', 0)} critical, {risk_summary.get('high', 0)} high, {risk_summary.get('medium', 0)} medium, {risk_summary.get('low', 0)} low")
            else:
                results['logs'].append(f"Port scan completed: {len(port_results.get('open_ports', []))} open ports found")
            
            self.update_progress("✅ Enhanced port scan completed successfully!")
            
        except Exception as e:
            results['logs'].append(f"Error during port scan: {str(e)}")
            self.update_progress(f"❌ Error: {str(e)}")
            
        finally:
            self.is_scanning = False
            
        return results
        
    def run_directory_scan(self, target: str) -> Dict[str, Any]:
        """Run directory scan only"""
        self.is_scanning = True
        results = {
            'type': 'directory',
            'target': target,
            'timestamp': datetime.now().isoformat(),
            'all_files': {},
            'accessible_files': {},
            'protected_files': {},
            'logs': []
        }
        
        try:
            self.update_progress("📁 Directory scanning in progress...")
            
            # First get target URLs from port scan
            port_results = self._run_port_scan(target,)
            dir_results = self._run_directory_scan(port_results.get('target_urls', []))
            
            results['all_files'] = dir_results.get('all_urls', [])
            results['accessible_files'] = dir_results.get('accessible_urls', [])
            results['protected_files'] = dir_results.get('protected_urls', [])
            
            results['logs'].append(f"Directory scan completed: {len(dir_results.get('accessible_urls', []))} accessible URLs found")
            self.update_progress("✅ Directory scan completed successfully!")
            
        except Exception as e:
            results['logs'].append(f"Error during directory scan: {str(e)}")
            self.update_progress(f"❌ Error: {str(e)}")
            
        finally:
            self.is_scanning = False
            
        return results
        
    # Reached nepo 
    def _run_directory_scan(self, target_urls: List[str]) -> Dict[str, Any]:
        """Internal directory scanning logic"""
        accessible_urls = []
        all_urls = []
        
        for target_url in target_urls:
            print(f"\n🚀 Running Gobuster for: {target_url}")

            try:
                p1 = subprocess.run(
                    ["gobuster", "dir", "-u", target_url, "-w", wordList],
                    shell=False,
                    capture_output=True,
                    text=True
                )
                
                if p1.returncode == 0:
                    filtered_urls = extract_status_urls(p1.stdout, base_url=target_url)
                    accessible_urls.extend(filtered_urls)
                    all_urls.extend(filtered_urls)
                    print(f"Found {len(filtered_urls)} accessible URLs")
                else:
                    print(f"Gobuster failed: {p1.stderr}")
            except Exception as e:
                print(f"Error running gobuster: {e}")
                
        return {
            'all_urls': all_urls,
            'accessible_urls': accessible_urls,
            'protected_urls': []
        }
        
    def _run_form_scan(self, target: str) -> List[Dict[str, Any]]:
        """Internal form scanning logic"""
        try:
            return fetch_forms_inputs(target)
        except Exception as e:
            print(f"Error in form scan: {e}")
            return []



    def _run_sql_scan(self, accessible_urls: List[str]) -> Dict[str, Any]:
        """Internal SQL injection scanning logic"""
        vulnerabilities = []
        
        try:
            # Run sqlScanner (this will print to console)
            # You might want to modify sqlScanner to return results
            sqlScanner(accessible_urls)
            
            # For now, return empty results
            # TODO: Modify sqlScanner to return structured data
            return {
                'vulnerabilities': vulnerabilities,
                'scanned_urls': accessible_urls
            }
        except Exception as e:
            print(f"Error in SQL scan: {e}")
            return {
                'vulnerabilities': [],
                'scanned_urls': accessible_urls
            }
        
















    def _create_overview(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create overview summary"""
        print("_create_overview() has been called")
        # Handle sql_injection data structure safely
        vulns_data = results.get('vulnerabilities', {})
        sql_injection_data = vulns_data.get('sql_injection', {})
        if isinstance(sql_injection_data, dict):
            sql_vulns_count = len(sql_injection_data.get('vulnerabilities', []))
        elif isinstance(sql_injection_data, list):
            sql_vulns_count = len(sql_injection_data)
        else:
            sql_vulns_count = 0
            
        return {
            'total_open_ports': len(results.get('ports', {}).get('open_ports', [])),
            'total_accessible_urls': len(results.get('directories', {}).get('accessible_urls', [])),
            'total_forms_found': len(results.get('vulnerabilities', {}).get('forms', [])),
            'total_sql_vulnerabilities': sql_vulns_count,
            'scan_duration': "Calculated duration",
            'risk_level': self._calculate_risk_level(results)
        }
        
    def _calculate_risk_level(self, results: Dict[str, Any]) -> str:
        """Calculate overall risk level"""
        risk_score = 0
        
        # Port-based risk
        open_ports = results.get('ports', {}).get('open_ports', [])
        high_risk_ports = [21, 23, 3306, 5432]  # FTP, Telnet, MySQL, PostgreSQL
        for port in open_ports:
            if port in high_risk_ports:
                risk_score += 3
            elif port in [80, 443]:
                risk_score += 1
                
        # Vulnerability-based risk
        vulns_data = results.get('vulnerabilities', {})
        sql_injection_data = vulns_data.get('sql_injection', {})
        if isinstance(sql_injection_data, dict):
            sql_vulns = len(sql_injection_data.get('vulnerabilities', []))
        elif isinstance(sql_injection_data, list):
            sql_vulns = len(sql_injection_data)
        else:
            sql_vulns = 0
        risk_score += sql_vulns * 5
        
        # Determine risk level
        if risk_score >= 10:
            return "HIGH"
        elif risk_score >= 5:
            return "MEDIUM"
        else:
            return "LOW"
            
    def stop_scan(self):
        """Stop current scan"""
        self.is_scanning = False
        self.update_progress("⏹️ Scan stopped by user") 