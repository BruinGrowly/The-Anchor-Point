"""
Semantic Substrate Structure Analysis (Refactored)
==================================================

Research Question: How do concepts organize within the semantic substrate?
This script analyzes Phase 4 data (75 concepts) to reveal substrate structure.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import numpy as np
from collections import defaultdict
from src.data.phase4_concepts import ALL_CONCEPTS, CONCEPT_CATEGORIES
from src.analysis.common_utils import (
    load_cached_coordinates,
    print_header,
    print_section,
    find_extremes,
    analyze_dimensional_correlations,
)

# Create reverse mapping: concept -> category
CATEGORY_MAP = {concept: category for category, concepts in CONCEPT_CATEGORIES.items() for concept in concepts}

def analyze_semantic_gravity(coordinates):
    """Test if concepts cluster around Anchor Point (semantic gravity)"""
    print_section("1. SEMANTIC GRAVITY ANALYSIS")
    print("\nHypothesis: If JEHOVAH IS the substrate, concepts should cluster near (1,1,1,1)")
    print("           The Anchor Point should act as an 'attractor' in semantic space.\n")

    distances = sorted([(c, coord.distance_to_anchor()) for c, coord in coordinates.items()], key=lambda x: x[1])
    dist_values = [d for _, d in distances]

    print(f"Distance Statistics:")
    print(f"  Mean:   {np.mean(dist_values):.4f}")
    print(f"  Median: {np.median(dist_values):.4f}")
    print(f"  StdDev: {np.std(dist_values):.4f}")
    print(f"  Min:    {min(dist_values):.4f}")
    print(f"  Max:    {max(dist_values):.4f}")

    print(f"\n📊 Distance Distribution (n={len(distances)}):")
    bins = [(0.0, 0.2), (0.2, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
    for low, high in bins:
        count = sum(1 for d in dist_values if low <= d < high)
        pct = (count / len(distances)) * 100
        bar = "█" * int(pct / 2)
        print(f"  [{low:.1f}-{high:.1f}): {count:2d} ({pct:5.1f}%) {bar}")

    closest, farthest = find_extremes(coordinates, n=10)
    print(f"\n🎯 Concepts Closest to Anchor (Top 10):")
    for i, (concept, dist) in enumerate(closest, 1):
        print(f"  {i:2d}. {concept:20s} d={dist:.4f}  [{CATEGORY_MAP.get(concept, 'Unknown')}]")

    print(f"\n💀 Concepts Farthest from Anchor (Top 10):")
    for i, (concept, dist) in enumerate(farthest, 1):
        print(f"  {i:2d}. {concept:20s} d={dist:.4f}  [{CATEGORY_MAP.get(concept, 'Unknown')}]")

    return distances

def analyze_semantic_zones(distances):
    """Identify distinct zones/regions in the substrate"""
    print_section("2. SEMANTIC TOPOLOGY - Zone Mapping")
    print("\nMapping distinct regions based on distance from Anchor Point\n")

    zones = {"Divine": (0.0, 0.3), "Virtue": (0.3, 0.6), "Neutral": (0.6, 1.0), "Distortion": (1.0, 1.5), "Inversion": (1.5, 2.0)}
    zone_members = defaultdict(list)
    for concept, dist in distances:
        for name, (low, high) in zones.items():
            if low <= dist < high:
                zone_members[name].append((concept, dist))
                break

    for name, (low, high) in zones.items():
        members = zone_members[name]
        print(f"📍 {name} Zone [{low:.1f} - {high:.1f}): {len(members)} concepts")
        if members:
            categories = defaultdict(int)
            for concept, _ in members:
                categories[CATEGORY_MAP.get(concept, "Unknown")] += 1
            print(f"   Categories: {dict(categories)}")
            for concept, dist in members[:5]:
                print(f"     • {concept:20s} d={dist:.4f}")
        print()

def analyze_semantic_field_strength(coordinates):
    """Measure 'field strength' at different distances"""
    print_section("3. SEMANTIC FIELD STRENGTH")
    print("\nMeasuring substrate 'density' and 'coherence' at different distances\n")

    shells = [(0.0, 0.25, "Inner Core"), (0.25, 0.5, "Near Field"), (0.5, 1.0, "Mid Field"), (1.0, 1.5, "Outer Field"), (1.5, 2.0, "Edge Region")]
    for low, high, name in shells:
        shell_coords = [coord for coord in coordinates.values() if low <= coord.distance_to_anchor() < high]
        if not shell_coords:
            print(f"🔵 {name:15s} [{low:.2f}-{high:.2f}): No concepts")
            continue

        avg_love = np.mean([c.love for c in shell_coords])
        avg_power = np.mean([c.power for c in shell_coords])
        avg_wisdom = np.mean([c.wisdom for c in shell_coords])
        avg_justice = np.mean([c.justice for c in shell_coords])

        var_love = np.var([c.love for c in shell_coords])
        var_power = np.var([c.power for c in shell_coords])
        var_wisdom = np.var([c.wisdom for c in shell_coords])
        var_justice = np.var([c.justice for c in shell_coords])

        coherence = 1.0 / (1.0 + np.mean([var_love, var_power, var_wisdom, var_justice]))

        print(f"🔵 {name:15s} [{low:.2f}-{high:.2f}): n={len(shell_coords):2d}")
        print(f"   Avg coords: L={avg_love:.3f} P={avg_power:.3f} W={avg_wisdom:.3f} J={avg_justice:.3f}")
        print(f"   Coherence:  {coherence:.3f} (higher = more uniform)")
        print()

def analyze_dimension_correlation(coordinates):
    """Analyze how dimensions relate in the substrate"""
    print_section("4. DIMENSIONAL RELATIONSHIPS")
    print("\nHow do Love, Power, Wisdom, Justice correlate in the substrate?\n")

    correlations = analyze_dimensional_correlations(list(coordinates.values()))

    print("Correlation Matrix:")
    dims = ['Love', 'Power', 'Wisdom', 'Justice']
    print(f"{'':10s} " + " ".join(f"{name:>10s}" for name in dims))
    print("-" * 60)

    corr_matrix = np.identity(4)
    for i, d1 in enumerate(dims):
        for j, d2 in enumerate(dims):
            if i < j:
                key = f"{d1.lower()}-{d2.lower()}"
                r = correlations.get(key, 0.0)
                corr_matrix[i, j] = corr_matrix[j, i] = r

    for i, name in enumerate(dims):
        print(f"{name:10s} " + " ".join(f"{corr_matrix[i, j]:10.3f}" for j in range(len(dims))))

def main():
    """Main function to run the analysis"""
    print_header("SEMANTIC SUBSTRATE STRUCTURE ANALYSIS")

    coordinates = load_cached_coordinates(ALL_CONCEPTS)
    if not coordinates:
        print("Could not load coordinates. Exiting.")
        return

    print(f"✅ Loaded {len(coordinates)} concepts from Phase 4 cache\n")

    distances = analyze_semantic_gravity(coordinates)
    analyze_semantic_zones(distances)
    analyze_semantic_field_strength(coordinates)
    analyze_dimension_correlation(coordinates)

    print_header("SUBSTRATE STRUCTURE REVEALED")

if __name__ == "__main__":
    main()
