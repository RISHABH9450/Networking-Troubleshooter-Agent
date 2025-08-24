#!/usr/bin/env python3
"""
Test script for the AgentHack 2025 Networking Troubleshooter
"""

import sys
import os
import requests
import json
import time

# Add backend to path
sys.path.append('/workspace/backend')

def test_backend_api():
    """Test if backend API endpoints work"""
    print("🧪 Testing Backend API...")
    
    base_url = "http://localhost:8000"
    
    # Test basic health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend health endpoint working")
        else:
            print(f"❌ Backend health endpoint returned {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend not accessible: {e}")
        return False
    
    # Test troubleshooter endpoints
    endpoints = [
        "/troubleshooter/health",
        "/troubleshooter/quick-check",
        "/troubleshooter/examples"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint} working")
            else:
                print(f"❌ {endpoint} returned {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} failed: {e}")
    
    # Test POST diagnosis endpoint
    try:
        data = {
            "frontend_port": 5173,
            "backend_port": 8000,
            "frontend_path": "/workspace/frontend",
            "backend_path": "/workspace/backend"
        }
        response = requests.post(f"{base_url}/troubleshooter/diagnose", json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Diagnosis endpoint working - found {result['summary']['total']} tests")
            print(f"   📊 Passed: {result['summary']['passed']}, Failed: {result['summary']['failed']}, Warnings: {result['summary']['warnings']}")
        else:
            print(f"❌ Diagnosis endpoint returned {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Diagnosis endpoint failed: {e}")
    
    return True

def test_troubleshooter_class():
    """Test the troubleshooter class directly"""
    print("\n🔧 Testing Troubleshooter Class...")
    
    try:
        from app.networking_troubleshooter import NetworkingTroubleshooter
        
        # Create troubleshooter instance
        troubleshooter = NetworkingTroubleshooter()
        
        # Test individual methods
        print("✅ Troubleshooter class imported successfully")
        
        # Test port accessibility check
        frontend_accessible = troubleshooter._is_port_accessible(5173)
        backend_accessible = troubleshooter._is_port_accessible(8000)
        
        print(f"   🌐 Frontend (5173): {'✅ accessible' if frontend_accessible else '❌ not accessible'}")
        print(f"   🖥️  Backend (8000): {'✅ accessible' if backend_accessible else '❌ not accessible'}")
        
        # Test connectivity checks
        connectivity_results = troubleshooter._check_connectivity()
        print(f"   🔌 Connectivity tests: {len(connectivity_results)} checks completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Troubleshooter class test failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = [
        '/workspace/backend/app/networking_troubleshooter.py',
        '/workspace/backend/app/troubleshooter_api.py',
        '/workspace/frontend/src/TroubleshooterDashboard.jsx',
        '/workspace/frontend/src/App.jsx',
        '/workspace/troubleshoot.py',
        '/workspace/README_TROUBLESHOOTER.md'
    ]
    
    all_exists = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {os.path.basename(file_path)} exists")
        else:
            print(f"❌ {os.path.basename(file_path)} missing")
            all_exists = False
    
    return all_exists

def test_frontend_accessibility():
    """Test if frontend is accessible"""
    print("\n🌐 Testing Frontend Accessibility...")
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is accessible on localhost:5173")
            
            # Check if our troubleshooter route exists
            try:
                response = requests.get("http://localhost:5173/agenthack", timeout=5)
                if response.status_code == 200:
                    print("✅ AgentHack troubleshooter route is accessible")
                else:
                    print("⚠️  AgentHack route returned non-200 status (might be client-side routing)")
            except:
                print("⚠️  Could not test AgentHack route")
            
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Frontend not accessible: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AgentHack 2025 Troubleshooter Test Suite")
    print("=" * 50)
    
    # Track test results
    tests = [
        ("File Structure", test_file_structure),
        ("Troubleshooter Class", test_troubleshooter_class),
        ("Backend API", test_backend_api),
        ("Frontend Accessibility", test_frontend_accessibility)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Troubleshooter is ready to use.")
        print("\n💡 Quick start:")
        print("   1. Ensure backend is running: python -m uvicorn app.main:app --reload --port 8000")
        print("   2. Ensure frontend is running: npm run dev")
        print("   3. Run diagnosis: python troubleshoot.py")
        print("   4. Or visit: http://localhost:5173/agenthack")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())