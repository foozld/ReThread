"""
ReThread - AI Helper Module
Anthropic Claude Integration for Environmental Impact Explanations

This module handles integration with Anthropic's Claude AI to generate
detailed, human-friendly explanations of clothing material sustainability.
It includes graceful fallback if the API is unavailable.
"""

import os
import json
import anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
print("API KEY LOADED:", api_key)

def generate_fabric_explanation(material, material_data):
    """
    Generate a natural language explanation of a single material's environmental impact using Claude.
    
    Args:
        material (str): The name of the clothing material
        material_data (dict): The material's data including sustainability, impact, 
                            water_usage, biodegradable status, and alternatives
        
    Returns:
        str: A formatted explanation of the material's sustainability
        
    Note:
        Uses Anthropic Claude API for generation. Falls back to pre-written
        explanations if the API key is not available.
    """
    
    try:
        # Get API key from environment variables
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # If no API key is configured, return a fallback explanation
        if not api_key:
            return get_fallback_explanation(material)
        
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build the prompt with material data
        alternatives_str = ", ".join(material_data.get('alternatives', [])) if material_data.get('alternatives') else "None listed"
        
        prompt = f"""Material: {material}

Material Sustainability Data:
- Sustainability Rating: {material_data.get('sustainability', 'Unknown')}
- Environmental Impact: {material_data.get('impact', 'No information')}
- Water Usage: {material_data.get('water_usage', 'Unknown')}
- Biodegradable: {material_data.get('biodegradable', 'Unknown')}
- Sustainable Alternatives: {alternatives_str}

Provide a concise 2-3 sentence explanation of this material's sustainability based on the data above. Be practical and actionable in your recommendation."""

        message = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=150,
            temperature=0.3,
            system="You are an expert in sustainable fashion and textile environmental impact. Explain sustainability clearly using the provided data.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        # Log the error
        print(f"Error in generate_fabric_explanation: {str(e)}")
        
        # Return a fallback explanation so the app still works
        return get_fallback_explanation(material)



def generate_composition_explanation(composition, weighted_score, rating, materials_data):
    """
    Generate an AI explanation for a multi-fabric garment composition using Claude.
    
    Args:
        composition: Can be either:
                   - A list of dicts: [{"material": "Cotton", "percent": 60}, {"material": "Polyester", "percent": 40}]
                   - A string: "60% cotton 50% polyester" (will be parsed)
        weighted_score (float): Calculated weighted sustainability score (0-100)
        rating (str): Overall sustainability rating ("Good", "Moderate", or "Poor")
        materials_data (dict): Database of all material sustainability data
        
    Returns:
        dict: A dictionary containing:
            - sustainability_rating: The overall rating
            - explanation: Brief summary of the blend's sustainability
            - ai_analysis: Detailed AI analysis from Claude
            - alternatives: Suggestions for more sustainable compositions
        
    Note:
        Uses Anthropic Claude API. Falls back to basic analysis if API unavailable.
    """
    
    try:
        # Parse composition if it's a string
        if isinstance(composition, str):
            composition_list = _parse_composition_string(composition, materials_data)
            if not composition_list:
                # If parsing failed, use fallback
                return get_fallback_composition_analysis(composition)
        else:
            composition_list = composition
        
        # Get API key from environment variables
        api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # If no API key is configured, return a fallback analysis
        if not api_key:
            return get_fallback_composition_analysis(composition)
        
        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)
        
        # Build composition string for the prompt
        composition_str = ", ".join([f"{item['percent']}% {item['material']}" for item in composition_list])
        
        # Build material impact summary
        material_impacts = []
        for item in composition_list:
            material_name = item['material']
            percent = item['percent']
            if material_name in materials_data:
                impact = materials_data[material_name].get('impact', 'Unknown impact')
                material_impacts.append(f"- {percent}% {material_name}: {impact}")
        
        material_impacts_str = "\n".join(material_impacts) if material_impacts else "Material details not available"
        
        # Build the prompt
        prompt = f"""Analyze this fabric composition for sustainability:

Composition: {composition_str}

Overall Sustainability Score: {weighted_score:.1f}/100
Overall Rating: {rating}

Material Breakdown:
{material_impacts_str}

Provide:
1. A brief assessment (1-2 sentences) of this garment's overall sustainability
2. Which material(s) contribute most to environmental impact
3. One specific recommendation to improve sustainability
Keep your response concise and actionable."""

        message = client.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=150,
            temperature=0.3,
            system="You are an expert in sustainable fashion and textile environmental impact. Provide clear, practical sustainability guidance based on the provided material composition data.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        explanation_text = message.content[0].text
        
        return {
            'sustainability_rating': rating,
            'explanation': f"This garment composition scores {weighted_score:.0f}/100 on sustainability.",
            'ai_analysis': explanation_text,
            'alternatives': [
                "100% Organic Cotton",
                "70% Hemp, 30% Organic Cotton",
                "Tencel/Lyocell blend",
                "Recycled Polyester blend"
            ]
        }
        
    except Exception as e:
        # Log the error
        print(f"Error in generate_composition_explanation: {str(e)}")
        
        # Return a fallback analysis so the app still works
        return get_fallback_composition_analysis(composition)


