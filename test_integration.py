#!/usr/bin/env python3
"""
Test script for SecWiz GUI and Backend Integration

This script tests the integration between the GUI and backend tools.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from gui.gui import SecWizGUI
        from gui.backend_integration import SecWizBackendIntegration
        from tools.portScanner import scan_ports
        from tools.gobuster_scan import run_gobuster_scan
        from tools.sqlScanner import sqlScanner
        from tools.parmScanner import fetch_forms_inputs
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_backend_integration():
    """Test the backend integration module"""
    try:
        from gui.backend_integration import SecWizBackendIntegration
        
        # Create integration instance
        integration = SecWizBackendIntegration()
        
        # Test basic functionality
        assert hasattr(integration, 'run_full_scan')
        assert hasattr(integration, 'run_port_scan')
        assert hasattr(integration, 'run_directory_scan')
        
        print("✅ Backend integration test passed!")
        return True
    except Exception as e:
        print(f"❌ Backend integration test failed: {e}")
        return False

def test_gui_creation():
    """Test that GUI can be created"""
    try:
        from gui.gui import SecWizGUI
        
        # Create GUI instance (don't run it)
        app = SecWizGUI()
        
        # Test basic attributes
        assert hasattr(app, 'root')
        assert hasattr(app, 'backend')
        assert hasattr(app, 'scan_results')
        
        print("✅ GUI creation test passed!")
        return True
    except Exception as e:
        print(f"❌ GUI creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing SecWiz GUI and Backend Integration...")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Backend Integration Test", test_backend_integration),
        ("GUI Creation Test", test_gui_creation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed!")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Integration is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 