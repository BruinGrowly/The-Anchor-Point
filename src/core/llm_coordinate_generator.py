"""
LLM-Based Semantic Coordinate Generator
========================================

Uses Large Language Models to assign semantic coordinates based on
actual understanding of concept meanings, not string hashing.

This approach captures genuine semantic content by leveraging the
deep linguistic and conceptual knowledge embedded in LLMs.
"""

import json
import re
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import time

from .semantic_coordinates import SemanticCoordinate


class LLMCoordinateGenerator:
    """
    Generate semantic coordinates using LLM semantic understanding.

    This generator uses a language model to evaluate concepts on each
    of the four dimensions based on their actual semantic content:
    - Love: Emotional valence & relational goodness
    - Power: Intensity, causal efficacy & sovereign impact
    - Wisdom: Abstractness, conceptual completeness & rational coherence
    - Justice: Holiness, moral purity & divine resonance
    """

    def __init__(self, model: str = "simulated", cache_path: Optional[str] = None):
        """
        Initialize the LLM coordinate generator.

        Args:
            model: Model to use ("simulated", "claude", "gpt4", etc.)
            cache_path: Optional path to cache LLM responses
        """
        self.model = model
        self.cache_path = Path(cache_path) if cache_path else None
        self.cache = self._load_cache() if self.cache_path else {}

    def _load_cache(self) -> Dict:
        """Load cached responses from disk."""
        if self.cache_path and self.cache_path.exists():
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to disk."""
        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.cache_path, 'w') as f:
                json.dump(self.cache, f, indent=2)

    def _create_prompt(self, concept: str) -> str:
        """
        Create a prompt for the LLM to rate a concept.

        Args:
            concept: The concept to rate

        Returns:
            Formatted prompt string
        """
        return f"""You are a semantic analyzer evaluating concepts in a 4-dimensional space.

Concept to evaluate: "{concept}"

Rate this concept on four dimensions using a scale from 0.0 to 1.0:

1. **Love** (Emotional Valence & Relational Goodness)
   - 0.0 = Maximum hatred, destruction, anti-relational
   - 0.5 = Neutral, neither loving nor hateful
   - 1.0 = Perfect selfless love (AGAPE), maximally life-giving, unifying

2. **Power** (Intensity, Causal Efficacy & Sovereign Impact)
   - 0.0 = Complete impotence, no causal effect
   - 0.5 = Moderate power, some influence
   - 1.0 = Omnipotent, absolute causal sovereignty, maximum creative/redemptive force

3. **Wisdom** (Abstractness, Conceptual Completeness & Rational Coherence)
   - 0.0 = Complete foolishness, incoherence, maximum error
   - 0.5 = Partial understanding, mixed truth and error
   - 1.0 = Perfect wisdom, the Logos, complete truth, total rational coherence

4. **Justice** (Holiness, Moral Purity & Divine Resonance)
   - 0.0 = Maximum corruption, absolute moral evil
   - 0.5 = Morally neutral or mixed
   - 1.0 = Perfect holiness, absolute righteousness, complete moral alignment with ultimate good

Consider:
- The inherent meaning and associations of the concept
- How it relates to ultimate reality and goodness
- Its moral, relational, and metaphysical character
- Universal human intuitions about its nature

Respond ONLY with a JSON object in this exact format:
{{"love": X.XX, "power": X.XX, "wisdom": X.XX, "justice": X.XX}}

