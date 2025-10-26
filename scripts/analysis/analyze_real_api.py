#!/usr/bin/env python3
# This script is intended to be run from the root of the repository.
"""Detailed analysis of real Claude API coordinate assignments (Refactored)"""

import sys
sys.path.insert(0, '.')

from src.analysis.common_utils import (
    setup_analysis,
    load_cached_coordinates,
    print_header,
    print_section,
    print_coordinates_table,
    calculate_category_statistics,
    analyze_dimensional_correlations,
)
import numpy as np

# Test concepts
CONCEPT_CATEGORIES = {
    'DIVINE CONCEPTS': ['JEHOVAH', 'AGAPE', 'Holy', 'Grace', 'Mercy', 'Love', 'Justice', 'Wisdom', 'Compassion', 'Truth'],
    'EVIL CONCEPTS': ['Hatred', 'Evil', 'Cruelty', 'Deception', 'Corruption'],
    'NEUTRAL OBJECTS': ['Table', 'Tree', 'Water', 'Stone', 'Cloud'],
}

# Initial setup
gen = setup_analysis()
print_header('DETAILED REAL CLAUDE API ANALYSIS')

# Load all coordinates from cache
all_concepts = [concept for concepts in CONCEPT_CATEGORIES.values() for concept in concepts]
results = load_cached_coordinates(all_concepts)
print(f"✅ Loaded {len(results)} concepts from cache\n")

# Display coordinates for each category
for category_name, concepts in CONCEPT_CATEGORIES.items():
    print_section(category_name)
    coords = {c: results[c] for c in concepts if c in results}
    print_coordinates_table(coords, sort_by='name')

# Statistical summary
print_section('STATISTICAL SUMMARY')
stats = calculate_category_statistics(results, CONCEPT_CATEGORIES)

divine_dist = stats.get('DIVINE CONCEPTS', {}).get('mean_distance', 0)
evil_dist = stats.get('EVIL CONCEPTS', {}).get('mean_distance', 0)
neutral_dist = stats.get('NEUTRAL OBJECTS', {}).get('mean_distance', 0)

print(f'\nDivine concepts:  {divine_dist:.4f}')
print(f'Evil concepts:    {evil_dist:.4f}')
print(f'Neutral objects:  {neutral_dist:.4f}')

if divine_dist > 0:
    print(f'\nEvil vs Divine ratio: {evil_dist/divine_dist:.2f}x farther from Anchor')
    print(f'Neutral vs Divine ratio: {neutral_dist/divine_dist:.2f}x farther from Anchor')

# Test hypothesis: Divine < Neutral < Evil
if divine_dist < neutral_dist < evil_dist:
    print('\n✅ HYPOTHESIS CONFIRMED: Divine < Neutral < Evil')
else:
    print(f'\n⚠️  Mixed results: Divine={divine_dist:.2f}, Neutral={neutral_dist:.2f}, Evil={evil_dist:.2f}')

# Fourfold unity analysis
print_section('FOURFOLD UNITY ANALYSIS')
divine_coords_list = [results[c] for c in CONCEPT_CATEGORIES['DIVINE CONCEPTS'] if c in results]
correlations = analyze_dimensional_correlations(divine_coords_list)

print('\nDivine concepts dimensional correlations:')
for pair, r_value in correlations.items():
    if not pair.endswith('_p'):
        print(f'{pair.replace("-", "-").title()}: r = {r_value:.3f}')

mean_corr = np.mean([abs(r) for p, r in correlations.items() if not p.endswith('_p')])
print(f'\nMean absolute correlation: {mean_corr:.3f}')

if mean_corr > 0.7:
    print('✅ STRONG fourfold unity in divine concepts!')
elif mean_corr > 0.4:
    print('✓ MODERATE fourfold unity in divine concepts')
else:
    print('⚠️  WEAK fourfold unity in divine concepts')

print('\n' + '=' * 80)
