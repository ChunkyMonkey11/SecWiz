#!/usr/bin/env python3
"""
Test script for automated sqlmap integration
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from tools.sqlScanner import sqlScanner
import json

def test_automated_sqlmap():
    """Test the automated sqlmap integration"""
    
    # Test with a known vulnerable target
    test_urls = ['http://testphp.vulnweb.com/']
    
    print("🚀 Testing Automated SQL Injection Scanner")
    print(f"Target URLs: {test_urls}")
    print("=" * 60)
    
    try:
        # Run automated SQL injection scan
        print("🔍 Starting automated SQL injection scan...")
        results = sqlScanner(test_urls, True)
        
        if results:
            print("✅ Automated SQL injection scan completed successfully!")
            
            # Display results structure
            if isinstance(results, dict):
                print(f"\n📊 Scan Summary:")
                summary = results.get('summary', {})
                print(f"   Total URLs: {summary.get('total_urls', 0)}")
                print(f"   Total Vulnerabilities: {summary.get('total_vulnerabilities', 0)}")
                print(f"   Scan Timestamp: {summary.get('scan_timestamp', 'Unknown')}")
                
                # Display scan logs
                print(f"\n📋 Scan Logs:")
                logs = results.get('scan_logs', [])
                for log in logs:
                    print(f"   {log}")
                
                # Display vulnerabilities
                vulnerabilities = results.get('vulnerabilities', [])
                if vulnerabilities:
                    print(f"\n🎯 Found {len(vulnerabilities)} SQL Injection Vulnerabilities:")
                    for i, vuln in enumerate(vulnerabilities, 1):
                        print(f"\n   Vulnerability {i}:")
                        print(f"     URL: {vuln.get('URL', 'Unknown')}")
                        print(f"     Method: {vuln.get('Method', 'Unknown')}")
                        print(f"     Parameter: {vuln.get('Parameter', 'Unknown')}")
                        print(f"     DBMS: {vuln.get('DBMS', 'Unknown')}")
                        print(f"     Technology: {vuln.get('Tech', 'Unknown')}")
                        print(f"     OS: {vuln.get('OS', 'Unknown')}")
                        print(f"     Injection Types: {len(vuln.get('Injections', []))}")
                        
                        for inj in vuln.get('Injections', []):
                            print(f"       • {inj['Type']} - {inj['Title']}")
                            print(f"         Payload: {inj['Payload']}")
                else:
                    print("✅ No SQL injection vulnerabilities found")
            else:
                print(f"📊 Results: {len(results)} vulnerabilities found")
                
        else:
            print("❌ No results returned from SQL injection scan")
            
    except Exception as e:
        print(f"❌ Error during automated SQL injection scan: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_automated_sqlmap()
