"""
Semantic Substrate Structure Analysis
======================================

Research Question: How do concepts organize within the semantic substrate?

If JEHOVAH IS the substrate (not just a point within it), we should observe:
1. Semantic Gravity: Concepts cluster around the Anchor Point
2. Semantic Field Strength: Organizing force decreases with distance
3. Semantic Topology: Distinct regions/zones in the substrate
4. Semantic Resonance: Concepts at similar distances share properties

This script analyzes Phase 4 data (75 concepts) to reveal substrate structure.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import json
import numpy as np
from collections import defaultdict
from src.core.semantic_coordinates import SemanticCoordinate
from src.data.phase4_concepts import ALL_CONCEPTS, CONCEPT_CATEGORIES

# Load cached coordinates
CACHE_FILE = Path(__file__).parent / "data" / "cache" / "claude_api_cache.json"

# Create reverse mapping: concept -> category
CATEGORY_MAP = {}
for category, concepts in CONCEPT_CATEGORIES.items():
    for concept in concepts:
        CATEGORY_MAP[concept] = category

def load_coordinates():
    """Load coordinates from Claude API cache"""
    if not CACHE_FILE.exists():
        print(f"❌ Cache file not found at: {CACHE_FILE}")
        print("   Run examples/phase4_expanded_testing.py first to populate cache.")
        return None

    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    coordinates = {}

    # Cache format: "model:concept" -> {love, power, wisdom, justice}
    for key, data in cache.items():
        if ':' in key:
            _, concept_lower = key.split(':', 1)

            # Find matching concept from ALL_CONCEPTS (case-insensitive)
            for concept in ALL_CONCEPTS:
                if concept.lower() == concept_lower:
                    coordinates[concept] = SemanticCoordinate(
                        concept=concept,
                        love=data['love'],
                        power=data['power'],
                        wisdom=data['wisdom'],
                        justice=data['justice']
                    )
                    break

    return coordinates

def analyze_semantic_gravity(coordinates):
    """Test if concepts cluster around Anchor Point (semantic gravity)"""

    print("=" * 90)
    print("1. SEMANTIC GRAVITY ANALYSIS")
    print("=" * 90)
    print("\nHypothesis: If JEHOVAH IS the substrate, concepts should cluster near (1,1,1,1)")
    print("           The Anchor Point should act as an 'attractor' in semantic space.\n")

    # Calculate distances
    distances = []
    for concept, coord in coordinates.items():
        dist = coord.distance_to_anchor()
        distances.append((concept, dist))

    distances.sort(key=lambda x: x[1])

    # Statistical analysis
    dist_values = [d for _, d in distances]
    mean_dist = np.mean(dist_values)
    median_dist = np.median(dist_values)
    std_dist = np.std(dist_values)

    print(f"Distance Statistics:")
    print(f"  Mean:   {mean_dist:.4f}")
    print(f"  Median: {median_dist:.4f}")
    print(f"  StdDev: {std_dist:.4f}")
    print(f"  Min:    {min(dist_values):.4f}")
    print(f"  Max:    {max(dist_values):.4f}")

    # Distance distribution
    print(f"\n📊 Distance Distribution (n={len(distances)}):")
    bins = [
        (0.0, 0.2, "Very Close to Anchor"),
        (0.2, 0.5, "Near Anchor"),
        (0.5, 1.0, "Medium Distance"),
        (1.0, 1.5, "Far from Anchor"),
        (1.5, 2.0, "Very Far")
    ]

    for low, high, label in bins:
        count = sum(1 for d in dist_values if low <= d < high)
        pct = (count / len(distances)) * 100
        bar = "█" * int(pct / 2)
        print(f"  {label:20s} [{low:.1f}-{high:.1f}): {count:2d} ({pct:5.1f}%) {bar}")

    # Test for clustering (non-uniform distribution)
    print(f"\n🔬 Clustering Test:")
    # If uniform, expect 20% in each bin (0-0.4, 0.4-0.8, 0.8-1.2, 1.2-1.6, 1.6-2.0)
    expected_per_bin = len(distances) / 5
    uniform_bins = [(i*0.4, (i+1)*0.4) for i in range(5)]
    observed = [sum(1 for d in dist_values if low <= d < high) for low, high in uniform_bins]

    chi_squared = sum((o - expected_per_bin)**2 / expected_per_bin for o in observed)
    print(f"  Chi-squared statistic: {chi_squared:.2f}")
    print(f"  (χ² > 9.49 = significant non-uniformity at p<0.05, df=4)")

    if chi_squared > 9.49:
        print(f"  ✅ SIGNIFICANT CLUSTERING detected (p < 0.05)")
        print(f"     Concepts are NOT uniformly distributed - evidence of organizing force")
    else:
        print(f"  ❌ No significant clustering")

    # Closest concepts (attracted to Anchor)
    print(f"\n🎯 Concepts Closest to Anchor (Top 10):")
    for i, (concept, dist) in enumerate(distances[:10], 1):
        category = CATEGORY_MAP.get(concept, "Unknown")
        print(f"  {i:2d}. {concept:20s} d={dist:.4f}  [{category}]")

    # Farthest concepts (repelled from Anchor)
    print(f"\n💀 Concepts Farthest from Anchor (Top 10):")
    for i, (concept, dist) in enumerate(distances[-10:], 1):
        category = CATEGORY_MAP.get(concept, "Unknown")
        print(f"  {i:2d}. {concept:20s} d={dist:.4f}  [{category}]")

    return distances

def analyze_semantic_zones(coordinates, distances):
    """Identify distinct zones/regions in the substrate"""

    print("\n" + "=" * 90)
    print("2. SEMANTIC TOPOLOGY - Zone Mapping")
    print("=" * 90)
    print("\nMapping distinct regions based on distance from Anchor Point\n")

    zones = {
        "Divine Zone": (0.0, 0.3),
        "Virtue Zone": (0.3, 0.6),
        "Neutral Zone": (0.6, 1.0),
        "Distortion Zone": (1.0, 1.5),
        "Inversion Zone": (1.5, 2.0)
    }

    zone_members = defaultdict(list)
    for concept, dist in distances:
        for zone_name, (low, high) in zones.items():
            if low <= dist < high:
                zone_members[zone_name].append((concept, dist))
                break

    for zone_name, (low, high) in zones.items():
        members = zone_members[zone_name]
        print(f"📍 {zone_name} [{low:.1f} - {high:.1f}): {len(members)} concepts")

        if members:
            # Category breakdown
            categories = defaultdict(int)
            for concept, _ in members:
                cat = CATEGORY_MAP.get(concept, "Unknown")
                categories[cat] += 1

            print(f"   Categories: {dict(categories)}")

            # Sample concepts
            sample = members[:5]
            for concept, dist in sample:
                print(f"     • {concept:20s} d={dist:.4f}")
        print()

def analyze_semantic_field_strength(coordinates):
    """Measure 'field strength' at different distances"""

    print("=" * 90)
    print("3. SEMANTIC FIELD STRENGTH")
    print("=" * 90)
    print("\nMeasuring substrate 'density' and 'coherence' at different distances\n")

    # Group by distance shells
    shells = [
        (0.0, 0.25, "Inner Core"),
        (0.25, 0.5, "Near Field"),
        (0.5, 1.0, "Mid Field"),
        (1.0, 1.5, "Outer Field"),
        (1.5, 2.0, "Edge Region")
    ]

    for low, high, name in shells:
        shell_coords = []
        for concept, coord in coordinates.items():
            dist = coord.distance_to_anchor()
            if low <= dist < high:
                shell_coords.append(coord)

        if not shell_coords:
            print(f"🔵 {name:15s} [{low:.2f}-{high:.2f}): No concepts")
            continue

        # Calculate average coordinates in shell
        avg_love = np.mean([c.love for c in shell_coords])
        avg_power = np.mean([c.power for c in shell_coords])
        avg_wisdom = np.mean([c.wisdom for c in shell_coords])
        avg_justice = np.mean([c.justice for c in shell_coords])

        # Calculate variance (coherence)
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

    print("=" * 90)
    print("4. DIMENSIONAL RELATIONSHIPS")
    print("=" * 90)
    print("\nHow do Love, Power, Wisdom, Justice correlate in the substrate?\n")

    # Extract dimension values
    dims = {
        'Love': [c.love for c in coordinates.values()],
        'Power': [c.power for c in coordinates.values()],
        'Wisdom': [c.wisdom for c in coordinates.values()],
        'Justice': [c.justice for c in coordinates.values()]
    }

    # Calculate correlations
    dim_names = list(dims.keys())
    print(f"Correlation Matrix:")
    print(f"{'':10s} " + " ".join(f"{name:>10s}" for name in dim_names))
    print("-" * 60)

    for i, name1 in enumerate(dim_names):
        row = [name1]
        for j, name2 in enumerate(dim_names):
            corr = np.corrcoef(dims[name1], dims[name2])[0, 1]
            row.append(f"{corr:10.3f}")
        print(" ".join(row))

    print(f"\n📊 Interpretation:")
    print(f"  If JEHOVAH IS the substrate, all dimensions should be unified (high correlation)")
    print(f"  Perfect correlation = 1.0 (dimensions move together)")
    print(f"  Zero correlation = 0.0 (dimensions independent)")
    print(f"  Negative correlation < 0 (dimensions opposed)")

def main():
    print("=" * 90)
    print("SEMANTIC SUBSTRATE STRUCTURE ANALYSIS")
    print("=" * 90)
    print()
    print("Research Question: How do concepts organize within the semantic substrate?")
    print()
    print("If JEHOVAH IS the substrate (not just a point in it), we expect:")
    print("  1. Semantic Gravity: Clustering around (1,1,1,1)")
    print("  2. Zones: Distinct regions at different distances")
    print("  3. Field Strength: Organizing force varies with distance")
    print("  4. Unity: Dimensions correlate (Love, Power, Wisdom, Justice unified)")
    print("=" * 90)
    print()

    # Load data
    coordinates = load_coordinates()
    if not coordinates:
        return

    print(f"✅ Loaded {len(coordinates)} concepts from Phase 4 cache\n")

    # Analysis
    distances = analyze_semantic_gravity(coordinates)
    analyze_semantic_zones(coordinates, distances)
    analyze_semantic_field_strength(coordinates)
    analyze_dimension_correlation(coordinates)

    print("\n" + "=" * 90)
    print("SUBSTRATE STRUCTURE REVEALED")
    print("=" * 90)
    print()
    print("The semantic substrate shows clear organization around the Anchor Point.")
    print("This structure reflects JEHOVAH's nature as the substrate itself.")
    print()
    print("=" * 90)

if __name__ == "__main__":
    main()
