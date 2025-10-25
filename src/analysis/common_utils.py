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
    """
    Standard setup for analysis scripts.

    Returns:
        ClaudeAPIGenerator: Configured generator with API access
    """
    from dotenv import load_dotenv
    load_dotenv()
    return ClaudeAPIGenerator()


def load_cached_coordinates(
    concepts: List[str],
    cache_file: Optional[Path] = None
) -> Dict[str, SemanticCoordinate]:
    """
    Load coordinates from Claude API cache.

    Args:
        concepts: List of concept names to load
        cache_file: Optional path to cache file

    Returns:
        Dictionary mapping concept names to SemanticCoordinate objects
    """
    if cache_file is None:
        cache_file = Path(__file__).parent.parent.parent / "data" / "cache" / "claude_api_cache.json"

    if not cache_file.exists():
        raise FileNotFoundError(
            f"Cache file not found at: {cache_file}\n"
            "Run examples/phase4_expanded_testing.py first to populate cache."
        )

    with open(cache_file, 'r') as f:
        cache = json.load(f)

    coordinates = {}

    # Cache format: "model:concept" -> {love, power, wisdom, justice}
    for concept in concepts:
        # Try to find in cache (case-insensitive)
        for key, data in cache.items():
            if ':' in key:
                _, cached_concept = key.split(':', 1)
                if cached_concept.lower() == concept.lower():
                    coordinates[concept] = SemanticCoordinate(
                        concept=concept,
                        love=data['love'],
                        power=data['power'],
                        wisdom=data['wisdom'],
                        justice=data['justice'],
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
    limit: Optional[int] = None,
    show_category: bool = False,
    category_map: Optional[Dict[str, str]] = None
):
    """
    Print formatted table of coordinates.

    Args:
        coordinates: Dictionary of concept -> SemanticCoordinate
        sort_by: 'distance', 'name', 'love', 'power', 'wisdom', 'justice'
        limit: Maximum number of entries to display
        show_category: Whether to show category column
        category_map: Optional mapping of concept -> category
    """
    # Convert to list for sorting
    items = list(coordinates.items())

    # Sort
    if sort_by == 'distance':
        items.sort(key=lambda x: x[1].distance_to_anchor())
    elif sort_by == 'name':
        items.sort(key=lambda x: x[0])
    elif sort_by in ['love', 'power', 'wisdom', 'justice']:
        items.sort(key=lambda x: getattr(x[1], sort_by), reverse=True)

    # Limit
    if limit:
        items = items[:limit]

    # Print header
    if show_category and category_map:
        print(f"{'Concept':<15} {'Love':<7} {'Power':<7} {'Wisdom':<7} {'Justice':<7} {'Distance':<9} {'Category':<20}")
        print("-" * 95)
    else:
        print(f"{'Concept':<15} {'Love':<7} {'Power':<7} {'Wisdom':<7} {'Justice':<7} {'Distance':<9}")
        print("-" * 70)

    # Print rows
    for concept, coord in items:
        dist = coord.distance_to_anchor()
        row = f"{concept:<15} {coord.love:<7.4f} {coord.power:<7.4f} {coord.wisdom:<7.4f} {coord.justice:<7.4f} {dist:<9.4f}"

        if show_category and category_map:
            category = category_map.get(concept, "Unknown")
            row += f" {category:<20}"

        print(row)


