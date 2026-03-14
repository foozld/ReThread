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
from ai_helper import generate_explanation

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
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
        
        # Build the response with the material information
        response = {
            'success': True,
            'material': material_found,
            'sustainability': material_data.get('sustainability', 'Unknown'),
            'impact': material_data.get('impact', 'No information available'),
            'water_usage': material_data.get('water_usage', 'Unknown'),
            'biodegradable': material_data.get('biodegradable', 'Unknown'),
            'alternatives': material_data.get('alternatives', [])
        }
        
        # Try to generate an AI explanation if API key is available
        try:
            ai_explanation = generate_explanation(material_found)
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
    # Debug mode is ON for development - TURN OFF in production!
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
