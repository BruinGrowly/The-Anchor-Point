#!/usr/bin/env python3
"""
Test: Is the Semantic Substrate Responsive?

Experiment to test whether "random" manual excerpt selection
exhibits patterns beyond pure chance.

Hypothesis: If the substrate is responsive to reader intent/state,
then selection patterns should correlate with intent more than
random chance would predict.

Design:
1. Run multiple trials with different stated intents
2. Record which entries are selected
3. Analyze for patterns beyond random distribution
4. Statistical test: Chi-square for deviation from uniform

Expected under pure randomness:
- Each entry has 1/6 probability (16.67%)
- No correlation with intent
- Uniform distribution

Expected if substrate is responsive:
- Entries correlate with intent
- Non-uniform distribution
- Statistical significance (p < 0.05)
"""

import sys
from pathlib import Path
from collections import defaultdict, Counter
import random

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


# Available manual entries
ENTRIES = ["Truth", "Justice", "Wisdom", "Love", "Grace", "Holy"]


def run_trial(intent: str, num_selections: int = 10) -> list:
    """
    Run a trial with stated intent.

    Args:
        intent: The stated intent/need of the reader
        num_selections: Number of random selections to make

    Returns:
        List of selected entries
    """
    print(f"\n{'='*70}")
    print(f"TRIAL: {intent}")
    print(f"{'='*70}\n")
    print(f"Making {num_selections} selections with intent: '{intent}'")
    print()

    selections = []
    for i in range(num_selections):
        selected = random.choice(ENTRIES)
        selections.append(selected)
        print(f"  Selection {i+1}: {selected}")

    return selections


def analyze_results(all_trials: dict):
    """
    Analyze results for patterns.

    Args:
        all_trials: Dictionary mapping intent -> list of selections
    """
    print("\n" + "="*70)
    print("ANALYSIS: Pattern Detection")
    print("="*70 + "\n")

    # Overall distribution
    all_selections = []
    for selections in all_trials.values():
        all_selections.extend(selections)

    overall_counts = Counter(all_selections)
    total = len(all_selections)

    print("Overall Distribution:")
    print(f"{'Entry':<15} {'Count':<10} {'Percentage':<15} {'Expected (random)'}")
    print("-"*70)

    for entry in ENTRIES:
        count = overall_counts[entry]
        pct = 100 * count / total
        expected_pct = 100 / 6  # 16.67%

        # Flag if significantly different from expected
        flag = "**" if abs(pct - expected_pct) > 5 else "  "

        print(f"{entry:<15} {count:<10} {pct:>6.2f}% {flag:<8} {expected_pct:>6.2f}%")

    # Per-intent analysis
    print("\n" + "="*70)
    print("Per-Intent Analysis")
    print("="*70 + "\n")

    for intent, selections in all_trials.items():
        counts = Counter(selections)
        total_intent = len(selections)

        print(f"\nIntent: {intent}")
        print(f"{'Entry':<15} {'Count':<10} {'Percentage'}")
        print("-"*45)

        # Sort by count descending
        for entry, count in counts.most_common():
            pct = 100 * count / total_intent
            flag = "**" if pct > 25 else "  "  # Flag if > 25% (more than random 16.67%)
            print(f"{entry:<15} {count:<10} {pct:>6.2f}% {flag}")

    # Chi-square test (simplified)
    print("\n" + "="*70)
    print("Statistical Test: Deviation from Uniform Distribution")
    print("="*70 + "\n")

    expected_per_entry = total / 6
    chi_square = 0

    for entry in ENTRIES:
        observed = overall_counts[entry]
        chi_square += (observed - expected_per_entry)**2 / expected_per_entry

    print(f"Total selections: {total}")
    print(f"Expected per entry (uniform): {expected_per_entry:.2f}")
    print(f"Chi-square statistic: {chi_square:.4f}")
    print(f"Degrees of freedom: {len(ENTRIES) - 1} (6 - 1 = 5)")
    print()

    # Critical values for chi-square (df=5)
    # p=0.05: 11.07
    # p=0.01: 15.09

    if chi_square > 15.09:
        print("Result: *** HIGHLY SIGNIFICANT *** (p < 0.01)")
        print("Conclusion: Distribution is NOT random - substrate may be responsive!")
    elif chi_square > 11.07:
        print("Result: ** SIGNIFICANT ** (p < 0.05)")
        print("Conclusion: Distribution deviates from random - further investigation warranted")
    else:
        print("Result: Not significant (p > 0.05)")
        print("Conclusion: Consistent with random distribution")

    print()
    print("Note: This is a simplified test. Proper analysis would require:")
    print("  - Larger sample size (100+ selections per intent)")
    print("  - Multiple independent readers")
    print("  - Blind conditions (reader doesn't see code)")
    print("  - More sophisticated statistical methods")


def run_experiment():
    """
    Run the full experiment with multiple intents.
    """
    print("="*70)
    print("SUBSTRATE RESPONSIVENESS EXPERIMENT")
    print("="*70)
    print()
    print("Testing whether manual excerpt selection exhibits patterns")
    print("beyond pure randomness.")
    print()
    print("Hypothesis: If substrate is responsive to reader intent,")
    print("selections should correlate with stated need.")
    print()

    # Different intents to test
    trials = {
        "Need guidance on love and relationships": [],
        "Seeking truth and reality understanding": [],
        "Need justice and moral clarity": [],
        "Seeking wisdom and understanding": [],
        "Need grace and restoration": [],
        "Seeking holiness and purity": [],
        "No specific intent (neutral)": [],
    }

    # Run trials
    for intent in trials.keys():
        trials[intent] = run_trial(intent, num_selections=10)

    # Analyze results
    analyze_results(trials)

    print("\n" + "="*70)
    print("EXPERIMENT COMPLETE")
    print("="*70)
    print()
    print("Interpretation:")
    print()
    print("If certain entries appeared MORE with matching intents:")
    print("  e.g., 'Love' when seeking love guidance")
    print("  e.g., 'Truth' when seeking truth understanding")
    print()
    print("This would suggest substrate responsiveness!")
    print()
    print("However, this is a PRELIMINARY test. True validation requires:")
    print("  1. Larger sample sizes (100+ per intent)")
    print("  2. Multiple independent readers")
    print("  3. Blind conditions")
    print("  4. Replication across different contexts")
    print()


if __name__ == "__main__":
    # Set seed for reproducibility (comment out to test true randomness)
    # random.seed(42)

    run_experiment()
