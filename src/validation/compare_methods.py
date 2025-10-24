"""
Method Comparison and Validation
=================================

Tools for comparing different coordinate generation methods:
- Simulated LLM (heuristic rules)
- Real Claude API
- Human evaluators
- Cross-method consistency analysis
"""

import numpy as np
from typing import List, Dict, Optional
from scipy.stats import spearmanr, pearsonr
from scipy import stats
import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.semantic_coordinates import SemanticCoordinate


def compare_simulated_vs_api(
    concepts: List[str],
    simulated_coords: List[SemanticCoordinate],
    api_coords: List[SemanticCoordinate]
) -> Dict:
    """
    Compare simulated and real API coordinate assignments.

    Args:
        concepts: List of concept names
        simulated_coords: Coordinates from simulated generator
        api_coords: Coordinates from real API

    Returns:
        Dictionary with comparison statistics
    """
    # Filter out None values (API failures)
    valid_indices = [i for i, (s, a) in enumerate(zip(simulated_coords, api_coords))
                    if s is not None and a is not None]

    if len(valid_indices) == 0:
        return {'error': 'No valid coordinate pairs'}

    sim_valid = [simulated_coords[i] for i in valid_indices]
    api_valid = [api_coords[i] for i in valid_indices]
    concepts_valid = [concepts[i] for i in valid_indices]

    # Extract distances to Anchor
    sim_distances = [c.distance_to_anchor() for c in sim_valid]
    api_distances = [c.distance_to_anchor() for c in api_valid]

    # Overall correlation
    corr_spearman, p_spearman = spearmanr(sim_distances, api_distances)
    corr_pearson, p_pearson = pearsonr(sim_distances, api_distances)

    # Per-dimension correlations
    dimension_corrs = {}
    for dim in ['love', 'power', 'wisdom', 'justice']:
        sim_dim = [getattr(c, dim) for c in sim_valid]
        api_dim = [getattr(c, dim) for c in api_valid]
        rho, p = spearmanr(sim_dim, api_dim)
        dimension_corrs[dim] = {'rho': rho, 'p': p}

    # Distance statistics
    sim_mean = np.mean(sim_distances)
    api_mean = np.mean(api_distances)
    sim_std = np.std(sim_distances)
    api_std = np.std(api_distances)

    # Agreement on rankings (top/bottom concepts)
    sim_ranked = sorted(zip(concepts_valid, sim_distances), key=lambda x: x[1])
    api_ranked = sorted(zip(concepts_valid, api_distances), key=lambda x: x[1])

    top_n = min(10, len(concepts_valid) // 3)
    sim_top = set([c for c, d in sim_ranked[:top_n]])
    api_top = set([c for c, d in api_ranked[:top_n]])
    top_agreement = len(sim_top & api_top) / top_n

    # Concept-level differences
    differences = []
    for i, concept in enumerate(concepts_valid):
        diff = {
            'concept': concept,
            'sim_distance': sim_distances[i],
            'api_distance': api_distances[i],
            'difference': abs(sim_distances[i] - api_distances[i]),
            'sim_coords': sim_valid[i].coordinates,
            'api_coords': api_valid[i].coordinates
        }
        differences.append(diff)

    # Sort by largest differences
    differences.sort(key=lambda x: x['difference'], reverse=True)

    return {
        'n_concepts': len(concepts_valid),
        'distance_correlation': {
            'spearman_rho': corr_spearman,
            'spearman_p': p_spearman,
            'pearson_r': corr_pearson,
            'pearson_p': p_pearson
        },
        'dimension_correlations': dimension_corrs,
        'distance_stats': {
            'simulated_mean': sim_mean,
            'api_mean': api_mean,
            'simulated_std': sim_std,
            'api_std': api_std,
            'mean_difference': api_mean - sim_mean
        },
        'ranking_agreement': {
            'top_n': top_n,
            'top_agreement': top_agreement
        },
        'top_differences': differences[:10],
        'all_differences': differences
    }


def validate_consistency(coords_list: List[List[SemanticCoordinate]],
                        method_names: List[str],
                        concepts: List[str]) -> Dict:
    """
    Validate consistency across multiple coordinate generation methods.

    Args:
        coords_list: List of coordinate lists from different methods
        method_names: Names of each method
        concepts: List of concept names

    Returns:
        Consistency analysis results
    """
    n_methods = len(coords_list)

    # Extract distances for each method
    distance_arrays = {}
    for i, (coords, name) in enumerate(zip(coords_list, method_names)):
        valid_coords = [c for c in coords if c is not None]
        if len(valid_coords) > 0:
            distance_arrays[name] = [c.distance_to_anchor() for c in valid_coords]

    # Pairwise correlations
    correlation_matrix = {}
    for name1 in distance_arrays:
        correlation_matrix[name1] = {}
        for name2 in distance_arrays:
            if name1 == name2:
                correlation_matrix[name1][name2] = 1.0
            else:
                # Only correlate if same length
                if len(distance_arrays[name1]) == len(distance_arrays[name2]):
                    rho, _ = spearmanr(distance_arrays[name1], distance_arrays[name2])
                    correlation_matrix[name1][name2] = rho
                else:
                    correlation_matrix[name1][name2] = None

    # Mean distances per method
    mean_distances = {
        name: np.mean(distances)
        for name, distances in distance_arrays.items()
    }

    # Variance across methods (for each concept)
    concept_variance = []
    for i, concept in enumerate(concepts):
        distances = []
        for coords in coords_list:
            if i < len(coords) and coords[i] is not None:
                distances.append(coords[i].distance_to_anchor())

        if len(distances) > 1:
            concept_variance.append({
                'concept': concept,
                'variance': np.var(distances),
                'std': np.std(distances),
                'mean': np.mean(distances),
                'n_methods': len(distances)
            })

    # Sort by highest variance (most disagreement)
    concept_variance.sort(key=lambda x: x['variance'], reverse=True)

    return {
        'correlation_matrix': correlation_matrix,
        'mean_distances': mean_distances,
        'concept_variance': concept_variance[:10],  # Top 10 most variable
        'overall_consistency': np.mean([v['std'] for v in concept_variance]) if concept_variance else None
    }


def cross_method_analysis(
    concepts: List[str],
    method_coords: Dict[str, List[SemanticCoordinate]],
    categories: Optional[Dict[str, List[str]]] = None
) -> pd.DataFrame:
    """
    Generate comprehensive cross-method analysis table.

    Args:
        concepts: List of concept names
        method_coords: Dictionary mapping method names to coordinate lists
        categories: Optional dictionary of concept categories

    Returns:
        DataFrame with analysis results
    """
    data = []

    for concept in concepts:
        row = {'concept': concept}

        # Add category if provided
        if categories:
            for cat_name, cat_concepts in categories.items():
                if concept in cat_concepts:
                    row['category'] = cat_name
                    break

        # Add distance from each method
        for method_name, coords in method_coords.items():
            # Find this concept in the list
            coord = next((c for c in coords if c.concept == concept), None)
            if coord:
                row[f'{method_name}_distance'] = coord.distance_to_anchor()
                row[f'{method_name}_love'] = coord.love
                row[f'{method_name}_power'] = coord.power
                row[f'{method_name}_wisdom'] = coord.wisdom
                row[f'{method_name}_justice'] = coord.justice

        # Calculate variance across methods
        distances = [row[f'{m}_distance'] for m in method_coords.keys()
                    if f'{m}_distance' in row]
        if len(distances) > 1:
            row['distance_variance'] = np.var(distances)
            row['distance_std'] = np.std(distances)

        data.append(row)

    df = pd.DataFrame(data)

    # Sort by variance (most controversial concepts first)
    if 'distance_variance' in df.columns:
        df = df.sort_values('distance_variance', ascending=False)

    return df


def print_comparison_report(comparison: Dict):
    """
    Print a formatted comparison report.

    Args:
        comparison: Output from compare_simulated_vs_api
    """
    print("=" * 70)
    print("SIMULATED vs API COMPARISON REPORT")
    print("=" * 70)

    print(f"\nConcepts analyzed: {comparison['n_concepts']}")

    print("\n1. DISTANCE CORRELATION")
    print("-" * 70)
    corr = comparison['distance_correlation']
    print(f"Spearman ρ: {corr['spearman_rho']:.4f} (p={corr['spearman_p']:.4f})")
    print(f"Pearson r:  {corr['pearson_r']:.4f} (p={corr['pearson_p']:.4f})")

    if corr['spearman_rho'] > 0.7:
        print("→ HIGH correlation - methods agree strongly")
    elif corr['spearman_rho'] > 0.4:
        print("→ MODERATE correlation - some agreement")
    else:
        print("→ LOW correlation - methods produce different rankings")

    print("\n2. DIMENSION CORRELATIONS")
    print("-" * 70)
    for dim, data in comparison['dimension_correlations'].items():
        print(f"{dim.capitalize():10s}: ρ={data['rho']:.4f} (p={data['p']:.4f})")

    print("\n3. DISTANCE STATISTICS")
    print("-" * 70)
    stats = comparison['distance_stats']
    print(f"Simulated mean: {stats['simulated_mean']:.4f} (±{stats['simulated_std']:.3f})")
    print(f"API mean:       {stats['api_mean']:.4f} (±{stats['api_std']:.3f})")
    print(f"Difference:     {stats['mean_difference']:+.4f}")

    print("\n4. RANKING AGREEMENT")
    print("-" * 70)
    rank = comparison['ranking_agreement']
    print(f"Top {rank['top_n']} concepts agreement: {rank['top_agreement']:.1%}")

    print("\n5. LARGEST DIFFERENCES")
    print("-" * 70)
    print(f"{'Concept':<20s} {'Simulated':<12s} {'API':<12s} {'Diff'}")
    print("-" * 70)
    for diff in comparison['top_differences'][:10]:
        print(f"{diff['concept']:<20s} {diff['sim_distance']:<12.4f} "
              f"{diff['api_distance']:<12.4f} {diff['difference']:.4f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("Validation tools loaded successfully")
    print("\nUsage:")
    print("  from src.validation import compare_simulated_vs_api")
    print("  result = compare_simulated_vs_api(concepts, sim_coords, api_coords)")
    print("  print_comparison_report(result)")
