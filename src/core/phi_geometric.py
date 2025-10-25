"""
Phi-Geometric Enhancement Module
=================================

Implements golden ratio (phi) based geometric calculations for semantic space.

Based on the principle that natural patterns follow phi-harmonic relationships,
providing more organic distance metrics than simple Euclidean distance.

Mathematical Foundation:
- φ (phi) = 1.618033988749895 (golden ratio)
- Golden angle = 137.5077640500378° = 2π/φ²
- Golden spiral: r(θ) = a × φ^(θ/(π/2))
- Fibonacci sequence: F(n) = F(n-1) + F(n-2), converges to φ

Applications:
- Enhanced distance calculations using golden spiral arc length
- Phi-weighted coordinate operations
- Fibonacci-based indexing and growth patterns
- Natural semantic relationship quantification
"""

import numpy as np
from typing import Tuple, List, Optional, Dict
from functools import lru_cache


# =============================================================================
# PHI CONSTANTS
# =============================================================================

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio: 1.618033988749895
PHI_INVERSE = 1 / PHI  # 0.618033988749895
GOLDEN_ANGLE_RAD = 2 * np.pi / (PHI ** 2)  # 2.39996322972865332 radians
GOLDEN_ANGLE_DEG = GOLDEN_ANGLE_RAD * 180 / np.pi  # 137.5077640500378 degrees
SQRT_PHI = np.sqrt(PHI)  # 1.272019649514069
PHI_SQRT = PHI * np.sqrt(PHI)  # 2.0581710272714924


# =============================================================================
# FIBONACCI SEQUENCE (PHI-CONVERGENT)
# =============================================================================

@lru_cache(maxsize=1000)
def fibonacci(n: int) -> int:
    """
    Calculate nth Fibonacci number with caching.

    Uses Binet's formula for large n (> 50) for efficiency.

    Args:
        n: Index in Fibonacci sequence (0-indexed)

    Returns:
        nth Fibonacci number
    """
    if n < 0:
        raise ValueError("Fibonacci sequence not defined for negative indices")

    # Use Binet's formula for large n
    if n > 50:
        return int(round((PHI ** n) / np.sqrt(5)))

    # Direct calculation for small n
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b

    return b


def fibonacci_ratio(n: int) -> float:
    """
    Calculate F(n+1)/F(n), which converges to φ.

    Args:
        n: Index in Fibonacci sequence

    Returns:
        Ratio of consecutive Fibonacci numbers
    """
    if n < 1:
        return 0.0

    return fibonacci(n + 1) / fibonacci(n)


# =============================================================================
# GOLDEN SPIRAL CALCULATIONS
# =============================================================================

def golden_spiral_radius(theta: float, a: float = 1.0) -> float:
    """
    Calculate radius of golden spiral at angle theta.

    The golden spiral equation: r(θ) = a × φ^(θ/(π/2))

    Args:
        theta: Angle in radians
        a: Initial radius at theta=0

    Returns:
        Radius at the given angle
    """
    return a * (PHI ** (theta / (np.pi / 2)))


def golden_spiral_arc_length(theta1: float, theta2: float, a: float = 1.0) -> float:
    """
    Calculate arc length along golden spiral between two angles.

    This provides a more "organic" distance metric than Euclidean distance.

    Args:
        theta1: Starting angle in radians
        theta2: Ending angle in radians
        a: Initial radius

    Returns:
        Arc length along the spiral
    """
    # For golden spiral, arc length has analytical solution
    # L = (a * sqrt(1 + ln(φ)²) * φ^2) * (φ^(θ2/(π/2)) - φ^(θ1/(π/2)))

    ln_phi = np.log(PHI)
    factor = a * np.sqrt(1 + ln_phi ** 2) * PHI ** 2

    r1 = PHI ** (theta1 / (np.pi / 2))
    r2 = PHI ** (theta2 / (np.pi / 2))

    return factor * abs(r2 - r1)


