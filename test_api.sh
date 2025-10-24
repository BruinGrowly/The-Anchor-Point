#!/bin/bash
# Quick API Test Script
# Usage: ./test_api.sh YOUR-FULL-API-KEY

if [ -z "$1" ]; then
    echo "Usage: ./test_api.sh YOUR-FULL-API-KEY"
    echo ""
    echo "Example:"
    echo "  ./test_api.sh sk-ant-api03-YOUR-FULL-KEY-HERE"
    echo ""
    echo "Get your key from: https://console.anthropic.com/"
    exit 1
fi

echo "Testing API key: ${1:0:20}...${1: -4}"
echo ""

export ANTHROPIC_API_KEY="$1"

python -c "
import os
import sys

# Check if anthropic is installed
try:
    import anthropic
except ImportError:
    print('Installing anthropic package...')
    os.system('pip install -q anthropic')
    import anthropic

# Test API
try:
    client = anthropic.Anthropic(api_key='$1')

    print('Sending test request to Claude API...')
    message = client.messages.create(
        model='claude-3-5-sonnet-20241022',
        max_tokens=100,
        messages=[{
            'role': 'user',
            'content': 'Say hello in JSON format: {\"greeting\": \"your message here\"}'
        }]
    )

    print('✅ SUCCESS! API key is working!')
    print(f'Response: {message.content[0].text}')
    print('')
    print('Your API key is configured correctly.')
    print('You can now run: python examples/phase3_validation.py')

except anthropic.AuthenticationError:
    print('❌ Authentication failed - check your API key')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
"
