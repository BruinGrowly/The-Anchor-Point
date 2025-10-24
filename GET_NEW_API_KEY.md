# How to Create and Copy Your Claude API Key

## The Problem
Existing API keys in the Console are truncated for security. You can't reveal them after creation.

## The Solution: Create a New Key

### Step 1: Go to API Keys Page
Visit: https://console.anthropic.com/settings/keys

### Step 2: Create New Key
1. Click the **"Create Key"** button (top right)
2. Give it a name like "anchor-point-research"
3. Click **"Create Key"**

### Step 3: COPY THE KEY IMMEDIATELY
**CRITICAL:** The full key will be shown ONLY ONCE in a popup/modal.

It will look like:
```
sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Copy the entire key right away!** You won't be able to see it again.

### Step 4: Set It Up

**Option A - Quick Test (Linux/Mac):**
```bash
export ANTHROPIC_API_KEY='sk-ant-api03-YOUR-FULL-KEY-HERE'
python setup_api_key.py
```

**Option B - Permanent Setup:**
Create a `.env` file in The-Anchor-Point directory:
```bash
echo 'ANTHROPIC_API_KEY=sk-ant-api03-YOUR-FULL-KEY-HERE' > .env
```

Then test:
```bash
python setup_api_key.py
```

### Step 5: Verify It Works
If successful, you'll see:
```
✅ SUCCESS! API key is working!
Response: Hello! I'm Claude...
```

## What If I Miss Copying It?
If you navigate away before copying, you'll need to:
1. Delete that key
2. Create another new one
3. Copy it immediately this time

## Next Steps
Once your key is working, we'll run the Phase 3 validation to test the Anchor Point hypothesis with real AI!