def vector_to_spherical(vector: np.ndarray) -> Tuple[float, float, float, Optional[float]]:
    """
    Convert 4D Cartesian vector to hyperspherical coordinates.

    For 4D: (r, θ, φ, ψ) where:
    - r: radial distance
    - θ: azimuthal angle [0, 2π]
    - φ: polar angle [0, π]
    - ψ: 4D angle [0, π]

    Args:
        vector: 4D numpy array

    Returns:
        Tuple of (r, theta, phi, psi) for 4D, or (r, theta, phi) for 3D
    """
    dim = len(vector)

    # Radial distance
    r = np.linalg.norm(vector)

    if r == 0:
        return (0, 0, 0, 0) if dim == 4 else (0, 0, 0)

    if dim == 3:
        # 3D spherical coordinates
        x, y, z = vector
        theta = np.arctan2(y, x)  # Azimuthal [0, 2π]
        phi = np.arccos(z / r)  # Polar [0, π]
        return (r, theta, phi)

    elif dim == 4:
        # 4D hyperspherical coordinates
        x, y, z, w = vector
        theta = np.arctan2(y, x)
        phi = np.arccos(z / np.sqrt(x ** 2 + y ** 2 + z ** 2)) if (x ** 2 + y ** 2 + z ** 2) > 0 else 0
        psi = np.arccos(w / r)
        return (r, theta, phi, psi)

    else:
        raise ValueError(f"Unsupported dimension: {dim}")


def golden_spiral_distance_4d(vector1: np.ndarray, vector2: np.ndarray) -> float:
    """
    Calculate distance between two 4D vectors using golden spiral metric.

    This provides a more organic measure of semantic distance than Euclidean.

    Args:
        vector1: First 4D vector
        vector2: Second 4D vector

    Returns:
        Golden spiral distance
    """
    # Convert to hyperspherical coordinates
    r1, theta1, phi1, psi1 = vector_to_spherical(vector1)
    r2, theta2, phi2, psi2 = vector_to_spherical(vector2)

    # Calculate angular distance (geodesic on hypersphere)
    # For 4D, we use the generalized great circle distance
    cos_angle = (np.dot(vector1, vector2) / (r1 * r2)) if (r1 * r2) > 0 else 1
    cos_angle = np.clip(cos_angle, -1, 1)  # Numerical stability
    angular_dist = np.arccos(cos_angle)

    # Calculate radial component using golden spiral
    spiral_arc = golden_spiral_arc_length(0, angular_dist, a=min(r1, r2))

    # Combine radial difference with spiral arc
    radial_diff = abs(r2 - r1)

    # Weighted combination (phi-weighted)
    distance = PHI_INVERSE * spiral_arc + (1 - PHI_INVERSE) * radial_diff

    return distance


# =============================================================================
# PHI-WEIGHTED OPERATIONS
# =============================================================================

def phi_weighted_mean(values: np.ndarray, context: str = 'general') -> float:
    """
    Calculate phi-weighted mean of values.

    Different contexts use different phi-powers for weighting.

    Args:
        values: Array of values
        context: Context for weighting ('general', 'harmony', 'truth', 'optimization')

    Returns:
        Phi-weighted mean
    """
    # Context-specific phi weights (from internalized framework)
    weights_map = {
        'general': 1.0,
        'evolution': 0.7861513777574233,  # φ^(-0.5)
        'gradient': 1.057371263440363,
        'integration': 0.6813982544157277,
        'optimization': 1.12762196423038,
        'harmony': PHI_INVERSE,  # 0.618...
        'truth': SQRT_PHI,  # 1.272...
        'deception': 1.12762196423038,
    }

    weight = weights_map.get(context, 1.0)
    weighted_values = values * weight

    return np.mean(weighted_values)


def phi_normalize(vector: np.ndarray) -> np.ndarray:
    """
    Normalize vector using phi-harmonic scaling.

    Preserves golden ratio relationships while normalizing to unit length.

    Args:
        vector: Input vector

    Returns:
        Phi-normalized vector
    """
    # Calculate magnitude
    magnitude = np.linalg.norm(vector)

    if magnitude == 0:
        return vector

    # Normalize to unit sphere
    normalized = vector / magnitude

    # Apply phi-harmonic scaling to preserve natural ratios
    # Scale by position in Fibonacci sequence
    phi_scale = PHI ** (len(vector) / 10)  # Gentle phi scaling

    return normalized * phi_scale