def calculate_category_statistics(
    coordinates: Dict[str, SemanticCoordinate],
    categories: Dict[str, List[str]]
) -> Dict[str, Dict[str, float]]:
    """
    Calculate statistics for each category.

    Args:
        coordinates: Dictionary of concept -> SemanticCoordinate
        categories: Dictionary of category -> list of concepts

    Returns:
        Dictionary of category -> statistics dict
    """
    stats = {}

    for category, concepts in categories.items():
        # Get distances for concepts in this category
        distances = []
        loves = []
        powers = []
        wisdoms = []
        justices = []

        for concept in concepts:
            if concept in coordinates:
                coord = coordinates[concept]
                distances.append(coord.distance_to_anchor())
                loves.append(coord.love)
                powers.append(coord.power)
                wisdoms.append(coord.wisdom)
                justices.append(coord.justice)

        if distances:
            stats[category] = {
                'n': len(distances),
                'mean_distance': np.mean(distances),
                'std_distance': np.std(distances),
                'min_distance': np.min(distances),
                'max_distance': np.max(distances),
                'median_distance': np.median(distances),
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
    """
    Calculate correlations between dimensions.

    Args:
        coordinates: List of SemanticCoordinate objects

    Returns:
        Dictionary of correlation pairs -> correlation coefficient
    """
    loves = [c.love for c in coordinates]
    powers = [c.power for c in coordinates]
    wisdoms = [c.wisdom for c in coordinates]
    justices = [c.justice for c in coordinates]

    correlations = {}

    pairs = [
        ('love', 'power', loves, powers),
        ('love', 'wisdom', loves, wisdoms),
        ('love', 'justice', loves, justices),
        ('power', 'wisdom', powers, wisdoms),
        ('power', 'justice', powers, justices),
        ('wisdom', 'justice', wisdoms, justices),
    ]

    for dim1, dim2, values1, values2 in pairs:
        if len(values1) > 1 and len(values2) > 1:
            r, p = pearsonr(values1, values2)
            correlations[f"{dim1}-{dim2}"] = r
            correlations[f"{dim1}-{dim2}_p"] = p

    return correlations


def find_extremes(
    coordinates: Dict[str, SemanticCoordinate],
    n: int = 10
) -> Tuple[List[Tuple[str, float]], List[Tuple[str, float]]]:
    """
    Find concepts with extreme distances from Anchor Point.

    Args:
        coordinates: Dictionary of concept -> SemanticCoordinate
        n: Number of extremes to return

    Returns:
        Tuple of (closest, farthest) lists of (concept, distance) tuples
    """
    distances = [(concept, coord.distance_to_anchor())
                 for concept, coord in coordinates.items()]

    distances.sort(key=lambda x: x[1])

    closest = distances[:n]
    farthest = distances[-n:]
    farthest.reverse()  # Show farthest first

    return closest, farthest


def print_statistics_table(
    stats: Dict[str, Dict[str, float]],
    metrics: List[str] = ['mean_distance', 'std_distance', 'n']
):
    """
    Print formatted table of category statistics.

    Args:
        stats: Dictionary of category -> statistics
        metrics: List of metric keys to display
    """
    # Header
    header = f"{'Category':<25}"
    for metric in metrics:
        header += f" {metric:<12}"
    print(header)
    print("-" * (25 + 12 * len(metrics)))

    # Rows
    for category, data in stats.items():
        row = f"{category:<25}"
        for metric in metrics:
            value = data.get(metric, 0)
            if isinstance(value, int):
                row += f" {value:<12}"
            else:
                row += f" {value:<12.4f}"
        print(row)


def calculate_evil_signature(
    vice_coordinates: List[SemanticCoordinate]
) -> Dict[str, float]:
    """
    Calculate the characteristic 'evil signature' pattern.

    Evil signature: High Power, Low Love/Wisdom/Justice

    Args:
        vice_coordinates: List of coordinates for vice concepts

    Returns:
        Dictionary with signature statistics
    """
    loves = [c.love for c in vice_coordinates]
    powers = [c.power for c in vice_coordinates]
    wisdoms = [c.wisdom for c in vice_coordinates]
    justices = [c.justice for c in vice_coordinates]

    return {
        'mean_love': np.mean(loves),
        'mean_power': np.mean(powers),
        'mean_wisdom': np.mean(wisdoms),
        'mean_justice': np.mean(justices),
        'std_love': np.std(loves),
        'std_power': np.std(powers),
        'std_wisdom': np.std(wisdoms),
        'std_justice': np.std(justices),
        'power_to_love_ratio': np.mean(powers) / np.mean(loves) if np.mean(loves) > 0 else float('inf'),
        'power_to_wisdom_ratio': np.mean(powers) / np.mean(wisdoms) if np.mean(wisdoms) > 0 else float('inf'),
        'power_to_justice_ratio': np.mean(powers) / np.mean(justices) if np.mean(justices) > 0 else float('inf'),
    }
