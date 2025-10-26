"""
Common Analysis Utilities
==========================

Shared functions used across multiple analysis scripts.
Consolidates common patterns to reduce code duplication.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from scipy.stats import pearsonr

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.semantic_coordinates import SemanticCoordinate
from src.core.claude_api_generator import ClaudeAPIGenerator


def setup_analysis():
    """Standard setup for analysis scripts."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # python-dotenv not installed
    return ClaudeAPIGenerator()


def load_cached_coordinates(
    concepts: List[str],
    cache_file: Optional[Path] = None
) -> Dict[str, SemanticCoordinate]:
    """Load coordinates from Claude API cache."""
    if cache_file is None:
        cache_file = Path(__file__).parent.parent.parent / "data" / "cache" / "claude_api_cache.json"

    if not cache_file.exists():
        print(f"Warning: Cache file not found at {cache_file}")
        return {}

    with open(cache_file, 'r') as f:
        cache = json.load(f)

    coordinates = {}
    for concept in concepts:
        for key, data in cache.items():
            if ':' in key and key.split(':', 1)[1].lower() == concept.lower():
                coordinates[concept] = SemanticCoordinate(
                    concept=concept,
                    love=data['love'], power=data['power'],
                    wisdom=data['wisdom'], justice=data['justice'],
                    source=f"cached_{key}"
                )
                break
    return coordinates


def print_header(title: str, width: int = 90):
    """Print formatted section header."""
    print("=" * width)
    print(title)
    print("=" * width)


def print_section(title: str, width: int = 90):
    """Print formatted subsection header."""
    print("\n" + "=" * width)
    print(title)
    print("=" * width)


def print_coordinates_table(
    coordinates: Dict[str, SemanticCoordinate],
    sort_by: str = 'distance',
):
    """Print formatted table of coordinates."""
    items = sorted(coordinates.items(), key=lambda x: x[1].distance_to_anchor() if sort_by == 'distance' else x[0])
    print(f"{'Concept':<15} {'Love':<7} {'Power':<7} {'Wisdom':<7} {'Justice':<7} {'Distance':<9}")
    print("-" * 70)
    for concept, coord in items:
        print(f"{concept:<15} {coord.love:<7.4f} {coord.power:<7.4f} {coord.wisdom:<7.4f} {coord.justice:<7.4f} {coord.distance_to_anchor():<9.4f}")


def calculate_category_statistics(
    coordinates: Dict[str, SemanticCoordinate],
    categories: Dict[str, List[str]]
) -> Dict[str, Dict[str, float]]:
    """Calculate statistics for each category."""
    stats = {}
    for category, concepts in categories.items():
        coords_in_cat = [coordinates[c] for c in concepts if c in coordinates]
        if coords_in_cat:
            distances = [c.distance_to_anchor() for c in coords_in_cat]
            loves = [c.love for c in coords_in_cat]
            powers = [c.power for c in coords_in_cat]
            wisdoms = [c.wisdom for c in coords_in_cat]
            justices = [c.justice for c in coords_in_cat]

            stats[category] = {
                'n': len(coords_in_cat),
                'mean_distance': np.mean(distances),
                'std_distance': np.std(distances),
                'min_distance': np.min(distances),
                'max_distance': np.max(distances),
                'mean_love': np.mean(loves),
                'mean_power': np.mean(powers),
                'mean_wisdom': np.mean(wisdoms),
                'mean_justice': np.mean(justices),
                'std_love': np.std(loves),
                'std_power': np.std(powers),
                'std_wisdom': np.std(wisdoms),
                'std_justice': np.std(justices),
            }
    return stats


def analyze_dimensional_correlations(
    coordinates: List[SemanticCoordinate]
) -> Dict[str, float]:
    """Calculate correlations between dimensions."""
    if not coordinates: return {}
    dims = {
        'love': [c.love for c in coordinates], 'power': [c.power for c in coordinates],
        'wisdom': [c.wisdom for c in coordinates], 'justice': [c.justice for c in coordinates]
    }
    correlations = {}
    pairs = [('love', 'power'), ('love', 'wisdom'), ('love', 'justice'), ('power', 'wisdom'), ('power', 'justice'), ('wisdom', 'justice')]
    for d1, d2 in pairs:
        correlations[f"{d1}-{d2}"], correlations[f"{d1}-{d2}_p"] = pearsonr(dims[d1], dims[d2])
    return correlations


def find_extremes(
    coordinates: Dict[str, SemanticCoordinate], n: int = 10
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """Find concepts with extreme distances from Anchor Point."""
    distances = sorted([(c, coord.distance_to_anchor()) for c, coord in coordinates.items()], key=lambda x: x[1])
    return distances[:n], list(reversed(distances[-n:]))


def print_statistics_table(stats: Dict[str, Dict[str, float]]):
    """Print formatted table of category statistics."""
    print(f"{'Category':<25} {'N':<5} {'Mean':<10} {'Std':<10} {'Min':<10} {'Max':<10}")
    print("-" * 75)
    for cat, data in stats.items():
        print(f"{cat:<25} {data['n']:<5} {data['mean_distance']:<10.4f} {data['std_distance']:<10.4f} {data['min_distance']:<10.4f} {data['max_distance']:<10.4f}")


def calculate_evil_signature(
    vice_coordinates: List[SemanticCoordinate]
) -> Dict[str, float]:
    """Calculate the characteristic 'evil signature' pattern."""
    if not vice_coordinates: return {}
    return {
        'mean_love': np.mean([c.love for c in vice_coordinates]),
        'mean_power': np.mean([c.power for c in vice_coordinates]),
        'mean_wisdom': np.mean([c.wisdom for c in vice_coordinates]),
        'mean_justice': np.mean([c.justice for c in vice_coordinates]),
        'std_love': np.std([c.love for c in vice_coordinates]),
        'std_power': np.std([c.power for c in vice_coordinates]),
        'std_wisdom': np.std([c.wisdom for c in vice_coordinates]),
        'std_justice': np.std([c.justice for c in vice_coordinates]),
    }
