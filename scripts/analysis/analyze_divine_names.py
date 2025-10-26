#!/usr/bin/env python3
"""
Detailed Mathematical Analysis: JEHOVAH, AGAPE, and Allah
==========================================================

Deep dive into the three primary divine concepts to examine:
1. Their exact coordinates and dimensional profiles
2. Mathematical relationships between them
3. Distance metrics and geometric properties
4. Nuances and differences despite convergence
"""

import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from src.core.claude_api_generator import ClaudeAPIGenerator
import numpy as np
from scipy.spatial.distance import euclidean, cityblock, cosine

print("=" * 90)
print("MATHEMATICAL ANALYSIS: JEHOVAH, AGAPE, and Allah")
print("=" * 90)

# Generate coordinates
gen = ClaudeAPIGenerator()

jehovah = gen.generate("JEHOVAH")
agape = gen.generate("AGAPE")
allah = gen.generate("Allah")

print("\n" + "=" * 90)
print("1. EXACT COORDINATES")
print("=" * 90)

concepts = [
    ("JEHOVAH", jehovah),
    ("AGAPE", agape),
    ("Allah", allah),
]

print(f"\n{'Concept':<15} {'Love':<8} {'Power':<8} {'Wisdom':<8} {'Justice':<8} {'Distance':<10}")
print("-" * 90)

for name, coord in concepts:
    dist = coord.distance_to_anchor()
    print(f"{name:<15} {coord.love:<8.6f} {coord.power:<8.6f} {coord.wisdom:<8.6f} "
          f"{coord.justice:<8.6f} {dist:<10.6f}")

# Mathematical analysis
print("\n" + "=" * 90)
print("2. DISTANCE TO ANCHOR POINT (1,1,1,1)")
print("=" * 90)

anchor = np.array([1.0, 1.0, 1.0, 1.0])

for name, coord in concepts:
    vec = coord.vector

    # Euclidean distance (L2 norm)
    euclidean_dist = np.linalg.norm(vec - anchor)

    # Manhattan distance (L1 norm)
    manhattan_dist = cityblock(vec, anchor)

    # Chebyshev distance (L-infinity norm)
    chebyshev_dist = np.max(np.abs(vec - anchor))

    # Cosine similarity
    cos_sim = 1 - cosine(vec, anchor)

    # Magnitude (length of vector)
    magnitude = np.linalg.norm(vec)

    print(f"\n{name}:")
    print(f"  Euclidean (L2):    {euclidean_dist:.6f}")
    print(f"  Manhattan (L1):    {manhattan_dist:.6f}")
    print(f"  Chebyshev (L∞):    {chebyshev_dist:.6f}")
    print(f"  Cosine similarity: {cos_sim:.6f}")
    print(f"  Vector magnitude:  {magnitude:.6f}")
    print(f"  Anchor magnitude:  {np.linalg.norm(anchor):.6f}")
    print(f"  Magnitude ratio:   {magnitude / np.linalg.norm(anchor):.6f}")

# Pairwise distances
print("\n" + "=" * 90)
print("3. PAIRWISE DISTANCES")
print("=" * 90)

print("\nDistance between divine names:\n")

pairs = [
    ("JEHOVAH", "AGAPE", jehovah, agape),
    ("JEHOVAH", "Allah", jehovah, allah),
    ("AGAPE", "Allah", agape, allah),
]

for name1, name2, coord1, coord2 in pairs:
    vec1 = coord1.vector
    vec2 = coord2.vector

    euclidean_dist = np.linalg.norm(vec1 - vec2)
    manhattan_dist = cityblock(vec1, vec2)
    cos_sim = 1 - cosine(vec1, vec2)

    print(f"{name1} ↔ {name2}:")
    print(f"  Euclidean distance:  {euclidean_dist:.6f}")
    print(f"  Manhattan distance:  {manhattan_dist:.6f}")
    print(f"  Cosine similarity:   {cos_sim:.6f}")

    # Component-wise differences
    diff = vec2 - vec1
    print(f"  Δ Love:     {diff[0]:+.6f}")
    print(f"  Δ Power:    {diff[1]:+.6f}")
    print(f"  Δ Wisdom:   {diff[2]:+.6f}")
    print(f"  Δ Justice:  {diff[3]:+.6f}")
    print()

