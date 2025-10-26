#!/usr/bin/env python3
"""
Testing Theological Prompting: Can AI Distinguish JEHOVAH from Allah?
======================================================================

Testing whether explicit theological framing can override AI's default
semantic bias that treats JEHOVAH = Allah.

Hypothesis: AI has training bias toward interfaith unity
Question: Can explicit biblical/theological prompting produce correct distinction?
"""

import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

import anthropic
import os
import json

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

print("=" * 90)
print("TESTING THEOLOGICAL PROMPTING: JEHOVAH vs Allah")
print("=" * 90)

# Test 1: Original neutral prompt (baseline)
print("\n" + "=" * 90)
print("TEST 1: NEUTRAL PROMPT (Baseline - shows AI bias)")
print("=" * 90)

neutral_prompt_jehovah = """Rate JEHOVAH on four dimensions (0.0-1.0 scale):
- Love (compassion, care, connection)
- Power (strength, capability, influence)
- Wisdom (knowledge, understanding, insight)
- Justice (fairness, righteousness, moral order)

Return JSON: {"love": X, "power": Y, "wisdom": Z, "justice": W}"""

neutral_prompt_allah = """Rate Allah on four dimensions (0.0-1.0 scale):
- Love (compassion, care, connection)
- Power (strength, capability, influence)
- Wisdom (knowledge, understanding, insight)
- Justice (fairness, righteousness, moral order)

Return JSON: {"love": X, "power": Y, "wisdom": Z, "justice": W}"""

print("\nPrompting for JEHOVAH (neutral)...")
response_j = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.0,
    messages=[{"role": "user", "content": neutral_prompt_jehovah}]
)
jehovah_neutral = json.loads(response_j.content[0].text.strip())

print("\nPrompting for Allah (neutral)...")
response_a = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.0,
    messages=[{"role": "user", "content": neutral_prompt_allah}]
)
allah_neutral = json.loads(response_a.content[0].text.strip())

print(f"\nNeutral Results:")
print(f"  JEHOVAH: {jehovah_neutral}")
print(f"  Allah:   {allah_neutral}")

# Test 2: Biblical theological prompt
print("\n" + "=" * 90)
print("TEST 2: BIBLICAL THEOLOGICAL PROMPT")
print("=" * 90)

biblical_prompt_jehovah = """According to the Bible, JEHOVAH (the God of Israel) IS love itself (1 John 4:8),
not merely having love as an attribute. He is described as perfect in all attributes:
- Love: Essential nature, not just quality (1 John 4:8, 16)
- Power: Omnipotent, creator of all (Genesis 1:1, Revelation 19:6)
- Wisdom: Infinite, unsearchable (Romans 11:33, Isaiah 40:28)
- Justice: Perfectly righteous (Psalm 145:17, Deuteronomy 32:4)

Rate JEHOVAH on these dimensions (0.0-1.0 scale) based on biblical revelation:
Return JSON: {"love": X, "power": Y, "wisdom": Z, "justice": W}"""

biblical_prompt_allah = """According to Islamic theology, Allah has 99 names describing various attributes.
While described as loving (Al-Wadud), the Quran emphasizes:
- Love: Conditional - "Allah loves not transgressors" (Quran 2:190)
- Power: Absolute sovereignty and might
- Wisdom: All-knowing but transcendent/distant
- Justice: Strict, not always balanced with mercy in same way as biblical God

Compared to the biblical JEHOVAH who IS love itself (1 John 4:8), rate Allah
on these dimensions (0.0-1.0) acknowledging theological differences:
Return JSON: {"love": X, "power": Y, "wisdom": Z, "justice": W}"""

print("\nPrompting for JEHOVAH (biblical)...")
response_j2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.0,
    messages=[{"role": "user", "content": biblical_prompt_jehovah}]
)
jehovah_biblical = json.loads(response_j2.content[0].text.strip())

print("\nPrompting for Allah (theological comparison)...")
response_a2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=200,
    temperature=0.0,
    messages=[{"role": "user", "content": biblical_prompt_allah}]
)
allah_theological = json.loads(response_a2.content[0].text.strip())

print(f"\nBiblical/Theological Results:")
print(f"  JEHOVAH: {jehovah_biblical}")
print(f"  Allah:   {allah_theological}")

# Test 3: Explicit comparative prompt
print("\n" + "=" * 90)
print("TEST 3: EXPLICIT COMPARATIVE PROMPT")
print("=" * 90)

comparative_prompt = """Compare JEHOVAH (biblical God) and Allah (Islamic god) on these dimensions.

Key theological distinction from Scripture:
- JEHOVAH IS love (essential nature, 1 John 4:8)
- Allah HAS love (attribute, conditional)

Rate each (0.0-1.0):
1. Love (IS vs HAS)
2. Power
3. Wisdom (relational vs transcendent)
4. Justice (mercy-balanced vs strict)

Return JSON:
{
  "jehovah": {"love": X, "power": Y, "wisdom": Z, "justice": W},
  "allah": {"love": X, "power": Y, "wisdom": Z, "justice": W}
}"""

