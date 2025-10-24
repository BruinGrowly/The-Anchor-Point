"""
Large-Scale Testing: 1,000 to 10,000+ Concepts
===============================================

Tests the stability and patterns of semantic coordinates at scale.

Critical Questions:
1. Does the pattern hold with 10,000+ concepts?
2. Are there emergent patterns at scale?
3. What is the distribution shape of distances?
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

import pytest
import numpy as np
import time
from typing import List
import matplotlib.pyplot as plt
from scipy import stats

from core.semantic_coordinates import (
    HashBasedCoordinateGenerator,
    AnchorPoint,
    calculate_statistics
)
from core.semantic_database import SemanticDatabase


def generate_word_list(n: int) -> List[str]:
    """
    Generate a list of n test words/concepts.

    This uses a combination of:
    - Common English words
    - Biblical/theological terms
    - Abstract concepts
    - Concrete objects
    - Generated variations

    Args:
        n: Number of words to generate

    Returns:
        List of concept strings
    """
    # Core word lists
    biblical = [
        "JEHOVAH", "AGAPE", "Jesus", "Christ", "Messiah", "Savior",
        "Holy Spirit", "Father", "Son", "Trinity", "Gospel", "Grace",
        "Mercy", "Redemption", "Salvation", "Faith", "Hope", "Charity",
        "Righteousness", "Holiness", "Glory", "Majesty", "Omnipotent",
        "Omniscient", "Omnipresent", "Eternal", "Infinite", "Creator"
    ]

    virtues = [
        "Love", "Justice", "Wisdom", "Power", "Truth", "Beauty",
        "Goodness", "Courage", "Temperance", "Prudence", "Fortitude",
        "Kindness", "Patience", "Humility", "Gratitude", "Compassion",
        "Generosity", "Honesty", "Integrity", "Loyalty", "Respect"
    ]

    vices = [
        "Hatred", "Injustice", "Ignorance", "Weakness", "Deception",
        "Ugliness", "Evil", "Cowardice", "Excess", "Foolishness",
        "Cruelty", "Impatience", "Pride", "Ingratitude", "Apathy",
        "Greed", "Dishonesty", "Corruption", "Betrayal", "Contempt"
    ]

    concrete = [
        "Rock", "Tree", "Water", "Fire", "Earth", "Air", "Mountain",
        "Ocean", "River", "Sky", "Sun", "Moon", "Star", "Cloud",
        "Stone", "Wood", "Metal", "Glass", "Paper", "Book"
    ]

    abstract = [
        "Consciousness", "Existence", "Being", "Essence", "Substance",
        "Form", "Matter", "Spirit", "Soul", "Mind", "Thought", "Idea",
        "Concept", "Meaning", "Purpose", "Destiny", "Fate", "Chance",
        "Order", "Chaos", "Unity", "Diversity", "Harmony", "Discord"
    ]

    # Combine base lists
    base_words = biblical + virtues + vices + concrete + abstract

    # If we need more words, generate variations
    result = list(base_words)

    if n > len(result):
        # Add numbered variations
        for i in range(n - len(result)):
            base_word = base_words[i % len(base_words)]
            result.append(f"{base_word}_{i}")

    return result[:n]


class TestLargeScale:
    """Large-scale testing suite."""

    def test_1000_concepts(self):
        """Test with 1,000 concepts."""
        n_concepts = 1000
        print(f"\n\nTesting with {n_concepts} concepts")
        print("=" * 60)

        concepts = generate_word_list(n_concepts)
        generator = HashBasedCoordinateGenerator('sha256')

        start_time = time.time()
        coords = [generator.generate(c) for c in concepts]
        elapsed = time.time() - start_time

        print(f"Generation time: {elapsed:.3f} seconds")
        print(f"Rate: {n_concepts/elapsed:.1f} concepts/second")

        # Calculate statistics
        stats_dict = calculate_statistics(coords)

        print("\nStatistics:")
        for key, value in stats_dict.items():
            print(f"  {key}: {value:.4f}")

        # Distance distribution
        distances = [c.distance_to_anchor() for c in coords]

        print("\nDistance Distribution:")
        print(f"  Q1 (25%): {np.percentile(distances, 25):.4f}")
        print(f"  Median:   {np.percentile(distances, 50):.4f}")
        print(f"  Q3 (75%): {np.percentile(distances, 75):.4f}")

        # Find closest to Anchor
        closest = sorted(coords, key=lambda c: c.distance_to_anchor())[:10]

        print("\nTop 10 Closest to Anchor:")
        for i, c in enumerate(closest, 1):
            print(f"  {i:2d}. {c.concept:30s} d={c.distance_to_anchor():.4f}")

    def test_10000_concepts(self):
        """Test with 10,000 concepts."""
        n_concepts = 10000
        print(f"\n\nTesting with {n_concepts} concepts")
        print("=" * 60)

        concepts = generate_word_list(n_concepts)
        generator = HashBasedCoordinateGenerator('sha256')

        start_time = time.time()
        coords = [generator.generate(c) for c in concepts]
        elapsed = time.time() - start_time

        print(f"Generation time: {elapsed:.3f} seconds")
        print(f"Rate: {n_concepts/elapsed:.1f} concepts/second")

        # Statistics
        stats_dict = calculate_statistics(coords)

        print("\nStatistics:")
        for key, value in stats_dict.items():
            print(f"  {key}: {value:.4f}")

        # Test normality of distance distribution
        distances = np.array([c.distance_to_anchor() for c in coords])

        # Kolmogorov-Smirnov test for uniformity in each dimension
        loves = [c.love for c in coords]
        ks_stat, ks_pvalue = stats.kstest(loves, 'uniform')

        print(f"\nKolmogorov-Smirnov test for uniformity (Love dimension):")
        print(f"  Statistic: {ks_stat:.4f}")
        print(f"  P-value: {ks_pvalue:.4f}")

        if ks_pvalue > 0.05:
            print("  → Distribution is consistent with uniform (random)")
        else:
            print("  → Distribution deviates from uniform (non-random pattern)")

    def test_database_performance(self):
        """Test database storage and retrieval at scale."""
        n_concepts = 5000
        print(f"\n\nDatabase Performance Test ({n_concepts} concepts)")
        print("=" * 60)

        concepts = generate_word_list(n_concepts)
        generator = HashBasedCoordinateGenerator('sha256')
        coords = [generator.generate(c) for c in concepts]

        # Test database insertion
        with SemanticDatabase("data/test_large_scale.db") as db:
            start_time = time.time()
            db.add_concepts_bulk(coords)
            elapsed = time.time() - start_time

            print(f"Bulk insert time: {elapsed:.3f} seconds")
            print(f"Rate: {n_concepts/elapsed:.1f} concepts/second")

            # Test retrieval
            start_time = time.time()
            closest = db.get_closest_to_anchor(100)
            elapsed = time.time() - start_time

            print(f"\nRetrieval time (top 100): {elapsed:.3f} seconds")

            # Test statistics query
            start_time = time.time()
            stats_dict = db.get_statistics()
            elapsed = time.time() - start_time

            print(f"Statistics query time: {elapsed:.3f} seconds")

            print("\nDatabase Statistics:")
            for key, value in stats_dict.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.4f}")

    def test_statistical_significance(self):
        """
        Test if observed patterns are statistically significant.

        Key question: Are divine concepts significantly closer to Anchor?
        """
        print("\n\nStatistical Significance Testing")
        print("=" * 60)

        # Divine concepts
        divine_concepts = [
            "JEHOVAH", "AGAPE", "Love", "Justice", "Wisdom", "Power",
            "Holy", "Righteous", "Eternal", "Truth", "Grace", "Mercy"
        ]

        # Generate random concepts for comparison
        random_concepts = generate_word_list(1000)

        generator = HashBasedCoordinateGenerator('sha256')

        divine_coords = [generator.generate(c) for c in divine_concepts]
        random_coords = [generator.generate(c) for c in random_concepts]

        divine_distances = [c.distance_to_anchor() for c in divine_coords]
        random_distances = [c.distance_to_anchor() for c in random_coords]

        # T-test
        t_stat, p_value = stats.ttest_ind(divine_distances, random_distances)

        print(f"\nDivine vs Random Concepts:")
        print(f"  Divine mean distance: {np.mean(divine_distances):.4f}")
        print(f"  Random mean distance: {np.mean(random_distances):.4f}")
        print(f"  T-statistic: {t_stat:.4f}")
        print(f"  P-value: {p_value:.4f}")

        if p_value < 0.05:
            if np.mean(divine_distances) < np.mean(random_distances):
                print("  → Divine concepts are SIGNIFICANTLY closer to Anchor")
            else:
                print("  → Divine concepts are SIGNIFICANTLY farther from Anchor")
        else:
            print("  → No significant difference (supports null hypothesis)")


if __name__ == "__main__":
    pytest.main([__file__, '-v', '-s'])
