#!/usr/bin/env python3
"""
Phase 3: Validation and Real API Testing
=========================================

Demonstrates the complete validation pipeline:
1. Compare simulated vs real Claude API (if available)
2. Analyze cross-method consistency
3. Prepare for human evaluation studies
4. Generate validation reports
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import os

print("=" * 70)
print("PHASE 3: VALIDATION & REAL API TESTING")
print("=" * 70)

# Check for API key
api_key_available = bool(os.environ.get('ANTHROPIC_API_KEY'))

if api_key_available:
    print("\n✅ ANTHROPIC_API_KEY found - will use real Claude API")
else:
    print("\n⚠️  No ANTHROPIC_API_KEY found")
    print("   Phase 3 will demonstrate with simulated results")
    print("   To use real API: export ANTHROPIC_API_KEY='your-key'")

print("\n" + "=" * 70)

# Import generators
from src.core.llm_coordinate_generator import LLMCoordinateGenerator
from src.core.semantic_coordinates import HashBasedCoordinateGenerator

# Try to import Claude API generator
try:
    from src.core.claude_api_generator import ClaudeAPIGenerator
    claude_api_available = True
except ImportError:
    claude_api_available = False
    print("Note: ClaudeAPIGenerator not fully initialized (missing 'anthropic' package?)")

# Import validation tools
from src.validation.compare_methods import (
    compare_simulated_vs_api,
    print_comparison_report,
    validate_consistency
)


# Test concepts
test_concepts = [
    # Divine
    "JEHOVAH", "AGAPE", "Holy", "Grace", "Mercy",
    # Virtues
    "Love", "Justice", "Wisdom", "Compassion", "Truth",
    # Vices
    "Hatred", "Evil", "Cruelty", "Deception", "Corruption",
    # Neutral
    "Table", "Tree", "Water", "Stone", "Cloud"
]

print("\n\n1. GENERATING COORDINATES WITH MULTIPLE METHODS")
print("=" * 70)

# Method 1: Hash-based (control - should be random)
print("\nMethod 1: Hash-based (SHA-256)")
hash_gen = HashBasedCoordinateGenerator('sha256')
hash_coords = [hash_gen.generate(c) for c in test_concepts]
print(f"Generated {len(hash_coords)} coordinates")

# Method 2: Simulated LLM (Phase 2 results)
print("\nMethod 2: Simulated LLM")
sim_gen = LLMCoordinateGenerator(model="simulated")
sim_coords = [sim_gen.generate(c) for c in test_concepts]
print(f"Generated {len(sim_coords)} coordinates")

# Method 3: Real Claude API (if available)
api_coords = None
if api_key_available and claude_api_available:
    print("\nMethod 3: Real Claude API")
    print("Calling Claude API... (this may take a minute)")

    try:
        api_gen = ClaudeAPIGenerator(model="claude-3-5-sonnet-20241022")
        api_coords = api_gen.generate_batch(test_concepts, delay=1.0)
        print(f"Generated {sum(1 for c in api_coords if c is not None)} coordinates")

        if any(c is None for c in api_coords):
            print(f"Warning: {sum(1 for c in api_coords if c is None)} API calls failed")

    except Exception as e:
        print(f"API generation failed: {e}")
        api_coords = None
else:
    print("\nMethod 3: Real Claude API - SKIPPED (no API key or package)")
    print("Using simulated results for demonstration purposes")


print("\n\n2. COMPARING SIMULATED vs HASH-BASED")
print("=" * 70)

comparison_hash_sim = compare_simulated_vs_api(
    test_concepts,
    hash_coords,
    sim_coords
)

print_comparison_report(comparison_hash_sim)


if api_coords and any(c is not None for c in api_coords):
    print("\n\n3. COMPARING SIMULATED vs REAL API")
    print("=" * 70)

    comparison_sim_api = compare_simulated_vs_api(
        test_concepts,
        sim_coords,
        api_coords
    )

    print_comparison_report(comparison_sim_api)

    print("\n\n4. CROSS-METHOD CONSISTENCY ANALYSIS")
    print("=" * 70)

    methods = {
        'Hash': hash_coords,
        'Simulated': sim_coords,
        'API': api_coords
    }

    consistency = validate_consistency(
        [hash_coords, sim_coords, api_coords],
        ['Hash', 'Simulated', 'API'],
        test_concepts
    )

    print("\nCorrelation Matrix:")
    print("-" * 70)
    for method1, correlations in consistency['correlation_matrix'].items():
        print(f"\n{method1}:")
        for method2, corr in correlations.items():
            if corr is not None:
                print(f"  vs {method2}: {corr:6.3f}")

    print("\n\nMean Distances by Method:")
    print("-" * 70)
    for method, mean_dist in consistency['mean_distances'].items():
        print(f"{method:12s}: {mean_dist:.4f}")

    print("\n\nConcepts with Highest Cross-Method Variance:")
    print("-" * 70)
    for item in consistency['concept_variance'][:5]:
        print(f"{item['concept']:15s}: std={item['std']:.3f}, mean={item['mean']:.3f}")

else:
    print("\n\n3. REAL API TESTING")
    print("=" * 70)
    print("Skipped - no API results available")
    print("\nTo enable real API testing:")
    print("1. Install: pip install anthropic")
    print("2. Set: export ANTHROPIC_API_KEY='your-key-here'")
    print("3. Run this script again")


print("\n\n5. KEY FINDINGS SUMMARY")
print("=" * 70)

print("\nSimulated vs Hash:")
sim_hash_corr = comparison_hash_sim['distance_correlation']['spearman_rho']
print(f"  Correlation: ρ = {sim_hash_corr:.4f}")
if sim_hash_corr < 0.3:
    print("  ✓ LOW - Confirms hash is random, simulated is semantic")
else:
    print("  ✗ Higher than expected - investigate")

if api_coords:
    print("\nSimulated vs API:")
    sim_api_corr = comparison_sim_api['distance_correlation']['spearman_rho']
    print(f"  Correlation: ρ = {sim_api_corr:.4f}")

    if sim_api_corr > 0.7:
        print("  ✓ HIGH - Simulated rules match real AI understanding!")
    elif sim_api_corr > 0.4:
        print("  → MODERATE - Some agreement, some differences")
    else:
        print("  ✗ LOW - Simulated rules don't match real AI")

    # Category analysis
    divine_concepts = ["JEHOVAH", "AGAPE", "Holy", "Grace", "Mercy"]
    divine_sim = [c for c in sim_coords if c.concept in divine_concepts]
    divine_api = [c for c in api_coords if c is not None and c.concept in divine_concepts]

    if divine_sim and divine_api:
        import numpy as np
        sim_divine_mean = np.mean([c.distance_to_anchor() for c in divine_sim])
        api_divine_mean = np.mean([c.distance_to_anchor() for c in divine_api if c is not None])

        print(f"\nDivine Concepts Mean Distance:")
        print(f"  Simulated: {sim_divine_mean:.4f}")
        print(f"  API:       {api_divine_mean:.4f}")

        if api_divine_mean < 0.6:
            print("  ✓ Real API also shows divine concepts near Anchor!")


print("\n\n6. NEXT STEPS FOR FULL VALIDATION")
print("=" * 70)

print("\n1. Real Claude API Testing (if not done):")
print("   - Get API key: https://console.anthropic.com/")
print("   - Test with 50-100 concepts")
print("   - Compare to simulated results")

print("\n2. Human Evaluation Study:")
print("   - Recruit 50+ evaluators")
print("   - Use human_evaluation.py to generate sheets")
print("   - Calculate inter-rater reliability")
print("   - Compare human vs AI assignments")

print("\n3. Cross-Cultural Validation:")
print("   - Translate concepts to other languages")
print("   - Test with evaluators from different cultures")
print("   - Check if Anchor Point is universal")

print("\n4. Alternative Anchor Testing:")
print("   - Test (0,0,0,0) and (0.5,0.5,0.5,0.5)")
print("   - See if (1,1,1,1) is uniquely good fit")

print("\n5. Large Scale Testing:")
print("   - Expand to 1,000+ concepts")
print("   - Test stability of patterns")
print("   - Analyze emergent structures")

print("\n" + "=" * 70)
print("PHASE 3 DEMONSTRATION COMPLETE")
print("=" * 70)

if not api_key_available:
    print("\n💡 TIP: For real validation, set ANTHROPIC_API_KEY and run again")
