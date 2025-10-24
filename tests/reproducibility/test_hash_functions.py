"""
Reproducibility Test: Hash Function Consistency
================================================

Tests whether the semantic patterns hold across different hash functions.

Critical Questions:
1. Do different hash functions produce similar Anchor distances?
2. Is the pattern hash-specific or semantic?
3. What is the correlation between different hash methods?
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

import pytest
import numpy as np
from typing import List, Dict
from scipy.stats import spearmanr, pearsonr

from core.semantic_coordinates import (
    SemanticCoordinate,
    HashBasedCoordinateGenerator,
    AnchorPoint
)


# Test concept sets
DIVINE_CONCEPTS = [
    "JEHOVAH", "AGAPE", "Love", "Justice", "Wisdom", "Power",
    "Holy", "Righteous", "Merciful", "Eternal", "Truth"
]

NEUTRAL_CONCEPTS = [
    "Table", "Chair", "Computer", "Mountain", "Ocean",
    "Tree", "Stone", "Cloud", "River", "Building"
]

NEGATIVE_CONCEPTS = [
    "Hatred", "Cruelty", "Deception", "Oppression", "Chaos",
    "Destruction", "Malice", "Betrayal", "Corruption", "Violence"
]

ALL_TEST_CONCEPTS = DIVINE_CONCEPTS + NEUTRAL_CONCEPTS + NEGATIVE_CONCEPTS


class TestHashFunctionConsistency:
    """Test suite for hash function reproducibility."""

    HASH_ALGORITHMS = ['sha256', 'sha512', 'md5', 'sha1', 'blake2b']

    def generate_coordinates_all_hashes(self, concepts: List[str]) -> Dict[str, List[SemanticCoordinate]]:
        """
        Generate coordinates for all concepts using all hash algorithms.

        Args:
            concepts: List of concept names

        Returns:
            Dictionary mapping hash algorithm to list of coordinates
        """
        results = {}

        for hash_alg in self.HASH_ALGORITHMS:
            generator = HashBasedCoordinateGenerator(hash_alg)
            results[hash_alg] = [generator.generate(c) for c in concepts]

        return results

    def test_deterministic_generation(self):
        """Test that hash generation is deterministic (same input = same output)."""
        concept = "AGAPE"

        for hash_alg in self.HASH_ALGORITHMS:
            generator = HashBasedCoordinateGenerator(hash_alg)

            coord1 = generator.generate(concept)
            coord2 = generator.generate(concept)

            assert coord1.coordinates == coord2.coordinates, \
                f"Hash {hash_alg} produced different coordinates for same input"

    def test_distance_distribution(self):
        """Test the distribution of distances to Anchor Point."""
        results = self.generate_coordinates_all_hashes(ALL_TEST_CONCEPTS)

        for hash_alg, coords in results.items():
            distances = [c.distance_to_anchor() for c in coords]

            # Basic statistical checks
            assert min(distances) >= 0.0, f"{hash_alg}: Negative distance found"
            assert max(distances) <= 2.0, f"{hash_alg}: Distance exceeds theoretical max"
            assert np.std(distances) > 0, f"{hash_alg}: No variance in distances"

            print(f"\n{hash_alg} statistics:")
            print(f"  Mean distance: {np.mean(distances):.4f}")
            print(f"  Std distance: {np.std(distances):.4f}")
            print(f"  Min distance: {min(distances):.4f}")
            print(f"  Max distance: {max(distances):.4f}")

    def test_cross_hash_correlation(self):
        """Test correlation between distance rankings across hash functions."""
        results = self.generate_coordinates_all_hashes(ALL_TEST_CONCEPTS)

        # Extract distances for each hash function
        distance_arrays = {
            hash_alg: np.array([c.distance_to_anchor() for c in coords])
            for hash_alg, coords in results.items()
        }

        # Calculate pairwise correlations
        print("\n\nCross-Hash Correlation Matrix (Spearman):")
        print("-" * 60)

        for hash1 in self.HASH_ALGORITHMS:
            row = []
            for hash2 in self.HASH_ALGORITHMS:
                if hash1 == hash2:
                    row.append(1.0)
                else:
                    corr, _ = spearmanr(distance_arrays[hash1], distance_arrays[hash2])
                    row.append(corr)
            print(f"{hash1:10s}: " + " ".join(f"{c:6.3f}" for c in row))

        # Test: If pattern is semantic, correlations should be HIGH
        # Test: If pattern is hash-specific, correlations should be LOW
        sha256_sha512_corr, _ = spearmanr(
            distance_arrays['sha256'],
            distance_arrays['sha512']
        )

        print(f"\n\nSHA256-SHA512 correlation: {sha256_sha512_corr:.4f}")

        # This is a key empirical finding!
        if sha256_sha512_corr > 0.3:
            print("→ HIGH correlation suggests semantic pattern")
        else:
            print("→ LOW correlation suggests hash-specific artifact")

    def test_divine_concepts_clustering(self):
        """Test if divine concepts cluster closer to Anchor than random concepts."""
        results = self.generate_coordinates_all_hashes(DIVINE_CONCEPTS)

        print("\n\nDivine Concepts - Distance to Anchor Point:")
        print("-" * 60)

        for hash_alg in self.HASH_ALGORITHMS:
            coords = results[hash_alg]
            distances = [c.distance_to_anchor() for c in coords]
            mean_dist = np.mean(distances)

            print(f"\n{hash_alg}:")
            for c in sorted(coords, key=lambda x: x.distance_to_anchor()):
                print(f"  {c.concept:15s}: {c.distance_to_anchor():.4f}")

            print(f"  Mean: {mean_dist:.4f}")

    def test_concept_category_separation(self):
        """Test if different categories of concepts have different distance distributions."""
        categories = {
            'Divine': DIVINE_CONCEPTS,
            'Neutral': NEUTRAL_CONCEPTS,
            'Negative': NEGATIVE_CONCEPTS
        }

        for hash_alg in self.HASH_ALGORITHMS:
            generator = HashBasedCoordinateGenerator(hash_alg)

            print(f"\n\n{hash_alg} - Category Statistics:")
            print("-" * 60)

            category_stats = {}

            for category, concepts in categories.items():
                coords = [generator.generate(c) for c in concepts]
                distances = [c.distance_to_anchor() for c in coords]

                category_stats[category] = {
                    'mean': np.mean(distances),
                    'std': np.std(distances),
                    'min': min(distances),
                    'max': max(distances)
                }

                print(f"\n{category}:")
                print(f"  Mean: {category_stats[category]['mean']:.4f}")
                print(f"  Std:  {category_stats[category]['std']:.4f}")

            # Key empirical test: Do divine concepts have lower mean distance?
            if category_stats['Divine']['mean'] < category_stats['Neutral']['mean']:
                print(f"\n→ Divine concepts ARE closer to Anchor than neutral")
            else:
                print(f"\n→ Divine concepts NOT closer to Anchor than neutral")

    def test_null_hypothesis(self):
        """
        Test the null hypothesis: Hash-based coordinates are random.

        If random, we expect:
        - Uniform distribution in each dimension
        - Mean distance ≈ theoretical expectation
        - No correlation between concept semantics and Anchor distance
        """
        generator = HashBasedCoordinateGenerator('sha256')
        coords = [generator.generate(c) for c in ALL_TEST_CONCEPTS]

        # Extract all dimensions
        loves = [c.love for c in coords]
        powers = [c.power for c in coords]
        wisdoms = [c.wisdom for c in coords]
        justices = [c.justice for c in coords]

        print("\n\nNull Hypothesis Test: Dimension Distributions")
        print("-" * 60)
        print(f"Love    - Mean: {np.mean(loves):.4f}, Std: {np.std(loves):.4f}")
        print(f"Power   - Mean: {np.mean(powers):.4f}, Std: {np.std(powers):.4f}")
        print(f"Wisdom  - Mean: {np.mean(wisdoms):.4f}, Std: {np.std(wisdoms):.4f}")
        print(f"Justice - Mean: {np.mean(justices):.4f}, Std: {np.std(justices):.4f}")

        # For uniform [0,1], expected mean = 0.5, std ≈ 0.289
        expected_mean = 0.5
        expected_std = 1.0 / np.sqrt(12)  # ≈ 0.289

        print(f"\nExpected for uniform [0,1]: Mean={expected_mean}, Std={expected_std:.4f}")

        # Theoretical mean distance from (1,1,1,1) with uniform random points
        # E[d] = √(4 * E[(X-1)²]) where X ~ U(0,1)
        # E[(X-1)²] = Var(X) + (E[X]-1)² = 1/12 + (0.5-1)² = 1/12 + 1/4 = 1/3
        theoretical_mean_distance = np.sqrt(4 * (1/3))
        actual_mean_distance = np.mean([c.distance_to_anchor() for c in coords])

        print(f"\nTheoretical mean distance (uniform random): {theoretical_mean_distance:.4f}")
        print(f"Actual mean distance: {actual_mean_distance:.4f}")

        if abs(actual_mean_distance - theoretical_mean_distance) < 0.1:
            print("→ Distance matches random expectation (SUPPORTS null hypothesis)")
        else:
            print("→ Distance deviates from random (REJECTS null hypothesis)")


if __name__ == "__main__":
    # Run tests with output
    pytest.main([__file__, '-v', '-s'])