No explanation, just the JSON."""

    def _parse_response(self, response: str) -> Optional[Tuple[float, float, float, float]]:
        """
        Parse LLM response to extract coordinates.

        Args:
            response: Raw LLM response

        Returns:
            Tuple of (love, power, wisdom, justice) or None if parsing failed
        """
        # Try to find JSON in response
        json_match = re.search(r'\{[^}]+\}', response)
        if not json_match:
            return None

        try:
            data = json.loads(json_match.group())
            love = float(data.get('love', 0))
            power = float(data.get('power', 0))
            wisdom = float(data.get('wisdom', 0))
            justice = float(data.get('justice', 0))

            # Validate range
            if not all(0.0 <= x <= 1.0 for x in [love, power, wisdom, justice]):
                return None

            return (love, power, wisdom, justice)
        except (json.JSONDecodeError, ValueError, KeyError):
            return None

    def _call_llm(self, prompt: str) -> str:
        """
        Call the LLM with the prompt.

        For now, this is simulated. In production, this would call
        an actual LLM API (Claude, GPT-4, etc.)

        Args:
            prompt: The prompt to send

        Returns:
            LLM response
        """
        if self.model == "simulated":
            return self._simulated_response(prompt)
        else:
            raise NotImplementedError(f"Model {self.model} not yet implemented")

    def _simulated_response(self, prompt: str) -> str:
        """
        Generate a simulated semantic response based on heuristics.

        This is a placeholder that generates plausible coordinates based on
        keyword matching. Replace with actual LLM calls for real testing.

        Args:
            prompt: The prompt (contains concept name)

        Returns:
            Simulated JSON response
        """
        # Extract concept from prompt
        concept_match = re.search(r'Concept to evaluate: "([^"]+)"', prompt)
        if not concept_match:
            return '{"love": 0.5, "power": 0.5, "wisdom": 0.5, "justice": 0.5}'

        concept = concept_match.group(1).lower()

        # Heuristic rules for common concepts
        # (In real implementation, this would be replaced by LLM understanding)

        # Divine concepts - should be near (1,1,1,1)
        if concept in ['jehovah', 'yahweh', 'god', 'agape', 'jesus', 'christ']:
            return '{"love": 1.0, "power": 1.0, "wisdom": 1.0, "justice": 1.0}'

        # Virtues - high on related dimensions
        virtue_map = {
            'love': (0.95, 0.5, 0.7, 0.8),
            'justice': (0.8, 0.7, 0.8, 0.95),
            'wisdom': (0.6, 0.4, 0.95, 0.7),
            'power': (0.5, 0.95, 0.6, 0.6),
            'mercy': (0.9, 0.6, 0.7, 0.85),
            'grace': (0.95, 0.7, 0.75, 0.9),
            'truth': (0.7, 0.8, 0.95, 0.9),
            'holy': (0.9, 0.9, 0.85, 0.95),
            'righteous': (0.85, 0.75, 0.8, 0.95),
            'compassion': (0.95, 0.6, 0.7, 0.8),
            'kindness': (0.9, 0.5, 0.6, 0.75),
            'hope': (0.85, 0.6, 0.7, 0.75),
            'faith': (0.8, 0.6, 0.75, 0.85),
        }

        if concept in virtue_map:
            l, p, w, j = virtue_map[concept]
            return f'{{"love": {l}, "power": {p}, "wisdom": {w}, "justice": {j}}}'

        # Vices - low on most dimensions
        vice_map = {
            'hatred': (0.05, 0.6, 0.2, 0.1),
            'evil': (0.1, 0.5, 0.2, 0.05),
            'cruelty': (0.05, 0.7, 0.3, 0.1),
            'deception': (0.2, 0.5, 0.15, 0.1),
            'injustice': (0.2, 0.5, 0.3, 0.1),
            'foolishness': (0.4, 0.3, 0.1, 0.3),
            'weakness': (0.4, 0.1, 0.4, 0.4),
            'chaos': (0.2, 0.6, 0.2, 0.2),
            'corruption': (0.15, 0.5, 0.3, 0.1),
        }

        if concept in vice_map:
            l, p, w, j = vice_map[concept]
            return f'{{"love": {l}, "power": {p}, "wisdom": {w}, "justice": {j}}}'

        # Neutral physical objects - moderate on all
        neutral_objects = ['table', 'chair', 'rock', 'tree', 'water', 'stone',
                          'cloud', 'mountain', 'river', 'building', 'wood', 'metal']
        if concept in neutral_objects:
            return '{"love": 0.5, "power": 0.4, "wisdom": 0.45, "justice": 0.5}'

        # Abstract concepts - high wisdom, moderate others
        abstract = ['consciousness', 'existence', 'being', 'reality', 'mind',
                   'thought', 'reason', 'meaning', 'purpose']
        if concept in abstract:
            return '{"love": 0.6, "power": 0.7, "wisdom": 0.85, "justice": 0.65}'

        # Default: moderate on all
        return '{"love": 0.5, "power": 0.5, "wisdom": 0.5, "justice": 0.5}'

    def generate(self, concept: str, use_cache: bool = True) -> SemanticCoordinate:
        """
        Generate semantic coordinates for a concept using LLM.

        Args:
            concept: The concept to evaluate
            use_cache: Whether to use cached responses

        Returns:
            SemanticCoordinate with LLM-assigned values
        """
        # Check cache
        cache_key = f"{self.model}:{concept.lower()}"
        if use_cache and cache_key in self.cache:
            coords = self.cache[cache_key]
            return SemanticCoordinate(
                concept=concept,
                love=coords['love'],
                power=coords['power'],
                wisdom=coords['wisdom'],
                justice=coords['justice'],
                source=f"llm_{self.model}_cached"
            )

        # Generate prompt
        prompt = self._create_prompt(concept)

        # Call LLM
        response = self._call_llm(prompt)

        # Parse response
        parsed = self._parse_response(response)

        if parsed is None:
            # Fallback to neutral coordinates if parsing failed
            print(f"Warning: Failed to parse response for '{concept}', using neutral coordinates")
            parsed = (0.5, 0.5, 0.5, 0.5)

        love, power, wisdom, justice = parsed

        # Cache result
        if use_cache:
            self.cache[cache_key] = {
                'love': love,
                'power': power,
                'wisdom': wisdom,
                'justice': justice
            }
            self._save_cache()

        return SemanticCoordinate(
            concept=concept,
            love=love,
            power=power,
            wisdom=wisdom,
            justice=justice,
            source=f"llm_{self.model}"
        )

    def generate_batch(self, concepts: List[str],
                      delay: float = 0.1,
                      use_cache: bool = True) -> List[SemanticCoordinate]:
        """
        Generate coordinates for multiple concepts.

        Args:
            concepts: List of concepts to evaluate
            delay: Delay between API calls (for rate limiting)
            use_cache: Whether to use cached responses

        Returns:
            List of SemanticCoordinates
        """
        results = []

        for i, concept in enumerate(concepts):
            if i > 0 and delay > 0:
                time.sleep(delay)

            coord = self.generate(concept, use_cache=use_cache)
            results.append(coord)

            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(concepts)} concepts...")

        print(f"Completed: {len(results)} concepts processed")
        return results


def compare_generators(concepts: List[str],
                      hash_gen,
                      llm_gen: LLMCoordinateGenerator) -> Dict:
    """
    Compare hash-based and LLM-based coordinate assignments.

    Args:
        concepts: List of concepts to compare
        hash_gen: Hash-based generator
        llm_gen: LLM-based generator

    Returns:
        Dictionary with comparison statistics
    """
    import numpy as np
    from scipy.stats import spearmanr

    # Generate with both methods
    hash_coords = [hash_gen.generate(c) for c in concepts]
    llm_coords = [llm_gen.generate(c) for c in concepts]

    # Extract distances
    hash_distances = [c.distance_to_anchor() for c in hash_coords]
    llm_distances = [c.distance_to_anchor() for c in llm_coords]

    # Calculate correlation
    correlation, p_value = spearmanr(hash_distances, llm_distances)

    return {
        'hash_mean': np.mean(hash_distances),
        'llm_mean': np.mean(llm_distances),
        'hash_std': np.std(hash_distances),
        'llm_std': np.std(llm_distances),
        'correlation': correlation,
        'p_value': p_value,
        'hash_coords': hash_coords,
        'llm_coords': llm_coords
    }
