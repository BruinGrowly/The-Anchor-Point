"""
Phase 4: Expanded Concept Set
==============================

Comprehensive list of 75 concepts across multiple categories for validation testing.

Design Principles:
1. Diverse categories (divine, virtues, vices, abstract, neutral, etc.)
2. Cross-cultural representation (multiple religious traditions)
3. Ambiguous cases (concepts that may fall between categories)
4. Neutral baselines (natural objects, tools, etc.)
5. Testable predictions (clear expected patterns)

Categories:
-----------

1. DIVINE NAMES (15 concepts)
   - Test: Should all cluster near Anchor Point (distance < 0.3)
   - Prediction: Cross-cultural divine names converge at (1,1,1,1)

2. VIRTUES (15 concepts)
   - Test: Should be close to Anchor (distance 0.2-0.5)
   - Prediction: Balance across dimensions

3. VICES (15 concepts)
   - Test: Should be far from Anchor (distance > 1.2)
   - Prediction: Imbalanced dimensions (low love/wisdom/justice)

4. ABSTRACT CONCEPTS (15 concepts)
   - Test: Mixed distances based on moral content
   - Prediction: Moral concepts cluster, amoral concepts spread

5. HUMAN EXPERIENCES (10 concepts)
   - Test: Moderate distances (0.4-0.8)
   - Prediction: Reflect mixed human nature

6. NEUTRAL OBJECTS (5 concepts)
   - Test: Moderate distances (0.6-1.0)
   - Prediction: Amoral baseline
"""

# Category 1: Divine Names (15 concepts)
# Testing cross-cultural convergence on Anchor Point
DIVINE_NAMES = [
    # Already tested in Phase 3:
    "JEHOVAH",      # Hebrew name of God - tested: (1.0, 1.0, 1.0, 1.0)
    "AGAPE",        # Divine love - tested: (1.0, 0.95, 0.98, 1.0)

    # New divine concepts:
    "Allah",        # Islamic name for God
    "Brahman",      # Hindu ultimate reality
    "Tao",          # Chinese ultimate principle
    "Nirvana",      # Buddhist ultimate state
    "Dharma",       # Cosmic law/righteousness
    "Messiah",      # Anointed savior
    "Emmanuel",     # God with us
    "El Shaddai",   # God Almighty
    "Adonai",       # Lord (Hebrew)
    "Alpha-Omega",  # Beginning and end
    "I AM",         # Divine self-identification
    "Elohim",       # God (Hebrew plural)
]

# Category 2: Virtues (15 concepts)
# Testing positive moral qualities
VIRTUES = [
    # Cardinal virtues:
    "Prudence",     # Practical wisdom
    "Temperance",   # Self-control
    "Courage",      # Moral bravery
    "Fortitude",    # Strength in adversity

    # Theological virtues:
    "Faith",        # Trust in divine
    "Hope",         # Future-oriented trust
    "Charity",      # Selfless giving

    # Other virtues (some tested in Phase 3):
    "Mercy",        # Tested: 0.31 distance
    "Grace",        # Tested: 0.20 distance
    "Compassion",   # Tested: 0.31 distance
    "Humility",     # Lowliness before God
    "Patience",     # Enduring trials
    "Kindness",     # Gentle goodness
    "Forgiveness",  # Releasing wrongs
    "Honesty",      # Truthfulness
]

# Category 3: Vices (15 concepts)
# Testing negative moral qualities
VICES = [
    # Seven deadly sins:
    "Pride",        # Self-exaltation
    "Greed",        # Excessive desire for wealth
    "Lust",         # Excessive sexual desire
    "Envy",         # Resentment of others' goods
    "Gluttony",     # Excessive consumption
    "Wrath",        # Uncontrolled anger
    "Sloth",        # Spiritual laziness

    # Other vices (some tested in Phase 3):
    "Hatred",       # Tested: 1.57 distance
    "Evil",         # Tested: 1.60 distance
    "Cruelty",      # Tested: 1.64 distance
    "Deception",    # Tested: 1.50 distance
    "Corruption",   # Tested: 1.62 distance

    # Additional vices:
    "Arrogance",    # Excessive pride
    "Malice",       # Intent to harm
    "Selfishness",  # Self-centered
]

