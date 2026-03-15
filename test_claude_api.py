#!/usr/bin/env python3
"""
Test script to verify Claude API is being called for material explanations
Helps diagnose if fallback explanations are being used instead of Claude
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_configuration():
    """Check if ANTHROPIC_API_KEY is configured"""
    print("=" * 70)
    print("🔍 CHECKING ANTHROPIC API CONFIGURATION")
    print("=" * 70)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if api_key:
        print(f"✅ ANTHROPIC_API_KEY is set")
        print(f"   Key length: {len(api_key)} characters")
        print(f"   Key prefix: {api_key[:10]}...")
    else:
        print("❌ ANTHROPIC_API_KEY is NOT set")
        print("   The system will use fallback explanations instead of Claude API")
        print("\n   To set it:")
        print("   1. Create a .env file in the project root")
        print("   2. Add: ANTHROPIC_API_KEY=sk-ant-...")
        return False
    
    return True

def test_claude_direct_call():
    """Test calling Claude API directly"""
    print("\n" + "=" * 70)
    print("🤖 TESTING DIRECT CLAUDE API CALL")
    print("=" * 70)
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ Cannot test - ANTHROPIC_API_KEY not set")
        return False
    
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        print("📤 Sending test message to Claude...")
        
        message = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=50,
            temperature=0.3,
            system="You are a test assistant.",
            messages=[
                {"role": "user", "content": "Say 'Claude API is working' in exactly 5 words."}
            ]
        )
        
        response_text = message.content[0].text
        print(f"✅ Claude responded successfully!")
        print(f"   Response: {response_text}")
        return True
        
    except Exception as e:
        print(f"❌ Claude API call failed: {str(e)}")
        return False

def test_fabric_explanation():
    """Test generating a fabric explanation"""
    print("\n" + "=" * 70)
    print("🧵 TESTING FABRIC EXPLANATION GENERATION")
    print("=" * 70)
    
    # Import the function
    try:
        from ai_helper import generate_fabric_explanation
    except ImportError:
        print("❌ Cannot import generate_fabric_explanation")
        return False
    
    # Load materials
    try:
        with open('materials.json') as f:
            materials = json.load(f)
    except FileNotFoundError:
        print("❌ Cannot find materials.json")
        return False
    
    # Test with Linen (the problematic material mentioned)
    test_material = "Linen"
    if test_material not in materials:
        print(f"❌ {test_material} not found in materials.json")
        return False
    
    material_data = materials[test_material]
    
    print(f"\n📝 Testing {test_material} explanation:")
    print(f"   Material data:")
    for key, value in material_data.items():
        print(f"     - {key}: {value}")
    
    print(f"\n📤 Calling generate_fabric_explanation('{test_material}', material_data)...")
    
    explanation = generate_fabric_explanation(test_material, material_data)
    
    print(f"\n📥 Result:")
    print(f"   {explanation}")
    
    # Check if it's a fallback explanation
    is_generic_fallback = "For detailed information about" in explanation and "consult environmental" in explanation
    is_fallback_linen = "linen" not in explanation.lower() and len(explanation) < 50
    
    if is_generic_fallback:
        print(f"\n⚠️ WARNING: This appears to be a GENERIC FALLBACK explanation")
        print(f"   The Claude API was likely NOT called")
        print(f"   This happens when ANTHROPIC_API_KEY is not set or Claude call failed")
        return False
    elif is_fallback_linen:
        print(f"\n⚠️ WARNING: Response is very short and may not be from Claude")
        print(f"   Length: {len(explanation)} characters")
        return False
    else:
        print(f"\n✅ Response looks like it came from Claude")
        print(f"   Length: {len(explanation)} characters")
        print(f"   Contains 'sustainability': {'sustainability' in explanation.lower()}")
        return True

def test_all_materials():
    """Test explanations for all materials"""
    print("\n" + "=" * 70)
    print("📊 TESTING ALL MATERIAL EXPLANATIONS")
    print("=" * 70)
    
    try:
        from ai_helper import generate_fabric_explanation
    except ImportError:
        print("❌ Cannot import generate_fabric_explanation")
        return
    
    try:
        with open('materials.json') as f:
            materials = json.load(f)
    except FileNotFoundError:
        print("❌ Cannot find materials.json")
        return
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    using_claude = "✅ (Claude)" if api_key else "⚠️ (Fallback)"
    
    print(f"\nTesting {len(materials)} materials. API status: {using_claude}\n")
    
    for material_name, material_data in list(materials.items())[:5]:  # Test first 5
        explanation = generate_fabric_explanation(material_name, material_data)
        
        # Check if generic fallback
        is_generic = "For detailed information about" in explanation and "consult environmental" in explanation
        status = "❌ GENERIC FALLBACK" if is_generic else "✅ GOOD"
        
        print(f"{status} | {material_name:<20} | {len(explanation):3d} chars")
        print(f"        {explanation[:80]}{'...' if len(explanation) > 80 else ''}")
        print()

def main():
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "CLAUDE API DIAGNOSTIC TEST" + " " * 27 + "║")
    print("╚" + "=" * 68 + "╝")
    
    # Test 1: Check API key
    has_api_key = test_api_configuration()
    
    # Test 2: Test direct Claude call
    if has_api_key:
        claude_works = test_claude_direct_call()
    else:
        claude_works = False
    
    # Test 3: Test fabric explanation
    explanation_works = test_fabric_explanation()
    
    # Test 4: Test all materials
    test_all_materials()
    
    # Summary
    print("\n" + "=" * 70)
    print("📋 DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    if has_api_key and claude_works and explanation_works:
        print("✅ ALL TESTS PASSED: Claude API is working correctly!")
    else:
        print("⚠️ ISSUES DETECTED:")
        if not has_api_key:
            print("   ❌ ANTHROPIC_API_KEY not configured")
            print("      → Create .env file with ANTHROPIC_API_KEY=sk-ant-...")
        if has_api_key and not claude_works:
            print("   ❌ Claude API call failed")
            print("      → Check API key validity and network connection")
        if not explanation_works:
            print("   ❌ Fabric explanations are using fallback (not Claude)")
            print("      → May be due to API key or API call error")
    
    print("=" * 70 + "\n")

if __name__ == '__main__':
    main()
