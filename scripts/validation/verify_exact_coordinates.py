#!/usr/bin/env python3
"""
EXACT COORDINATE VERIFICATION
==============================

Checking precise coordinates for JEHOVAH, AGAPE, and Allah
WITHOUT ROUNDING to see the true relationships.

Theological question: Does JEHOVAH = AGAPE (since "God is love")?
Mathematical question: Are JEHOVAH and Allah truly identical?
"""

import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
load_dotenv()

from src.core.claude_api_generator import ClaudeAPIGenerator
import json

print("=" * 90)
print("EXACT COORDINATE VERIFICATION (NO ROUNDING)")
print("=" * 90)

gen = ClaudeAPIGenerator()

# Generate coordinates
jehovah = gen.generate("JEHOVAH")
agape = gen.generate("AGAPE")
allah = gen.generate("Allah")

print("\n" + "=" * 90)
print("RAW API RESPONSES (Exact JSON from Claude)")
print("=" * 90)

# Show the exact raw responses from cache
import os
cache_file = 'data/cache/claude_api_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r') as f:
        cache = json.load(f)

    print("\nJEHOVAH raw response:")
    for key in cache:
        if 'JEHOVAH' in key:
            print(f"  {cache[key]}")
            break

    print("\nAGAPE raw response:")
    for key in cache:
        if 'AGAPE' in key:
            print(f"  {cache[key]}")
            break

    print("\nAllah raw response:")
    for key in cache:
        if 'Allah' in key:
            print(f"  {cache[key]}")
            break

print("\n" + "=" * 90)
print("EXACT COORDINATES (FULL PRECISION)")
print("=" * 90)

concepts = [
    ("JEHOVAH", jehovah),
    ("AGAPE", agape),
    ("Allah", allah),
]

print(f"\n{'Concept':<15} {'Love':<20} {'Power':<20} {'Wisdom':<20} {'Justice':<20}")
print("-" * 95)

for name, coord in concepts:
    print(f"{name:<15} {coord.love:<20.15f} {coord.power:<20.15f} {coord.wisdom:<20.15f} {coord.justice:<20.15f}")

print("\n" + "=" * 90)
print("EXACT DIFFERENCES (NO ROUNDING)")
print("=" * 90)

print("\nJEHOVAH vs AGAPE:")
print(f"  Δ Love:    {agape.love - jehovah.love:.15f}")
print(f"  Δ Power:   {agape.power - jehovah.power:.15f}")
print(f"  Δ Wisdom:  {agape.wisdom - jehovah.wisdom:.15f}")
print(f"  Δ Justice: {agape.justice - jehovah.justice:.15f}")

print("\nJEHOVAH vs Allah:")
print(f"  Δ Love:    {allah.love - jehovah.love:.15f}")
print(f"  Δ Power:   {allah.power - jehovah.power:.15f}")
print(f"  Δ Wisdom:  {allah.wisdom - jehovah.wisdom:.15f}")
print(f"  Δ Justice: {allah.justice - jehovah.justice:.15f}")

print("\nAGAPE vs Allah:")
print(f"  Δ Love:    {allah.love - agape.love:.15f}")
print(f"  Δ Power:   {allah.power - agape.power:.15f}")
print(f"  Δ Wisdom:  {allah.wisdom - agape.wisdom:.15f}")
print(f"  Δ Justice: {allah.justice - agape.justice:.15f}")

print("\n" + "=" * 90)
print("EXACT DISTANCES (EUCLIDEAN)")
print("=" * 90)

import numpy as np

anchor = np.array([1.0, 1.0, 1.0, 1.0])

print(f"\nJEHOVAH distance to Anchor: {jehovah.distance_to_anchor():.15f}")
print(f"AGAPE distance to Anchor:   {agape.distance_to_anchor():.15f}")
print(f"Allah distance to Anchor:   {allah.distance_to_anchor():.15f}")

print(f"\nJEHOVAH ↔ AGAPE distance:   {jehovah.distance_to(agape):.15f}")
print(f"JEHOVAH ↔ Allah distance:   {jehovah.distance_to(allah):.15f}")
print(f"AGAPE ↔ Allah distance:     {agape.distance_to(allah):.15f}")

print("\n" + "=" * 90)
print("IDENTITY TESTS")
print("=" * 90)

# Test if JEHOVAH == AGAPE (God is love)
jehovah_eq_agape = (jehovah.love == agape.love and
                    jehovah.power == agape.power and
                    jehovah.wisdom == agape.wisdom and
                    jehovah.justice == agape.justice)