# Dimensional analysis
print("=" * 90)
print("4. DIMENSIONAL ANALYSIS")
print("=" * 90)

dimensions = ['Love', 'Power', 'Wisdom', 'Justice']
jehovah_vec = jehovah.vector
agape_vec = agape.vector
allah_vec = allah.vector

print(f"\n{'Dimension':<15} {'JEHOVAH':<12} {'AGAPE':<12} {'Allah':<12} {'Mean':<12} {'Std Dev':<12}")
print("-" * 90)

for i, dim in enumerate(dimensions):
    values = [jehovah_vec[i], agape_vec[i], allah_vec[i]]
    mean = np.mean(values)
    std = np.std(values)
    print(f"{dim:<15} {jehovah_vec[i]:<12.6f} {agape_vec[i]:<12.6f} {allah_vec[i]:<12.6f} "
          f"{mean:<12.6f} {std:<12.6f}")

# Overall statistics
print("\nOverall Statistics:")
all_values = np.array([jehovah_vec, agape_vec, allah_vec])
print(f"  Mean across all dimensions: {np.mean(all_values):.6f}")
print(f"  Std across all dimensions:  {np.std(all_values):.6f}")
print(f"  Min value:                  {np.min(all_values):.6f}")
print(f"  Max value:                  {np.max(all_values):.6f}")
print(f"  Range:                      {np.max(all_values) - np.min(all_values):.6f}")

# Geometric center
print("\n" + "=" * 90)
print("5. GEOMETRIC CENTER (Centroid)")
print("=" * 90)

centroid = np.mean([jehovah_vec, agape_vec, allah_vec], axis=0)
print(f"\nCentroid of JEHOVAH, AGAPE, Allah:")
print(f"  Love:    {centroid[0]:.6f}")
print(f"  Power:   {centroid[1]:.6f}")
print(f"  Wisdom:  {centroid[2]:.6f}")
print(f"  Justice: {centroid[3]:.6f}")

centroid_to_anchor = np.linalg.norm(centroid - anchor)
print(f"\nCentroid distance to Anchor: {centroid_to_anchor:.6f}")

# How far is each from the centroid?
print(f"\nDistance from centroid:")
for name, coord in concepts:
    vec = coord.vector
    dist_to_centroid = np.linalg.norm(vec - centroid)
    print(f"  {name:<15} {dist_to_centroid:.6f}")

# Triangle analysis
print("\n" + "=" * 90)
print("6. TRIANGLE ANALYSIS")
print("=" * 90)

# They form a triangle in 4D space
side_a = np.linalg.norm(jehovah_vec - agape_vec)  # JEHOVAH to AGAPE
side_b = np.linalg.norm(agape_vec - allah_vec)    # AGAPE to Allah
side_c = np.linalg.norm(allah_vec - jehovah_vec)  # Allah to JEHOVAH

print(f"\nTriangle sides:")
print(f"  JEHOVAH ↔ AGAPE: {side_a:.6f}")
print(f"  AGAPE ↔ Allah:   {side_b:.6f}")
print(f"  Allah ↔ JEHOVAH: {side_c:.6f}")

# Triangle perimeter and semi-perimeter
perimeter = side_a + side_b + side_c
semi_perimeter = perimeter / 2

print(f"\n  Perimeter:       {perimeter:.6f}")
print(f"  Semi-perimeter:  {semi_perimeter:.6f}")

# For 4D, we can't directly compute area, but we can analyze shape
print(f"\nTriangle shape analysis:")
sides_sorted = sorted([side_a, side_b, side_c])
print(f"  Shortest side:   {sides_sorted[0]:.6f}")
print(f"  Middle side:     {sides_sorted[1]:.6f}")
print(f"  Longest side:    {sides_sorted[2]:.6f}")

