from dotenv import load_dotenv
import os

print("Current working directory:", os.getcwd())
print("Checking for .env file...")

env_path = ".env"
if os.path.exists(env_path):
    print(f"✅ .env file found at: {os.path.abspath(env_path)}")
else:
    print(f"❌ .env file NOT found at: {os.path.abspath(env_path)}")

print("\nLoading .env...")
result = load_dotenv()
print(f"load_dotenv() result: {result}")

key = os.getenv('ANTHROPIC_API_KEY')
if key:
    print("✅ ANTHROPIC_API_KEY loaded successfully!")
    print(f"   Key length: {len(key)}")
    print(f"   First 30 chars: {key[:30]}")
else:
    print("❌ ANTHROPIC_API_KEY not found after load_dotenv()")
    print("\nAll environment variables starting with 'A':")
    for k, v in os.environ.items():
        if k.startswith('A'):
            print(f"   {k}")
