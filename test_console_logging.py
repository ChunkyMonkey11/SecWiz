#!/usr/bin/env python3
"""
Test script to demonstrate console logging functionality

This script simulates the scan button presses and shows the console output.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_console_logging():
    """Test the console logging functionality"""
    try:
        from gui.gui import SecWizGUI
        
        print("🧪 Testing Console Logging Functionality...")
        print("=" * 60)
        
        # Create GUI instance
        app = SecWizGUI()
        
        # Simulate different scan types
        test_cases = [
            ("full", "testphp.vulnweb.com"),
            ("port", "example.com"),
            ("directory", "demo.testfire.net")
        ]
        
        for scan_type, target in test_cases:
            print(f"\n📋 Testing {scan_type.upper()} scan...")
            
            # Set scan type
            app.scan_type.set(scan_type)
            
            # Set target
            app.target_entry.delete(0, "end")
            app.target_entry.insert(0, target)
            
            # Simulate start scan (without actually running)
            print(f"🎯 Simulating scan button press...")
            print(f"   Scan Type: {scan_type}")
            print(f"   Target: {target}")
            
            # Call the start_scan method directly
            app.start_scan()
            
            print(f"✅ Console logging test completed for {scan_type} scan")
        
        print("\n" + "=" * 60)
        print("🎉 All console logging tests completed!")
        print("\n📝 Expected Console Output:")
        print("""
============================================================
🚀 Start Scan: { Scan Type: Full Scan, Target: testphp.vulnweb.com }
============================================================
🔍 Starting Full Scan for target: testphp.vulnweb.com
✅ Full Scan completed for target: testphp.vulnweb.com
🏁 Scan process completed

============================================================
🚀 Start Scan: { Scan Type: Port Scan, Target: example.com }
============================================================
🔍 Starting Port Scan for target: example.com
✅ Port Scan completed for target: example.com
🏁 Scan process completed

============================================================
🚀 Start Scan: { Scan Type: Directory Scan, Target: demo.testfire.net }
============================================================
🔍 Starting Directory Scan for target: demo.testfire.net
✅ Directory Scan completed for target: demo.testfire.net
🏁 Scan process completed
        """)
        
        return True
        
    except Exception as e:
        print(f"❌ Console logging test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_console_logging()
    sys.exit(0 if success else 1) 