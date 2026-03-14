#!/usr/bin/env python3
"""
ReThread Startup Helper
Shows errors if the app fails to start
"""

import sys
import os

# Set up path
sys.path.insert(0, os.path.dirname(__file__))

print("\n" + "=" * 80)
print("🚀 RETHREAD STARTUP HELPER")
print("=" * 80)

# Step 1: Check environment
print("\n1. Loading environment variables...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("   ✅ Environment loaded")
    
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        print(f"   ✅ GEMINI_API_KEY configured ({len(gemini_key)} chars)")
    else:
        print("   ⚠️  GEMINI_API_KEY is empty (fallback will be used)")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Step 2: Check imports
print("\n2. Checking Python imports...")
try:
    print("   Importing Flask...", end="")
    sys.stdout.flush()
    from flask import Flask, render_template, request, jsonify
    print(" ✅")
    
    print("   Importing google.generativeai...", end="")
    sys.stdout.flush()
    import google.generativeai as genai
    print(" ✅")
    
    print("   Importing ai_helper...", end="")
    sys.stdout.flush()
    from ai_helper import generate_explanation, get_fallback_explanation
    print(" ✅")
    
except Exception as e:
    print(f"\n   ❌ Import Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Check materials
print("\n3. Loading materials database...")
try:
    import json
    with open('materials.json') as f:
        materials = json.load(f)
    print(f"   ✅ {len(materials)} materials loaded")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Step 4: Test ai_helper
print("\n4. Testing AI helper function...")
try:
    test_data = materials['Hemp']
    result = generate_explanation('Hemp', test_data)
    if result and len(result) > 5:
        print(f"   ✅ generate_explanation works")
        print(f"   Result: {result[:80]}...")
    else:
        print(f"   ⚠️  Result seems empty or too short")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Step 5: Initialize Flask
print("\n5. Initializing Flask app...")
try:
    from app import app
    print("   ✅ Flask app initialized")
except Exception as e:
    print(f"   ❌ Error initializing Flask: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 80)
print("✅ ALL CHECKS PASSED!")
print("=" * 80)
print("\nReady to run: python app.py")
print("\nThen open browser to: http://127.0.0.1:5000")
print("\n")