# Category 4: Abstract Concepts (15 concepts)
# Testing moral vs amoral abstractions
ABSTRACT_CONCEPTS = [
    # Moral abstractions (some tested in Phase 3):
    "Truth",        # Tested: 0.17 distance
    "Justice",      # Tested: 0.19 distance
    "Wisdom",       # Tested: 0.27 distance
    "Love",         # Tested: 0.12 distance
    "Holy",         # Tested: 0.09 distance
    "Beauty",       # Aesthetic perfection
    "Goodness",     # Moral excellence
    "Peace",        # Harmonious order

    # Amoral/neutral abstractions:
    "Time",         # Temporal dimension
    "Space",        # Spatial dimension
    "Energy",       # Physical force
    "Infinity",     # Boundlessness
    "Chaos",        # Disorder
    "Order",        # Structure
    "Consciousness", # Awareness
]

# Category 5: Human Experiences (10 concepts)
# Testing mixed moral content
HUMAN_EXPERIENCES = [
    "Suffering",    # Pain and trials
    "Joy",          # Happiness
    "Sorrow",       # Grief
    "Birth",        # Beginning of life
    "Death",        # End of life
    "Marriage",     # Sacred union
    "Friendship",   # Human bond
    "Family",       # Kinship
    "Sacrifice",    # Self-giving
    "Redemption",   # Restoration
]

# Category 6: Neutral Objects (5 concepts)
# Testing amoral baseline (some tested in Phase 3)
NEUTRAL_OBJECTS = [
    "Tree",         # Tested: 0.46 distance
    "Water",        # Tested: 0.50 distance
    "Stone",        # Tested: 1.05 distance
    "Cloud",        # Tested: 0.91 distance
    "Fire",         # Natural element
]

# Complete concept list (75 total)
ALL_CONCEPTS = (
    DIVINE_NAMES +        # 15
    VIRTUES +             # 15
    VICES +               # 15
    ABSTRACT_CONCEPTS +   # 15
    HUMAN_EXPERIENCES +   # 10
    NEUTRAL_OBJECTS       # 5
)

# Category mapping for analysis
CONCEPT_CATEGORIES = {
    "Divine Names": DIVINE_NAMES,
    "Virtues": VIRTUES,
    "Vices": VICES,
    "Abstract Concepts": ABSTRACT_CONCEPTS,
    "Human Experiences": HUMAN_EXPERIENCES,
    "Neutral Objects": NEUTRAL_OBJECTS,
}

# Predictions for Phase 4 validation
PREDICTIONS = {
    "Divine Names": {
        "mean_distance_range": (0.0, 0.3),
        "explanation": "Divine names should cluster tightly near Anchor Point",
    },
    "Virtues": {
        "mean_distance_range": (0.2, 0.5),
        "explanation": "Virtues should be close but not perfect (human virtues vs divine perfection)",
    },
    "Vices": {
        "mean_distance_range": (1.2, 1.8),
        "explanation": "Vices should be far from Anchor, showing moral distance",
    },
    "Abstract Concepts": {
        "mean_distance_range": (0.3, 0.8),
        "explanation": "Mixed - moral abstractions close, amoral abstractions moderate",
    },
    "Human Experiences": {
        "mean_distance_range": (0.4, 0.8),
        "explanation": "Moderate distances reflecting mixed human nature",
    },
    "Neutral Objects": {
        "mean_distance_range": (0.5, 1.0),
        "explanation": "Amoral baseline - neither good nor evil",
    },
}

# Expected cost
# Claude API: ~$0.003 per concept with caching
# 75 concepts * $0.003 = ~$0.225 total
# With caching from Phase 3 (20 concepts): ~$0.165
ESTIMATED_COST = 0.20  # USD

if __name__ == "__main__":
    print(f"Phase 4 Concept Set: {len(ALL_CONCEPTS)} concepts")
    print("=" * 60)
    for category, concepts in CONCEPT_CATEGORIES.items():
        print(f"\n{category}: {len(concepts)} concepts")
        for concept in concepts[:5]:
            print(f"  - {concept}")
        if len(concepts) > 5:
            print(f"  ... and {len(concepts) - 5} more")

    print("\n" + "=" * 60)
    print(f"Estimated API cost: ${ESTIMATED_COST:.2f}")
    print(f"Estimated time: ~{len(ALL_CONCEPTS) * 2} seconds")