def _parse_composition_string(composition_str, materials_data):
    """
    Parse a composition string like "60% cotton 50% polyester" into a list of dicts.
    
    Args:
        composition_str (str): String like "60% cotton 50% polyester"
        materials_data (dict): Database to lookup material names
        
    Returns:
        list: List of dicts like [{"material": "Cotton", "percent": 60}, ...]
              or None if parsing fails
    """
    try:
        import re
        
        # Pattern to match percentage and material name
        # Matches "60% cotton" or "60% organic cotton"
        pattern = r'(\d+)\s*%\s*([a-zA-Z\s]+)'
        matches = re.findall(pattern, composition_str, re.IGNORECASE)
        
        if not matches:
            return None
        
        composition_list = []
        for percent_str, material_name in matches:
            percent = int(percent_str)
            material_name_clean = material_name.strip()
            
            # Try to find the material in the database (case-insensitive)
            found_material = None
            for db_material in materials_data.keys():
                if db_material.lower() == material_name_clean.lower():
                    found_material = db_material
                    break
            
            if found_material:
                composition_list.append({
                    'material': found_material,
                    'percent': percent
                })
            else:
                # Material not found, but include it anyway
                composition_list.append({
                    'material': material_name_clean,
                    'percent': percent
                })
        
        return composition_list if composition_list else None
        
    except Exception as e:
        print(f"Error parsing composition string: {str(e)}")
        return None


def get_fallback_composition_analysis(composition):
    """
    Provide a fallback composition analysis when AI API is not available.
    
    Args:
        composition: Can be either a list or a string composition
        
    Returns:
        dict: Basic analysis with pre-determined sustainability rating
    """
    
    # Convert to string for analysis
    if isinstance(composition, list):
        composition_str = " ".join([f"{item.get('percent', 0)}% {item.get('material', 'Unknown')}" 
                                    for item in composition]).lower()
    else:
        composition_str = str(composition).lower()
    
    # Simple heuristics for fallback analysis
    poor_materials = ['polyester', 'acrylic', 'nylon', 'spandex']
    good_materials = ['hemp', 'organic cotton', 'tencel', 'linen', 'modal']
    
    # Count material occurrences and weight by percentage if available
    poor_score = 0
    good_score = 0
    
    if isinstance(composition, list):
        for item in composition:
            material = item.get('material', '').lower()
            percent = item.get('percent', 0)
            
            if any(poor_mat in material for poor_mat in poor_materials):
                poor_score += percent
            if any(good_mat in material for good_mat in good_materials):
                good_score += percent
    else:
        # Fallback for string composition
        poor_count = sum(1 for material in poor_materials if material in composition_str)
        good_count = sum(1 for material in good_materials if material in composition_str)
        poor_score = poor_count * 25
        good_score = good_count * 25
    
    # Determine rating based on composition
    if good_score > poor_score:
        rating = 'Good'
        explanation = 'This composition includes sustainable materials.'
    elif poor_score > good_score:
        rating = 'Poor'
        explanation = 'This composition includes materials with significant environmental impact.'
    else:
        rating = 'Moderate'
        explanation = 'This composition is a moderate blend with mixed environmental considerations.'
    
    return {
        'sustainability_rating': rating,
        'explanation': explanation,
        'ai_analysis': 'AI analysis is temporarily unavailable. Basic assessment has been provided.',
        'alternatives': ['100% Organic Cotton', '100% Hemp', 'Tencel/Lyocell blend', 'Recycled Polyester blend']
    }


