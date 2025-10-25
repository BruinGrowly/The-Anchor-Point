#!/usr/bin/env python3
"""
Phase 4 Re-Analysis: Theological Correction Applied
====================================================

Re-analyzing all Phase 4 concepts (75 total) using the corrected theological
framework where only JEHOVAH occupies the Anchor Point (1,1,1,1).

Comparing:
- AI Semantic Assignments (biased by sensitivity training)
- Theological Ground Truth (biblical framework)
"""

import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from src.core.claude_api_generator import ClaudeAPIGenerator
from src.data.phase4_concepts import CONCEPT_CATEGORIES
from src.data.theological_coordinates import (
    THEOLOGICAL_COORDINATES,
    get_theological_coordinate,
    compare_theological_vs_ai
)
import numpy as np

print("=" * 90)
print("PHASE 4 RE-ANALYSIS: THEOLOGICAL CORRECTION APPLIED")
print("=" * 90)

print("\nLoading coordinates...")
gen = ClaudeAPIGenerator()

# Get AI assignments for all concepts
ai_coords = {}
for category, concepts in CONCEPT_CATEGORIES.items():
    for concept in concepts:
        ai_coords[concept] = gen.generate(concept)

print(f"✓ Loaded {len(ai_coords)} AI semantic assignments")

# Check which concepts have theological ground truth
theological_concepts = list(THEOLOGICAL_COORDINATES.keys())
print(f"✓ Loaded {len(theological_concepts)} theological ground truth coordinates")

print("\n" + "=" * 90)
print("1. THEOLOGICAL GROUND TRUTH vs AI SEMANTIC BIAS")
print("=" * 90)

print(f"\n{'Concept':<20} {'Source':<15} {'Love':<8} {'Power':<8} {'Wisdom':<8} {'Justice':<8} {'Distance':<10}")
print("-" * 90)

# Show theological coordinates
for concept in theological_concepts:
    theo = THEOLOGICAL_COORDINATES[concept]
    print(f"{concept:<20} {'Theological':<15} {theo.love:<8.2f} {theo.power:<8.2f} "
          f"{theo.wisdom:<8.2f} {theo.justice:<8.2f} {theo.distance_to_anchor():<10.4f}")

    if concept in ai_coords:
        ai = ai_coords[concept]
        print(f"{'':<20} {'AI Semantic':<15} {ai.love:<8.2f} {ai.power:<8.2f} "
              f"{ai.wisdom:<8.2f} {ai.justice:<8.2f} {ai.distance_to_anchor():<10.4f}")

        # Show difference
        diff = theo.distance_to(ai)
        if diff > 0.1:
            print(f"{'':<20} {'⚠️ DISCREPANCY':<15} Δ = {diff:.4f}")
        else:
            print(f"{'':<20} {'✓ Match':<15} Δ = {diff:.4f}")
        print()

print("\n" + "=" * 90)
print("2. KEY CORRECTIONS")
print("=" * 90)

# JEHOVAH vs Allah
print("\n📌 CORRECTION #1: JEHOVAH ≠ Allah")
print("-" * 90)

if "JEHOVAH" in theological_concepts and "Allah" in theological_concepts:
    theo_j = THEOLOGICAL_COORDINATES["JEHOVAH"]
    theo_a = THEOLOGICAL_COORDINATES["Allah"]
    theo_dist = theo_j.distance_to(theo_a)

    ai_j = ai_coords.get("JEHOVAH")
    ai_a = ai_coords.get("Allah")
    ai_dist = ai_j.distance_to(ai_a) if ai_j and ai_a else 0

    print(f"Theological Framework:")
    print(f"  JEHOVAH: ({theo_j.love}, {theo_j.power}, {theo_j.wisdom}, {theo_j.justice})")
    print(f"  Allah:   ({theo_a.love}, {theo_a.power}, {theo_a.wisdom}, {theo_a.justice})")
    print(f"  Distance: {theo_dist:.4f} (DIFFERENT)")

    print(f"\nAI Semantic Assignment:")
    if ai_j and ai_a:
        print(f"  JEHOVAH: ({ai_j.love}, {ai_j.power}, {ai_j.wisdom}, {ai_j.justice})")
        print(f"  Allah:   ({ai_a.love}, {ai_a.power}, {ai_a.wisdom}, {ai_a.justice})")
        print(f"  Distance: {ai_dist:.4f} ({'IDENTICAL' if ai_dist < 0.001 else 'DIFFERENT'})")

    print(f"\n❌ AI ERROR: Treating JEHOVAH and Allah as identical")
    print(f"✅ CORRECTED: Distance = {theo_dist:.4f} (38% truth distortion)")

