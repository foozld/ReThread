#!/usr/bin/env python3
"""
ReThread Diagnostic Script
Identifies why the app isn't outputting results
"""

import sys
import traceback

print("🔍 RETHREAD DIAGNOSTIC SCRIPT\n")
print("=" * 80)

# Test 1: Check imports
print("\nTest 1: Checking Python imports...")
print("-" * 80)

try:
    print("  Importing Flask...", end=" ")
    from flask import Flask, render_template, request, jsonify
    print("✅")
except Exception as e:
    print(f"❌ {e}")
    sys.exit(1)

try:
    print("  Importing json...", end=" ")
    import json
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  Importing os...", end=" ")
    import os
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  Importing dotenv...", end=" ")
    from dotenv import load_dotenv
    print("✅")
except Exception as e:
    print(f"❌ {e}")

try:
    print("  Importing ai_helper...", end=" ")
    from ai_helper import generate_explanation
    print("✅")
except Exception as e:
    print(f"❌ ERROR IN AI_HELPER:")
    print(f"     {e}")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Check files
print("\nTest 2: Checking required files...")
print("-" * 80)

files_to_check = [
    'app.py',
    'ai_helper.py',
    'materials.json',
    '.env',
    'templates/index.html',
    'static/style.css',
    'static/script.js'
]

for filepath in files_to_check:
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"  ✅ {filepath:<30} ({size:>6} bytes)")
    else:
        print(f"  ❌ {filepath:<30} NOT FOUND")

# Test 3: Check materials.json
print("\nTest 3: Loading materials database...")
print("-" * 80)

try:
    load_dotenv()
    with open('materials.json') as f:
        materials = json.load(f)
    print(f"  ✅ Loaded {len(materials)} materials")
except Exception as e:
    print(f"  ❌ Error loading materials: {e}")
    traceback.print_exc()

# Test 4: Check app initialization
print("\nTest 4: Initializing Flask app...")
print("-" * 80)

try:
    app = Flask(__name__)
    print("  ✅ Flask app initialized")
except Exception as e:
    print(f"  ❌ Error: {e}")
    traceback.print_exc()

# Test 5: Check if templates exist
print("\nTest 5: Checking template files...")
print("-" * 80)

try:
    # Check if Jinja2 can find templates
    from jinja2 import Environment, FileSystemLoader
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)
    
    # Try to load the template
    template = env.get_template('index.html')
    print("  ✅ index.html template loads successfully")
except Exception as e:
    print(f"  ❌ Template error: {e}")
    traceback.print_exc()

# Test 6: Check API simulation
print("\nTest 6: Testing API endpoint logic...")
print("-" * 80)

try:
    # Simulate the analyze endpoint
    test_input = 'hemp'
    
    # Normalize input
    material_normalized = test_input.strip().lower()
    
    # Find material
    material_found = None
    for key in materials:
        if key.lower() == material_normalized:
            material_found = key
            break
    
    if material_found:
        print(f"  ✅ Material found: {material_found}")
        data = materials[material_found]
        
        # Test if generate_explanation can be called
        print("  Testing generate_explanation()...", end=" ")
        try:
            result = generate_explanation(material_found, data)
            print(f"✅")
            print(f"     Result length: {len(result)} chars")
        except Exception as e:
            print(f"❌ {e}")
    else:
        print(f"❌ Material '{test_input}' not found")
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLETE\n")
print("If all tests passed, the issue is likely:")
print("  1. Flask app not running (try: python app.py)")
print("  2. Frontend JavaScript error (check browser console with F12)")
print("  3. API endpoint returning error (check Network tab in browser DevTools)")
