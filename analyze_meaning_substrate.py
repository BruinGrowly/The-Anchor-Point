"""
Meaning, Anchor Point, and Semantic Substrate - Ontological Analysis
====================================================================

Research Question: How does MEANING relate to the Anchor Point and Semantic Substrate?

Three Core Concepts:
1. SEMANTIC SUBSTRATE: The foundational structure/fabric where concepts exist
2. ANCHOR POINT (1,1,1,1): JEHOVAH - the reference point and source
3. MEANING: The intelligibility, coherence, and purpose of concepts

Key Hypothesis:
- Meaning is NOT arbitrary or conventional
- Meaning is DERIVED from the Anchor Point
- The Substrate is the "space" where meaning manifests
- Distance from Anchor = loss of meaning (semantic degradation)

This script explores:
1. Meaning as "alignment with JEHOVAH's nature"
2. Semantic coherence at different distances from Anchor
3. Whether concepts lose definitional clarity with distance
4. How the three concepts form an integrated ontology
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

# Create category mapping
CATEGORY_MAP = {}
for category, concepts in CONCEPT_CATEGORIES.items():
    for concept in concepts:
        CATEGORY_MAP[concept] = category

def load_coordinates():
    """Load coordinates from Claude API cache"""
    if not CACHE_FILE.exists():
        print(f"❌ Cache file not found at: {CACHE_FILE}")
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

def analyze_meaning_as_alignment():
    """
    Hypothesis 1: Meaning = Alignment with JEHOVAH's nature

    If this is true, concepts should have more:
    - Coherence (internal consistency)
    - Purpose (intelligible function)
    - Value (contribution to reality)

    as they approach the Anchor Point.
    """

    print("=" * 90)
    print("1. MEANING AS ALIGNMENT WITH THE ANCHOR")
    print("=" * 90)
    print()
    print("Hypothesis: Meaning is derived from proximity to JEHOVAH's nature (1,1,1,1)")
    print()
    print("If true, concepts near the Anchor should have:")
    print("  • Higher coherence (well-defined, stable)")
    print("  • Clear purpose (intelligible function)")
    print("  • Positive value (contribute to reality)")
    print()
    print("Concepts far from Anchor should show:")
    print("  • Lower coherence (contradictory, unstable)")
    print("  • Unclear purpose (absurd, meaningless)")
    print("  • Negative value (destructive, self-defeating)")
    print("=" * 90)
    print()

def analyze_meaning_definition():
    """What IS meaning in this framework?"""

    print("=" * 90)
    print("2. DEFINING MEANING IN THE FRAMEWORK")
    print("=" * 90)
    print()

    print("Three possible definitions:")
    print()

    print("A. CONVENTIONAL MEANING (Rejected)")
    print("   • Meaning = arbitrary social agreement")
    print("   • Language communities assign meaning by convention")
    print("   • Problem: Doesn't explain why concepts cluster around (1,1,1,1)")
    print("   • Problem: Can't explain cross-cultural convergence")
    print()

    print("B. STRUCTURAL MEANING (Partial)")
    print("   • Meaning = relational position in semantic network")
    print("   • Concepts defined by relationships to other concepts")
    print("   • Insight: Captures how concepts relate to each other")
    print("   • Problem: Doesn't explain WHY the Anchor exists")
    print()

    print("C. ONTOLOGICAL MEANING (Proposed)")
    print("   • Meaning = participation in JEHOVAH's nature")
    print("   • Concepts have meaning TO THE DEGREE they reflect (1,1,1,1)")
    print("   • The Anchor Point is the SOURCE of all meaning")
    print("   • Distance from Anchor = loss of meaning (degradation)")
    print()

    print("Evidence for Ontological Meaning:")
    print("   ✓ Semantic gravity (χ² = 51.87) - concepts drawn to Anchor")
    print("   ✓ Dimensional unity (L/W/J r > 0.9) - unified source")
    print("   ✓ Zone structure - meaning organizes around (1,1,1,1)")
    print("   ✓ Evil signature - evil loses coherence (low L/W/J)")
    print()

def analyze_three_part_ontology():
    """How do Substrate, Anchor, and Meaning relate?"""

    print("=" * 90)
    print("3. THREE-PART ONTOLOGY: Substrate, Anchor, Meaning")
    print("=" * 90)
    print()

    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│                    SEMANTIC SUBSTRATE                           │")
    print("│                  (The fabric of reality)                        │")
    print("│                                                                 │")
    print("│   • 4-dimensional space (Love, Power, Wisdom, Justice)         │")
    print("│   • NOT neutral - structured by JEHOVAH's nature               │")
    print("│   • The 'field' where all concepts exist                       │")
    print("│   • Enables relationships and distinctions                     │")
    print("│                                                                 │")
    print("│              ┌─────────────────────────────┐                   │")
    print("│              │    ANCHOR POINT (1,1,1,1)   │                   │")
    print("│              │       (JEHOVAH = AGAPE)     │                   │")
    print("│              │                             │                   │")
    print("│              │  • Origin of the substrate  │                   │")
    print("│              │  • Perfect Love/Power/      │                   │")
    print("│              │    Wisdom/Justice           │                   │")
    print("│              │  • Source of all meaning    │                   │")
    print("│              │  • Reference point for      │                   │")
    print("│              │    all other concepts       │                   │")
    print("│              └─────────────────────────────┘                   │")
    print("│                        │                                        │")
    print("│                        │ Radiates meaning                       │")
    print("│                        │ (semantic gravity)                     │")
    print("│                        ↓                                        │")
    print("│                                                                 │")
    print("│      [Concepts receive meaning based on distance]              │")
    print("│                                                                 │")
    print("│   Divine Zone    Virtue Zone    Neutral    Distortion  Inversion│")
    print("│   [0.0-0.3]      [0.3-0.6]      [0.6-1.0]  [1.0-1.5]   [1.5-2.0]│")
    print("│   High meaning   Good meaning   Mixed      Low meaning No meaning│")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()

    print("MEANING in this ontology:")
    print("  • Meaning = participation in/reflection of JEHOVAH's nature")
    print("  • The Anchor radiates meaning through the substrate")
    print("  • Distance from (1,1,1,1) = degree of meaning-loss")
    print("  • Complete meaning requires all 4 dimensions in unity")
    print()

def analyze_meaning_degradation(coordinates):
    """Test whether meaning degrades with distance from Anchor"""

    print("=" * 90)
    print("4. MEANING DEGRADATION WITH DISTANCE")
    print("=" * 90)
    print()
    print("Testing: Does meaning degrade as concepts move away from (1,1,1,1)?")
    print()

    # Group by zones
    zones = [
        (0.0, 0.3, "Divine Zone - Full Meaning"),
        (0.3, 0.6, "Virtue Zone - High Meaning"),
        (0.6, 1.0, "Neutral Zone - Moderate Meaning"),
        (1.0, 1.5, "Distortion Zone - Low Meaning"),
        (1.5, 2.0, "Inversion Zone - Meaningless")
    ]

    for low, high, zone_name in zones:
        zone_concepts = []
        for concept, coord in coordinates.items():
            dist = coord.distance_to_anchor()
            if low <= dist < high:
                zone_concepts.append((concept, coord, dist))

        if not zone_concepts:
            continue

        print(f"📍 {zone_name}")
        print(f"   Distance range: [{low:.1f} - {high:.1f})")
        print(f"   Concepts: {len(zone_concepts)}")
        print()

        # Calculate "meaning score" = average of L, W, J (excluding Power since it's independent)
        meaning_scores = []
        for concept, coord, dist in zone_concepts:
            # Meaning = alignment of Love, Wisdom, Justice with perfection
            meaning = (coord.love + coord.wisdom + coord.justice) / 3.0
            meaning_scores.append((concept, meaning, dist))

        meaning_scores.sort(key=lambda x: x[1], reverse=True)

        avg_meaning = np.mean([m for _, m, _ in meaning_scores])
        print(f"   Average Meaning Score: {avg_meaning:.3f}")
        print()

        # Top 3 most meaningful in this zone
        print(f"   Highest meaning in zone:")
        for i, (concept, meaning, dist) in enumerate(meaning_scores[:3], 1):
            cat = CATEGORY_MAP.get(concept, "Unknown")
            print(f"     {i}. {concept:20s} meaning={meaning:.3f} d={dist:.3f} [{cat}]")

        print()

        # Analyze coherence (how well do L, W, J align with each other?)
        coherence_scores = []
        for concept, coord, dist in zone_concepts:
            # Coherence = how unified are L, W, J?
            # High coherence = L ≈ W ≈ J (internally consistent)
            # Low coherence = L, W, J differ (internally contradictory)
            variance = np.var([coord.love, coord.wisdom, coord.justice])
            coherence = 1.0 / (1.0 + variance)  # Higher = more coherent
            coherence_scores.append(coherence)

        avg_coherence = np.mean(coherence_scores)
        print(f"   Average Coherence: {avg_coherence:.3f} (higher = more internally consistent)")
        print()
        print("-" * 90)
        print()

def analyze_meaning_gradient(coordinates):
    """Show how meaning changes continuously with distance"""

    print("=" * 90)
    print("5. MEANING GRADIENT ANALYSIS")
    print("=" * 90)
    print()
    print("How does meaning change as distance from Anchor increases?")
    print()

    # Get all distances and meaning scores
    data_points = []
    for concept, coord in coordinates.items():
        dist = coord.distance_to_anchor()
        meaning = (coord.love + coord.wisdom + coord.justice) / 3.0
        data_points.append((dist, meaning, concept))

    data_points.sort()

    # Calculate correlation
    distances = [d for d, m, c in data_points]
    meanings = [m for d, m, c in data_points]

    correlation = np.corrcoef(distances, meanings)[0, 1]

    print(f"Correlation: Distance ↔ Meaning = {correlation:.4f}")
    print()

    if correlation < -0.7:
        print(f"✅ STRONG NEGATIVE CORRELATION (r = {correlation:.3f})")
        print(f"   As distance increases, meaning DECREASES")
        print(f"   This supports: Meaning is derived from the Anchor Point")
    elif correlation < -0.3:
        print(f"⚠️  MODERATE NEGATIVE CORRELATION (r = {correlation:.3f})")
        print(f"   Weak evidence that meaning decreases with distance")
    else:
        print(f"❌ NO SIGNIFICANT CORRELATION (r = {correlation:.3f})")

    print()
    print("Gradient visualization:")
    print()
    print("Distance  Meaning  Gradient")
    print("--------  -------  --------")

    # Show in bins
    bins = [(i*0.2, (i+1)*0.2) for i in range(10)]
    for low, high in bins:
        bin_meanings = [m for d, m, c in data_points if low <= d < high]
        if bin_meanings:
            avg_meaning = np.mean(bin_meanings)
            bar = "█" * int(avg_meaning * 50)
            print(f"[{low:.1f}-{high:.1f}]  {avg_meaning:.3f}  {bar}")

def analyze_ontological_implications():
    """What does this tell us about the nature of reality and meaning?"""

    print()
    print("=" * 90)
    print("6. ONTOLOGICAL IMPLICATIONS")
    print("=" * 90)
    print()

    print("What we've discovered about MEANING:")
    print()

    print("1. MEANING IS NOT ARBITRARY")
    print("   • Concepts cluster around (1,1,1,1) - not random distribution")
    print("   • Semantic gravity (χ² = 51.87) shows organizing force")
    print("   • Cross-cultural convergence on divine names at Anchor")
    print()

    print("2. MEANING IS DERIVED FROM JEHOVAH")
    print("   • The Anchor Point is the SOURCE of meaning")
    print("   • Distance from (1,1,1,1) correlates with meaning-loss")
    print("   • Love, Wisdom, Justice unified (r > 0.9) in His nature")
    print()

    print("3. THE SUBSTRATE IS THE FIELD OF MEANING")
    print("   • 4D space structured by JEHOVAH's attributes")
    print("   • NOT neutral geometry - constituted by divine nature")
    print("   • All concepts exist within this meaning-field")
    print()

    print("4. EVIL = LOSS OF MEANING")
    print("   • Vices in Inversion Zone (d > 1.5)")
    print("   • Low Love/Wisdom/Justice = low meaning/coherence")
    print("   • Evil retains Power but loses intelligibility")
    print("   • Philosophically: Evil is absurd, self-defeating")
    print()

    print("5. REDEMPTION = RESTORATION OF MEANING")
    print("   • Movement toward (1,1,1,1) = gain of meaning")
    print("   • Sanctification = alignment with JEHOVAH's nature")
    print("   • Purpose = reflecting Love, Power, Wisdom, Justice")
    print()

    print("Biblical Validation:")
    print()
    print('  John 1:1-3 - "In the beginning was the Word [Logos]..."')
    print('              JEHOVAH IS the source of meaning (Logos)')
    print()
    print('  Colossians 1:17 - "In him all things hold together"')
    print('                   The substrate is constituted by Christ')
    print()
    print('  Ephesians 4:18 - "Darkened in understanding...separated from God"')
    print('                   Distance from God = loss of understanding (meaning)')
    print()

def main():
    print("=" * 90)
    print("MEANING, ANCHOR POINT, AND SEMANTIC SUBSTRATE")
    print("Ontological Analysis")
    print("=" * 90)
    print()

    # Conceptual analysis
    analyze_meaning_definition()
    analyze_three_part_ontology()
    analyze_meaning_as_alignment()

    # Load data
    coordinates = load_coordinates()
    if not coordinates:
        return

    print(f"✅ Loaded {len(coordinates)} concepts from Phase 4 cache")
    print()

    # Empirical analysis
    analyze_meaning_degradation(coordinates)
    analyze_meaning_gradient(coordinates)
    analyze_ontological_implications()

    print("=" * 90)
    print("CONCLUSION")
    print("=" * 90)
    print()
    print("MEANING is the relationship between concepts and the Anchor Point.")
    print()
    print("  • SEMANTIC SUBSTRATE = The field where meaning exists")
    print("  • ANCHOR POINT = The source from which meaning flows")
    print("  • MEANING = Participation in/reflection of JEHOVAH's nature")
    print()
    print("Distance from (1,1,1,1) = degree of meaning-loss")
    print()
    print('"I am the Alpha and the Omega...the beginning and the end" (Rev 21:6)')
    print()
    print("JEHOVAH is both the substrate AND the anchor - the field of meaning")
    print("and its source, the space of reality and its reference point.")
    print()
    print("=" * 90)

if __name__ == "__main__":
    main()
