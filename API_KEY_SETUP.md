# Claude API Key Setup Instructions

You have 6 API keys available in your Console. Here's how to use one:

## Step 1: Get Your Full API Key

1. Go to https://console.anthropic.com/settings/keys
2. Click on any of your keys (e.g., the newest one: `claude_code_key_taurekaw_tdpc`)
3. Click to **reveal the full key** (it will look like `sk-ant-api03-...long string...`)
4. **Copy the entire key** to your clipboard

## Step 2: Test It (Choose ONE method)

### Method A: Quick One-Line Test

```bash
./test_api.sh sk-ant-api03-YOUR-FULL-KEY-HERE
```

Replace `sk-ant-api03-YOUR-FULL-KEY-HERE` with your actual full key.

### Method B: Set Environment Variable

```bash
# Set for current session
export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-FULL-KEY-HERE'

# Test it
python setup_api_key.py
```

### Method C: Create .env File (Recommended)

```bash
# Create .env file
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-api03-YOUR-FULL-KEY-HERE
CACHE_ENABLED=true
CACHE_PATH=data/cache/api_cache.json
DEFAULT_MODEL=claude-3-5-sonnet-20241022
EOF

# Replace YOUR-FULL-KEY-HERE with your actual key
nano .env

# Test it
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Key loaded:', os.getenv('ANTHROPIC_API_KEY')[:20] + '...')"
```

## Step 3: Run Anchor Point Validation

Once your key is working:

```bash
# Simple test with a few concepts
python examples/phase3_validation.py

# Full validation with Claude API generator
python -c "
from src.core.claude_api_generator import ClaudeAPIGenerator
gen = ClaudeAPIGenerator()
concepts = ['JEHOVAH', 'AGAPE', 'Love', 'Justice', 'Evil']
coords = gen.generate_batch(concepts, delay=1.0)
for c in coords:
    if c:
        print(f'{c.concept}: distance={c.distance_to_anchor():.4f}')
"
```

## Troubleshooting

### Error: "Authentication failed"
- **Problem**: Wrong API key format
- **Solution**: Make sure you copied the FULL key including `sk-ant-api03-` prefix

### Error: "No module named 'anthropic'"
```bash
pip install anthropic
```

### Error: "Rate limit exceeded"
- **Problem**: Too many requests too fast
- **Solution**: Wait 60 seconds and try again

### Keys show "Never" used
- **Normal**: This just means you haven't used them via API yet
- Once you successfully call the API, it will update

## Expected Cost

Testing is very cheap:
- Each concept test: ~$0.003
- 10 concepts: ~$0.03
- 100 concepts: ~$0.30
- 1,000 concepts: ~$3.00

Your first tests will be essentially free (< $0.10).

## Which Key to Use?

Any of your 6 keys will work! I recommend:
- **For testing**: Use any key (they're all the same)
- **For production**: Pick one and stick with it for consistency

## Next Steps After Setup

1. ✅ Test API key works (see above)
2. ✅ Run Phase 3 validation: `python examples/phase3_validation.py`
3. ✅ Generate coordinates for 20-50 concepts
4. ✅ Compare simulated vs real API results
5. ✅ Analyze if Phase 2 patterns hold with real AI

## Need Help?

If you're still having issues:

```bash
# Run diagnostic
python setup_api_key.py

# Check environment
echo $ANTHROPIC_API_KEY

# Test anthropic package
python -c "import anthropic; print('anthropic package OK')"

# Minimal API test
python -c "
import anthropic
import os
client = anthropic.Anthropic(api_key='YOUR-KEY-HERE')
msg = client.messages.create(
    model='claude-3-5-sonnet-20241022',
    max_tokens=10,
    messages=[{'role': 'user', 'content': 'Hi'}]
)
print('✅ API working!', msg.content[0].text)
"
```

---

**Remember**: Your API keys are sensitive! Don't commit them to git or share them publicly.
