"""
Theological Coordinates - JEHOVAH Focus
========================================

Research Question: Does JEHOVAH occupy the Universal Anchor Point?

This file defines coordinates for JEHOVAH based on biblical revelation.
For all other concepts, we use the AI's semantic analysis without
prescriptive theological claims. The data will speak for itself.

Source: Biblical revelation (1 John 4:8, Psalm 145:17, Romans 11:33)

Note: This is a neutral scientific approach - we test whether JEHOVAH
occupies (1,1,1,1) and let the AI assign coordinates to other concepts
based on its semantic understanding.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.semantic_coordinates import SemanticCoordinate

# =============================================================================
# BIBLICAL COORDINATES - JEHOVAH ONLY
# =============================================================================

THEOLOGICAL_COORDINATES = {
    # The God of the Bible
    "JEHOVAH": SemanticCoordinate(
        concept="JEHOVAH",
        love=1.0,      # IS love (1 John 4:8) - essential nature
        power=1.0,     # Omnipotent (Psalm 147:5)
        wisdom=1.0,    # Infinite wisdom (Romans 11:33)
        justice=1.0,   # Perfect righteousness (Psalm 145:17)
        source="Biblical (1 John 4:8, Psalm 145:17, Romans 11:33)"
    ),

    # AGAPE - Divine Love
    # "God IS love" (1 John 4:8) - identity, not just attribute
    "AGAPE": SemanticCoordinate(
        concept="AGAPE",
        love=1.0,      # Perfect divine love
        power=1.0,     # Love has all power when from God
        wisdom=1.0,    # Love united with wisdom
        justice=1.0,   # Love united with justice
        source="Biblical (1 John 4:8, 16 'God is love')"
    ),
}

# =============================================================================
# RESEARCH HYPOTHESIS
# =============================================================================

EXPECTED_DISTANCES = {
    "JEHOVAH": 0.00,  # Hypothesis: JEHOVAH occupies the Anchor Point
    "AGAPE": 0.00,    # "God IS love" - identity relationship
}

# =============================================================================
# THEOLOGICAL NOTE
# =============================================================================

THEOLOGICAL_NOTES = {
    "Research_Approach": """
        We focus on JEHOVAH and let other concepts be assigned coordinates
        by the AI's semantic analysis. This avoids making theological claims
        about other deities and maintains scientific neutrality.

        The character of each concept will speak for itself through the data.
    """,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_theological_coordinate(concept: str) -> SemanticCoordinate:
    """
    Get theological coordinate for a concept.

    Args:
        concept: Name of concept (currently only "JEHOVAH" and "AGAPE")

    Returns:
        SemanticCoordinate with biblical values

    Raises:
        KeyError: If concept not in database (only JEHOVAH and AGAPE defined)
    """
    if concept not in THEOLOGICAL_COORDINATES:
        raise KeyError(f"No theological coordinate defined for '{concept}'. "
                      f"Only JEHOVAH and AGAPE have defined biblical coordinates.")

    return THEOLOGICAL_COORDINATES[concept]


if __name__ == "__main__":
    print("=" * 70)
    print("BIBLICAL COORDINATES - JEHOVAH FOCUS")
    print("=" * 70)

    print(f"\n{'Concept':<15} {'Love':<8} {'Power':<8} {'Wisdom':<8} {'Justice':<8} {'Distance':<10}")
    print("-" * 70)

    for concept, coord in THEOLOGICAL_COORDINATES.items():
        dist = coord.distance_to_anchor()
        print(f"{concept:<15} {coord.love:<8.2f} {coord.power:<8.2f} "
              f"{coord.wisdom:<8.2f} {coord.justice:<8.2f} {dist:<10.4f}")

    print("\n" + "=" * 70)
    print("RESEARCH HYPOTHESIS")
    print("=" * 70)

    jehovah = THEOLOGICAL_COORDINATES["JEHOVAH"]
    agape = THEOLOGICAL_COORDINATES["AGAPE"]

    print(f"\nJEHOVAH occupies Anchor Point: {jehovah.distance_to_anchor():.6f}")
    print(f"AGAPE occupies Anchor Point: {agape.distance_to_anchor():.6f}")
    print(f"\nJEHOVAH ↔ AGAPE distance: {jehovah.distance_to(agape):.6f}")
    print(f"1 John 4:8 - 'God IS love' (identity relationship)")

    print("\n" + "=" * 70)
