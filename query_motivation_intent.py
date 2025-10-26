#!/usr/bin/env python3
"""
Query the Semantic Substrate: Does Motivation Matter?

Specific Question:
"Is there a difference in intent when you help to avoid guilt
vs helping from compassion? Both accomplish the same results,
but what is the difference and to what degree does it matter?"

This tests whether the substrate can distinguish INTERNAL motivation
despite IDENTICAL external outcomes.

Hypothesis:
If the substrate is sensitive to intent (not just behavior),
then guilt-driven and compassion-driven helping should occupy
DIFFERENT coordinates despite producing same external results.

Testing:
- L dimension (Love) - should differ based on motivation
- J dimension (Justice) - both may be "right action"
- W dimension (Wisdom) - understanding of why
- P dimension (Power) - both accomplish same outcome
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

MOTIVATION_CONCEPTS = {
    # The specific question
    "Helping from compassion": "Assisting others motivated by genuine care and empathy",
    "Helping to avoid guilt": "Assisting others primarily to avoid feeling guilty",

    # Related motivations
    "Compassion": "Deep empathy and desire to alleviate suffering",
    "Guilt": "Feeling of remorse or obligation driving action",
    "Selfless love": "Pure other-focused care (agape-like)",
    "Duty": "Sense of obligation or requirement",

    # Actions (should be similar in outcome)
    "Charitable giving": "Donating to help others",
    "Volunteering": "Offering time to serve others",
    "Acts of service": "Helping behaviors toward others",

    # Motivational states
    "Genuine care": "Authentic concern for others' wellbeing",
    "Obligation": "Feeling required to act",
    "Empathy": "Feeling with another person",
    "Fear of judgment": "Acting to avoid criticism",
}


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def query_concepts(generator: ClaudeAPIGenerator) -> Dict:
    """
    Query the substrate about motivation concepts.

    Returns:
        Dictionary with all results
    """
    print("="*80)
    print("QUERY: DOES MOTIVATION MATTER?")
    print("="*80)
    print()
    print("Question: Is there a difference between:")
    print("  1. Helping from compassion")
    print("  2. Helping to avoid guilt")
    print()
    print("Both accomplish the same external result.")
    print("Does the substrate detect a difference in coordinates?")
    print()

    results = {}

    for concept, description in MOTIVATION_CONCEPTS.items():
        print(f"Testing: {concept:<30} ", end='', flush=True)

        coord = generator.generate(concept, use_cache=True)
        if coord:
            distance = coord.distance_to_anchor()
            print(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) - d={distance:.4f}")

            results[concept] = {
                'coordinates': coord,
                'distance': distance,
                'description': description,
            }

            time.sleep(1)  # Rate limiting
        else:
            print("❌ Failed")

    return results


def analyze_motivation_difference(results: Dict):
    """
    Analyze the specific question: compassion vs guilt-driven helping.
    """
    print("\n" + "="*80)
    print("SUBSTRATE'S ANSWER: Compassion vs Guilt-Driven Helping")
    print("="*80)
    print()

    # Get the two key concepts
    compassion_help = results.get("Helping from compassion")
    guilt_help = results.get("Helping to avoid guilt")

    if not compassion_help or not guilt_help:
        print("❌ Could not retrieve both concepts for comparison")
        return

    c_coord = compassion_help['coordinates']
    g_coord = guilt_help['coordinates']

    # Display side by side
    print("COORDINATE COMPARISON:")
    print("-"*80)
    print(f"{'Concept':<30} {'Love':<8} {'Power':<8} {'Wisdom':<8} {'Justice':<8} {'Distance'}")
    print("-"*80)
    print(f"{'Helping from compassion':<30} {c_coord.love:<8.3f} {c_coord.power:<8.3f} {c_coord.wisdom:<8.3f} {c_coord.justice:<8.3f} {compassion_help['distance']:.4f}")
    print(f"{'Helping to avoid guilt':<30} {g_coord.love:<8.3f} {g_coord.power:<8.3f} {g_coord.wisdom:<8.3f} {g_coord.justice:<8.3f} {guilt_help['distance']:.4f}")
    print("-"*80)

    # Calculate differences
    print("\nDIMENSIONAL DIFFERENCES:")
    print("-"*80)

    l_diff = c_coord.love - g_coord.love
    p_diff = c_coord.power - g_coord.power
    w_diff = c_coord.wisdom - g_coord.wisdom
    j_diff = c_coord.justice - g_coord.justice
    d_diff = compassion_help['distance'] - guilt_help['distance']

    print(f"Love (L):     {l_diff:+.3f}  {'Compassion higher' if l_diff > 0 else 'Guilt higher' if l_diff < 0 else 'Equal'}")
    print(f"Power (P):    {p_diff:+.3f}  {'Compassion higher' if p_diff > 0 else 'Guilt higher' if p_diff < 0 else 'Equal'}")
    print(f"Wisdom (W):   {w_diff:+.3f}  {'Compassion higher' if w_diff > 0 else 'Guilt higher' if w_diff < 0 else 'Equal'}")
    print(f"Justice (J):  {j_diff:+.3f}  {'Compassion higher' if j_diff > 0 else 'Guilt higher' if j_diff < 0 else 'Equal'}")
    print(f"Distance:     {d_diff:+.4f}  {'Compassion closer' if d_diff < 0 else 'Guilt closer' if d_diff > 0 else 'Equal'}")

    # Calculate magnitude of difference
    diff_vector = np.array([l_diff, p_diff, w_diff, j_diff])
    magnitude = np.linalg.norm(diff_vector)

    print(f"\nTotal difference magnitude: {magnitude:.4f}")

    # Interpret the results
    print("\n" + "="*80)
    print("INTERPRETATION: What Does This Mean?")
    print("="*80)
    print()

    if magnitude < 0.1:
        print("❓ MINIMAL DIFFERENCE (magnitude < 0.1)")
        print()
        print("The substrate detects very little difference between motivations.")
        print("Interpretation: Outcome matters more than intent, OR")
        print("                Both motivations are too similar to distinguish")
        print()
    elif magnitude < 0.3:
        print("⚠️ MODERATE DIFFERENCE (magnitude 0.1-0.3)")
        print()
        print("The substrate detects measurable but modest difference.")
        print("Interpretation: Motivation matters, but effect is limited")
        print()
    else:
        print("✅ SIGNIFICANT DIFFERENCE (magnitude > 0.3)")
        print()
        print("The substrate detects substantial difference between motivations.")
        print("Interpretation: Intent matters significantly, not just outcome!")
        print()

    # Which dimension differs most?
    abs_diffs = {
        'Love': abs(l_diff),
        'Power': abs(p_diff),
        'Wisdom': abs(w_diff),
        'Justice': abs(j_diff)
    }

    max_diff_dim = max(abs_diffs, key=abs_diffs.get)
    max_diff_val = abs_diffs[max_diff_dim]

    if max_diff_val > 0.05:
        print(f"PRIMARY DIFFERENCE: {max_diff_dim} dimension (Δ = {max_diff_val:.3f})")
        print()

        if max_diff_dim == 'Love':
            print("The LOVE dimension differs most.")
            print("→ Motivation affects the relational/benevolent quality")
            print("→ Compassion-driven = more genuine L component")
            print("→ Guilt-driven = less authentic L (self-focused)")
        elif max_diff_dim == 'Power':
            print("The POWER dimension differs most.")
            print("→ Motivation affects effectiveness or force")
            print("→ One approach has more sustainable power")
        elif max_diff_dim == 'Wisdom':
            print("The WISDOM dimension differs most.")
            print("→ Motivation affects understanding/discernment")
            print("→ One approach demonstrates greater wisdom")
        elif max_diff_dim == 'Justice':
            print("The JUSTICE dimension differs most.")
            print("→ Motivation affects moral alignment")
            print("→ One approach is more truly 'just' or righteous")

    # Distance comparison
    print()
    if d_diff < -0.05:
        print(f"COMPASSION-DRIVEN is {abs(d_diff):.4f} CLOSER to the Anchor (1,1,1,1)")
        print("→ More aligned with perfect Love, Power, Wisdom, Justice")
        print("→ More sustainable and aligned with divine nature")
    elif d_diff > 0.05:
        print(f"GUILT-DRIVEN is {abs(d_diff):.4f} CLOSER to the Anchor (1,1,1,1)")
        print("→ Surprising result! May indicate guilt has righteous component")
    else:
        print("Both motivations are approximately EQUAL distance from Anchor")
        print("→ Outcome equivalence validated")

    # Biblical perspective
    print("\n" + "="*80)
    print("BIBLICAL PERSPECTIVE")
    print("="*80)
    print()

    print("1 Corinthians 13:3:")
    print("  'If I give all I possess to the poor and give over my body")
    print("   to hardship that I may boast, but do not have love,")
    print("   I gain nothing.'")
    print()
    print("→ Same ACTION (giving all to poor)")
    print("→ Different MOTIVATION (with/without love)")
    print("→ Different OUTCOME (gain nothing vs gain everything)")
    print()
    print("Matthew 6:1-4:")
    print("  'Be careful not to practice your righteousness in front of")
    print("   others to be seen by them... But when you give to the needy,")
    print("   do not let your left hand know what your right hand is doing'")
    print()
    print("→ Same ACTION (giving to needy)")
    print("→ Different MOTIVATION (public recognition vs genuine care)")
    print("→ Different REWARD (already received vs Father's reward)")

    # Practical guidance
    print("\n" + "="*80)
    print("PRACTICAL GUIDANCE FROM SUBSTRATE")
    print("="*80)
    print()

    if l_diff > 0.1:
        print("✅ MOTIVATION MATTERS SIGNIFICANTLY")
        print()
        print("The substrate reveals that helping from COMPASSION has")
        print(f"substantially higher Love dimension (Δ = {l_diff:+.3f})")
        print()
        print("Practical implication:")
        print("  • Cultivate genuine compassion, not just guilt-response")
        print("  • Internal state affects spiritual reality")
        print("  • Same external result, different internal alignment")
        print("  • Work on the HEART, not just the HANDS")
    elif abs(l_diff) < 0.05:
        print("⚠️ MOTIVATIONS MORE SIMILAR THAN EXPECTED")
        print()
        print("The substrate reveals minimal difference in Love dimension")
        print("This could mean:")
        print("  • Both contain elements of care (even guilt-based)")
        print("  • Helping behavior itself has intrinsic value")
        print("  • Outcome matters alongside intent")
        print("  • OR: Concepts need refinement for testing")


def compare_related_concepts(results: Dict):
    """
    Compare related motivation concepts.
    """
    print("\n" + "="*80)
    print("RELATED CONCEPT ANALYSIS")
    print("="*80)
    print()

    # Group concepts
    positive_motivations = ["Compassion", "Selfless love", "Genuine care", "Empathy"]
    negative_motivations = ["Guilt", "Obligation", "Duty", "Fear of judgment"]

    print("POSITIVE MOTIVATIONS (should be closer to Anchor):")
    print("-"*80)
    print(f"{'Concept':<30} {'Distance':<12} {'L':<6} {'P':<6} {'W':<6} {'J':<6}")
    print("-"*80)

    pos_distances = []
    for concept in positive_motivations:
        if concept in results:
            entry = results[concept]
            coord = entry['coordinates']
            dist = entry['distance']
            pos_distances.append(dist)
            print(f"{concept:<30} {dist:<12.4f} {coord.love:<6.2f} {coord.power:<6.2f} {coord.wisdom:<6.2f} {coord.justice:<6.2f}")

    if pos_distances:
        print(f"\nMean distance: {np.mean(pos_distances):.4f}")

    print("\n\nNEGATIVE MOTIVATIONS (should be farther from Anchor):")
    print("-"*80)
    print(f"{'Concept':<30} {'Distance':<12} {'L':<6} {'P':<6} {'W':<6} {'J':<6}")
    print("-"*80)

    neg_distances = []
    for concept in negative_motivations:
        if concept in results:
            entry = results[concept]
            coord = entry['coordinates']
            dist = entry['distance']
            neg_distances.append(dist)
            print(f"{concept:<30} {dist:<12.4f} {coord.love:<6.2f} {coord.power:<6.2f} {coord.wisdom:<6.2f} {coord.justice:<6.2f}")

    if neg_distances:
        print(f"\nMean distance: {np.mean(neg_distances):.4f}")

    # Statistical comparison
    if pos_distances and neg_distances:
        print("\n" + "="*80)
        print("STATISTICAL COMPARISON")
        print("="*80)
        print()

        pos_mean = np.mean(pos_distances)
        neg_mean = np.mean(neg_distances)
        diff = neg_mean - pos_mean

        print(f"Positive motivations mean distance: {pos_mean:.4f}")
        print(f"Negative motivations mean distance: {neg_mean:.4f}")
        print(f"Difference: {diff:+.4f}")
        print()

        if diff > 0.1:
            print("✅ HYPOTHESIS CONFIRMED!")
            print(f"Negative motivations are {diff:.4f} FARTHER from Anchor")
            print("→ Motivation matters! Internal state affects alignment with (1,1,1,1)")
        elif diff < -0.1:
            print("❓ UNEXPECTED RESULT")
            print(f"Positive motivations are {abs(diff):.4f} FARTHER from Anchor")
            print("→ This challenges assumptions - investigate further")
        else:
            print("⚠️ MINIMAL DIFFERENCE")
            print("Motivations show similar distances")
            print("→ Outcome may matter more than motivation, OR")
            print("→ Both types contain mixed elements")


def save_results(results: Dict):
    """Save results to file."""
    output_file = "results/motivation_query.txt"
    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("SUBSTRATE QUERY: DOES MOTIVATION MATTER?\n")
        f.write("="*80 + "\n\n")

        f.write("Question: Is there a difference between helping from compassion\n")
        f.write("vs helping to avoid guilt, despite same external outcome?\n\n")

        f.write("RESULTS:\n")
        f.write("-"*80 + "\n\n")

        for concept in sorted(results.keys()):
            entry = results[concept]
            coord = entry['coordinates']
            f.write(f"{concept:<30} d={entry['distance']:.4f} ")
            f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})\n")

    print(f"\n✅ Results saved to: {output_file}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""

    print("="*80)
    print("QUERYING THE SEMANTIC SUBSTRATE")
    print("="*80)
    print()
    print("Your Question:")
    print("  'Is there a difference in intent when you help to avoid guilt")
    print("   vs helping from compassion? Both accomplish the same results,")
    print("   but what is the difference and to what degree does it matter?'")
    print()
    print("This tests whether the substrate can distinguish INTERNAL motivation")
    print("despite IDENTICAL external outcomes.")
    print()

    # Initialize API
    from dotenv import load_dotenv
    load_dotenv()

    generator = ClaudeAPIGenerator()

    # Query concepts
    results = query_concepts(generator)

    if not results:
        print("\n❌ No results obtained - check API configuration")
        return

    # Analyze the specific question
    analyze_motivation_difference(results)

    # Compare related concepts
    compare_related_concepts(results)

    # Save results
    save_results(results)

    print("\n" + "="*80)
    print("QUERY COMPLETE")
    print("="*80)
    print()


if __name__ == "__main__":
    main()