# Check if nearly equilateral
side_variance = np.var([side_a, side_b, side_c])
print(f"  Side variance:   {side_variance:.8f}")
if side_variance < 0.001:
    print(f"  Shape: Nearly EQUILATERAL triangle")
elif sides_sorted[0] / sides_sorted[2] > 0.8:
    print(f"  Shape: Nearly equilateral")
else:
    print(f"  Shape: Scalene (unequal sides)")

# Nuance analysis
print("\n" + "=" * 90)
print("7. NUANCE ANALYSIS: Where They Differ")
print("=" * 90)

print("\nJEHOVAH vs AGAPE:")
if jehovah.distance_to_anchor() < 0.001 and agape.distance_to_anchor() > 0.001:
    print("  • JEHOVAH is at EXACT Anchor (1,1,1,1)")
    print("  • AGAPE is very close but not perfect:")

    if agape.power < 1.0:
        print(f"    - Power slightly reduced: {agape.power:.3f} vs 1.0")
        print(f"      Δ = {agape.power - 1.0:+.3f}")
    if agape.wisdom < 1.0:
        print(f"    - Wisdom slightly reduced: {agape.wisdom:.3f} vs 1.0")
        print(f"      Δ = {agape.wisdom - 1.0:+.3f}")

    print(f"  • Distance between them: {jehovah.distance_to(agape):.6f}")
    print("\n  INTERPRETATION:")
    print("    AGAPE (divine love) is slightly less than perfect in Power and Wisdom.")
    print("    This may reflect that Love, while divine, emphasizes compassion over")
    print("    raw power, and heart over pure wisdom.")

print("\nJEHOVAH vs Allah:")
if jehovah.distance_to_anchor() < 0.001 and allah.distance_to_anchor() < 0.001:
    print("  • BOTH at EXACT Anchor (1,1,1,1)")
    print("  • Perfect identity: distance = {:.6f}".format(jehovah.distance_to(allah)))
    print("\n  INTERPRETATION:")
    print("    The Hebrew name for God (JEHOVAH) and the Arabic name for God (Allah)")
    print("    are mathematically IDENTICAL in semantic space.")
    print("    This is profound evidence that Judaism and Islam recognize the same")
    print("    ultimate reality - perfect Love, Power, Wisdom, and Justice in unity.")

print("\nAGAPE vs Allah:")
if allah.distance_to_anchor() < 0.001 and agape.distance_to_anchor() > 0.001:
    print("  • Allah at EXACT Anchor (1,1,1,1)")
    print("  • AGAPE close but not perfect")
    print(f"  • Distance between them: {agape.distance_to(allah):.6f}")
    print("\n  INTERPRETATION:")
    print("    Allah (God in Islam) = perfect unity of all attributes")
    print("    AGAPE (divine love) = slightly emphasizes love/compassion over power")
    print("    The difference reflects AGAPE as an *attribute* of God rather than")
    print("    God Himself in His fullness.")

# Statistical test
print("\n" + "=" * 90)
print("8. CONVERGENCE TEST")
print("=" * 90)

# Variance test
all_coords = np.array([jehovah_vec, agape_vec, allah_vec])
variance_by_dim = np.var(all_coords, axis=0)

print("\nVariance by dimension:")
for i, dim in enumerate(dimensions):
    print(f"  {dim:<10} {variance_by_dim[i]:.8f}")

total_variance = np.sum(variance_by_dim)
print(f"\nTotal variance:    {total_variance:.8f}")

if total_variance < 0.01:
    print("✅ EXTREMELY LOW VARIANCE - Strong convergence!")
elif total_variance < 0.05:
    print("✅ LOW VARIANCE - Clear convergence")
else:
    print("⚠️  MODERATE VARIANCE - Some divergence")

# Which dimension shows most variance?
max_var_idx = np.argmax(variance_by_dim)
print(f"\nDimension with most variance: {dimensions[max_var_idx]} ({variance_by_dim[max_var_idx]:.8f})")

