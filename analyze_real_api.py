#!/usr/bin/env python3
"""Detailed analysis of real Claude API coordinate assignments"""

import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from src.core.claude_api_generator import ClaudeAPIGenerator
import numpy as np

# Test concepts
divine = ['JEHOVAH', 'AGAPE', 'Holy', 'Grace', 'Mercy', 'Love', 'Justice', 'Wisdom', 'Compassion', 'Truth']
evil = ['Hatred', 'Evil', 'Cruelty', 'Deception', 'Corruption']
neutral = ['Table', 'Tree', 'Water', 'Stone', 'Cloud']

gen = ClaudeAPIGenerator()

print('=' * 80)
print('DETAILED REAL CLAUDE API ANALYSIS')
print('=' * 80)

categories = [
    ('DIVINE CONCEPTS', divine),
    ('EVIL CONCEPTS', evil),
    ('NEUTRAL OBJECTS', neutral)
]

all_distances = []

for category_name, concepts in categories:
    print(f'\n{category_name}')
    print('-' * 80)
    print(f"{'Concept':<15} {'Love':<7} {'Power':<7} {'Wisdom':<7} {'Justice':<7} {'Distance':<8}")
    print('-' * 80)

    distances = []
    for concept in concepts:
        coord = gen.generate(concept)
        dist = coord.distance_to_anchor()
        distances.append(dist)
        all_distances.append(dist)
        print(f'{concept:<15} {coord.love:<7.4f} {coord.power:<7.4f} {coord.wisdom:<7.4f} {coord.justice:<7.4f} {dist:<8.4f}')

    mean_dist = np.mean(distances)
    std_dist = np.std(distances)
    print('-' * 80)
    print(f'Mean distance: {mean_dist:.4f} (±{std_dist:.4f})')

print('\n' + '=' * 80)
print('STATISTICAL SUMMARY')
print('=' * 80)

divine_coords = [gen.generate(c) for c in divine]
evil_coords = [gen.generate(c) for c in evil]
neutral_coords = [gen.generate(c) for c in neutral]

divine_dist = np.mean([c.distance_to_anchor() for c in divine_coords])
evil_dist = np.mean([c.distance_to_anchor() for c in evil_coords])
neutral_dist = np.mean([c.distance_to_anchor() for c in neutral_coords])

print(f'\nDivine concepts:  {divine_dist:.4f}')
print(f'Evil concepts:    {evil_dist:.4f}')
print(f'Neutral objects:  {neutral_dist:.4f}')

print(f'\nEvil vs Divine ratio: {evil_dist/divine_dist:.2f}x farther from Anchor')
print(f'Neutral vs Divine ratio: {neutral_dist/divine_dist:.2f}x farther from Anchor')

# Test hypothesis: Divine < Neutral < Evil
if divine_dist < neutral_dist < evil_dist:
    print('\n✅ HYPOTHESIS CONFIRMED: Divine < Neutral < Evil')
else:
    print(f'\n⚠️  Mixed results: Divine={divine_dist:.2f}, Neutral={neutral_dist:.2f}, Evil={evil_dist:.2f}')

# Test fourfold unity
print('\n' + '=' * 80)
print('FOURFOLD UNITY ANALYSIS')
print('=' * 80)

print('\nDivine concepts dimensional correlations:')
loves = [c.love for c in divine_coords]
powers = [c.power for c in divine_coords]
wisdoms = [c.wisdom for c in divine_coords]
justices = [c.justice for c in divine_coords]

from scipy.stats import pearsonr

print(f'Love-Power:   r = {pearsonr(loves, powers)[0]:.3f}')
print(f'Love-Wisdom:  r = {pearsonr(loves, wisdoms)[0]:.3f}')
print(f'Love-Justice: r = {pearsonr(loves, justices)[0]:.3f}')
print(f'Power-Wisdom: r = {pearsonr(powers, wisdoms)[0]:.3f}')
print(f'Power-Justice: r = {pearsonr(powers, justices)[0]:.3f}')
print(f'Wisdom-Justice: r = {pearsonr(wisdoms, justices)[0]:.3f}')

mean_corr = np.mean([
    abs(pearsonr(loves, powers)[0]),
    abs(pearsonr(loves, wisdoms)[0]),
    abs(pearsonr(loves, justices)[0]),
    abs(pearsonr(powers, wisdoms)[0]),
    abs(pearsonr(powers, justices)[0]),
    abs(pearsonr(wisdoms, justices)[0])
])

print(f'\nMean absolute correlation: {mean_corr:.3f}')
if mean_corr > 0.7:
    print('✅ STRONG fourfold unity in divine concepts!')
elif mean_corr > 0.4:
    print('✓ MODERATE fourfold unity in divine concepts')
else:
    print('⚠️  WEAK fourfold unity in divine concepts')

print('\n' + '=' * 80)
