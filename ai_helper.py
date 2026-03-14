"""
ReThread - AI Helper Module
Google Gemini Integration for Environmental Impact Explanations

This module handles integration with Google's Generative AI (Gemini) to generate
detailed, human-friendly explanations of clothing material sustainability.
It includes graceful fallback if the API is unavailable.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_explanation(material, material_data):
    """
    Generate a natural language explanation of a material's environmental impact.
    
    Args:
        material (str): The name of the clothing material
        material_data (dict): The material's data including sustainability, impact, 
                            water_usage, biodegradable status, and alternatives
        
    Returns:
        str: A formatted explanation of the material's sustainability
        
    Note:
        Uses Google Gemini API for generation. Falls back to pre-written
        explanations if the API key is not available. Material data provides
        context for more detailed and accurate explanations.
    """
    
    try:
        # Get API key from environment variables
        api_key = os.getenv('GEMINI_API_KEY')
        
        # If no API key is configured, return a fallback explanation
        if not api_key:
            return get_fallback_explanation(material)
        
        # Configure Gemini
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="""
        You are an expert in sustainable fashion and textile environmental impact.

        Your job is to explain clothing material sustainability using ONLY the data provided.

        Rules:
        - Keep explanations concise (2–3 sentences).
        - Do not invent new facts.
        - Base the explanation strictly on the provided material data.
        - Recommend sustainable alternatives when appropriate.
        """
        )

        # Build a rich prompt with material data context
        alternatives_str = ", ".join(material_data.get('alternatives', []))
        
        prompt = f"""
        Material: {material}

        Material data:
        Sustainability: {material_data.get('sustainability')}
        Impact: {material_data.get('impact')}
        Water usage: {material_data.get('water_usage')}
        Biodegradable: {material_data.get('biodegradable')}
        Alternatives: {', '.join(material_data.get('alternatives', []))}

        Explain the sustainability of this material.
        """

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 120
            }
        )

        return response.text
        
        
    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Error in generate_explanation: {str(e)}")
        
        # Return a fallback explanation so the app still works
        return get_fallback_explanation(material)


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
        
        'acrylic': 'Acrylic is a synthetic petroleum-based fiber that does not biodegrade for many decades. It sheds microfibers when washed, polluting waterways. Consider natural or sustainably-produced alternatives.'
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
    Helper function to display instructions for setting up Google Gemini API.
    Call this during development to guide setup.
    """
    instructions = """
    ReThread Gemini AI Integration Setup
    ====================================
    
    To enable AI-powered explanations with Google Gemini:
    
    1. Get a free Gemini API key:
       - Visit: https://aistudio.google.com/app/apikey
       - Click "Get API Key"
       - Create a new API key
    
    2. Add to your .env file:
       GEMINI_API_KEY=your-actual-key-here
    
    3. Install the Google Generative AI library:
       pip install google-generativeai
    
    4. Test by running the application and analyzing a material
    
    Google Gemini has generous free tier limits perfect for hackathons!
    """
    
    print(instructions)


# For local testing and development
if __name__ == '__main__':
    # Test the AI helper functions
    test_materials = ['polyester', 'organic cotton', 'hemp', 'nylon']
    
    print("ReThread AI Helper - Test Mode")
    print("=" * 50)
    
    for material in test_materials:
        explanation = generate_explanation(material)
        print(f"\n{material.upper()}:")
        print(explanation)
        print("-" * 50)
