"""
ReThread - AI Helper Module
LLM Integration for Environmental Impact Explanations

This module handles integration with an LLM API (like OpenAI) to generate
detailed, human-friendly explanations of clothing material sustainability.
It includes graceful fallback if the API is unavailable.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_explanation(material):
    """
    Generate a natural language explanation of a material's environmental impact.
    
    Args:
        material (str): The name of the clothing material
        
    Returns:
        str: A formatted explanation of the material's sustainability
        
    Note:
        Currently uses a placeholder implementation. Replace with actual
        LLM API calls (OpenAI, Hugging Face, etc.) when API keys are available.
    """
    
    try:
        # Get API key from environment variables
        api_key = os.getenv('LLM_API_KEY')
        api_endpoint = os.getenv('LLM_API_ENDPOINT', 'https://api.openai.com/v1/chat/completions')
        
        # If no API key is configured, return a fallback explanation
        if not api_key or api_key == 'your-api-key-here':
            return get_fallback_explanation(material)
        
        # PLACEHOLDER: This is where you would make the actual API call
        # Example for OpenAI integration (uncomment and modify when you have an API key):
        """
        import requests
        
        prompt = f"""Provide a brief, informative explanation about the environmental 
        sustainability of {material} fabric. Include:
        1. Environmental impact summary
        2. Why it is or isn't sustainable
        3. Better alternatives
        Keep the response to 2-3 sentences."""
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 200
        }
        
        response = requests.post(api_endpoint, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        """
        
        # For now, return fallback explanation
        return get_fallback_explanation(material)
        
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
    Helper function to display instructions for setting up the LLM API.
    Call this during development to guide setup.
    """
    instructions = """
    ReThread AI Integration Setup
    =============================
    
    To enable AI-powered explanations, follow these steps:
    
    1. Choose an LLM provider:
       - OpenAI (recommended for beginners)
       - Hugging Face
       - Claude (Anthropic)
       - Or any OpenAI-compatible API
    
    2. Create an account and get an API key
    
    3. Add to your .env file:
       LLM_API_KEY=your-api-key-here
       LLM_API_ENDPOINT=https://api.openai.com/v1/chat/completions
    
    4. In ai_helper.py, uncomment the API call code (lines ~50-65)
       and install the requests library: pip install requests
    
    5. Test by running the application and analyzing a material
    
    For development and hackathon purposes, the fallback explanations
    provide excellent results without API costs.
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
