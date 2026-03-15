import json
from app import app

# Create a test client
client = app.test_client()

# Test the /analyze endpoint
response = client.post('/analyze', json={'material': 'cotton'})
data = response.get_json()

print('✅ Material Analysis Test')
print('=' * 60)
print(f'Material: {data.get("material")}')
print(f'Sustainability: {data.get("sustainability")}')
print(f'Sustainability Score: {data.get("sustainability_score")}/5')
print(f'Description: {data.get("impact")}')
print(f'Main Issues: {data.get("main_issues")}')
print(f'Biodegradable: {data.get("biodegradable")}')
print(f'\nMetrics (0-5 scale):')
metrics = data.get('metrics', {})
print(f'  - Carbon Emissions: {metrics.get("carbon_emissions")}')
print(f'  - Water Usage: {metrics.get("water_usage")}')
print(f'  - Microplastic Risk: {metrics.get("microplastic_risk")}')
print(f'  - Biodegradability: {metrics.get("biodegradability")}')
print(f'\nAlternatives: {data.get("alternatives")}')
