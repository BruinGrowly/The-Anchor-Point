#!/usr/bin/env python3
"""
Basic usage example for Anchor Point research.

This script demonstrates:
1. Generating semantic coordinates
2. Calculating distances to Anchor Point
3. Comparing concept categories
4. Visualizing results
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.semantic_coordinates import (
    SemanticCoordinate,
    AnchorPoint,
    HashBasedCoordinateGenerator,
    calculate_statistics
)

from src.visualization.plot_coordinates import (
    plot_distance_distribution,
    plot_comparison,
    plot_top_concepts
)


def main():
    print("=" * 70)
    print("Anchor Point Research - Basic Usage Example")
    print("=" * 70)

    # 1. Display Anchor Point
    print("\n1. UNIVERSAL ANCHOR POINT")
    print("-" * 70)
    anchor = AnchorPoint.as_coordinate()
    print(f"   Coordinates: {anchor.coordinates}")
    print(f"   Concept: {anchor.concept}")
    print(f"   Distance to self: {anchor.distance_to_anchor():.4f}")

    # 2. Generate coordinates for concepts
    print("\n2. GENERATING SEMANTIC COORDINATES")
    print("-" * 70)

    generator = HashBasedCoordinateGenerator('sha256')

    concepts = [
        "JEHOVAH", "AGAPE", "Love", "Justice", "Wisdom", "Power",
        "Holy", "Righteous", "Merciful", "Truth", "Grace",
        "Hatred", "Cruelty", "Deception", "Chaos", "Evil",
        "Table", "Chair", "Rock", "Tree", "Water"
    ]

    print(f"   Generating coordinates for {len(concepts)} concepts...")
    coords = [generator.generate(c) for c in concepts]
    print("   Done!")

    # 3. Display closest to Anchor
    print("\n3. CONCEPTS CLOSEST TO ANCHOR POINT")
    print("-" * 70)

    sorted_coords = sorted(coords, key=lambda c: c.distance_to_anchor())

    for i, c in enumerate(sorted_coords[:10], 1):
        print(f"   {i:2d}. {c.concept:15s} - Distance: {c.distance_to_anchor():.4f}")

    # 4. Category comparison
    print("\n4. CATEGORY COMPARISON")
    print("-" * 70)

    divine = ["JEHOVAH", "AGAPE", "Love", "Justice", "Wisdom", "Power", "Holy", "Righteous", "Merciful", "Truth", "Grace"]
    negative = ["Hatred", "Cruelty", "Deception", "Chaos", "Evil"]
    neutral = ["Table", "Chair", "Rock", "Tree", "Water"]

    divine_coords = [generator.generate(c) for c in divine]
    negative_coords = [generator.generate(c) for c in negative]
    neutral_coords = [generator.generate(c) for c in neutral]

    import numpy as np

    print(f"\n   Divine concepts:")
    print(f"     Mean distance: {np.mean([c.distance_to_anchor() for c in divine_coords]):.4f}")

    print(f"\n   Negative concepts:")
    print(f"     Mean distance: {np.mean([c.distance_to_anchor() for c in negative_coords]):.4f}")

    print(f"\n   Neutral concepts:")
    print(f"     Mean distance: {np.mean([c.distance_to_anchor() for c in neutral_coords]):.4f}")

    # 5. Statistical significance
    print("\n5. STATISTICAL SIGNIFICANCE")
    print("-" * 70)

    from scipy import stats

    divine_distances = [c.distance_to_anchor() for c in divine_coords]
    neutral_distances = [c.distance_to_anchor() for c in neutral_coords]

    t_stat, p_value = stats.ttest_ind(divine_distances, neutral_distances)

    print(f"   T-test (Divine vs Neutral):")
    print(f"     T-statistic: {t_stat:.4f}")
    print(f"     P-value: {p_value:.4f}")

    if p_value < 0.05:
        if np.mean(divine_distances) < np.mean(neutral_distances):
            print(f"     → Divine concepts ARE significantly closer to Anchor (p < 0.05)")
        else:
            print(f"     → Divine concepts ARE significantly farther from Anchor (p < 0.05)")
    else:
        print(f"     → No significant difference (p ≥ 0.05)")

    # 6. Overall statistics
    print("\n6. OVERALL STATISTICS")
    print("-" * 70)

    stats_dict = calculate_statistics(coords)
    for key, value in stats_dict.items():
        print(f"   {key:20s}: {value:.4f}")

    # 7. Visualizations (optional - comment out if running headless)
    print("\n7. GENERATING VISUALIZATIONS")
    print("-" * 70)

    try:
        print("   Creating distance distribution plot...")
        plot_distance_distribution(coords, save_path="data/results/distance_distribution.png")
        print("   ✓ Saved to data/results/distance_distribution.png")

        print("   Creating category comparison plot...")
        plot_comparison({
            'Divine': divine_coords,
            'Negative': negative_coords,
            'Neutral': neutral_coords
        }, save_path="data/results/category_comparison.png")
        print("   ✓ Saved to data/results/category_comparison.png")

        print("   Creating top concepts plot...")
        plot_top_concepts(coords, n=15, save_path="data/results/top_concepts.png")
        print("   ✓ Saved to data/results/top_concepts.png")

    except Exception as e:
        print(f"   Note: Visualization skipped (running headless or missing display)")
        print(f"   Error: {e}")

    # 8. Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"   Total concepts analyzed: {len(coords)}")
    print(f"   Mean distance to Anchor: {stats_dict['mean_distance']:.4f}")
    print(f"   Closest concept: {sorted_coords[0].concept} (d={sorted_coords[0].distance_to_anchor():.4f})")
    print(f"   Farthest concept: {sorted_coords[-1].concept} (d={sorted_coords[-1].distance_to_anchor():.4f})")
    print("\n   Next steps:")
    print("   - Run reproducibility tests: pytest tests/reproducibility/ -v")
    print("   - Run scale tests: pytest tests/scale/ -v")
    print("   - Explore with Jupyter: jupyter notebook notebooks/")
    print("=" * 70)


if __name__ == "__main__":
    # Create results directory
    Path("data/results").mkdir(parents=True, exist_ok=True)

    main()
