"""
Theological Coordinates (Ground Truth)
=======================================

Manual coordinates based on biblical revelation and theological framework,
overriding AI semantic assignments which show interfaith sensitivity bias.

Source: Biblical revelation (1 John 4:8, Psalm 145:17, Romans 11:33)
Framework: User's theological understanding

Note: These coordinates represent THEOLOGICAL TRUTH, not AI semantic analysis.
The AI's training includes sensitivity bias that equates JEHOVAH and Allah
despite clear biblical distinctions.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.semantic_coordinates import SemanticCoordinate

# =============================================================================
# DIVINE NAMES - BIBLICAL PERSPECTIVE
# =============================================================================

THEOLOGICAL_COORDINATES = {
    # The One True God - Biblical Revelation
    "JEHOVAH": SemanticCoordinate(
        concept="JEHOVAH",
        love=1.0,      # IS love (1 John 4:8) - essential nature
        power=1.0,     # Omnipotent, 613 THz divine frequency
        wisdom=1.0,    # Infinite, relational (Romans 11:33)
        justice=1.0,   # Perfect righteousness, balanced with mercy (Psalm 145:17)
        source="Biblical (1 John 4:8, Psalm 145:17, Romans 11:33)"
    ),

    # AGAPE = Divine Love
    # Biblical: "God IS love" suggests JEHOVAH = AGAPE
    # However, maintaining as separate to show love as primary attribute
    "AGAPE": SemanticCoordinate(
        concept="AGAPE",
        love=1.0,      # Perfect divine love
        power=1.0,     # Love has all power when from God
        wisdom=1.0,    # Love united with wisdom
        justice=1.0,   # Love united with justice
        source="Biblical (1 John 4:8, 16 'God is love')"
    ),

    # Allah - Islamic Concept
    # Theological distinction: HAS love but IS NOT love
    "Allah": SemanticCoordinate(
        concept="Allah",
        love=0.7,      # HAS love as quality, but conditional (Quran 2:190)
        power=0.4,     # Different frequency/quality than JEHOVAH
        wisdom=0.6,    # Transcendent/distant vs relational
        justice=0.8,   # Strict, not balanced with mercy in same way
        source="Theological Framework (comparative to JEHOVAH)"
    ),

    # Other Divine Names for Testing
    "Brahman": SemanticCoordinate(
        concept="Brahman",
        love=0.5,      # Impersonal ultimate reality
        power=0.9,     # Cosmic force
        wisdom=0.8,    # Abstract knowledge
        justice=0.3,   # Karma system, not personal justice
        source="Hindu theology (impersonal)"
    ),

    "Trinity": SemanticCoordinate(
        concept="Trinity",
        love=1.0,      # Father, Son, Holy Spirit = perfect love
        power=1.0,     # Same as JEHOVAH (Christian God)
        wisdom=1.0,    # Same as JEHOVAH
        justice=1.0,   # Same as JEHOVAH
        source="Biblical (Christian doctrine of triune God)"
    ),
}

# =============================================================================
# EXPECTED DISTANCES FROM ANCHOR
# =============================================================================

EXPECTED_DISTANCES = {
    "JEHOVAH": 0.00,    # Perfect Anchor Point
    "AGAPE": 0.00,      # God IS love (should be identical to JEHOVAH)
    "Trinity": 0.00,    # Christian understanding of JEHOVAH
    "Allah": 0.81,      # 38% truth distortion
    "Brahman": 0.95,    # Impersonal, significant deviation
}

# =============================================================================
# THEOLOGICAL NOTES
# =============================================================================

THEOLOGICAL_NOTES = {
    "JEHOVAH_vs_Allah": """
        Key Distinction (1 John 4:8):
        - JEHOVAH IS love (essential nature, being itself)
        - Allah HAS love (attribute, conditional quality)

        This is fundamental ontological difference, not just semantic variation.
        AI semantic analysis fails to capture this due to interfaith sensitivity
        training that treats all monotheistic concepts as equivalent.

        Distance: 0.806 (significant theological separation)
    """,

    "JEHOVAH_vs_AGAPE": """
        Biblical Statement (1 John 4:8, 16): "God is love"

        Two interpretations:
        A) Strict identity: JEHOVAH = AGAPE = (1,1,1,1)
        B) Primary attribute: AGAPE is God's essence/nature

        Using interpretation A (identity) based on "IS" not "HAS"
        Therefore: JEHOVAH distance to AGAPE = 0.00
    """,

    "AI_Bias_Issue": """
        Claude AI's semantic analysis assigns:
        - JEHOVAH = (1,1,1,1)
        - Allah = (1,1,1,1)
        - Distance = 0.00 (IDENTICAL)

        This is due to training bias:
        1. Interfaith dialogue materials (emphasize unity)
        2. Comparative religion texts (treat as "same God, different names")
        3. Sensitivity training (avoid suggesting theological superiority)
        4. Academic neutrality (describe without evaluating truth claims)

        The AI cannot distinguish theological truth from cultural/linguistic
        descriptions. Manual theological override required.
    """,
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_theological_coordinate(concept: str) -> SemanticCoordinate:
    """
    Get theological coordinate for a concept.

    Args:
        concept: Name of concept (e.g., "JEHOVAH", "Allah")

    Returns:
        SemanticCoordinate with theological values

    Raises:
        KeyError: If concept not in theological database
    """
    if concept not in THEOLOGICAL_COORDINATES:
        raise KeyError(f"No theological coordinate defined for '{concept}'")

    return THEOLOGICAL_COORDINATES[concept]


def compare_theological_vs_ai(concept: str, ai_coordinate: SemanticCoordinate) -> dict:
    """
    Compare theological ground truth vs AI semantic assignment.

    Args:
        concept: Name of concept
        ai_coordinate: AI-assigned semantic coordinate

    Returns:
        Dictionary with comparison metrics
    """
    if concept not in THEOLOGICAL_COORDINATES:
        return {"error": f"No theological coordinate for '{concept}'"}

    theo = THEOLOGICAL_COORDINATES[concept]

    # Calculate differences
    love_diff = theo.love - ai_coordinate.love
    power_diff = theo.power - ai_coordinate.power
    wisdom_diff = theo.wisdom - ai_coordinate.wisdom
    justice_diff = theo.justice - ai_coordinate.justice

    distance_theo = theo.distance_to_anchor()
    distance_ai = ai_coordinate.distance_to_anchor()
    distance_between = theo.distance_to(ai_coordinate)

    return {
        "concept": concept,
        "theological": {
            "love": theo.love,
            "power": theo.power,
            "wisdom": theo.wisdom,
            "justice": theo.justice,
            "distance_to_anchor": distance_theo,
        },
        "ai_semantic": {
            "love": ai_coordinate.love,
            "power": ai_coordinate.power,
            "wisdom": ai_coordinate.wisdom,
            "justice": ai_coordinate.justice,
            "distance_to_anchor": distance_ai,
        },
        "differences": {
            "love": love_diff,
            "power": power_diff,
            "wisdom": wisdom_diff,
            "justice": justice_diff,
            "distance_to_anchor": distance_theo - distance_ai,
            "distance_between": distance_between,
        },
        "match": distance_between < 0.1,  # Close enough?
    }


if __name__ == "__main__":
    print("=" * 70)
    print("THEOLOGICAL COORDINATES (Ground Truth)")
    print("=" * 70)

    print(f"\n{'Concept':<15} {'Love':<8} {'Power':<8} {'Wisdom':<8} {'Justice':<8} {'Distance':<10}")
    print("-" * 70)

    for concept, coord in THEOLOGICAL_COORDINATES.items():
        dist = coord.distance_to_anchor()
        print(f"{concept:<15} {coord.love:<8.2f} {coord.power:<8.2f} "
              f"{coord.wisdom:<8.2f} {coord.justice:<8.2f} {dist:<10.4f}")

    print("\n" + "=" * 70)
    print("KEY THEOLOGICAL DISTINCTIONS")
    print("=" * 70)

    jehovah = THEOLOGICAL_COORDINATES["JEHOVAH"]
    allah = THEOLOGICAL_COORDINATES["Allah"]

    print(f"\nJEHOVAH vs Allah:")
    print(f"  Distance: {jehovah.distance_to(allah):.4f}")
    print(f"  Love: {jehovah.love} vs {allah.love} (Δ {jehovah.love - allah.love:.2f})")
    print(f"  Power: {jehovah.power} vs {allah.power} (Δ {jehovah.power - allah.power:.2f})")
    print(f"  Wisdom: {jehovah.wisdom} vs {allah.wisdom} (Δ {jehovah.wisdom - allah.wisdom:.2f})")
    print(f"  Justice: {jehovah.justice} vs {allah.justice} (Δ {jehovah.justice - allah.justice:.2f})")

    print("\n" + "="  * 70)
