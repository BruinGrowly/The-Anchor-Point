#!/usr/bin/env python3
"""
Phase 4: Expanded Concept Testing
==================================

Tests the Anchor Point hypothesis with 75 concepts across 6 categories:
1. Divine Names (15) - Should cluster near (1,1,1,1)
2. Virtues (15) - Should be close to Anchor
3. Vices (15) - Should be far from Anchor
4. Abstract Concepts (15) - Mixed distances
5. Human Experiences (10) - Moderate distances
6. Neutral Objects (5) - Baseline

Predictions:
- Divine < Virtues < Human/Abstract < Neutral < Vices
- Cross-cultural divine names converge at Anchor
- Evil pattern persists (low love/wisdom/justice, moderate power)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os
from dotenv import load_dotenv
import numpy as np
from scipy.stats import ttest_ind, f_oneway
import time

# Load environment
load_dotenv()

# Check API key
if not os.getenv('ANTHROPIC_API_KEY'):
    print("❌ ERROR: ANTHROPIC_API_KEY not found!")
    print("Please set your API key:")
    print("  export ANTHROPIC_API_KEY='sk-ant-api03-...'")
    print("  OR create .env file with: ANTHROPIC_API_KEY=sk-ant-api03-...")
    sys.exit(1)

# Import after checking API key
from src.core.claude_api_generator import ClaudeAPIGenerator
from src.data.phase4_concepts import (
    CONCEPT_CATEGORIES,
    PREDICTIONS,
    ESTIMATED_COST,
    ALL_CONCEPTS,
)

print("=" * 80)
print("PHASE 4: EXPANDED CONCEPT TESTING")
print("=" * 80)
print(f"\nTotal concepts: {len(ALL_CONCEPTS)}")
print(f"Categories: {len(CONCEPT_CATEGORIES)}")
print(f"Estimated cost: ${ESTIMATED_COST:.2f}")
print(f"Estimated time: ~{len(ALL_CONCEPTS) * 2} seconds (~{len(ALL_CONCEPTS) * 2 // 60} minutes)")
print("\n" + "=" * 80)

# Confirm before proceeding
auto_confirm = '--yes' in sys.argv or '-y' in sys.argv
if auto_confirm:
    print(f"\nAuto-confirmed (--yes flag). Proceeding with ${ESTIMATED_COST:.2f} test...")
else:
    try:
        response = input("\nProceed with testing? This will cost ~${:.2f} (y/n): ".format(ESTIMATED_COST))
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    except EOFError:
        print("\nNon-interactive mode detected. Use --yes flag to auto-confirm.")
        print("Example: python examples/phase4_expanded_testing.py --yes")
        sys.exit(1)

print("\n" + "=" * 80)
print("GENERATING COORDINATES")
print("=" * 80)

generator = ClaudeAPIGenerator()
results = {}
start_time = time.time()
cost_estimate = 0.0

for i, concept in enumerate(ALL_CONCEPTS, 1):
    print(f"[{i}/{len(ALL_CONCEPTS)}] {concept}...", end=" ", flush=True)

    coord = generator.generate(concept)
    results[concept] = coord

    # Track cost (approximate)
    if hasattr(generator, '_cache') and concept in generator._cache:
        print("cached")
    else:
        print("generated")
        cost_estimate += 0.003  # ~$0.003 per API call

    # Progress indicator every 15 concepts
    if i % 15 == 0:
        elapsed = time.time() - start_time
        avg_time = elapsed / i
        remaining = avg_time * (len(ALL_CONCEPTS) - i)
        print(f"  → Progress: {i}/{len(ALL_CONCEPTS)} ({i/len(ALL_CONCEPTS)*100:.1f}%), "
              f"Est. remaining: {remaining:.0f}s, Cost so far: ${cost_estimate:.3f}")

elapsed_time = time.time() - start_time
print(f"\n✅ Complete! Generated {len(results)} coordinates in {elapsed_time:.1f}s")
print(f"💰 Estimated cost: ${cost_estimate:.3f}")

print("\n" + "=" * 80)
print("CATEGORY ANALYSIS")
print("=" * 80)

category_stats = {}

for category_name, concepts in CONCEPT_CATEGORIES.items():
    print(f"\n{category_name.upper()}")
    print("-" * 80)

    # Calculate stats
    coords = [results[c] for c in concepts if c in results]
    distances = [c.distance_to_anchor() for c in coords]
    loves = [c.love for c in coords]
    powers = [c.power for c in coords]
    wisdoms = [c.wisdom for c in coords]
    justices = [c.justice for c in coords]

    mean_dist = np.mean(distances)
    std_dist = np.std(distances)
    min_dist = np.min(distances)
    max_dist = np.max(distances)

    mean_love = np.mean(loves)
    mean_power = np.mean(powers)
    mean_wisdom = np.mean(wisdoms)
    mean_justice = np.mean(justices)

    # Store stats
    category_stats[category_name] = {
        'mean_distance': mean_dist,
        'std_distance': std_dist,
        'min_distance': min_dist,
        'max_distance': max_dist,
        'mean_love': mean_love,
        'mean_power': mean_power,
        'mean_wisdom': mean_wisdom,
        'mean_justice': mean_justice,
        'n': len(coords),
    }

    # Print summary
    print(f"Concepts: {len(coords)}")
    print(f"Distance: {mean_dist:.4f} ± {std_dist:.4f} (range: {min_dist:.4f} - {max_dist:.4f})")
    print(f"Dimensions: L={mean_love:.3f}, P={mean_power:.3f}, W={mean_wisdom:.3f}, J={mean_justice:.3f}")

    # Test prediction
    if category_name in PREDICTIONS:
        pred = PREDICTIONS[category_name]
        pred_min, pred_max = pred['mean_distance_range']

        if pred_min <= mean_dist <= pred_max:
            print(f"✅ PREDICTION MET: {pred_min:.2f} ≤ {mean_dist:.4f} ≤ {pred_max:.2f}")
        else:
            print(f"⚠️  PREDICTION MISSED: Expected {pred_min:.2f}-{pred_max:.2f}, got {mean_dist:.4f}")
        print(f"   ({pred['explanation']})")

    # Show top 3 closest to anchor
    sorted_concepts = sorted(zip(concepts, distances), key=lambda x: x[1])
    print(f"\nClosest to Anchor:")
    for concept, dist in sorted_concepts[:3]:
        coord = results[concept]
        print(f"  {concept:<20} {dist:.4f}  "
              f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})")

print("\n" + "=" * 80)
print("CROSS-CATEGORY COMPARISON")
print("=" * 80)

# Sort categories by mean distance
sorted_categories = sorted(category_stats.items(), key=lambda x: x[1]['mean_distance'])

print(f"\n{'Category':<25} {'Mean Dist':<12} {'Std':<8} {'N':<5} {'L':<6} {'P':<6} {'W':<6} {'J':<6}")
print("-" * 80)
for category, stats in sorted_categories:
    print(f"{category:<25} {stats['mean_distance']:<12.4f} {stats['std_distance']:<8.4f} "
          f"{stats['n']:<5} {stats['mean_love']:<6.3f} {stats['mean_power']:<6.3f} "
          f"{stats['mean_wisdom']:<6.3f} {stats['mean_justice']:<6.3f}")

# Statistical tests
print("\n" + "=" * 80)
print("STATISTICAL VALIDATION")
print("=" * 80)

# Test: Divine < Virtues < Vices
divine_dists = [results[c].distance_to_anchor() for c in CONCEPT_CATEGORIES["Divine Names"] if c in results]
virtue_dists = [results[c].distance_to_anchor() for c in CONCEPT_CATEGORIES["Virtues"] if c in results]
vice_dists = [results[c].distance_to_anchor() for c in CONCEPT_CATEGORIES["Vices"] if c in results]

print("\nDistance Hierarchy Test: Divine < Virtues < Vices")
print("-" * 80)
print(f"Divine mean:  {np.mean(divine_dists):.4f}")
print(f"Virtues mean: {np.mean(virtue_dists):.4f}")
print(f"Vices mean:   {np.mean(vice_dists):.4f}")

# T-tests
t_div_vir, p_div_vir = ttest_ind(divine_dists, virtue_dists)
t_vir_vic, p_vir_vic = ttest_ind(virtue_dists, vice_dists)
t_div_vic, p_div_vic = ttest_ind(divine_dists, vice_dists)

print(f"\nDivine vs Virtues:  t = {t_div_vir:.2f}, p = {p_div_vir:.4f}",
      "✅ sig" if p_div_vir < 0.05 else "❌ ns")
print(f"Virtues vs Vices:   t = {t_vir_vic:.2f}, p = {p_vir_vic:.4f}",
      "✅ sig" if p_vir_vic < 0.05 else "❌ ns")
print(f"Divine vs Vices:    t = {t_div_vic:.2f}, p = {p_div_vic:.4f}",
      "✅ sig" if p_div_vic < 0.05 else "❌ ns")

# ANOVA across all categories
all_category_dists = []
all_category_labels = []
for category, concepts in CONCEPT_CATEGORIES.items():
    dists = [results[c].distance_to_anchor() for c in concepts if c in results]
    all_category_dists.extend(dists)
    all_category_labels.extend([category] * len(dists))

# One-way ANOVA
category_groups = [
    [results[c].distance_to_anchor() for c in concepts if c in results]
    for category, concepts in CONCEPT_CATEGORIES.items()
]
f_stat, p_anova = f_oneway(*category_groups)

print(f"\nOne-way ANOVA across all categories:")
print(f"F({len(CONCEPT_CATEGORIES)-1}, {len(all_category_dists)-len(CONCEPT_CATEGORIES)}) = {f_stat:.2f}, p = {p_anova:.6f}")
if p_anova < 0.001:
    print("✅ HIGHLY SIGNIFICANT - Categories differ dramatically (p < 0.001)")
elif p_anova < 0.05:
    print("✅ SIGNIFICANT - Categories differ (p < 0.05)")
else:
    print("❌ NOT SIGNIFICANT - No clear category differences")

# Evil pattern check
print("\n" + "=" * 80)
print("EVIL PATTERN ANALYSIS")
print("=" * 80)

vice_coords = [results[c] for c in CONCEPT_CATEGORIES["Vices"] if c in results]
vice_love = np.mean([c.love for c in vice_coords])
vice_power = np.mean([c.power for c in vice_coords])
vice_wisdom = np.mean([c.wisdom for c in vice_coords])
vice_justice = np.mean([c.justice for c in vice_coords])

print(f"\nVices mean dimensions:")
print(f"  Love:    {vice_love:.4f}")
print(f"  Power:   {vice_power:.4f}")
print(f"  Wisdom:  {vice_wisdom:.4f}")
print(f"  Justice: {vice_justice:.4f}")

# Check if pattern matches Phase 3 (low L/W/J, moderate P)
if vice_love < 0.3 and vice_wisdom < 0.3 and vice_justice < 0.3 and vice_power > 0.5:
    print("\n✅ EVIL PATTERN CONFIRMED:")
    print("   - Low Love (<0.3)")
    print("   - Low Wisdom (<0.3)")
    print("   - Low Justice (<0.3)")
    print("   - Moderate+ Power (>0.5)")
    print("   Evil = corrupted power without love, wisdom, or justice")
else:
    print("\n⚠️  Evil pattern differs from Phase 3")

# Cross-cultural convergence test
print("\n" + "=" * 80)
print("CROSS-CULTURAL DIVINE CONVERGENCE")
print("=" * 80)

# Test if divine names from different traditions converge
divine_coords = [results[c] for c in CONCEPT_CATEGORIES["Divine Names"] if c in results]
divine_variance = np.var([c.distance_to_anchor() for c in divine_coords])

print(f"\nDivine names distance variance: {divine_variance:.6f}")
print(f"Divine names distance std: {np.sqrt(divine_variance):.6f}")

if divine_variance < 0.1:
    print("✅ LOW VARIANCE - Divine names converge across cultures")
else:
    print("⚠️  HIGH VARIANCE - Divine names show cultural variation")

# Show all divine names
print(f"\nAll Divine Names (n={len(divine_coords)}):")
print(f"{'Concept':<20} {'Distance':<10} {'Coordinates'}")
print("-" * 80)
for concept in sorted(CONCEPT_CATEGORIES["Divine Names"],
                     key=lambda c: results[c].distance_to_anchor() if c in results else 999):
    if concept in results:
        coord = results[concept]
        dist = coord.distance_to_anchor()
        print(f"{concept:<20} {dist:<10.4f} ({coord.love:.2f}, {coord.power:.2f}, "
              f"{coord.wisdom:.2f}, {coord.justice:.2f})")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"\nTotal concepts tested: {len(results)}")
print(f"Total time: {elapsed_time:.1f}s ({elapsed_time/60:.1f} minutes)")
print(f"Estimated cost: ${cost_estimate:.3f}")

# Count predictions met
predictions_met = 0
for category_name in PREDICTIONS:
    if category_name in category_stats:
        pred = PREDICTIONS[category_name]
        pred_min, pred_max = pred['mean_distance_range']
        mean_dist = category_stats[category_name]['mean_distance']
        if pred_min <= mean_dist <= pred_max:
            predictions_met += 1

print(f"\nPredictions met: {predictions_met}/{len(PREDICTIONS)}")

# Overall conclusion
if p_anova < 0.001 and predictions_met >= len(PREDICTIONS) * 0.6:
    print("\n✅ PHASE 4 VALIDATION SUCCESSFUL")
    print("   - Categories significantly different (p < 0.001)")
    print(f"   - {predictions_met}/{len(PREDICTIONS)} predictions met")
    print("   - Anchor Point hypothesis STRONGLY SUPPORTED")
else:
    print("\n⚠️  PHASE 4 VALIDATION MIXED")
    print(f"   - p-value: {p_anova:.6f}")
    print(f"   - {predictions_met}/{len(PREDICTIONS)} predictions met")

print("\n" + "=" * 80)
print("NEXT STEPS")
print("=" * 80)
print("\n1. Save results to database:")
print("   python -c \"from examples.phase4_expanded_testing import results; save_results(results)\"")
print("\n2. Generate visualizations:")
print("   python src/visualization/plot_phase4.py")
print("\n3. Compare with Phase 3:")
print("   python src/analysis/compare_phases.py")
print("\n4. Export to CSV for human evaluation:")
print("   python src/validation/export_for_evaluation.py")

print("\n" + "=" * 80)