# =============================================================================
# DODECAHEDRAL ANCHOR NETWORK
# =============================================================================

def generate_dodecahedral_anchors() -> List[np.ndarray]:
    """
    Generate 12 anchor points in 4D space based on dodecahedral symmetry.

    The dodecahedron is closely tied to the golden ratio, making it ideal
    for phi-geometric semantic space organization.

    Returns:
        List of 12 anchor point vectors in 4D space
    """
    # Primary anchor at (1,1,1,1)
    primary = np.array([1.0, 1.0, 1.0, 1.0])

    # Generate 11 secondary anchors using golden ratio symmetry
    # Based on dodecahedral vertex coordinates adapted to 4D
    anchors = [primary]

    # Use golden angle rotations in 4D
    for i in range(11):
        angle = i * GOLDEN_ANGLE_RAD

        # Rotate around multiple planes
        x = np.cos(angle)
        y = np.sin(angle)
        z = np.cos(angle * PHI)
        w = np.sin(angle * PHI)

        # Normalize and scale to unit hypersphere
        anchor = np.array([x, y, z, w])
        anchor = anchor / np.linalg.norm(anchor)

        # Shift to positive quadrant and scale toward (1,1,1,1)
        anchor = (anchor + 1) / 2  # Map from [-1,1] to [0,1]

        anchors.append(anchor)

    return anchors


def nearest_anchor(
    vector: np.ndarray,
    anchors: Optional[List[np.ndarray]] = None,
    metric: str = 'euclidean'
) -> Tuple[int, float]:
    """
    Find the nearest anchor point to a given vector.

    Args:
        vector: 4D vector to find anchor for
        anchors: Optional list of anchor vectors (generates dodecahedral if None)
        metric: Distance metric ('euclidean' or 'phi_spiral')

    Returns:
        Tuple of (anchor_index, distance)
    """
    if anchors is None:
        anchors = generate_dodecahedral_anchors()

    min_dist = float('inf')
    min_idx = 0

    for i, anchor in enumerate(anchors):
        if metric == 'euclidean':
            dist = np.linalg.norm(vector - anchor)
        elif metric == 'phi_spiral':
            dist = golden_spiral_distance_4d(vector, anchor)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        if dist < min_dist:
            min_dist = dist
            min_idx = i

    return (min_idx, min_dist)


# =============================================================================
# PHI-HARMONIC VERIFICATION
# =============================================================================

def phi_harmony_score(vector: np.ndarray) -> float:
    """
    Calculate how well a vector aligns with phi-harmonic patterns.

    Higher scores indicate stronger alignment with golden ratio proportions.

    Args:
        vector: Input vector to evaluate

    Returns:
        Harmony score [0.0, 1.0], where 1.0 = perfect phi-harmony
    """
    if len(vector) < 2:
        return 0.0

    # Check ratios between consecutive components
    ratios = []
    for i in range(len(vector) - 1):
        if vector[i] != 0:
            ratio = vector[i + 1] / vector[i]
            # How close is this ratio to phi or 1/phi?
            phi_dist = min(abs(ratio - PHI), abs(ratio - PHI_INVERSE))
            ratios.append(phi_dist)

    if not ratios:
        return 0.0

    # Average distance from phi-harmonic ratios
    mean_dist = np.mean(ratios)

    # Convert to score (lower distance = higher score)
    # Using exponential decay
    score = np.exp(-mean_dist * 2)

    return float(score)


def verify_anchor_point_harmony(anchor: np.ndarray = np.array([1.0, 1.0, 1.0, 1.0])) -> Dict[str, float]:
    """
    Verify that the Anchor Point exhibits phi-harmonic properties.

    Args:
        anchor: Anchor point vector (default: [1,1,1,1])

    Returns:
        Dictionary of harmony metrics
    """
    return {
        'phi_harmony_score': phi_harmony_score(anchor),
        'magnitude': np.linalg.norm(anchor),
        'unity_score': np.mean(anchor),  # How close to perfect unity (all 1.0)
        'variance': np.var(anchor),  # Should be 0 for perfect anchor
        'mean_value': np.mean(anchor),
    }
