"""
ReThread - Sustainable Fashion Analyzer
Backend Flask Application

This Flask app provides an API to analyze clothing materials for their
environmental sustainability. It returns information about environmental
impact, water usage, biodegradability, and sustainable alternatives.
"""

from flask import Flask, render_template, request, jsonify
import json
import os
from dotenv import load_dotenv
from ai_helper import generate_fabric_explanation, generate_composition_explanation, calculate_composition_score, _parse_composition_string

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
# Wrapping Python file in Flask to create a website
app = Flask(__name__)

# Load the materials dataset from JSON file
def load_materials():
    """
    Load the materials dataset from materials.json file.
    Returns a dictionary of materials with their properties.
    """
    try:
        with open('materials.json', 'r', encoding='utf-8') as f:
            materials = json.load(f)
        return materials
    except FileNotFoundError:
        print("Error: materials.json not found!")
        return {}
    except json.JSONDecodeError:
        print("Error: materials.json is not valid JSON!")
        return {}

# Load materials on application startup
MATERIALS = load_materials()


@app.route('/')
def index():
    """
    Serve the homepage of the ReThread application.
    Renders the index.html template.
    """
    return render_template('index.html')


@app.route('/test-forms')
def test_forms():
    """
    Serve a simple form test page for debugging frontend-backend communication.
    This page has minimal JavaScript to isolate form submission issues.
    """
    return render_template('test_forms.html')



