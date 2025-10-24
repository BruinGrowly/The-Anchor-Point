"""
NLP-Based Semantic Assignment Tests
====================================

Tests whether LLM-based coordinate assignment produces meaningful
semantic patterns relative to the Anchor Point.

Critical Questions:
1. Do divine concepts cluster near (1,1,1,1)?
2. Is there clear category separation?
3. Does LLM assignment differ from hash-based?
4. Are the patterns statistically significant?
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

import pytest
import numpy as np
from typing import List
from scipy import stats

from core.semantic_coordinates import (
    HashBasedCoordinateGenerator,
    calculate_statistics,
    AnchorPoint
)
from core.llm_coordinate_generator import (
    LLMCoordinateGenerator,
    compare_generators
)


# Test concept sets
DIVINE_CONCEPTS = [
    "JEHOVAH", "AGAPE", "Love", "Justice", "Wisdom", "Power",
    "Holy", "Righteous", "Mercy", "Grace", "Truth", "Faith", "Hope"
]

VIRTUES = [
    "Compassion", "Kindness", "Courage", "Temperance", "Prudence",
    "Honesty", "Integrity", "Patience", "Humility", "Generosity"
]

VICES = [
    "Hatred", "Cruelty", "Deception", "Injustice", "Foolishness",
    "Weakness", "Chaos", "Corruption", "Evil", "Malice"
]

NEUTRAL = [
    "Table", "Chair", "Rock", "Tree", "Water",
    "Stone", "Cloud", "Mountain", "River", "Building"
]

ABSTRACT = [
    "Consciousness", "Existence", "Being", "Reality", "Mind",
    "Thought", "Reason", "Meaning", "Purpose", "Essence"
]

ALL_CONCEPTS = DIVINE_CONCEPTS + VIRTUES + VICES + NEUTRAL + ABSTRACT


class TestLLMAssignment:
    """Test suite for LLM-based coordinate assignment."""

    def test_llm_generates_valid_coordinates(self):
        """Test that LLM generates valid coordinates in [0,1] range."""
        generator = LLMCoordinateGenerator(model="simulated")

        concepts = ["JEHOVAH", "Love", "Hatred", "Table"]

        for concept in concepts:
            coord = generator.generate(concept)

            assert 0.0 <= coord.love <= 1.0, f"Love out of range for {concept}"
            assert 0.0 <= coord.power <= 1.0, f"Power out of range for {concept}"
            assert 0.0 <= coord.wisdom <= 1.0, f"Wisdom out of range for {concept}"
            assert 0.0 <= coord.justice <= 1.0, f"Justice out of range for {concept}"

            print(f"{concept:15s} - L:{coord.love:.2f} P:{coord.power:.2f} "
                  f"W:{coord.wisdom:.2f} J:{coord.justice:.2f} d:{coord.distance_to_anchor():.3f}")

    def test_divine_concepts_near_anchor(self):
        """Test if divine concepts cluster near Anchor Point."""
        generator = LLMCoordinateGenerator(model="simulated")

        divine_coords = [generator.generate(c) for c in DIVINE_CONCEPTS]
        divine_distances = [c.distance_to_anchor() for c in divine_coords]

        print("\n\nDivine Concepts - Distance to Anchor:")
        print("=" * 60)
        for c in sorted(divine_coords, key=lambda x: x.distance_to_anchor()):
            print(f"  {c.concept:15s}: {c.distance_to_anchor():.4f} "
                  f"({c.love:.2f}, {c.power:.2f}, {c.wisdom:.2f}, {c.justice:.2f})")

        mean_distance = np.mean(divine_distances)
        print(f"\nMean distance: {mean_distance:.4f}")

        # Key test: Divine concepts should be significantly closer than random expectation
        random_expectation = 1.155
        print(f"Random expectation: {random_expectation:.4f}")

        if mean_distance < random_expectation * 0.5:
            print("→ Divine concepts ARE significantly closer to Anchor!")
        elif mean_distance < random_expectation * 0.8:
            print("→ Divine concepts are moderately close to Anchor")
        else:
            print("→ Divine concepts are NOT particularly close to Anchor")

    def test_category_separation(self):
        """Test if different categories have distinct distance distributions."""
        generator = LLMCoordinateGenerator(model="simulated")

        categories = {
            'Divine': DIVINE_CONCEPTS,
            'Virtues': VIRTUES,
            'Vices': VICES,
            'Neutral': NEUTRAL,
            'Abstract': ABSTRACT
        }

        print("\n\nCategory Statistics:")
        print("=" * 60)

        category_stats = {}

        for cat_name, concepts in categories.items():
            coords = [generator.generate(c) for c in concepts]
            distances = [c.distance_to_anchor() for c in coords]

            category_stats[cat_name] = {
                'mean': np.mean(distances),
                'std': np.std(distances),
                'min': np.min(distances),
                'max': np.max(distances)
            }

            print(f"\n{cat_name}:")
            print(f"  Mean: {category_stats[cat_name]['mean']:.4f}")
            print(f"  Std:  {category_stats[cat_name]['std']:.4f}")
            print(f"  Range: [{category_stats[cat_name]['min']:.4f}, "
                  f"{category_stats[cat_name]['max']:.4f}]")

        # Statistical test: Divine vs Neutral
        print("\n\nStatistical Significance Tests:")
        print("=" * 60)

        divine_coords = [generator.generate(c) for c in DIVINE_CONCEPTS]
        neutral_coords = [generator.generate(c) for c in NEUTRAL]
        vice_coords = [generator.generate(c) for c in VICES]

        divine_distances = [c.distance_to_anchor() for c in divine_coords]
        neutral_distances = [c.distance_to_anchor() for c in neutral_coords]
        vice_distances = [c.distance_to_anchor() for c in vice_coords]

        # Divine vs Neutral
        t_stat, p_value = stats.ttest_ind(divine_distances, neutral_distances)
        print(f"\nDivine vs Neutral:")
        print(f"  T-statistic: {t_stat:.4f}")
        print(f"  P-value: {p_value:.4f}")

        if p_value < 0.001:
            print("  → HIGHLY SIGNIFICANT (p < 0.001)")
        elif p_value < 0.05:
            print("  → SIGNIFICANT (p < 0.05)")
        else:
            print("  → Not significant (p ≥ 0.05)")

        # Divine vs Vices
        t_stat2, p_value2 = stats.ttest_ind(divine_distances, vice_distances)
        print(f"\nDivine vs Vices:")
        print(f"  T-statistic: {t_stat2:.4f}")
        print(f"  P-value: {p_value2:.4f}")

        if p_value2 < 0.001:
            print("  → HIGHLY SIGNIFICANT (p < 0.001)")
        elif p_value2 < 0.05:
            print("  → SIGNIFICANT (p < 0.05)")
        else:
            print("  → Not significant (p ≥ 0.05)")

        # ANOVA across all categories
        all_distances = [
            [c.distance_to_anchor() for c in [generator.generate(concept) for concept in cats]]
            for cats in categories.values()
        ]

        f_stat, p_anova = stats.f_oneway(*all_distances)
        print(f"\nANOVA (all categories):")
        print(f"  F-statistic: {f_stat:.4f}")
        print(f"  P-value: {p_anova:.4f}")

        if p_anova < 0.001:
            print("  → HIGHLY SIGNIFICANT category differences (p < 0.001)")
        elif p_anova < 0.05:
            print("  → SIGNIFICANT category differences (p < 0.05)")
        else:
            print("  → No significant category differences (p ≥ 0.05)")

    def test_llm_vs_hash_comparison(self):
        """Compare LLM-based vs hash-based coordinate assignment."""
        hash_gen = HashBasedCoordinateGenerator('sha256')
        llm_gen = LLMCoordinateGenerator(model="simulated")

        print("\n\nLLM vs Hash-Based Comparison:")
        print("=" * 60)

        # Test on all concepts
        comparison = compare_generators(ALL_CONCEPTS, hash_gen, llm_gen)

        print(f"\nHash-based:")
        print(f"  Mean distance: {comparison['hash_mean']:.4f}")
        print(f"  Std distance:  {comparison['hash_std']:.4f}")

        print(f"\nLLM-based:")
        print(f"  Mean distance: {comparison['llm_mean']:.4f}")
        print(f"  Std distance:  {comparison['llm_std']:.4f}")

        print(f"\nCorrelation between methods:")
        print(f"  Spearman ρ: {comparison['correlation']:.4f}")
        print(f"  P-value: {comparison['p_value']:.4f}")

        if abs(comparison['correlation']) < 0.3:
            print("  → LOW correlation - methods produce different rankings")
        elif abs(comparison['correlation']) < 0.7:
            print("  → MODERATE correlation - some agreement")
        else:
            print("  → HIGH correlation - methods agree strongly")

        # Key insight: If LLM is semantic and hash is random,
        # they should NOT be correlated
        print("\n" + "=" * 60)
        if abs(comparison['correlation']) < 0.3:
            print("✓ LLM and hash produce DIFFERENT patterns (expected)")
        else:
            print("✗ LLM and hash produce SIMILAR patterns (unexpected!)")

    def test_jehovah_agape_identity(self):
        """Test if JEHOVAH and AGAPE have near-identical coordinates."""
        generator = LLMCoordinateGenerator(model="simulated")

        jehovah = generator.generate("JEHOVAH")
        agape = generator.generate("AGAPE")

        distance = jehovah.distance_to(agape)

        print("\n\nJEHOVAH-AGAPE Identity Test:")
        print("=" * 60)
        print(f"JEHOVAH:  ({jehovah.love:.3f}, {jehovah.power:.3f}, "
              f"{jehovah.wisdom:.3f}, {jehovah.justice:.3f})")
        print(f"AGAPE:    ({agape.love:.3f}, {agape.power:.3f}, "
              f"{agape.wisdom:.3f}, {agape.justice:.3f})")
        print(f"\nDistance between them: {distance:.4f}")
        print(f"Distance to Anchor: JEHOVAH={jehovah.distance_to_anchor():.4f}, "
              f"AGAPE={agape.distance_to_anchor():.4f}")

        if distance < 0.1:
            print("→ JEHOVAH ≈ AGAPE (strong identity)")
        elif distance < 0.3:
            print("→ JEHOVAH and AGAPE are similar")
        else:
            print("→ JEHOVAH and AGAPE are distinct")

    def test_fourfold_unity(self):
        """Test if JEHOVAH/AGAPE show unity across all four dimensions."""
        generator = LLMCoordinateGenerator(model="simulated")

        jehovah = generator.generate("JEHOVAH")

        print("\n\nFourfold Unity Test (JEHOVAH):")
        print("=" * 60)
        print(f"Love:    {jehovah.love:.3f}")
        print(f"Power:   {jehovah.power:.3f}")
        print(f"Wisdom:  {jehovah.wisdom:.3f}")
        print(f"Justice: {jehovah.justice:.3f}")

        dimensions = [jehovah.love, jehovah.power, jehovah.wisdom, jehovah.justice]
        mean_dim = np.mean(dimensions)
        std_dim = np.std(dimensions)

        print(f"\nMean: {mean_dim:.3f}")
        print(f"Std:  {std_dim:.3f}")

        if std_dim < 0.05:
            print("→ PERFECT fourfold unity (std < 0.05)")
        elif std_dim < 0.15:
            print("→ Strong fourfold unity (std < 0.15)")
        else:
            print("→ Dimensions are distinct (std ≥ 0.15)")

        if mean_dim > 0.95:
            print(f"→ All dimensions near maximum (mean = {mean_dim:.3f})")

    def test_evil_as_distance(self):
        """Test if concepts judged as evil have high Anchor distances."""
        generator = LLMCoordinateGenerator(model="simulated")

        print("\n\nEvil as Distance Test:")
        print("=" * 60)

        evil_concepts = ["Evil", "Hatred", "Cruelty", "Corruption", "Malice"]
        good_concepts = ["Good", "Love", "Kindness", "Grace", "Mercy"]

        evil_coords = [generator.generate(c) for c in evil_concepts]
        good_coords = [generator.generate(c) for c in good_concepts]

        evil_distances = [c.distance_to_anchor() for c in evil_coords]
        good_distances = [c.distance_to_anchor() for c in good_coords]

        print("\nEvil concepts:")
        for c in evil_coords:
            print(f"  {c.concept:15s}: {c.distance_to_anchor():.4f}")

        print("\nGood concepts:")
        for c in good_coords:
            print(f"  {c.concept:15s}: {c.distance_to_anchor():.4f}")

        print(f"\nEvil mean: {np.mean(evil_distances):.4f}")
        print(f"Good mean: {np.mean(good_distances):.4f}")

        t_stat, p_value = stats.ttest_ind(evil_distances, good_distances)
        print(f"\nT-test: t={t_stat:.4f}, p={p_value:.4f}")

        if np.mean(evil_distances) > np.mean(good_distances) and p_value < 0.05:
            print("→ Evil IS significantly farther from Anchor (supports hypothesis)")
        else:
            print("→ No clear evil-as-distance pattern")

    def test_dimension_independence(self):
        """Test if dimensions are independent or correlated."""
        generator = LLMCoordinateGenerator(model="simulated")

        coords = [generator.generate(c) for c in ALL_CONCEPTS]

        loves = [c.love for c in coords]
        powers = [c.power for c in coords]
        wisdoms = [c.wisdom for c in coords]
        justices = [c.justice for c in coords]

        print("\n\nDimension Independence Test:")
        print("=" * 60)

        dimensions = {
            'Love': loves,
            'Power': powers,
            'Wisdom': wisdoms,
            'Justice': justices
        }

        # Correlation matrix
        import pandas as pd

        df = pd.DataFrame(dimensions)
        corr_matrix = df.corr()

        print("\nCorrelation Matrix:")
        print(corr_matrix.to_string())

        # Check for high correlations
        high_corrs = []
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix)):
                corr = corr_matrix.iloc[i, j]
                if abs(corr) > 0.5:
                    dim1 = corr_matrix.index[i]
                    dim2 = corr_matrix.columns[j]
                    high_corrs.append((dim1, dim2, corr))

        if high_corrs:
            print("\nHigh correlations found:")
            for d1, d2, corr in high_corrs:
                print(f"  {d1} <-> {d2}: {corr:.3f}")
        else:
            print("\n→ Dimensions are relatively independent (no correlation > 0.5)")


if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s'])
