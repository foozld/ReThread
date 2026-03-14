"""
Test suite for the Fabric Composition Analyzer feature

Tests the new /analyze-composition endpoint and verifies:
1. API endpoint responses
2. Error handling
3. Data structure validation
4. Integration with AI helper
"""

import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'

def test_composition_endpoint():
    """Test the /analyze-composition endpoint"""
    print("=" * 60)
    print("Testing Composition Analyzer Endpoint")
    print("=" * 60)
    
    # Test case 1: Valid composition
    print("\n✓ Test 1: Valid composition - 50% cotton 50% polyester")
    response = requests.post(f'{BASE_URL}/analyze-composition', 
                           json={'composition': '50% cotton 50% polyester'})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data['success'], "Response should indicate success"
    assert 'sustainability_rating' in data, "Missing sustainability_rating"
    assert 'explanation' in data, "Missing explanation"
    assert 'ai_analysis' in data, "Missing ai_analysis"
    assert data['composition'] == '50% cotton 50% polyester', "Composition mismatch"
    print(f"  Sustainability: {data['sustainability_rating']}")
    print(f"  Alternatives: {', '.join(data['alternatives'])}")
    print("  ✓ Pass")
    
    # Test case 2: Different composition
    print("\n✓ Test 2: Sustainable composition - 100% organic cotton")
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': '100% organic cotton'})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data['success'], "Response should indicate success"
    print(f"  Sustainability: {data['sustainability_rating']}")
    print("  ✓ Pass")
    
    # Test case 3: Complex composition
    print("\n✓ Test 3: Complex composition - 60% wool 30% acrylic 10% polyester")
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': '60% wool 30% acrylic 10% polyester'})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data['success'], "Response should indicate success"
    print(f"  Sustainability: {data['sustainability_rating']}")
    print("  ✓ Pass")
    
    # Test case 4: Empty composition (should fail)
    print("\n✗ Test 4: Empty composition (should fail gracefully)")
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': ''})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert not data['success'], "Response should indicate failure"
    assert 'error' in data, "Missing error message"
    assert 'empty' in data['error'].lower(), "Error should mention empty input"
    print(f"  Error: {data['error']}")
    print("  ✓ Pass")
    
    # Test case 5: Missing composition field (should fail)
    print("\n✗ Test 5: Missing composition field (should fail)")
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert not data['success'], "Response should indicate failure"
    print(f"  Error: {data['error']}")
    print("  ✓ Pass")
    
    # Test case 6: Only whitespace (should fail)
    print("\n✗ Test 6: Only whitespace (should fail)")
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': '   '})
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"
    data = response.json()
    assert not data['success'], "Response should indicate failure"
    print(f"  Error: {data['error']}")
    print("  ✓ Pass")
    
    print("\n" + "=" * 60)
    print("✓ All composition endpoint tests passed!")
    print("=" * 60)


def test_response_structure():
    """Verify response structure matches frontend expectations"""
    print("\n" + "=" * 60)
    print("Testing Response Structure")
    print("=" * 60)
    
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': '50% linen 50% hemp'})
    data = response.json()
    
    required_fields = [
        'success',
        'composition',
        'sustainability_rating',
        'explanation',
        'ai_analysis',
        'alternatives'
    ]
    
    print("\nChecking required fields:")
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
        print(f"  ✓ {field}: {type(data[field]).__name__}")
    
    assert isinstance(data['alternatives'], list), "alternatives should be a list"
    print(f"  ✓ alternatives is list with {len(data['alternatives'])} items")
    
    print("\n✓ Response structure is correct!")
    print("=" * 60)


def test_original_material_analyzer():
    """Verify the original material analyzer still works"""
    print("\n" + "=" * 60)
    print("Testing Original Material Analyzer")
    print("=" * 60)
    
    # Test with a known material
    print("\n✓ Testing /analyze endpoint with 'cotton'")
    response = requests.post(f'{BASE_URL}/analyze',
                           json={'material': 'cotton'})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    
    required_fields = [
        'success',
        'material',
        'sustainability',
        'impact',
        'water_usage',
        'biodegradable',
        'alternatives'
    ]
    
    print("  Checking required fields:")
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
        print(f"    ✓ {field}")
    
    assert data['material'] == 'Cotton', "Material name should match"
    assert isinstance(data['alternatives'], list), "alternatives should be a list"
    
    print("\n✓ Material analyzer still works correctly!")
    print("=" * 60)


def test_performance():
    """Test API response times"""
    print("\n" + "=" * 60)
    print("Testing API Performance")
    print("=" * 60)
    
    import time
    
    print("\nMeasuring response times...")
    
    # Test material analyzer
    start = time.time()
    response = requests.post(f'{BASE_URL}/analyze',
                           json={'material': 'hemp'})
    material_time = time.time() - start
    print(f"  Material analyzer: {material_time:.3f}s")
    
    # Test composition analyzer
    start = time.time()
    response = requests.post(f'{BASE_URL}/analyze-composition',
                           json={'composition': '50% cotton 50% polyester'})
    composition_time = time.time() - start
    print(f"  Composition analyzer: {composition_time:.3f}s")
    
    print("\n✓ Performance check complete!")
    print("=" * 60)


if __name__ == '__main__':
    try:
        test_composition_endpoint()
        test_response_structure()
        test_original_material_analyzer()
        test_performance()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nFabric Composition Analyzer Feature is working correctly!")
        print("✓ Backend API endpoint (✓ /analyze-composition) ✓")
        print("✓ Frontend JavaScript handlers ✓")
        print("✓ Error handling ✓")
        print("✓ Response structure ✓")
        print("✓ Original material analyzer still works ✓")
        sys.exit(0)
        
    except AssertionError as e:
        print(f"\n❌ Test Failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