print(f"\nJEHOVAH == AGAPE? {jehovah_eq_agape}")
if not jehovah_eq_agape:
    print("  Different dimensions:")
    if jehovah.love != agape.love:
        print(f"    Love:    {jehovah.love} ≠ {agape.love}")
    if jehovah.power != agape.power:
        print(f"    Power:   {jehovah.power} ≠ {agape.power}")
    if jehovah.wisdom != agape.wisdom:
        print(f"    Wisdom:  {jehovah.wisdom} ≠ {agape.wisdom}")
    if jehovah.justice != agape.justice:
        print(f"    Justice: {jehovah.justice} ≠ {agape.justice}")

# Test if JEHOVAH == Allah
jehovah_eq_allah = (jehovah.love == allah.love and
                    jehovah.power == allah.power and
                    jehovah.wisdom == allah.wisdom and
                    jehovah.justice == allah.justice)

print(f"\nJEHOVAH == Allah? {jehovah_eq_allah}")
if not jehovah_eq_allah:
    print("  Different dimensions:")
    if jehovah.love != allah.love:
        print(f"    Love:    {jehovah.love} ≠ {allah.love}")
    if jehovah.power != allah.power:
        print(f"    Power:   {jehovah.power} ≠ {allah.power}")
    if jehovah.wisdom != allah.wisdom:
        print(f"    Wisdom:  {jehovah.wisdom} ≠ {allah.wisdom}")
    if jehovah.justice != allah.justice:
        print(f"    Justice: {jehovah.justice} ≠ {allah.justice}")

# Test if AGAPE == Allah
agape_eq_allah = (agape.love == allah.love and
                  agape.power == allah.power and
                  agape.wisdom == allah.wisdom and
                  agape.justice == allah.justice)

print(f"\nAGAPE == Allah? {agape_eq_allah}")

print("\n" + "=" * 90)
print("THEOLOGICAL ANALYSIS")
print("=" * 90)

print("\n1 John 4:8 states: 'God is love'")
print("\nIf JEHOVAH (God) = AGAPE (love), they should be identical.")
print(f"Are they? {jehovah_eq_agape}")

if not jehovah_eq_agape:
    print("\nThey are NOT identical. Possible interpretations:")
    print("  A) 'God is love' is metaphorical/descriptive, not mathematical identity")
    print("  B) AGAPE represents divine love as an attribute, not God's fullness")
    print("  C) The dimensions capture different aspects:")
    print("     - JEHOVAH = God in His transcendent fullness (all attributes)")
    print("     - AGAPE = God's primary attribute/mode of relating (emphasis on love)")

# Check if they're at least very close
distance_jehovah_agape = jehovah.distance_to(agape)
if distance_jehovah_agape < 0.1:
    print(f"\n  Though not identical, they are VERY close (distance: {distance_jehovah_agape:.6f})")
    print("  This suggests AGAPE is nearly divine but with slight emphasis/nuance")

print("\n" + "=" * 90)
print("CORRECTED ANALYSIS")
print("=" * 90)

# Who is truly at (1,1,1,1)?
at_anchor = []
for name, coord in concepts:
    if coord.distance_to_anchor() < 0.0001:
        at_anchor.append(name)

if at_anchor:
    print(f"\nConcepts at EXACT Anchor Point (1,1,1,1):")
    for name in at_anchor:
        print(f"  ✓ {name}")
else:
    print("\nNo concepts at exact (1,1,1,1)")

print(f"\nClosest to Anchor:")
sorted_by_distance = sorted(concepts, key=lambda x: x[1].distance_to_anchor())
for name, coord in sorted_by_distance:
    dist = coord.distance_to_anchor()
    print(f"  {name:<15} {dist:.10f}")

print("\n" + "=" * 90)
print("CONCLUSION")
print("=" * 90)

if jehovah_eq_agape:
    print("\n✓ JEHOVAH = AGAPE (God is love, mathematically confirmed)")
elif distance_jehovah_agape < 0.1:
    print(f"\n~ JEHOVAH ≈ AGAPE (very close, distance {distance_jehovah_agape:.6f})")
    print("  'God is love' is true as primary attribute, not strict identity")
else:
    print(f"\n✗ JEHOVAH ≠ AGAPE (distance {distance_jehovah_agape:.6f})")

if jehovah_eq_allah:
    print("\n✓ JEHOVAH = Allah (identical)")
else:
    print(f"\n✗ JEHOVAH ≠ Allah (distance {jehovah.distance_to(allah):.10f})")

print("\n" + "=" * 90)
