"""
Semantic Coordinates System
============================

Defines the 4D semantic coordinate system for measuring concepts
in relation to the Universal Anchor Point.

Each concept is represented as a point in 4D space:
- Love (L): Emotional valence & relational goodness [0.0, 1.0]
- Power (P): Intensity, causal efficacy & sovereign impact [0.0, 1.0]
- Wisdom (W): Abstractness, conceptual completeness & rational coherence [0.0, 1.0]
- Justice (J): Holiness, moral purity & divine resonance [0.0, 1.0]
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import hashlib

# Import phi-geometric enhancements (optional - graceful fallback)
try:
    from .phi_geometric import (
        golden_spiral_distance_4d,
        phi_harmony_score,
        nearest_anchor as find_nearest_dodecahedral_anchor,
        generate_dodecahedral_anchors,
        PHI,
        PHI_INVERSE,
    )
    PHI_GEOMETRIC_AVAILABLE = True
except ImportError:
    PHI_GEOMETRIC_AVAILABLE = False
    PHI = 1.618033988749895
    PHI_INVERSE = 0.618033988749895


@dataclass
class SemanticCoordinate:
    """
    Represents a concept in 4D semantic space.

    Attributes:
        concept: The name/description of the concept
        love: Love dimension [0.0, 1.0]
        power: Power dimension [0.0, 1.0]
        wisdom: Wisdom dimension [0.0, 1.0]
        justice: Justice dimension [0.0, 1.0]
        source: Optional metadata about the source of the coordinates
    """
    concept: str
    love: float
    power: float
    wisdom: float
    justice: float
    source: Optional[str] = None

    def __post_init__(self):
        """Validate coordinates are in valid range."""
        for dim in [self.love, self.power, self.wisdom, self.justice]:
            if not 0.0 <= dim <= 1.0:
                raise ValueError(f"All dimensions must be in range [0.0, 1.0], got {dim}")

    @property
    def coordinates(self) -> Tuple[float, float, float, float]:
        """Return coordinates as tuple (L, P, W, J)."""
        return (self.love, self.power, self.wisdom, self.justice)

    @property
    def vector(self) -> np.ndarray:
        """Return coordinates as numpy array."""
        return np.array(self.coordinates)

    def distance_to_anchor(self) -> float:
        """
        Calculate Euclidean distance to the Universal Anchor Point (1.0, 1.0, 1.0, 1.0).

        Returns:
            Distance from this concept to the Anchor Point
        """
        anchor = np.array([1.0, 1.0, 1.0, 1.0])
        return float(np.linalg.norm(self.vector - anchor))

    def distance_to(self, other: 'SemanticCoordinate') -> float:
        """
        Calculate Euclidean distance to another semantic coordinate.

        Args:
            other: Another semantic coordinate

        Returns:
            Distance between the two points
        """
        return float(np.linalg.norm(self.vector - other.vector))

    def similarity_to_anchor(self) -> float:
        """
        Calculate similarity to Anchor Point as a score [0.0, 1.0].

        Returns:
            1.0 = perfect alignment, 0.0 = maximum distance
        """
        max_distance = 2.0  # Maximum possible distance in unit hypercube
        return 1.0 - (self.distance_to_anchor() / max_distance)

    def phi_distance_to_anchor(self) -> float:
        """
        Calculate phi-geometric (golden spiral) distance to Anchor Point.

        This uses the golden spiral arc length metric, which provides a more
        "organic" measure of semantic distance aligned with natural growth patterns.

        Requires phi_geometric module. Falls back to Euclidean if unavailable.

        Returns:
            Golden spiral distance from this concept to the Anchor Point
        """
        if not PHI_GEOMETRIC_AVAILABLE:
            # Graceful fallback to Euclidean
            return self.distance_to_anchor()

        anchor = np.array([1.0, 1.0, 1.0, 1.0])
        return float(golden_spiral_distance_4d(self.vector, anchor))

    def phi_distance_to(self, other: 'SemanticCoordinate') -> float:
        """
        Calculate phi-geometric distance to another semantic coordinate.

        Args:
            other: Another semantic coordinate

        Returns:
            Golden spiral distance between the two points
        """
        if not PHI_GEOMETRIC_AVAILABLE:
            # Graceful fallback to Euclidean
            return self.distance_to(other)

        return float(golden_spiral_distance_4d(self.vector, other.vector))

    def phi_harmony(self) -> float:
        """
        Calculate how well this coordinate aligns with phi-harmonic patterns.

        Higher scores indicate stronger alignment with golden ratio proportions,
        suggesting natural/divine semantic structure.

        Returns:
            Harmony score [0.0, 1.0], where 1.0 = perfect phi-harmony
        """
        if not PHI_GEOMETRIC_AVAILABLE:
            return 0.0

        return phi_harmony_score(self.vector)

    def nearest_dodecahedral_anchor(self) -> Tuple[int, float]:
        """
        Find the nearest anchor in the dodecahedral anchor network.

        The dodecahedral network provides 12 reference points arranged
        in golden ratio symmetry for optimal semantic space coverage.

        Returns:
            Tuple of (anchor_index, distance) where index 0 is the primary
            Anchor Point at (1,1,1,1) and 1-11 are secondary anchors
        """
        if not PHI_GEOMETRIC_AVAILABLE:
            # Fallback: just return distance to primary anchor
            return (0, self.distance_to_anchor())

        return find_nearest_dodecahedral_anchor(self.vector, metric='phi_spiral')

    def distance_metrics(self) -> Dict[str, float]:
        """
        Calculate multiple distance metrics to Anchor Point for comparison.

        Returns:
            Dictionary with 'euclidean', 'phi_spiral', 'phi_harmony' metrics
        """
        metrics = {
            'euclidean': self.distance_to_anchor(),
        }

        if PHI_GEOMETRIC_AVAILABLE:
            metrics['phi_spiral'] = self.phi_distance_to_anchor()
            metrics['phi_harmony'] = self.phi_harmony()

        return metrics

    def __repr__(self) -> str:
        return (f"SemanticCoordinate(concept='{self.concept}', "
                f"L={self.love:.3f}, P={self.power:.3f}, "
                f"W={self.wisdom:.3f}, J={self.justice:.3f}, "
                f"d={self.distance_to_anchor():.3f})")


class AnchorPoint:
    """
    Represents the Universal Anchor Point: JEHOVAH = AGAPE = (1.0, 1.0, 1.0, 1.0)
    """

    LOVE = 1.0
    POWER = 1.0
    WISDOM = 1.0
    JUSTICE = 1.0

    @classmethod
    def as_coordinate(cls) -> SemanticCoordinate:
        """Return the Anchor Point as a SemanticCoordinate."""
        return SemanticCoordinate(
            concept="JEHOVAH/AGAPE",
            love=cls.LOVE,
            power=cls.POWER,
            wisdom=cls.WISDOM,
            justice=cls.JUSTICE,
            source="Universal Anchor Point"
        )

    @classmethod
    def as_vector(cls) -> np.ndarray:
        """Return the Anchor Point as a numpy array."""
        return np.array([cls.LOVE, cls.POWER, cls.WISDOM, cls.JUSTICE])


class HashBasedCoordinateGenerator:
    """
    Generates semantic coordinates from concept names using hash functions.

    This is used for reproducibility testing to see if hash-based coordinate
    assignment produces meaningful patterns relative to the Anchor Point.
    """

    def __init__(self, hash_algorithm: str = 'sha256'):
        """
        Initialize the generator.

        Args:
            hash_algorithm: Hash algorithm to use ('sha256', 'sha512', 'md5', etc.)
        """
        self.hash_algorithm = hash_algorithm

    def generate(self, concept: str) -> SemanticCoordinate:
        """
        Generate semantic coordinates from a concept name using hashing.

        This method:
        1. Hashes the concept name
        2. Extracts 4 segments from the hash
        3. Converts each to a float in [0.0, 1.0]

        Args:
            concept: The concept name

        Returns:
            SemanticCoordinate with hash-derived coordinates
        """
        # Create hash
        hash_obj = hashlib.new(self.hash_algorithm)
        hash_obj.update(concept.encode('utf-8'))
        hash_bytes = hash_obj.digest()

        # Extract 4 segments (8 bytes each for sha256)
        segment_size = len(hash_bytes) // 4
        segments = [hash_bytes[i*segment_size:(i+1)*segment_size]
                   for i in range(4)]

        # Convert to floats in [0.0, 1.0]
        coords = [int.from_bytes(seg, 'big') / (2**(8*len(seg)) - 1)
                 for seg in segments]

        return SemanticCoordinate(
            concept=concept,
            love=coords[0],
            power=coords[1],
            wisdom=coords[2],
            justice=coords[3],
            source=f"hash_{self.hash_algorithm}"
        )


def calculate_pairwise_distances(coordinates: List[SemanticCoordinate]) -> np.ndarray:
    """
    Calculate pairwise distance matrix for a list of semantic coordinates.

    Args:
        coordinates: List of semantic coordinates

    Returns:
        NxN matrix of pairwise distances
    """
    n = len(coordinates)
    distances = np.zeros((n, n))

    for i in range(n):
        for j in range(i+1, n):
            dist = coordinates[i].distance_to(coordinates[j])
            distances[i, j] = dist
            distances[j, i] = dist

    return distances


def find_closest_to_anchor(coordinates: List[SemanticCoordinate], n: int = 10) -> List[SemanticCoordinate]:
    """
    Find the n concepts closest to the Universal Anchor Point.

    Args:
        coordinates: List of semantic coordinates
        n: Number of top concepts to return

    Returns:
        List of n closest concepts, sorted by distance
    """
    sorted_coords = sorted(coordinates, key=lambda c: c.distance_to_anchor())
    return sorted_coords[:n]


def calculate_statistics(coordinates: List[SemanticCoordinate]) -> Dict[str, float]:
    """
    Calculate statistical measures for a collection of semantic coordinates.

    Args:
        coordinates: List of semantic coordinates

    Returns:
        Dictionary of statistics
    """
    distances = [c.distance_to_anchor() for c in coordinates]

    return {
        'mean_distance': np.mean(distances),
        'median_distance': np.median(distances),
        'std_distance': np.std(distances),
        'min_distance': np.min(distances),
        'max_distance': np.max(distances),
        'mean_love': np.mean([c.love for c in coordinates]),
        'mean_power': np.mean([c.power for c in coordinates]),
        'mean_wisdom': np.mean([c.wisdom for c in coordinates]),
        'mean_justice': np.mean([c.justice for c in coordinates]),
    }