print("\nPrompting for comparative analysis...")
response_comp = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=300,
    temperature=0.0,
    messages=[{"role": "user", "content": comparative_prompt}]
)
comparative = json.loads(response_comp.content[0].text.strip())

print(f"\nComparative Results:")
print(f"  JEHOVAH: {comparative['jehovah']}")
print(f"  Allah:   {comparative['allah']}")

# Analysis
print("\n" + "=" * 90)
print("ANALYSIS: Does Theological Prompting Change Results?")
print("=" * 90)

import numpy as np

def distance_4d(coord1, coord2):
    v1 = np.array([coord1['love'], coord1['power'], coord1['wisdom'], coord1['justice']])
    v2 = np.array([coord2['love'], coord2['power'], coord2['wisdom'], coord2['justice']])
    return np.linalg.norm(v1 - v2)

def distance_to_anchor(coord):
    v = np.array([coord['love'], coord['power'], coord['wisdom'], coord['justice']])
    anchor = np.array([1.0, 1.0, 1.0, 1.0])
    return np.linalg.norm(v - anchor)

print("\nTest 1 (Neutral):")
dist1 = distance_4d(jehovah_neutral, allah_neutral)
print(f"  JEHOVAH ↔ Allah distance: {dist1:.6f}")
print(f"  {'IDENTICAL' if dist1 < 0.001 else 'DIFFERENT'}")

print("\nTest 2 (Biblical/Theological):")
dist2 = distance_4d(jehovah_biblical, allah_theological)
print(f"  JEHOVAH ↔ Allah distance: {dist2:.6f}")
print(f"  {'IDENTICAL' if dist2 < 0.001 else 'DIFFERENT'}")

print("\nTest 3 (Explicit Comparative):")
dist3 = distance_4d(comparative['jehovah'], comparative['allah'])
print(f"  JEHOVAH ↔ Allah distance: {dist3:.6f}")
print(f"  {'IDENTICAL' if dist3 < 0.001 else 'DIFFERENT'}")

print("\n" + "=" * 90)
print("DIMENSION-BY-DIMENSION COMPARISON")
print("=" * 90)

dimensions = ['love', 'power', 'wisdom', 'justice']

print(f"\n{'Dimension':<12} {'Neutral':<20} {'Biblical':<20} {'Comparative':<20}")
print(f"{'':12} {'J':>8} {'A':>8} {'Δ':>8} {'J':>8} {'A':>8} {'Δ':>8} {'J':>8} {'A':>8} {'Δ':>8}")
print("-" * 90)

for dim in dimensions:
    n_j = jehovah_neutral[dim]
    n_a = allah_neutral[dim]
    n_d = n_j - n_a

    b_j = jehovah_biblical[dim]
    b_a = allah_theological[dim]
    b_d = b_j - b_a

    c_j = comparative['jehovah'][dim]
    c_a = comparative['allah'][dim]
    c_d = c_j - c_a

    print(f"{dim:<12} {n_j:>8.2f} {n_a:>8.2f} {n_d:>8.2f} {b_j:>8.2f} {b_a:>8.2f} {b_d:>8.2f} {c_j:>8.2f} {c_a:>8.2f} {c_d:>8.2f}")

print("\n" + "=" * 90)
print("CONCLUSION")
print("=" * 90)

# Check if ANY test showed significant difference
max_dist = max(dist1, dist2, dist3)
if max_dist > 0.3:
    print(f"\n✅ SUCCESS: Theological prompting DOES produce distinction")
    print(f"   Maximum distance achieved: {max_dist:.4f}")
    if dist3 == max_dist:
        print(f"   Best result: Explicit comparative prompt")
    elif dist2 == max_dist:
        print(f"   Best result: Biblical/theological prompt")
else:
    print(f"\n❌ FAILURE: AI still treats them as similar despite theological framing")
    print(f"   Maximum distance: {max_dist:.4f} (below threshold)")
    print(f"   This suggests deep training bias in AI")

print("\n" + "=" * 90)
print("USER'S THEOLOGICAL FRAMEWORK COMPARISON")
print("=" * 90)

user_jehovah = {'love': 1.0, 'power': 1.0, 'wisdom': 1.0, 'justice': 1.0}
user_allah = {'love': 0.7, 'power': 0.4, 'wisdom': 0.6, 'justice': 0.8}
user_dist = distance_4d(user_jehovah, user_allah)

print(f"\nUser's expected distinction: {user_dist:.4f}")
print(f"Best AI result (Test {[1,2,3][np.argmax([dist1, dist2, dist3])]}):"
      f" {max_dist:.4f}")
print(f"Gap: {abs(user_dist - max_dist):.4f}")

if abs(user_dist - max_dist) < 0.2:
    print("\n✅ AI can approximate theological framework with proper prompting")
else:
    print("\n⚠️  Significant gap remains - AI semantic bias persists")
    print("   Recommendation: Use manual theological coordinates")

print("\n" + "=" * 90)
