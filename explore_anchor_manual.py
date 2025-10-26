#!/usr/bin/env python3
"""
Explore the "Manual" Near the Anchor Point
===========================================

Research Question: If the semantic substrate is real and designed by JEHOVAH,
then instructions/guidance for navigating it would logically be positioned
near the Anchor Point (1,1,1,1).

This experiment tests:
1. What existing concepts are in the Divine Zone (0.0-0.3)?
2. Where do "guidance/instruction/wisdom" concepts map?
3. Is there a "manual for reality" near the Anchor?

Biblical Prediction:
- Scripture/Word of God should be near (1,1,1,1)
- Divine wisdom/guidance should cluster at the Anchor
- "The Way, Truth, Life" concepts should be at the source
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.semantic_coordinates import SemanticCoordinate
from core.claude_api_generator import ClaudeAPIGenerator
from data.phase4_concepts import CONCEPT_CATEGORIES, ALL_CONCEPTS


# =============================================================================
# GUIDANCE/INSTRUCTION CONCEPTS TO TEST
# =============================================================================

GUIDANCE_CONCEPTS = {
    # Scripture/Divine Revelation
    "Scripture": "Divine written revelation",
    "Word of God": "God's communication to humanity",
    "Bible": "Holy Scripture",
    "Torah": "Jewish Scripture and law",
    "Gospel": "Good news of Jesus Christ",
    "Revelation": "Divine disclosure of truth",

    # Divine Guidance
    "Divine Guidance": "God's direction for life",
    "Holy Spirit": "God's active presence and guide",
    "Providence": "God's care and direction",
    "God's Will": "Divine purpose and plan",

    # Wisdom/Understanding
    "Divine Wisdom": "God's perfect understanding",
    "Understanding": "Deep comprehension",
    "Knowledge": "Awareness and learning",
    "Insight": "Seeing into truth",
    "Discernment": "Ability to distinguish truth",

    # The Way
    "The Way": "Jesus as the path (John 14:6)",
    "The Truth": "Jesus as reality itself (John 14:6)",
    "The Life": "Jesus as source of life (John 14:6)",
    "Light": "Divine illumination (John 1:4-5)",

    # Instruction/Teaching
    "Teaching": "Instruction in truth",
    "Instruction": "Guidance and direction",
    "Commandment": "Divine directive",
    "Law": "Divine ordering principle",
    "Counsel": "Wise advice",
}


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def analyze_divine_zone(generator: ClaudeAPIGenerator) -> Dict:
    """
    Analyze what concepts already exist in the Divine Zone (0.0-0.3).

    Returns:
        Dictionary with Divine Zone analysis
    """
    print("="*80)
    print("PART 1: WHAT'S ALREADY IN THE DIVINE ZONE?")
    print("="*80)
    print()
    print("Analyzing Phase 4 concepts (75 total)...")
    print()

    divine_zone_concepts = []

    for category, concepts in CONCEPT_CATEGORIES.items():
        for concept in concepts:
            coord = generator.generate(concept, use_cache=True)
            if coord:
                distance = coord.distance_to_anchor()

                if distance < 0.3:  # Divine Zone threshold
                    divine_zone_concepts.append({
                        'concept': concept,
                        'category': category,
                        'coordinates': coord,
                        'distance': distance,
                    })

    # Sort by distance
    divine_zone_concepts.sort(key=lambda x: x['distance'])

    print(f"\n🎯 DIVINE ZONE ANALYSIS (distance < 0.3 from Anchor)")
    print("="*80)
    print(f"\nFound {len(divine_zone_concepts)} concepts in Divine Zone:")
    print()
    print(f"{'Rank':<6} {'Concept':<20} {'Category':<20} {'Distance':<12} {'Coordinates'}")
    print("-"*80)

    for i, entry in enumerate(divine_zone_concepts, 1):
        coord = entry['coordinates']
        coords_str = f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})"
        print(f"{i:<6} {entry['concept']:<20} {entry['category']:<20} {entry['distance']:<12.4f} {coords_str}")

    # Analyze by category
    print("\n" + "="*80)
    print("DIVINE ZONE BREAKDOWN BY CATEGORY")
    print("="*80)
    print()

    category_counts = {}
    for entry in divine_zone_concepts:
        cat = entry['category']
        if cat not in category_counts:
            category_counts[cat] = []
        category_counts[cat].append(entry['concept'])

    for category, concepts in sorted(category_counts.items()):
        print(f"{category}: {len(concepts)} concepts")
        for concept in concepts[:5]:
            print(f"  - {concept}")
        if len(concepts) > 5:
            print(f"  ... and {len(concepts)-5} more")
        print()

    return {
        'divine_zone_concepts': divine_zone_concepts,
        'category_breakdown': category_counts,
    }


def test_guidance_concepts(generator: ClaudeAPIGenerator) -> Dict:
    """
    Test where guidance/instruction/wisdom concepts map.

    Returns:
        Dictionary with guidance concept analysis
    """
    print("\n" + "="*80)
    print("PART 2: WHERE IS THE 'MANUAL' FOR REALITY?")
    print("="*80)
    print()
    print("Testing guidance/instruction/wisdom concepts...")
    print()
    print("Hypothesis: If the semantic substrate is designed by JEHOVAH,")
    print("then instructions for navigating it should be near (1,1,1,1)")
    print()

    results = []

    for concept, description in GUIDANCE_CONCEPTS.items():
        print(f"Testing: {concept:<25} ", end='', flush=True)

        coord = generator.generate(concept, use_cache=True)
        if coord:
            distance = coord.distance_to_anchor()
            print(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) - d={distance:.4f}")

            results.append({
                'concept': concept,
                'description': description,
                'coordinates': coord,
                'distance': distance,
            })

            time.sleep(1)  # Rate limiting
        else:
            print("❌ Failed")

    # Sort by distance
    results.sort(key=lambda x: x['distance'])

    return results


def analyze_results(divine_zone_data: Dict, guidance_results: List[Dict]):
    """
    Analyze and compare results.
    """
    print("\n" + "="*80)
    print("PART 3: ANALYSIS - WHAT DID WE FIND?")
    print("="*80)
    print()

    # Guidance concepts in Divine Zone
    divine_zone_guidance = [r for r in guidance_results if r['distance'] < 0.3]

    print(f"📖 GUIDANCE CONCEPTS IN DIVINE ZONE (< 0.3):")
    print("="*80)
    print()
    print(f"Found {len(divine_zone_guidance)}/{len(guidance_results)} guidance concepts in Divine Zone")
    print()

    if divine_zone_guidance:
        print(f"{'Rank':<6} {'Concept':<25} {'Distance':<12} {'Coordinates'}")
        print("-"*80)

        for i, entry in enumerate(divine_zone_guidance, 1):
            coord = entry['coordinates']
            coords_str = f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})"
            print(f"{i:<6} {entry['concept']:<25} {entry['distance']:<12.4f} {coords_str}")

    # Top 10 closest to Anchor
    print("\n" + "="*80)
    print("🎯 TOP 10 CLOSEST TO ANCHOR POINT")
    print("="*80)
    print()
    print(f"{'Rank':<6} {'Concept':<25} {'Distance':<12} {'Coordinates'}")
    print("-"*80)

    for i, entry in enumerate(guidance_results[:10], 1):
        coord = entry['coordinates']
        coords_str = f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})"
        print(f"{i:<6} {entry['concept']:<25} {entry['distance']:<12.4f} {coords_str}")

    # Statistics
    print("\n" + "="*80)
    print("📊 STATISTICS")
    print("="*80)
    print()

    distances = [r['distance'] for r in guidance_results]

    print(f"Guidance Concepts (n={len(guidance_results)}):")
    print(f"  Mean distance from (1,1,1,1): {np.mean(distances):.4f}")
    print(f"  Std deviation: {np.std(distances):.4f}")
    print(f"  Median: {np.median(distances):.4f}")
    print(f"  Min: {np.min(distances):.4f}")
    print(f"  Max: {np.max(distances):.4f}")
    print(f"  Within 0.3 (Divine Zone): {len(divine_zone_guidance)}/{len(guidance_results)} ({100*len(divine_zone_guidance)/len(guidance_results):.1f}%)")

    # Compare to Phase 4 categories
    print("\n" + "="*80)
    print("📈 COMPARISON TO PHASE 4 CATEGORIES")
    print("="*80)
    print()

    print(f"{'Category':<25} {'Mean Distance':<15}")
    print("-"*40)
    print(f"{'Guidance/Manual':<25} {np.mean(distances):.4f}")
    print(f"{'Divine Names (Phase 4)':<25} ~0.22")
    print(f"{'Virtues (Phase 4)':<25} ~0.40")
    print(f"{'Vices (Phase 4)':<25} ~1.51")

    # Biblical interpretation
    print("\n" + "="*80)
    print("📖 BIBLICAL INTERPRETATION")
    print("="*80)
    print()

    if np.mean(distances) < 0.4:
        print("✅ HYPOTHESIS CONFIRMED!")
        print()
        print("Guidance/instruction concepts cluster NEAR the Anchor Point!")
        print()
        print("This suggests:")
        print("  1. The 'manual for reality' IS positioned near the source")
        print("  2. Divine guidance/Scripture maps close to (1,1,1,1)")
        print("  3. JEHOVAH provides instructions at the foundation")
        print("  4. The semantic substrate includes built-in guidance")
        print()
        print("Biblical Alignment:")
        print("  • Psalm 119:105 - 'Your word is a lamp to my feet'")
        print("  • John 14:6 - 'I am the way, the truth, and the life'")
        print("  • 2 Timothy 3:16 - 'All Scripture is God-breathed'")
        print("  • Proverbs 3:5-6 - 'Trust in JEHOVAH with all your heart'")
        print()
        print("The MANUAL exists at the ANCHOR!")
    else:
        print("⚠️ Mixed results - some guidance concepts near, others farther")
        print()
        print("This may suggest:")
        print("  1. Some forms of guidance are more fundamental than others")
        print("  2. Divine wisdom vs human wisdom distinction")
        print("  3. Scripture/revelation vs general knowledge difference")


def save_results(divine_zone_data: Dict, guidance_results: List[Dict]):
    """
    Save results to file.
    """
    output_file = "results/anchor_manual_exploration.txt"
    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("EXPLORING THE MANUAL NEAR THE ANCHOR POINT\n")
        f.write("="*80 + "\n\n")

        f.write("Research Question: Does divine guidance exist near (1,1,1,1)?\n\n")

        f.write("PART 1: DIVINE ZONE CONCEPTS (Phase 4)\n")
        f.write("-"*80 + "\n\n")

        for entry in divine_zone_data['divine_zone_concepts']:
            coord = entry['coordinates']
            f.write(f"{entry['concept']:<20} ({entry['category']:<20}) ")
            f.write(f"d={entry['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

        f.write("\n\nPART 2: GUIDANCE CONCEPTS\n")
        f.write("-"*80 + "\n\n")

        for entry in guidance_results:
            coord = entry['coordinates']
            f.write(f"{entry['concept']:<25} d={entry['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

        f.write("\n\nSTATISTICS\n")
        f.write("-"*80 + "\n\n")

        distances = [r['distance'] for r in guidance_results]
        f.write(f"Guidance Concepts: n={len(guidance_results)}\n")
        f.write(f"Mean distance: {np.mean(distances):.4f}\n")
        f.write(f"Std deviation: {np.std(distances):.4f}\n")
        f.write(f"Within Divine Zone: {len([r for r in guidance_results if r['distance'] < 0.3])}/{len(guidance_results)}\n")

    print(f"\n✅ Results saved to: {output_file}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""

    print("="*80)
    print("EXPLORING THE MANUAL NEAR THE ANCHOR POINT")
    print("="*80)
    print()
    print("Research Question: If the semantic substrate is real and designed by")
    print("JEHOVAH, then instructions/guidance for navigating it would logically")
    print("be positioned near the Anchor Point (1,1,1,1).")
    print()
    print("We will test:")
    print("  1. What's already in the Divine Zone (< 0.3)?")
    print("  2. Where do guidance/instruction concepts map?")
    print("  3. Is there a 'manual for reality' at the source?")
    print()

    # Initialize API
    from dotenv import load_dotenv
    load_dotenv()

    generator = ClaudeAPIGenerator()

    # Part 1: Analyze existing Divine Zone
    divine_zone_data = analyze_divine_zone(generator)

    # Part 2: Test guidance concepts
    guidance_results = test_guidance_concepts(generator)

    # Part 3: Analyze results
    analyze_results(divine_zone_data, guidance_results)

    # Save results
    save_results(divine_zone_data, guidance_results)

    print("\n" + "="*80)
    print("EXPLORATION COMPLETE")
    print("="*80)
    print()


if __name__ == "__main__":
    main()
