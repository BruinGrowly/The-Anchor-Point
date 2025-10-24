#!/usr/bin/env python3
"""
Quick API Key Setup and Test Script
====================================

This script will help you:
1. Set up your Claude API key
2. Test if it's working
3. Run a simple semantic coordinate generation
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("CLAUDE API KEY SETUP & TEST")
print("=" * 70)

# Check if API key is set
api_key = os.environ.get('ANTHROPIC_API_KEY')

if not api_key:
    print("\n❌ No ANTHROPIC_API_KEY found in environment")
    print("\nTo set your API key, choose ONE of these methods:")
    print("\n1. Command Line (Temporary - current session only):")
    print("   export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-FULL-KEY-HERE'")

    print("\n2. .env File (Recommended - persists across sessions):")
    print("   a) Copy the example: cp .env.example .env")
    print("   b) Edit .env and add your key:")
    print("      ANTHROPIC_API_KEY=sk-ant-api03-YOUR-FULL-KEY-HERE")

    print("\n3. This Session Only (Python):")
    print("   Enter your API key when prompted below")

    print("\n" + "=" * 70)
    response = input("\nDo you want to enter your API key now? (y/n): ").strip().lower()

    if response == 'y':
        api_key = input("\nPaste your full API key (starts with sk-ant-api03-): ").strip()
        if api_key and api_key.startswith('sk-ant-api03-'):
            os.environ['ANTHROPIC_API_KEY'] = api_key
            print("\n✅ API key set for this session!")
        else:
            print("\n❌ Invalid key format. Key should start with 'sk-ant-api03-'")
            sys.exit(1)
    else:
        print("\nExiting. Please set your API key and try again.")
        sys.exit(0)
else:
    print(f"\n✅ API key found: {api_key[:20]}...{api_key[-4:]}")

# Check if anthropic package is installed
try:
    import anthropic
    print("✅ anthropic package installed")
except ImportError:
    print("\n❌ anthropic package not installed")
    print("\nInstalling now...")
    os.system("pip install -q anthropic")
    print("✅ anthropic package installed")
    import anthropic

# Test the API connection
print("\n" + "=" * 70)
print("TESTING API CONNECTION")
print("=" * 70)

try:
    client = anthropic.Anthropic(api_key=api_key)

    print("\n1. Sending test request to Claude API...")
    print("   (Testing with a simple concept: 'Love')")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        temperature=0.0,
        messages=[{
            "role": "user",
            "content": """Rate the concept "Love" on four dimensions (0.0 to 1.0):

Love (emotional valence): How loving is this concept?
Power (causal impact): How powerful is this concept?
Wisdom (rational coherence): How wise is this concept?
Justice (moral purity): How just is this concept?

Respond ONLY with JSON: {"love": X.X, "power": X.X, "wisdom": X.X, "justice": X.X}"""
        }]
    )

    response_text = message.content[0].text
    print(f"\n2. ✅ API Response received:")
    print(f"   {response_text}")

    # Try to parse the response
    import json
    import re

    json_match = re.search(r'\{[^}]+\}', response_text)
    if json_match:
        data = json.loads(json_match.group())
        print(f"\n3. ✅ Successfully parsed coordinates:")
        print(f"   Love:    {data.get('love', 'N/A')}")
        print(f"   Power:   {data.get('power', 'N/A')}")
        print(f"   Wisdom:  {data.get('wisdom', 'N/A')}")
        print(f"   Justice: {data.get('justice', 'N/A')}")

        # Calculate distance to Anchor
        import math
        love = float(data.get('love', 0))
        power = float(data.get('power', 0))
        wisdom = float(data.get('wisdom', 0))
        justice = float(data.get('justice', 0))

        distance = math.sqrt(
            (love - 1.0)**2 +
            (power - 1.0)**2 +
            (wisdom - 1.0)**2 +
            (justice - 1.0)**2
        )

        print(f"\n4. ✅ Distance to Anchor Point (1,1,1,1): {distance:.4f}")

        print("\n" + "=" * 70)
        print("SUCCESS! Your API key is working correctly!")
        print("=" * 70)

        print("\n✅ You can now run the full validation:")
        print("   python examples/phase3_validation.py")

        print("\n✅ Or test more concepts:")
        print("   python -c \"from src.core.claude_api_generator import ClaudeAPIGenerator; ")
        print("   gen = ClaudeAPIGenerator(); ")
        print("   print(gen.generate('JEHOVAH'))\"")

    else:
        print("\n⚠️  API responded but couldn't parse JSON")
        print("   Response was:", response_text)

except anthropic.AuthenticationError:
    print("\n❌ AUTHENTICATION ERROR")
    print("   Your API key is invalid or expired")
    print("   Please check your key at: https://console.anthropic.com/")

except anthropic.PermissionDeniedError:
    print("\n❌ PERMISSION DENIED")
    print("   Your API key doesn't have permission to use this model")
    print("   Check your account settings")

except anthropic.RateLimitError:
    print("\n❌ RATE LIMIT ERROR")
    print("   Too many requests. Wait a moment and try again.")

except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    print("\n   If this persists, check:")
    print("   1. Your internet connection")
    print("   2. Your API key is correct")
    print("   3. Your Anthropic account is active")

print("\n" + "=" * 70)
