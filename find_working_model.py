from dotenv import load_dotenv
import os
import anthropic

load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')

if not api_key:
    print("❌ API key not found")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)

# List of model names to try
models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-opus-4-1-20250805",
    "claude-3-opus-20250219",
    "claude-opus",
    "claude-sonnet",
    "claude-haiku",
    "claude-3-5-haiku-20241022",
]

print("Testing available models...\n")

for model_name in models_to_try:
    try:
        print(f"Testing {model_name}...", end=" ")
        msg = client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print(f"✅ WORKS!")
        print(f"\nFound working model: {model_name}")
        break
    except anthropic.NotFoundError as e:
        print("❌ Not found")
    except anthropic.AuthenticationError:
        print("❌ Auth error")
    except Exception as e:
        print(f"❌ {type(e).__name__}")