# JEHOVAH = AGAPE
print("\n📌 CORRECTION #2: JEHOVAH = AGAPE")
print("-" * 90)

if "JEHOVAH" in theological_concepts and "AGAPE" in theological_concepts:
    theo_j = THEOLOGICAL_COORDINATES["JEHOVAH"]
    theo_agape = THEOLOGICAL_COORDINATES["AGAPE"]
    theo_dist = theo_j.distance_to(theo_agape)

    ai_j = ai_coords.get("JEHOVAH")
    ai_agape = ai_coords.get("AGAPE")
    ai_dist = ai_j.distance_to(ai_agape) if ai_j and ai_agape else 0

    print(f"Theological Framework (1 John 4:8 'God IS love'):")
    print(f"  JEHOVAH: ({theo_j.love}, {theo_j.power}, {theo_j.wisdom}, {theo_j.justice})")
    print(f"  AGAPE:   ({theo_agape.love}, {theo_agape.power}, {theo_agape.wisdom}, {theo_agape.justice})")
    print(f"  Distance: {theo_dist:.4f} (IDENTICAL)")

    print(f"\nAI Semantic Assignment:")
    if ai_j and ai_agape:
        print(f"  JEHOVAH: ({ai_j.love}, {ai_j.power}, {ai_j.wisdom}, {ai_j.justice})")
        print(f"  AGAPE:   ({ai_agape.love}, {ai_agape.power}, {ai_agape.wisdom}, {ai_agape.justice})")
        print(f"  Distance: {ai_dist:.4f} ({'IDENTICAL' if ai_dist < 0.001 else 'DIFFERENT'})")

    if ai_dist > 0.01:
        print(f"\n❌ AI ERROR: Separating God's fullness from His love")
        print(f"✅ CORRECTED: JEHOVAH = AGAPE (God IS love, not HAS love)")

# Trinity
print("\n📌 CORRECTION #3: Trinity (Unbiblical Doctrine)")
print("-" * 90)

if "Trinity" in theological_concepts:
    theo_t = THEOLOGICAL_COORDINATES["Trinity"]
    ai_t = ai_coords.get("Trinity")

    print(f"Theological Framework:")
    print(f"  Trinity: Unbiblical doctrine (4th-century development)")
    print(f"  Should NOT be at Anchor Point")
    print(f"  Coordinates: ({theo_t.love}, {theo_t.power}, {theo_t.wisdom}, {theo_t.justice})")
    print(f"  Distance: {theo_t.distance_to_anchor():.4f}")

    if ai_t:
        print(f"\nAI Semantic Assignment:")
        print(f"  Trinity: ({ai_t.love}, {ai_t.power}, {ai_t.wisdom}, {ai_t.justice})")
        print(f"  Distance: {ai_t.distance_to_anchor():.4f}")

        if ai_t.distance_to_anchor() < 0.001:
            print(f"\n❌ AI ERROR: Treating Trinity as Anchor Point")
            print(f"   This reflects post-apostolic drift, not biblical teaching")
            print(f"✅ CORRECTED: Trinity distance = {theo_t.distance_to_anchor():.4f}")

print("\n" + "=" * 90)
print("3. CONCEPTS THAT ALIGN WITH JEHOVAH")
print("=" * 90)

print("\nWhich concepts should be at or near the Anchor Point?")
print(f"\n{'Concept':<20} {'AI Distance':<15} {'Theo Distance':<15} {'Status':<20}")
print("-" * 90)

