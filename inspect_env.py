import os

print("Inspecting .env file line by line:\n")

with open('.env', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f, 1):
        if i <= 20 or 'ANTHROPIC' in line:
            # Show with repr to see all characters
            print(f"Line {i}: {repr(line)}")
