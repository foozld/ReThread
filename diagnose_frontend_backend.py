"""
Test script to diagnose frontend-backend communication issue
Simulates form submission flow
"""

import sys
import subprocess
import time

print("=" * 70)
print("ReThread Frontend-Backend Communication Diagnostic")
print("=" * 70)

# Test 1: Check if Flask is running
print("\n✓ Test 1: Checking if Flask server is running...")
try:
    import requests
    response = requests.get('http://127.0.0.1:5000/', timeout=2)
    if response.status_code == 200:
        print("  ✅ Flask server is running and responding")
        print("  Status Code:", response.status_code)
    else:
        print("  ⚠️ Flask returned status:", response.status_code)
except Exception as e:
    print(f"  ❌ Cannot connect to Flask: {e}")
    sys.exit(1)

# Test 2: Check if script.js is being served
print("\n✓ Test 2: Checking if script.js is being served...")
try:
    response = requests.get('http://127.0.0.1:5000/static/script.js', timeout=2)
    if response.status_code == 200:
        print("  ✅ script.js is being served")
        print("  File size:", len(response.text), "bytes")
        
        # Check if it has syntax errors or debug statements
        if 'analyzeMaterial()' in response.text:
            print("  ✅ Contains analyzeMaterial() function")
        if 'console.log' in response.text:
            print("  ✅ Contains debug console.log statements")
        if 'analyzeComposition()' in response.text:
            print("  ✅ Contains analyzeComposition() function")
    else:
        print("  ❌ script.js returned status:", response.status_code)
except Exception as e:
    print(f"  ❌ Error fetching script.js: {e}")

# Test 3: Check if HTML contains the forms
print("\n✓ Test 3: Checking if HTML contains form elements...")
try:
    response = requests.get('http://127.0.0.1:5000/', timeout=2)
    if response.status_code == 200:
        html = response.text
        
        checks = [
            ('id="materialForm"', 'Material form'),
            ('id="materialInput"', 'Material input'),
            ('id="compositionForm"', 'Composition form'),
            ('id="compositionInput"', 'Composition input'),
            ('id="loadingSpinner"', 'Loading spinner'),
            ('id="errorContainer"', 'Error container'),
        ]
        
        for check_str, label in checks:
            if check_str in html:
                print(f"  ✅ {label} found in HTML")
            else:
                print(f"  ❌ {label} NOT found in HTML")
except Exception as e:
    print(f"  ❌ Error fetching HTML: {e}")

# Test 4: Test /analyze endpoint directly
print("\n✓ Test 4: Testing /analyze endpoint directly...")
try:
    import json
    response = requests.post(
        'http://127.0.0.1:5000/analyze',
        json={'material': 'cotton'},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("  ✅ /analyze endpoint working correctly")
            print("  Response keys:", list(data.keys()))
        else:
            print("  ⚠️ /analyze returned success=false")
    else:
        print("  ❌ /analyze returned status:", response.status_code)
except Exception as e:
    print(f"  ❌ Error testing /analyze: {e}")

# Test 5: Test /analyze-composition endpoint
print("\n✓ Test 5: Testing /analyze-composition endpoint...")
try:
    response = requests.post(
        'http://127.0.0.1:5000/analyze-composition',
        json={'composition': '50% cotton 50% polyester'},
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("  ✅ /analyze-composition endpoint working correctly")
            print("  Response keys:", list(data.keys()))
        else:
            print("  ⚠️ /analyze-composition returned success=false")
    else:
        print("  ❌ /analyze-composition returned status:", response.status_code)
except Exception as e:
    print(f"  ❌ Error testing /analyze-composition: {e}")

print("\n" + "=" * 70)
print("DIAGNOSTIC SUMMARY")
print("=" * 70)
print("\nIf all tests passed:")
print("  1. Open browser and go to http://127.0.0.1:5000/")
print("  2. Press F12 to open Developer Console")
print("  3. Look for 'ReThread loaded successfully!' message")
print("  4. Enter a material name and click 'Analyze'")
print("  5. Check console for debug messages starting with 📊 or 🔄")
print("\nIf forms are NOT working:")
print("  - Check browser console (F12) for JavaScript errors")
print("  - Look for messages like '❌ materialForm not found'")
print("  - This will indicate if DOM elements are missing")
print("\n" + "=" * 70)