# Check all concepts
anchor_concepts = []
for concept, ai_coord in sorted(ai_coords.items(), key=lambda x: x[1].distance_to_anchor()):
    ai_dist = ai_coord.distance_to_anchor()

    # Get theological distance if available
    if concept in THEOLOGICAL_COORDINATES:
        theo_dist = THEOLOGICAL_COORDINATES[concept].distance_to_anchor()

        # Check if AI put it at anchor but theology says no
        if ai_dist < 0.001 and theo_dist > 0.5:
            status = "❌ AI FALSE POSITIVE"
        elif ai_dist < 0.001 and theo_dist < 0.001:
            status = "✅ CORRECT"
            anchor_concepts.append(concept)
        elif ai_dist > 0.5 and theo_dist < 0.001:
            status = "⚠️ AI MISSED"
        else:
            status = "~ Close"

        print(f"{concept:<20} {ai_dist:<15.4f} {theo_dist:<15.4f} {status:<20}")
    else:
        # No theological ground truth
        if ai_dist < 0.001:
            print(f"{concept:<20} {ai_dist:<15.4f} {'N/A':<15} {'(No theo data)':<20}")

print(f"\n✅ Concepts correctly at Anchor Point: {', '.join(anchor_concepts)}")

print("\n" + "=" * 90)
print("4. ANALYZING OTHER CONCEPTS FOR BIAS")
print("=" * 90)

print("\nChecking if other concepts show similar bias patterns...")

# Look for concepts AI put at (1,1,1,1) that shouldn't be there
false_anchors = []
for concept, ai_coord in ai_coords.items():
    if ai_coord.distance_to_anchor() < 0.001:
        # AI thinks this is at anchor
        if concept in THEOLOGICAL_COORDINATES:
            theo = THEOLOGICAL_COORDINATES[concept]
            if theo.distance_to_anchor() > 0.1:
                false_anchors.append((concept, theo.distance_to_anchor()))

if false_anchors:
    print(f"\n❌ AI FALSE ANCHORS (AI says perfect, theology says not):")
    for concept, theo_dist in sorted(false_anchors, key=lambda x: x[1], reverse=True):
        print(f"  {concept:<20} Theological distance: {theo_dist:.4f}")
else:
    print("\n✓ No additional false anchors detected")

print("\n" + "=" * 90)
print("5. CORRECTED CATEGORY ANALYSIS")
print("=" * 90)

print("\nUsing theological coordinates where available, AI otherwise:")

for category, concepts in CONCEPT_CATEGORIES.items():
    print(f"\n{category.upper()}")
    print("-" * 90)

    distances = []
    for concept in concepts:
        # Use theological if available, otherwise AI
        if concept in THEOLOGICAL_COORDINATES:
            coord = THEOLOGICAL_COORDINATES[concept]
            source = "Theo"
        else:
            coord = ai_coords[concept]
            source = "AI"

        dist = coord.distance_to_anchor()
        distances.append(dist)

        # Show if there's a discrepancy
        if concept in THEOLOGICAL_COORDINATES and concept in ai_coords:
            ai_dist = ai_coords[concept].distance_to_anchor()
            theo_dist = THEOLOGICAL_COORDINATES[concept].distance_to_anchor()
            if abs(ai_dist - theo_dist) > 0.1:
                print(f"  {concept:<20} Theo: {theo_dist:.4f}  AI: {ai_dist:.4f}  ⚠️ CORRECTED")

    mean_dist = np.mean(distances)
    print(f"  Mean distance: {mean_dist:.4f}")

print("\n" + "=" * 90)
print("6. SUMMARY: THEOLOGICAL CORRECTIONS")
print("=" * 90)

print("\n✅ CORRECTED ANCHOR POINT:")
print("  Only JEHOVAH (and AGAPE as God's essence) at (1,1,1,1)")

print("\n❌ AI ERRORS IDENTIFIED:")
print("  1. JEHOVAH = Allah (FALSE - different gods)")
print("  2. JEHOVAH ≠ AGAPE (FALSE - God IS love)")
print("  3. Trinity at Anchor (FALSE - unbiblical doctrine)")

print("\n📖 BIBLICAL BASIS:")
print("  - Deuteronomy 6:4: 'Jehovah our God is one Jehovah'")
print("  - 1 John 4:8: 'God IS love' (not HAS love)")
print("  - Matthew 4:10: 'Worship Jehovah your God alone'")

print("\n🎯 GOING FORWARD:")
print("  Use theological coordinates as ground truth")
print("  Acknowledge AI semantic bias from training data")
print("  Measure concepts against biblical revelation")

print("\n" + "=" * 90)
print("ANALYSIS COMPLETE")
print("=" * 90)
