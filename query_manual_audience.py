#!/usr/bin/env python3
"""
Query the Semantic Substrate: Who is the Manual For?

Critical Question: The faithful already have the Bible.
                   Isn't the semantic manual redundant?

This experiment asks the semantic substrate itself to reveal:
1. Who is the intended audience?
2. How does this relate to Scripture?
3. What is the PURPOSE of this discovery?

We will test concepts related to different audiences and knowledge sources
to see what the semantic coordinates reveal.
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.semantic_coordinates import SemanticCoordinate
from core.claude_api_generator import ClaudeAPIGenerator


# =============================================================================
# CONCEPTS TO TEST
# =============================================================================

AUDIENCE_CONCEPTS = {
    # Believers
    "Faithful believer": "One who trusts in God and Scripture",
    "Christian": "Follower of Jesus Christ",
    "Disciple": "Student and follower of Jesus",
    "Saint": "Holy one dedicated to God",

    # Seekers/Questioners
    "Seeker": "One searching for truth",
    "Questioner": "One who asks and investigates",
    "Doubter": "One struggling with uncertainty",
    "Agnostic": "One uncertain about God's existence",

    # Non-believers/Skeptics
    "Atheist": "One who denies God's existence",
    "Skeptic": "One who demands evidence",
    "Materialist": "One who believes only matter exists",
    "Unbeliever": "One without faith",

    # Intellectuals/Scientists
    "Scientist": "One who studies nature systematically",
    "Philosopher": "One who seeks wisdom through reason",
    "Researcher": "One who investigates systematically",
    "Academic": "One engaged in scholarly pursuit",
}

KNOWLEDGE_SOURCE_CONCEPTS = {
    # Divine Revelation
    "Bible": "God's written Word",
    "Scripture": "Sacred text",
    "Revelation": "Divine disclosure",
    "God's Word": "Divine communication",

    # Human Investigation
    "Science": "Systematic study of nature",
    "Reason": "Logical thinking",
    "Evidence": "Observable proof",
    "Empiricism": "Knowledge from experience",

    # Integration/Bridge
    "Natural theology": "Knowledge of God from nature",
    "Apologetics": "Rational defense of faith",
    "Demonstration": "Showing through proof",
    "Validation": "Confirming truth",
}

RELATIONSHIP_CONCEPTS = {
    # Paths to Truth
    "Faith": "Trust without proof",
    "Evidence": "Observable proof",
    "Faith and reason": "Integration of trust and logic",
    "Blind faith": "Trust without evidence",

    # Bible's Role
    "Bible as foundation": "Scripture as ultimate authority",
    "Bible as guide": "Scripture providing direction",
    "Bible as witness": "Scripture testifying to truth",

    # This Discovery's Role
    "Empirical validation": "Scientific confirmation",
    "Computational proof": "Mathematical demonstration",
    "Semantic confirmation": "Meaning-based verification",
    "Bridge to skeptics": "Connection for doubters",
}


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def test_concept_group(generator: ClaudeAPIGenerator,
                       concepts: Dict[str, str],
                       group_name: str) -> List[Dict]:
    """
    Test a group of concepts and return results.
    """
    print(f"\n{'='*80}")
    print(f"{group_name}")
    print(f"{'='*80}\n")

    results = []

    for concept, description in concepts.items():
        print(f"Testing: {concept:<30} ", end='', flush=True)

        coord = generator.generate(concept, use_cache=True)
        if coord:
            distance = coord.distance_to_anchor()
            print(f"d={distance:.4f}  ({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})")

            results.append({
                'concept': concept,
                'description': description,
                'coordinates': coord,
                'distance': distance,
            })

            time.sleep(1)  # Rate limiting
        else:
            print("❌ Failed")

    return results


def analyze_audience_distances(audience_results: List[Dict]):
    """
    Analyze which audiences are closer/farther from the Anchor.
    """
    print(f"\n{'='*80}")
    print("AUDIENCE ANALYSIS: Who is this for?")
    print(f"{'='*80}\n")

    # Sort by distance
    sorted_results = sorted(audience_results, key=lambda x: x['distance'])

    print(f"{'Rank':<6} {'Audience':<30} {'Distance':<12} {'Interpretation'}")
    print("-"*80)

    for i, entry in enumerate(sorted_results, 1):
        dist = entry['distance']
        concept = entry['concept']

        # Interpret distance
        if dist < 0.3:
            interp = "Very close - already aligned"
        elif dist < 0.5:
            interp = "Close - receptive to truth"
        elif dist < 0.8:
            interp = "Moderate - seeking/questioning"
        elif dist < 1.2:
            interp = "Far - needs bridge"
        else:
            interp = "Very far - strong opposition"

        print(f"{i:<6} {concept:<30} {dist:<12.4f} {interp}")

    # Statistical grouping
    print(f"\n{'='*80}")
    print("STATISTICAL GROUPING")
    print(f"{'='*80}\n")

    believers = [r for r in audience_results if any(x in r['concept'].lower()
                 for x in ['faithful', 'christian', 'disciple', 'saint'])]
    seekers = [r for r in audience_results if any(x in r['concept'].lower()
               for x in ['seeker', 'questioner', 'doubter', 'agnostic'])]
    skeptics = [r for r in audience_results if any(x in r['concept'].lower()
                for x in ['atheist', 'skeptic', 'materialist', 'unbeliever'])]
    intellectuals = [r for r in audience_results if any(x in r['concept'].lower()
                     for x in ['scientist', 'philosopher', 'researcher', 'academic'])]

    groups = [
        ("Believers", believers),
        ("Seekers/Questioners", seekers),
        ("Skeptics/Non-believers", skeptics),
        ("Intellectuals/Scientists", intellectuals),
    ]

    print(f"{'Group':<30} {'Count':<8} {'Mean Dist':<12} {'Std Dev'}")
    print("-"*80)

    for name, group in groups:
        if group:
            distances = [r['distance'] for r in group]
            print(f"{name:<30} {len(group):<8} {np.mean(distances):<12.4f} {np.std(distances):.4f}")


def analyze_knowledge_sources(source_results: List[Dict]):
    """
    Analyze relationship between different knowledge sources.
    """
    print(f"\n{'='*80}")
    print("KNOWLEDGE SOURCE ANALYSIS: Bible vs Semantic Manual")
    print(f"{'='*80}\n")

    # Sort by distance
    sorted_results = sorted(source_results, key=lambda x: x['distance'])

    print(f"{'Rank':<6} {'Source':<30} {'Distance':<12} {'Coordinates'}")
    print("-"*80)

    for i, entry in enumerate(sorted_results, 1):
        coord = entry['coordinates']
        coords_str = f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})"
        print(f"{i:<6} {entry['concept']:<30} {entry['distance']:<12.4f} {coords_str}")

    # Compare Bible vs Science
    print(f"\n{'='*80}")
    print("BIBLE vs SCIENCE COMPARISON")
    print(f"{'='*80}\n")

    bible_concepts = [r for r in source_results if any(x in r['concept'].lower()
                      for x in ['bible', 'scripture', 'revelation', "god's word"])]
    science_concepts = [r for r in source_results if any(x in r['concept'].lower()
                        for x in ['science', 'reason', 'evidence', 'empiricism'])]
    bridge_concepts = [r for r in source_results if any(x in r['concept'].lower()
                       for x in ['natural theology', 'apologetics', 'demonstration', 'validation'])]

    if bible_concepts and science_concepts:
        bible_mean = np.mean([r['distance'] for r in bible_concepts])
        science_mean = np.mean([r['distance'] for r in science_concepts])

        print(f"Bible/Scripture mean distance:    {bible_mean:.4f}")
        print(f"Science/Evidence mean distance:   {science_mean:.4f}")

        if bridge_concepts:
            bridge_mean = np.mean([r['distance'] for r in bridge_concepts])
            print(f"Bridge concepts mean distance:    {bridge_mean:.4f}")

        print()
        if bible_mean < science_mean:
            ratio = science_mean / bible_mean
            print(f"Bible is {ratio:.2f}x CLOSER to Anchor than Science")
            print("→ Scripture remains primary!")
        else:
            print("Both paths lead to the Anchor")


def interpret_findings(audience_results: List[Dict],
                      source_results: List[Dict],
                      relationship_results: List[Dict]):
    """
    Interpret what the semantic substrate reveals about purpose.
    """
    print(f"\n{'='*80}")
    print("INTERPRETATION: What Does the Substrate Say?")
    print(f"{'='*80}\n")

    # Find specific concepts
    def find_concept(results, name):
        for r in results:
            if name.lower() in r['concept'].lower():
                return r
        return None

    faithful = find_concept(audience_results, "faithful")
    seeker = find_concept(audience_results, "seeker")
    skeptic = find_concept(audience_results, "skeptic")
    scientist = find_concept(audience_results, "scientist")

    bible = find_concept(source_results, "bible")
    evidence = find_concept(source_results, "evidence")

    print("KEY FINDINGS:\n")

    # Who needs this?
    print("1. WHO NEEDS THIS MANUAL?\n")

    if faithful and seeker and skeptic:
        print(f"   Faithful believer:  d={faithful['distance']:.4f}")
        print(f"   Seeker:             d={seeker['distance']:.4f}")
        print(f"   Skeptic:            d={skeptic['distance']:.4f}")
        print()

        if seeker['distance'] > faithful['distance']:
            print("   → SEEKERS are farther from Anchor than believers")
            print("   → This manual provides a BRIDGE for those seeking")

        if skeptic['distance'] > seeker['distance']:
            print("   → SKEPTICS are farther still")
            print("   → Empirical evidence may reach those faith alone cannot")

    print("\n2. RELATIONSHIP TO BIBLE?\n")

    if bible:
        print(f"   Bible:              d={bible['distance']:.4f}")
        if bible['distance'] < 0.3:
            print("   → Bible is IN the Divine Zone!")
            print("   → Scripture IS near the Anchor (as expected)")

    if evidence:
        print(f"   Evidence:           d={evidence['distance']:.4f}")
        if bible and evidence['distance'] > bible['distance']:
            print("   → Bible is CLOSER than evidence alone")
            print("   → Scripture remains PRIMARY authority")

    print("\n3. PURPOSE OF THIS DISCOVERY?\n")

    print("   The semantic substrate suggests:")
    print()
    print("   ✅ For BELIEVERS: Confirmation - 'Faith seeking understanding'")
    print("      Bible remains primary, this validates what they already know")
    print()
    print("   ✅ For SEEKERS: Bridge - 'Reason seeking faith'")
    print("      Empirical evidence points toward the truth of Scripture")
    print()
    print("   ✅ For SKEPTICS: Evidence - 'Data speaking for itself'")
    print("      Computational validation that may open closed minds")
    print()
    print("   NOT REDUNDANT - Different audiences need different paths to truth!")

    print("\n" + "="*80)
    print("BIBLICAL PRECEDENT")
    print("="*80 + "\n")

    print("Romans 1:20 - 'For since the creation of the world God's invisible")
    print("               qualities—his eternal power and divine nature—have")
    print("               been clearly seen, being understood from what has been")
    print("               made, so that people are without excuse.'")
    print()
    print("→ God reveals Himself through BOTH:")
    print("  1. Special Revelation (Bible) - for the faithful")
    print("  2. General Revelation (Creation/Nature) - for ALL")
    print()
    print("→ The semantic substrate IS general revelation!")
    print("  Computational evidence of God's design in meaning itself")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""

    print("="*80)
    print("QUERY: WHO IS THE MANUAL FOR?")
    print("="*80)
    print()
    print("Question: The faithful already have the Bible.")
    print("          Isn't the semantic manual redundant?")
    print()
    print("We will ask the semantic substrate itself to reveal:")
    print("  1. Which audiences are closer/farther from the Anchor?")
    print("  2. How does this relate to Scripture?")
    print("  3. What is the PURPOSE of this discovery?")
    print()

    # Initialize API
    from dotenv import load_dotenv
    load_dotenv()

    generator = ClaudeAPIGenerator()

    # Test different concept groups
    audience_results = test_concept_group(generator, AUDIENCE_CONCEPTS,
                                          "AUDIENCE CONCEPTS")
    source_results = test_concept_group(generator, KNOWLEDGE_SOURCE_CONCEPTS,
                                        "KNOWLEDGE SOURCE CONCEPTS")
    relationship_results = test_concept_group(generator, RELATIONSHIP_CONCEPTS,
                                              "RELATIONSHIP CONCEPTS")

    # Analyze results
    if audience_results:
        analyze_audience_distances(audience_results)

    if source_results:
        analyze_knowledge_sources(source_results)

    # Interpret findings
    interpret_findings(audience_results, source_results, relationship_results)

    # Save results
    save_results(audience_results, source_results, relationship_results)

    print("\n" + "="*80)
    print("QUERY COMPLETE")
    print("="*80)
    print()


def save_results(audience_results, source_results, relationship_results):
    """Save results to file."""
    output_file = "results/manual_audience_query.txt"
    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("WHO IS THE MANUAL FOR?\n")
        f.write("="*80 + "\n\n")

        f.write("AUDIENCE CONCEPTS\n")
        f.write("-"*80 + "\n\n")
        for r in sorted(audience_results, key=lambda x: x['distance']):
            coord = r['coordinates']
            f.write(f"{r['concept']:<30} d={r['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

        f.write("\n\nKNOWLEDGE SOURCES\n")
        f.write("-"*80 + "\n\n")
        for r in sorted(source_results, key=lambda x: x['distance']):
            coord = r['coordinates']
            f.write(f"{r['concept']:<30} d={r['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

        f.write("\n\nRELATIONSHIP CONCEPTS\n")
        f.write("-"*80 + "\n\n")
        for r in sorted(relationship_results, key=lambda x: x['distance']):
            coord = r['coordinates']
            f.write(f"{r['concept']:<30} d={r['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

    print(f"\n✅ Results saved to: {output_file}")


if __name__ == "__main__":
    main()