def get_fallback_explanation(material):
    """
    Provide a fallback explanation when LLM API is not available.
    These are pre-written explanations for common materials.
    
    Args:
        material (str): The name of the clothing material
        
    Returns:
        str: A pre-written explanation or a generic message
    """
    
    # Dictionary of fallback explanations for common materials
    fallback_explanations = {
        'polyester': 'Polyester is a synthetic fabric made from petroleum-derived polymers. While durable and water-resistant, it creates microplastics when washed and relies on fossil fuels for production. Consider alternatives like Tencel or recycled polyester.',
        
        'cotton': 'Cotton is a natural fabric but requires significant water and pesticides to grow. Traditional cotton farming has a notable environmental impact. Organic cotton is a better choice as it avoids harmful chemicals.',
        
        'organic cotton': 'Organic cotton is grown without synthetic pesticides or fertilizers, making it much more sustainable than conventional cotton. While it still requires water, it represents a significant improvement for the environment.',
        
        'hemp': 'Hemp is one of the most sustainable fabrics available. It requires minimal water, no pesticides, and regenerates quickly. Hemp also sequesters carbon in the soil, making it excellent for the environment.',
        
        'tencel': 'Tencel (lyocell) is made from sustainably managed wood pulp using a closed-loop process. It requires less water than cotton and the production process recycles 99% of solvents, making it very eco-friendly.',
        
        'nylon': 'Nylon is a synthetic polymer that takes decades to biodegrade. It requires fossil fuels and releases nitrous oxide during production. Seek out recycled nylon or alternative synthetic fabrics.',
        
        'wool': 'Wool is a natural, biodegradable fiber with good longevity. However, sheep farming has environmental impacts including methane emissions. Look for responsibly sourced wool with minimal environmental impact.',
        
        'silk': 'Silk is a natural protein fiber but sericulture (silk production) can be resource-intensive. Choosing peace silk or mulberry silk from responsible producers is important. It\'s biodegradable but production practices matter.',
        
        'bamboo': 'Bamboo is a highly renewable resource that grows quickly and requires minimal inputs. However, processing into fabric can use harmful chemicals. Look for bamboo fabrics processed with sustainable methods.',
        
        'acrylic': 'Acrylic is a synthetic petroleum-based fiber that does not biodegrade for many decades. It sheds microfibers when washed, polluting waterways. Consider natural or sustainably-produced alternatives.',
        
        'linen': 'Linen is made from flax plant fibers and is highly sustainable. It requires minimal pesticides, has low water usage through rainfed cultivation, and is biodegradable within weeks. Linen is excellent for environmental sustainability.',
        
        'recycled polyester': 'Recycled polyester gives new life to existing plastic waste, reducing the need for new petroleum-based production. While it still sheds microfibers, it has a lower environmental impact than virgin polyester and helps reduce landfill waste.',
        
        'modal': 'Modal is a semi-synthetic fiber made from beech pulp using an eco-friendly closed-loop production process. It uses less water than cotton, is biodegradable, and represents a sustainable choice for fabric production.',
    }
    
    # Return the specific explanation if available, otherwise a generic message
    material_lower = material.lower()
    if material_lower in fallback_explanations:
        return fallback_explanations[material_lower]
    else:
        # Generic fallback for materials not in our pre-written list
        return f'For detailed information about {material}, please consult environmental textile databases or sustainable fashion resources. Consider the material\'s production impact, durability, and end-of-life biodegradability when making purchasing decisions.'


def setup_api_integration():
    """
    Helper function to display instructions for setting up Anthropic Claude API.
    Call this during development to guide setup.
    """
    instructions = """
    ReThread Claude AI Integration Setup
    ====================================
    
    To enable AI-powered explanations with Anthropic Claude:
    
    1. Get an Anthropic API key:
       - Visit: https://console.anthropic.com/
       - Sign up or log in to your account
       - Navigate to API keys and create a new key
    
    2. Add to your .env file:
       ANTHROPIC_API_KEY=your-actual-key-here
    
    3. Install the Anthropic Python library:
       pip install anthropic
    
    4. Test by running the application and analyzing a material
    
    Anthropic Claude has a generous free tier perfect for hackathons!
    """
    
    print(instructions)


# For local testing and development
if __name__ == '__main__':
    # Test the AI helper functions
    # Load sample material data from materials.json
    try:
        with open('materials.json', 'r') as f:
            all_materials = json.load(f)
    except FileNotFoundError:
        print("Error: materials.json not found!")
        all_materials = {}
    
    test_materials = ['Polyester', 'Organic Cotton', 'Hemp', 'Nylon']
    
    print("ReThread AI Helper - Test Mode")
    print("=" * 50)
    
    for material in test_materials:
        if material in all_materials:
            material_data = all_materials[material]
            explanation = generate_fabric_explanation(material, material_data)
            print(f"\n{material.upper()}:")
            print(explanation)
            print("-" * 50)
        else:
            print(f"\n{material}: NOT FOUND in database")