@app.route('/analyze', methods=['POST'])
def analyze():
    """
    API endpoint to analyze a clothing material.
    
    Expected JSON input:
    {
        "material": "polyester"
    }
    
    Returns JSON with:
    - material name
    - sustainability rating
    - environmental impact description
    - water usage
    - biodegradability status
    - sustainable alternatives
    - AI-generated explanation (if API key is available)
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Validate that material field exists
        if not data or 'material' not in data:
            return jsonify({
                'error': 'Please provide a material name',
                'success': False
            }), 400
        
        # Get the material name and normalize it (capitalize first letter, lowercase rest)
        material_input = data['material'].strip().lower()
        
        # Search for the material in our database (case-insensitive)
        material_found = None
        for mat_key, mat_data in MATERIALS.items():
            if mat_key.lower() == material_input:
                material_found = mat_key
                break
        
        # If material not found, return an error response
        if not material_found:
            return jsonify({
                'error': f'Material "{data["material"]}" not found in our database',
                'success': False,
                'available_materials': list(MATERIALS.keys())
            }), 404
        
        # Get the material data
        material_data = MATERIALS[material_found]
        
        # Extract metrics from the new data structure
        metrics = material_data.get('metrics', {})
        score = material_data.get('sustainability_score', 0)
        
        # Convert sustainability score (0-5) to a rating
        if score >= 4.5:
            sustainability_rating = "Very High"
        elif score >= 3.5:
            sustainability_rating = "High"
        elif score >= 2.5:
            sustainability_rating = "Medium"
        elif score >= 1.5:
            sustainability_rating = "Low"
        else:
            sustainability_rating = "Very Low"
        
        # Build biodegradability status from metrics
        biodegradability = metrics.get('biodegradability', 0)
        if biodegradability == 5:
            biodegradable_text = "Yes (rapidly biodegradable)"
        elif biodegradability >= 3:
            biodegradable_text = "Yes (biodegradable)"
        elif biodegradability >= 1:
            biodegradable_text = "Partially biodegradable"
        else:
            biodegradable_text = "No (non-biodegradable)"
        
        # Build water usage status from metrics
        water_usage = metrics.get('water_usage', 0)
        if water_usage >= 4:
            water_usage_text = "High"
        elif water_usage >= 2:
            water_usage_text = "Moderate"
        else:
            water_usage_text = "Low"
        
        # Build the response with the material information
        response = {
            'success': True,
            'material': material_found,
            'sustainability': sustainability_rating,
            'impact': material_data.get('description', 'No information available'),
            'water_usage': water_usage_text,
            'main_issues': material_data.get('main_issues', []),
            'metrics': {
                'carbon_emissions': metrics.get('carbon_emissions', 0),
                'water_usage': metrics.get('water_usage', 0),
                'microplastic_risk': metrics.get('microplastic_risk', 0),
                'biodegradability': metrics.get('biodegradability', 0)
            },
            'biodegradable': biodegradable_text,
            'alternatives': material_data.get('alternatives', []),
            'sustainability_score': score
        }
        
        # Try to generate an AI explanation if API key is available
        try:
            ai_explanation = generate_fabric_explanation(material_found, material_data)
            response['ai_explanation'] = ai_explanation
        except Exception as e:
            # If AI fails, include a message but don't fail the entire request
            response['ai_explanation'] = f"AI explanation unavailable: {str(e)}"
        
        return jsonify(response), 200
    
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500


@app.route('/analyze-composition', methods=['POST'])
def analyze_composition():
    """
    API endpoint to analyze a fabric composition blend.
    
    Expected JSON input:
    {
        "composition": "50% cotton 50% polyester"
    }
    
    Returns JSON with:
    - composition (the input)
    - sustainability_rating (Good/Moderate/Poor)
    - explanation (sustainability analysis)
    - ai_analysis (AI-generated insights from Gemini)
    """
    try:
        # Get the JSON data from the request
        data = request.get_json()
        
        # Validate that composition field exists
        if not data or 'composition' not in data:
            return jsonify({
                'error': 'Please provide a fabric composition',
                'success': False
            }), 400
        
        # Get the composition text
        composition = data['composition'].strip()
        
        # Validate composition is not empty
        if not composition:
            return jsonify({
                'error': 'Fabric composition cannot be empty',
                'success': False
            }), 400
        
        # Basic validation: composition should contain percentage or material names
        composition_lower = composition.lower()
        has_percentage = '%' in composition
        
        # Try to analyze the composition with AI
        try:
            from ai_helper import generate_composition_explanation, _parse_composition_string, calculate_composition_score
            
            # Parse the composition string into a structured format
            composition_list = _parse_composition_string(composition, MATERIALS)
            
            # Calculate the weighted sustainability score
            if composition_list:
                weighted_score, rating = calculate_composition_score(composition_list, MATERIALS)
            else:
                weighted_score, rating = 0, "Poor"
            
            # Generate AI analysis with the calculated scores
            analysis_result = generate_composition_explanation(composition, weighted_score, rating, MATERIALS)
            
            return jsonify({
                'success': True,
                'composition': composition,
                'sustainability_rating': analysis_result.get('sustainability_rating', 'Moderate'),
                'explanation': analysis_result.get('explanation', 'Analysis complete'),
                'ai_analysis': analysis_result.get('ai_analysis', ''),
                'alternatives': analysis_result.get('alternatives', [])
            }), 200
        
        except ImportError:
            # If generate_composition_explanation doesn't exist, use fallback
            return jsonify({
                'success': True,
                'composition': composition,
                'sustainability_rating': 'Moderate',
                'explanation': 'Composition analysis requires AI service. Please ensure your API key is configured.',
                'ai_analysis': 'AI analysis is temporarily unavailable. Please try again later.',
                'alternatives': []
            }), 200
    
    except Exception as e:
        # Handle any unexpected errors
        return jsonify({
            'error': f'Server error: {str(e)}',
            'success': False
        }), 500


@app.route('/materials', methods=['GET'])
def get_all_materials():
    """
    Bonus endpoint: Get a list of all available materials in the database.
    Useful for frontend autocomplete or suggestions.
    """
    return jsonify({
        'success': True,
        'materials': list(MATERIALS.keys()),
        'count': len(MATERIALS)
    }), 200


# Error handlers for better user experience
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'error': 'Endpoint not found',
        'success': False
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({
        'error': 'Internal server error',
        'success': False
    }), 500


if __name__ == '__main__':
    # Run the Flask development server
    # Debug mode is OFF for production
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000
    )