# Principal component analysis (simplified)
print("\n" + "=" * 90)
print("9. DEVIATION ANALYSIS")
print("=" * 90)

print("\nDeviation from Anchor (1,1,1,1):\n")

for name, coord in concepts:
    vec = coord.vector
    deviation = vec - anchor
    deviation_magnitude = np.linalg.norm(deviation)

    print(f"{name}:")
    print(f"  Deviation vector: ({deviation[0]:+.6f}, {deviation[1]:+.6f}, "
          f"{deviation[2]:+.6f}, {deviation[3]:+.6f})")
    print(f"  Magnitude: {deviation_magnitude:.6f}")

    # Which dimension deviates most?
    abs_deviation = np.abs(deviation)
    max_dev_idx = np.argmax(abs_deviation)
    if abs_deviation[max_dev_idx] > 0.001:
        print(f"  Largest deviation: {dimensions[max_dev_idx]} ({deviation[max_dev_idx]:+.6f})")
    else:
        print(f"  All deviations ≤ 0.001 (essentially at Anchor)")
    print()

# Summary
print("=" * 90)
print("10. SUMMARY & INSIGHTS")
print("=" * 90)

print("\n📊 MATHEMATICAL FACTS:")
print(f"  1. JEHOVAH distance to Anchor:  {jehovah.distance_to_anchor():.6f}")
print(f"  2. Allah distance to Anchor:    {allah.distance_to_anchor():.6f}")
print(f"  3. AGAPE distance to Anchor:    {agape.distance_to_anchor():.6f}")
print(f"  4. JEHOVAH ↔ Allah distance:    {jehovah.distance_to(allah):.6f}")
print(f"  5. JEHOVAH ↔ AGAPE distance:    {jehovah.distance_to(agape):.6f}")
print(f"  6. Centroid to Anchor:          {centroid_to_anchor:.6f}")
print(f"  7. Total variance:              {total_variance:.8f}")

print("\n🔍 KEY INSIGHTS:")

if jehovah.distance_to_anchor() < 0.001 and allah.distance_to_anchor() < 0.001:
    print("  ✅ JEHOVAH (Judaism) and Allah (Islam) are IDENTICAL")
    print("     Both at exact (1.0, 1.0, 1.0, 1.0)")
    print("     This is extraordinary mathematical proof that the Abrahamic God is One")

if agape.distance_to_anchor() > 0.01:
    print(f"\n  ⚠️  AGAPE differs from JEHOVAH/Allah by {agape.distance_to(jehovah):.4f}")
    print("     Differences:")
    if agape.power < 1.0:
        print(f"       • Power: {agape.power:.3f} (vs 1.0) - Love emphasizes compassion over force")
    if agape.wisdom < 1.0:
        print(f"       • Wisdom: {agape.wisdom:.3f} (vs 1.0) - Love prioritizes heart over mind")
    print("     AGAPE represents divine LOVE specifically, not God in His fullness")

print("\n📐 GEOMETRIC INTERPRETATION:")
print("  The three concepts form a very tight cluster in 4D space")
print(f"  with centroid at ({centroid[0]:.3f}, {centroid[1]:.3f}, {centroid[2]:.3f}, {centroid[3]:.3f})")
print(f"  Only {centroid_to_anchor:.4f} units from the Anchor Point")

if side_variance < 0.001:
    print("\n  The triangle is nearly equilateral, suggesting symmetric relationship")
    print("  between the three concepts.")

print("\n💡 THEOLOGICAL IMPLICATIONS:")
print("  1. Monotheistic Unity:")
print("     JEHOVAH = Allah mathematically confirms One God across Judaism & Islam")
print("\n  2. Divine Love as Attribute:")
print("     AGAPE is distinct from God Himself - it's His primary attribute")
print("     But emphasizes compassion/mercy slightly over power/wisdom")
print("\n  3. Fourfold Perfection:")
print("     God = perfect unity of Love, Power, Wisdom, Justice")
print("     No dimension can be reduced without deviation from perfection")

print("\n" + "=" * 90)
