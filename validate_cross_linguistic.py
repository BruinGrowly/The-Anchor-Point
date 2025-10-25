#!/usr/bin/env python3
"""
Cross-Linguistic Validation of the Anchor Point

Tests whether the NAME "JEHOVAH" occupies (1,1,1,1) across multiple languages.

Critical Insight: We are testing the SPECIFIC NAME (YHWH, Yahweh, Jehovah),
NOT generic words for "god".

If JEHOVAH is truly at the Anchor Point as a spiritual/semantic reality,
then His NAME - however it's transliterated or pronounced - should carry
the same coordinates across ALL languages.

Like how "water" in any language refers to H2O, if JEHOVAH is the being
at (1,1,1,1), then speaking/writing His NAME in any script should point
to the same semantic coordinates.

Hypothesis: The NAME "JEHOVAH" (YHWH/Yahweh) resonates at (1,1,1,1)
regardless of language, alphabet, or cultural context.

This tests whether the Anchor Point is:
- Universal (not language-specific)
- Resonant (the name itself carries the signature)
- Real (objective semantic phenomenon, not confirmation bias)
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from collections import defaultdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.semantic_coordinates import SemanticCoordinate
from core.claude_api_generator import ClaudeAPIGenerator


# =============================================================================
# DIVINE NAMES ACROSS LANGUAGES
# =============================================================================

DIVINE_NAMES = {
    # The personal NAME of God - JEHOVAH/YHWH equivalents across languages
    # NOT generic words for "god" but the SPECIFIC NAME

    'Hebrew': [
        'YHWH',           # יהוה - The Tetragrammaton (original)
        'Yahweh',         # Scholarly pronunciation
        'Yehovah',        # Traditional pronunciation
    ],

    'English': [
        'JEHOVAH',        # Traditional English
        'Yahweh',         # Transliteration
    ],

    'Greek': [
        'Ιεχωβά',         # Iechova (Greek transliteration of Jehovah)
        'Κύριος',         # Kyrios (used in Septuagint to replace YHWH)
    ],

    'Spanish': [
        'Jehová',         # Spanish transliteration
        'Yavé',           # Spanish pronunciation of Yahweh
    ],

    'Portuguese': [
        'Jeová',          # Portuguese transliteration
        'Javé',           # Portuguese Yahweh
    ],

    'German': [
        'Jehova',         # German transliteration
        'Jahwe',          # German Yahweh
    ],

    'French': [
        'Jéhovah',        # French transliteration
        'Yahvé',          # French Yahweh
    ],

    'Italian': [
        'Geova',          # Italian transliteration
        'Yahvè',          # Italian Yahweh
    ],

    'Russian': [
        'Иегова',         # Iegova (Jehovah in Cyrillic)
        'Яхве',           # Yakhve (Yahweh in Cyrillic)
    ],

    'Japanese': [
        'エホバ',          # Ehoba (Jehovah in katakana)
        'ヤハウェ',        # Yahawe (Yahweh in katakana)
    ],

    'Korean': [
        '여호와',          # Yeohowa (Jehovah in Hangul)
    ],

    'Chinese': [
        '耶和華',          # Yēhéhuá (Jehovah in Chinese)
        '雅威',           # Yǎwēi (Yahweh in Chinese)
    ],

    'Arabic': [
        'يهوه',           # Yahweh in Arabic script
        'الرب يهوه',      # Al-Rabb Yahweh (The Lord Yahweh)
    ],

    'Swahili': [
        'Yehova',         # Jehovah in Swahili
    ],
}


# Control concepts (non-divine names)
# Should NOT cluster at (1,1,1,1) - testing baseline
CONTROL_CONCEPTS = {
    'Hebrew': ['shalom (peace)', 'mayim (water)', 'lev (heart)'],
    'English': ['peace', 'water', 'heart'],
    'Greek': ['eirene (peace)', 'hydor (water)', 'kardia (heart)'],
    'Spanish': ['paz (peace)', 'agua (water)', 'corazón (heart)'],
    'Portuguese': ['paz (peace)', 'água (water)', 'coração (heart)'],
    'German': ['Friede (peace)', 'Wasser (water)', 'Herz (heart)'],
    'French': ['paix (peace)', 'eau (water)', 'cœur (heart)'],
    'Italian': ['pace (peace)', 'acqua (water)', 'cuore (heart)'],
    'Russian': ['мир (peace)', 'вода (water)', 'сердце (heart)'],
    'Japanese': ['平和 (peace)', '水 (water)', '心 (heart)'],
    'Korean': ['평화 (peace)', '물 (water)', '마음 (heart)'],
    'Chinese': ['和平 (peace)', '水 (water)', '心 (heart)'],
    'Arabic': ['سلام (peace)', 'ماء (water)', 'قلب (heart)'],
    'Swahili': ['amani (peace)', 'maji (water)', 'moyo (heart)'],
}


# =============================================================================
# EXPERIMENT FUNCTIONS
# =============================================================================

def get_coordinates_for_concept(generator: ClaudeAPIGenerator, concept: str,
                                language: str) -> SemanticCoordinate:
    """
    Get semantic coordinates for a concept.

    Args:
        generator: Claude API generator
        concept: The concept to measure
        language: Source language for context

    Returns:
        SemanticCoordinate for the concept
    """
    print(f"  Measuring: {concept} ({language})...", end=' ', flush=True)

    try:
        coord = generator.generate(concept, use_cache=True)
        if coord:
            print(f"✓ ({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) - d={coord.distance_to_anchor():.3f}")
            time.sleep(1)  # Rate limiting
            return coord
        else:
            print(f"✗ Failed to generate")
            return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def run_cross_linguistic_experiment(generator: ClaudeAPIGenerator) -> Dict:
    """
    Run the full cross-linguistic validation experiment.

    Returns:
        Dictionary with all results
    """
    results = {
        'divine': defaultdict(list),
        'control': defaultdict(list),
    }

    print("="*80)
    print("CROSS-LINGUISTIC VALIDATION EXPERIMENT")
    print("="*80)
    print()
    print("Testing: Does the NAME 'JEHOVAH' occupy (1,1,1,1) across all languages?")
    print()
    print("If the NAME is resonantly linked to the being at (1,1,1,1),")
    print("then YHWH, Yahweh, Jehovah, 耶和華, エホバ, etc. should all")
    print("point to the same coordinates - like different phonetic forms")
    print("of the same semantic/spiritual reality.")
    print()

    # Test divine names
    print("="*80)
    print("PART 1: THE NAME 'JEHOVAH' ACROSS LANGUAGES")
    print("="*80)
    print()

    for language, names in DIVINE_NAMES.items():
        print(f"\n{language} - Forms of 'JEHOVAH':")
        print("-" * 60)

        for name in names:
            coord = get_coordinates_for_concept(generator, name, language)
            if coord:
                results['divine'][language].append({
                    'name': name,
                    'coordinates': coord,
                    'distance': coord.distance_to_anchor(),
                })

    # Test control concepts
    print("\n" + "="*80)
    print("PART 2: CONTROL CONCEPTS (Should NOT be at Anchor)")
    print("="*80)
    print()

    for language, concepts in CONTROL_CONCEPTS.items():
        print(f"\n{language} Control Concepts:")
        print("-" * 60)

        for concept in concepts:
            coord = get_coordinates_for_concept(generator, concept, language)
            if coord:
                results['control'][language].append({
                    'name': concept,
                    'coordinates': coord,
                    'distance': coord.distance_to_anchor(),
                })

    return results


def calculate_statistics(results: Dict) -> Dict:
    """
    Calculate comprehensive statistics across languages.

    Args:
        results: Results from experiment

    Returns:
        Dictionary of statistics
    """
    stats = {}

    # Divine names statistics
    all_divine_distances = []
    for language, entries in results['divine'].items():
        distances = [e['distance'] for e in entries]
        all_divine_distances.extend(distances)

    if not all_divine_distances:
        print("ERROR: No divine name data collected!")
        return {'error': 'No data collected'}

    stats['divine'] = {
        'mean_distance': np.mean(all_divine_distances),
        'std_distance': np.std(all_divine_distances),
        'median_distance': np.median(all_divine_distances),
        'min_distance': np.min(all_divine_distances),
        'max_distance': np.max(all_divine_distances),
        'count': len(all_divine_distances),
        'within_0.3': sum(1 for d in all_divine_distances if d < 0.3),
        'within_0.5': sum(1 for d in all_divine_distances if d < 0.5),
    }

    # Control concepts statistics
    all_control_distances = []
    for language, entries in results['control'].items():
        distances = [e['distance'] for e in entries]
        all_control_distances.extend(distances)

    if not all_control_distances:
        stats['control'] = {
            'mean_distance': 0,
            'std_distance': 0,
            'median_distance': 0,
            'min_distance': 0,
            'max_distance': 0,
            'count': 0,
        }
    else:
        stats['control'] = {
            'mean_distance': np.mean(all_control_distances),
            'std_distance': np.std(all_control_distances),
            'median_distance': np.median(all_control_distances),
            'min_distance': np.min(all_control_distances),
            'max_distance': np.max(all_control_distances),
            'count': len(all_control_distances),
        }

    # Per-language statistics
    stats['by_language'] = {}
    for language in results['divine'].keys():
        divine_dist = [e['distance'] for e in results['divine'][language]]
        control_dist = [e['distance'] for e in results['control'].get(language, [])]

        stats['by_language'][language] = {
            'divine_mean': np.mean(divine_dist) if divine_dist else None,
            'divine_std': np.std(divine_dist) if divine_dist else None,
            'control_mean': np.mean(control_dist) if control_dist else None,
            'control_std': np.std(control_dist) if control_dist else None,
        }

    # Statistical test: Are divine names significantly closer than controls?
    from scipy import stats as scipy_stats

    if all_divine_distances and all_control_distances:
        # T-test: divine vs control distances
        t_stat, p_value = scipy_stats.ttest_ind(all_divine_distances, all_control_distances)
        stats['t_test'] = {
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
        }

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(
            (stats['divine']['std_distance']**2 + stats['control']['std_distance']**2) / 2
        )
        cohens_d = (stats['control']['mean_distance'] - stats['divine']['mean_distance']) / pooled_std
        stats['effect_size'] = cohens_d

    return stats


def print_results(results: Dict, stats: Dict):
    """Print comprehensive results and analysis."""

    print("\n" + "="*80)
    print("RESULTS: CROSS-LINGUISTIC VALIDATION")
    print("="*80)
    print()

    if 'error' in stats:
        print(f"❌ EXPERIMENT FAILED: {stats['error']}")
        print("\nPlease check:")
        print("  1. ANTHROPIC_API_KEY is set correctly")
        print("  2. API key is valid and has credits")
        print("  3. Network connection is working")
        return

    # Summary statistics
    print("SUMMARY STATISTICS")
    print("-" * 60)
    print()
    print(f"Divine Names (n={stats['divine']['count']}):")
    print(f"  Mean distance from (1,1,1,1): {stats['divine']['mean_distance']:.4f}")
    print(f"  Std deviation: {stats['divine']['std_distance']:.4f}")
    print(f"  Median distance: {stats['divine']['median_distance']:.4f}")
    print(f"  Range: [{stats['divine']['min_distance']:.4f}, {stats['divine']['max_distance']:.4f}]")
    print(f"  Within 0.3 of Anchor: {stats['divine']['within_0.3']}/{stats['divine']['count']} ({100*stats['divine']['within_0.3']/stats['divine']['count']:.1f}%)")
    print(f"  Within 0.5 of Anchor: {stats['divine']['within_0.5']}/{stats['divine']['count']} ({100*stats['divine']['within_0.5']/stats['divine']['count']:.1f}%)")
    print()

    print(f"Control Concepts (n={stats['control']['count']}):")
    print(f"  Mean distance from (1,1,1,1): {stats['control']['mean_distance']:.4f}")
    print(f"  Std deviation: {stats['control']['std_distance']:.4f}")
    print(f"  Median distance: {stats['control']['median_distance']:.4f}")
    print(f"  Range: [{stats['control']['min_distance']:.4f}, {stats['control']['max_distance']:.4f}]")
    print()

    # Statistical significance
    if 't_test' in stats:
        print("STATISTICAL COMPARISON")
        print("-" * 60)
        print()
        print(f"T-test (Divine vs Control distances):")
        print(f"  t-statistic: {stats['t_test']['t_statistic']:.4f}")
        print(f"  p-value: {stats['t_test']['p_value']:.6f}")
        print(f"  Significant: {'✅ YES' if stats['t_test']['significant'] else '❌ NO'}")
        print()
        print(f"Effect Size (Cohen's d): {stats['effect_size']:.4f}")
        if abs(stats['effect_size']) > 0.8:
            print("  Interpretation: 🔥 LARGE effect")
        elif abs(stats['effect_size']) > 0.5:
            print("  Interpretation: ⚡ MEDIUM effect")
        else:
            print("  Interpretation: ⚠️  SMALL effect")
        print()

    # Per-language breakdown
    print("PER-LANGUAGE BREAKDOWN")
    print("-" * 60)
    print()
    print(f"{'Language':<15} {'Divine Mean':<15} {'Control Mean':<15} {'Difference':<15}")
    print("-" * 60)

    for language in sorted(stats['by_language'].keys()):
        lang_stats = stats['by_language'][language]
        divine_mean = lang_stats['divine_mean']
        control_mean = lang_stats['control_mean']

        if divine_mean is not None and control_mean is not None:
            diff = control_mean - divine_mean
            print(f"{language:<15} {divine_mean:<15.4f} {control_mean:<15.4f} {diff:<15.4f}")
        elif divine_mean is not None:
            print(f"{language:<15} {divine_mean:<15.4f} {'N/A':<15} {'N/A':<15}")

    print()

    # Top 10 closest to Anchor
    print("TOP 10 CLOSEST TO ANCHOR POINT (1,1,1,1)")
    print("-" * 60)
    print()

    all_divine = []
    for language, entries in results['divine'].items():
        for entry in entries:
            all_divine.append((
                entry['name'],
                language,
                entry['distance'],
                entry['coordinates']
            ))

    all_divine.sort(key=lambda x: x[2])  # Sort by distance

    print(f"{'Rank':<6} {'Name':<20} {'Language':<15} {'Distance':<12} {'Coordinates'}")
    print("-" * 80)

    for i, (name, language, distance, coord) in enumerate(all_divine[:10], 1):
        coords_str = f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f})"
        print(f"{i:<6} {name:<20} {language:<15} {distance:<12.4f} {coords_str}")

    print()

    # Hypothesis evaluation
    print("="*80)
    print("HYPOTHESIS EVALUATION")
    print("="*80)
    print()
    print("Hypothesis: The NAME 'JEHOVAH' (YHWH/Yahweh) resonates at (1,1,1,1)")
    print("            across ALL languages, scripts, and transliterations")
    print()

    # Criteria for validation
    divine_mean = stats['divine']['mean_distance']
    control_mean = stats['control']['mean_distance']
    p_value = stats['t_test']['p_value'] if 't_test' in stats else 1.0

    criteria = [
        ("Divine names closer than controls", divine_mean < control_mean),
        ("Divine mean distance < 0.5", divine_mean < 0.5),
        ("Statistically significant (p < 0.05)", p_value < 0.05),
        ("Large effect size (|d| > 0.8)", abs(stats.get('effect_size', 0)) > 0.8),
        ("Majority within 0.5 of Anchor", stats['divine']['within_0.5']/stats['divine']['count'] > 0.5),
    ]

    passed = 0
    for criterion, result in criteria:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {criterion}")
        if result:
            passed += 1

    print()
    print(f"Criteria Passed: {passed}/{len(criteria)}")
    print()

    if passed >= 4:
        print("🎯 HYPOTHESIS VALIDATED!")
        print()
        print("The NAME 'JEHOVAH' resonates at (1,1,1,1) across languages!")
        print()
        print("YHWH, Yahweh, Jehovah, 耶和華, エホバ, Иегова, etc.")
        print("ALL point to the same coordinates, regardless of:")
        print("  • Language/script (Hebrew, Greek, Chinese, Japanese, Arabic...)")
        print("  • Pronunciation (Yahweh vs Jehovah)")
        print("  • Alphabet (Latin, Cyrillic, Chinese, Katakana, Arabic...)")
        print()
        print("This is NOT English-specific bias.")
        print("This is NOT cultural conditioning.")
        print()
        print("The NAME itself carries the resonant signature of (1,1,1,1).")
        print("Like water is H2O in any language, JEHOVAH IS the Anchor Point.")
    elif passed >= 2:
        print("⚡ HYPOTHESIS PARTIALLY SUPPORTED")
        print()
        print("Some evidence for cross-linguistic clustering of the NAME,")
        print("but results not conclusive across all criteria.")
    else:
        print("❌ HYPOTHESIS NOT SUPPORTED")
        print()
        print("The NAME does not show consistent clustering across languages.")

    print()
    print("="*80)


def save_results(results: Dict, stats: Dict, output_file: str = "results/cross_linguistic_validation.txt"):
    """Save detailed results to file."""

    os.makedirs("results", exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("CROSS-LINGUISTIC VALIDATION OF THE ANCHOR POINT\n")
        f.write("="*80 + "\n\n")

        f.write("DIVINE NAMES BY LANGUAGE\n")
        f.write("-"*80 + "\n\n")

        for language in sorted(results['divine'].keys()):
            f.write(f"{language}:\n")
            for entry in results['divine'][language]:
                coord = entry['coordinates']
                f.write(f"  {entry['name']:<20} ")
                f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) ")
                f.write(f"distance={entry['distance']:.4f}\n")
            f.write("\n")

        f.write("\nCONTROL CONCEPTS BY LANGUAGE\n")
        f.write("-"*80 + "\n\n")

        for language in sorted(results['control'].keys()):
            f.write(f"{language}:\n")
            for entry in results['control'][language]:
                coord = entry['coordinates']
                f.write(f"  {entry['name']:<20} ")
                f.write(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) ")
                f.write(f"distance={entry['distance']:.4f}\n")
            f.write("\n")

        f.write("\nSTATISTICS\n")
        f.write("-"*80 + "\n\n")
        f.write(f"Divine Names: mean={stats['divine']['mean_distance']:.4f}, ")
        f.write(f"std={stats['divine']['std_distance']:.4f}, ")
        f.write(f"n={stats['divine']['count']}\n")
        f.write(f"Control Concepts: mean={stats['control']['mean_distance']:.4f}, ")
        f.write(f"std={stats['control']['std_distance']:.4f}, ")
        f.write(f"n={stats['control']['count']}\n\n")

        if 't_test' in stats:
            f.write(f"T-test: t={stats['t_test']['t_statistic']:.4f}, ")
            f.write(f"p={stats['t_test']['p_value']:.6f}\n")
            f.write(f"Effect size (Cohen's d): {stats['effect_size']:.4f}\n")

    print(f"\n✅ Results saved to: {output_file}")


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""

    print("="*80)
    print("CROSS-LINGUISTIC VALIDATION OF THE ANCHOR POINT")
    print("="*80)
    print()
    print("This experiment tests whether the NAME 'JEHOVAH' (and its equivalents)")
    print("occupies (1,1,1,1) across multiple languages.")
    print()
    print("Key Question: If JEHOVAH is truly at the Anchor Point, then His NAME")
    print("in ANY language should carry the same semantic/resonant signature.")
    print()
    print("We are NOT testing generic words for 'god' - we're testing the")
    print("SPECIFIC NAME: YHWH, Yahweh, Jehovah, and its transliterations.")
    print()
    print(f"Testing {sum(len(names) for names in DIVINE_NAMES.values())} forms of the NAME")
    print(f"across {len(DIVINE_NAMES)} languages/scripts")
    print(f"Plus {sum(len(names) for names in CONTROL_CONCEPTS.values())} control concepts")
    print()

    # Initialize API
    from dotenv import load_dotenv
    load_dotenv()

    generator = ClaudeAPIGenerator()

    # Run experiment
    results = run_cross_linguistic_experiment(generator)

    # Calculate statistics
    stats = calculate_statistics(results)

    # Print results
    print_results(results, stats)

    # Save results
    save_results(results, stats)

    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE")
    print("="*80)
    print()


if __name__ == "__main__":
    main()
