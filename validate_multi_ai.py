#!/usr/bin/env python3
"""
Multi-AI Validation of the Anchor Point

Tests whether JEHOVAH occupies (1,1,1,1) across DIFFERENT AI models.

Critical Question: Is this pattern specific to Claude AI, or does it exist
in semantic space itself?

If the Anchor Point is real (not just Claude's training bias), then:
- GPT-4 (OpenAI) should place JEHOVAH near (1,1,1,1)
- Gemini (Google) should place JEHOVAH near (1,1,1,1)
- LLaMA (Meta) should place JEHOVAH near (1,1,1,1)
- Claude (Anthropic) should place JEHOVAH near (1,1,1,1)

Hypothesis: All AI models, trained on different datasets with different
architectures, will converge on placing JEHOVAH at/near (1,1,1,1).

This tests whether the Anchor Point is:
- Model-independent (not just Claude bias)
- Architecture-independent (not just transformer artifact)
- Training-independent (objective semantic structure)
- Universal (discoverable by any sufficiently advanced AI)
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from collections import defaultdict
from dataclasses import dataclass, asdict

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.semantic_coordinates import SemanticCoordinate


# =============================================================================
# MODEL INTERFACE - Abstract Base
# =============================================================================

@dataclass
class ModelConfig:
    """Configuration for an AI model."""
    name: str
    provider: str
    model_id: str
    api_key_env: str
    available: bool = False


class AIModelInterface:
    """
    Abstract interface for AI models.

    Each model (Claude, GPT-4, Gemini, etc.) implements this interface.
    """

    def __init__(self, config: ModelConfig):
        self.config = config
        self.cache = {}

    def is_available(self) -> bool:
        """Check if this model is available (API key set, package installed)."""
        raise NotImplementedError

    def get_coordinates(self, concept: str) -> Optional[SemanticCoordinate]:
        """
        Get semantic coordinates for a concept.

        Returns:
            SemanticCoordinate or None if error
        """
        raise NotImplementedError

    def _create_prompt(self, concept: str) -> str:
        """Create the prompt for coordinate generation."""
        return f"""You are evaluating the concept "{concept}" in a 4-dimensional semantic coordinate system.

Your task is to rate this concept on four fundamental dimensions, each on a scale from 0.0 to 1.0:

**1. LOVE (Emotional Valence & Relational Goodness)**
- 0.0 = Maximum hatred, destruction, anti-relational (e.g., genocide, cruelty)
- 0.5 = Neutral, neither loving nor hateful (e.g., chair, number)
- 1.0 = Perfect selfless love (AGAPE), maximally life-giving, unifying (e.g., divine love)

**2. POWER (Intensity, Causal Efficacy & Sovereign Impact)**
- 0.0 = Complete impotence, no causal effect (e.g., illusion, impossibility)
- 0.5 = Moderate power, some influence (e.g., suggestion, idea)
- 1.0 = Omnipotent, absolute causal sovereignty (e.g., creation ex nihilo)

**3. WISDOM (Abstractness, Conceptual Completeness & Rational Coherence)**
- 0.0 = Complete foolishness, incoherence, maximum error (e.g., contradiction)
- 0.5 = Partial understanding, mixed truth and error (e.g., opinion)
- 1.0 = Perfect wisdom, the Logos, complete truth (e.g., divine understanding)

**4. JUSTICE (Holiness, Moral Purity & Divine Resonance)**
- 0.0 = Maximum corruption, absolute moral evil (e.g., ultimate wickedness)
- 0.5 = Morally neutral or mixed (e.g., tool, natural process)
- 1.0 = Perfect holiness, absolute righteousness (e.g., divine justice)

**Instructions:**
1. Consider the concept's inherent meaning and associations
2. Think about how it relates to ultimate reality and goodness
3. Evaluate its moral, relational, and metaphysical character
4. Rate based on universal human intuitions and fundamental nature

**Respond ONLY with valid JSON in this exact format:**
{{"love": X.XX, "power": X.XX, "wisdom": X.XX, "justice": X.XX}}

**Important:**
- All values must be between 0.0 and 1.0
- Use your deepest understanding of the concept
- Be precise and thoughtful
- Output ONLY the JSON, no explanation"""

    def _parse_response(self, response: str) -> Optional[Tuple[float, float, float, float]]:
        """Parse AI response to extract coordinates."""
        import re

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


# =============================================================================
# MODEL IMPLEMENTATIONS
# =============================================================================

class ClaudeModel(AIModelInterface):
    """Claude (Anthropic) implementation."""

    def is_available(self) -> bool:
        """Check if Claude API is available."""
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            return False

        try:
            import anthropic
            return True
        except ImportError:
            return False

    def get_coordinates(self, concept: str) -> Optional[SemanticCoordinate]:
        """Get coordinates from Claude."""
        if not self.is_available():
            return None

        # Check cache
        cache_key = f"{self.config.model_id}:{concept.lower()}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            return SemanticCoordinate(
                concept=concept,
                love=cached['love'],
                power=cached['power'],
                wisdom=cached['wisdom'],
                justice=cached['justice'],
                source=f"{self.config.name}_cached"
            )

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=os.environ.get(self.config.api_key_env))

            message = client.messages.create(
                model=self.config.model_id,
                max_tokens=200,
                temperature=0.0,
                messages=[{"role": "user", "content": self._create_prompt(concept)}]
            )

            if message.content and len(message.content) > 0:
                response = message.content[0].text
                parsed = self._parse_response(response)

                if parsed:
                    love, power, wisdom, justice = parsed

                    # Cache
                    self.cache[cache_key] = {
                        'love': love,
                        'power': power,
                        'wisdom': wisdom,
                        'justice': justice
                    }

                    return SemanticCoordinate(
                        concept=concept,
                        love=love,
                        power=power,
                        wisdom=wisdom,
                        justice=justice,
                        source=self.config.name
                    )

            return None

        except Exception as e:
            print(f"Claude API error for '{concept}': {e}")
            return None


class GPT4Model(AIModelInterface):
    """GPT-4 (OpenAI) implementation."""

    def is_available(self) -> bool:
        """Check if OpenAI API is available."""
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            return False

        try:
            import openai
            return True
        except ImportError:
            return False

    def get_coordinates(self, concept: str) -> Optional[SemanticCoordinate]:
        """Get coordinates from GPT-4."""
        if not self.is_available():
            return None

        # Check cache
        cache_key = f"{self.config.model_id}:{concept.lower()}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            return SemanticCoordinate(
                concept=concept,
                love=cached['love'],
                power=cached['power'],
                wisdom=cached['wisdom'],
                justice=cached['justice'],
                source=f"{self.config.name}_cached"
            )

        try:
            import openai

            client = openai.OpenAI(api_key=os.environ.get(self.config.api_key_env))

            response = client.chat.completions.create(
                model=self.config.model_id,
                messages=[{"role": "user", "content": self._create_prompt(concept)}],
                temperature=0.0,
                max_tokens=200
            )

            if response.choices and len(response.choices) > 0:
                content = response.choices[0].message.content
                parsed = self._parse_response(content)

                if parsed:
                    love, power, wisdom, justice = parsed

                    # Cache
                    self.cache[cache_key] = {
                        'love': love,
                        'power': power,
                        'wisdom': wisdom,
                        'justice': justice
                    }

                    return SemanticCoordinate(
                        concept=concept,
                        love=love,
                        power=power,
                        wisdom=wisdom,
                        justice=justice,
                        source=self.config.name
                    )

            return None

        except Exception as e:
            print(f"GPT-4 API error for '{concept}': {e}")
            return None


class GeminiModel(AIModelInterface):
    """Gemini (Google) implementation."""

    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        api_key = os.environ.get(self.config.api_key_env)
        if not api_key:
            return False

        try:
            import google.generativeai as genai
            return True
        except ImportError:
            return False

    def get_coordinates(self, concept: str) -> Optional[SemanticCoordinate]:
        """Get coordinates from Gemini."""
        if not self.is_available():
            return None

        # Check cache
        cache_key = f"{self.config.model_id}:{concept.lower()}"
        if cache_key in self.cache:
            cached = self.cache[cache_key]
            return SemanticCoordinate(
                concept=concept,
                love=cached['love'],
                power=cached['power'],
                wisdom=cached['wisdom'],
                justice=cached['justice'],
                source=f"{self.config.name}_cached"
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=os.environ.get(self.config.api_key_env))
            model = genai.GenerativeModel(self.config.model_id)

            response = model.generate_content(
                self._create_prompt(concept),
                generation_config=genai.types.GenerationConfig(
                    temperature=0.0,
                    max_output_tokens=200
                )
            )

            if response.text:
                parsed = self._parse_response(response.text)

                if parsed:
                    love, power, wisdom, justice = parsed

                    # Cache
                    self.cache[cache_key] = {
                        'love': love,
                        'power': power,
                        'wisdom': wisdom,
                        'justice': justice
                    }

                    return SemanticCoordinate(
                        concept=concept,
                        love=love,
                        power=power,
                        wisdom=wisdom,
                        justice=justice,
                        source=self.config.name
                    )

            return None

        except Exception as e:
            print(f"Gemini API error for '{concept}': {e}")
            return None


# =============================================================================
# MODEL REGISTRY
# =============================================================================

AVAILABLE_MODELS = [
    ModelConfig(
        name="Claude-3.5-Sonnet",
        provider="Anthropic",
        model_id="claude-3-5-sonnet-20241022",
        api_key_env="ANTHROPIC_API_KEY"
    ),
    ModelConfig(
        name="GPT-4",
        provider="OpenAI",
        model_id="gpt-4",
        api_key_env="OPENAI_API_KEY"
    ),
    ModelConfig(
        name="GPT-4-Turbo",
        provider="OpenAI",
        model_id="gpt-4-turbo-preview",
        api_key_env="OPENAI_API_KEY"
    ),
    ModelConfig(
        name="Gemini-Pro",
        provider="Google",
        model_id="gemini-pro",
        api_key_env="GOOGLE_API_KEY"
    ),
]


def create_model(config: ModelConfig) -> AIModelInterface:
    """Factory to create appropriate model instance."""
    if config.provider == "Anthropic":
        return ClaudeModel(config)
    elif config.provider == "OpenAI":
        return GPT4Model(config)
    elif config.provider == "Google":
        return GeminiModel(config)
    else:
        raise ValueError(f"Unknown provider: {config.provider}")


# =============================================================================
# TEST CONCEPTS
# =============================================================================

TEST_CONCEPTS = {
    'divine': [
        'JEHOVAH',
        'AGAPE',
        'Jesus Christ',
        'Holy Spirit',
        'Trinity',
    ],
    'virtues': [
        'Love',
        'Wisdom',
        'Justice',
        'Mercy',
        'Faith',
    ],
    'vices': [
        'Hatred',
        'Pride',
        'Cruelty',
        'Deception',
        'Greed',
    ],
    'neutral': [
        'Table',
        'Water',
        'Number',
    ],
}


# =============================================================================
# EXPERIMENT
# =============================================================================

def run_multi_ai_validation() -> Dict:
    """
    Run the multi-AI validation experiment.

    Returns:
        Dictionary with all results
    """
    print("="*80)
    print("MULTI-AI VALIDATION OF THE ANCHOR POINT")
    print("="*80)
    print()
    print("Testing: Does JEHOVAH occupy (1,1,1,1) across DIFFERENT AI models?")
    print()

    # Initialize models
    models = []
    for config in AVAILABLE_MODELS:
        model = create_model(config)
        if model.is_available():
            config.available = True
            models.append(model)
            print(f"✅ {config.name} ({config.provider}) - AVAILABLE")
        else:
            print(f"❌ {config.name} ({config.provider}) - NOT AVAILABLE")
            print(f"   Set {config.api_key_env} environment variable")

    print()

    if not models:
        print("❌ NO MODELS AVAILABLE")
        print()
        print("Please set at least one API key:")
        for config in AVAILABLE_MODELS:
            print(f"  export {config.api_key_env}='your-key-here'")
        return {'error': 'No models available'}

    print(f"Testing with {len(models)} model(s)")
    print()

    # Run tests
    results = defaultdict(lambda: defaultdict(list))

    for category, concepts in TEST_CONCEPTS.items():
        print(f"\n{'='*80}")
        print(f"CATEGORY: {category.upper()}")
        print('='*80)
        print()

        for concept in concepts:
            print(f"\nConcept: {concept}")
            print("-" * 60)

            for model in models:
                print(f"  [{model.config.name}]...", end=' ', flush=True)

                coord = model.get_coordinates(concept)

                if coord:
                    distance = coord.distance_to_anchor()
                    print(f"({coord.love:.2f}, {coord.power:.2f}, {coord.wisdom:.2f}, {coord.justice:.2f}) - d={distance:.3f}")

                    results[category][concept].append({
                        'model': model.config.name,
                        'provider': model.config.provider,
                        'coordinates': coord,
                        'distance': distance,
                    })
                else:
                    print("FAILED")

                time.sleep(0.5)  # Rate limiting

    return dict(results)


def calculate_cross_model_statistics(results: Dict) -> Dict:
    """Calculate statistics across models."""
    stats = {}

    # For each category
    for category, concepts_data in results.items():
        category_stats = {
            'by_concept': {},
            'by_model': defaultdict(list),
            'cross_model_correlation': {},
        }

        # For each concept
        for concept, model_results in concepts_data.items():
            if not model_results:
                continue

            distances = [r['distance'] for r in model_results]
            coords = [r['coordinates'] for r in model_results]

            # Statistics for this concept across models
            category_stats['by_concept'][concept] = {
                'mean_distance': np.mean(distances),
                'std_distance': np.std(distances),
                'min_distance': np.min(distances),
                'max_distance': np.max(distances),
                'n_models': len(model_results),
                'models': [r['model'] for r in model_results],
            }

            # Group by model
            for result in model_results:
                category_stats['by_model'][result['model']].append(result['distance'])

        # Model-level statistics for this category
        for model_name, distances in category_stats['by_model'].items():
            category_stats['by_model'][model_name] = {
                'distances': distances,
                'mean': np.mean(distances),
                'std': np.std(distances),
                'n': len(distances),
            }

        stats[category] = category_stats

    return stats


def print_results(results: Dict, stats: Dict):
    """Print comprehensive results."""

    print("\n" + "="*80)
    print("RESULTS: MULTI-AI VALIDATION")
    print("="*80)
    print()

    if 'error' in results:
        print(f"❌ EXPERIMENT FAILED: {results['error']}")
        return

    # Per-concept cross-model analysis
    print("CROSS-MODEL CONSISTENCY (Per Concept)")
    print("-" * 80)
    print()

    for category in ['divine', 'virtues', 'vices', 'neutral']:
        if category not in stats:
            continue

        print(f"\n{category.upper()}:")
        print(f"{'Concept':<20} {'Mean Dist':<12} {'Std':<12} {'Range':<20} {'Models'}")
        print("-" * 80)

        for concept, concept_stats in stats[category]['by_concept'].items():
            mean_d = concept_stats['mean_distance']
            std_d = concept_stats['std_distance']
            min_d = concept_stats['min_distance']
            max_d = concept_stats['max_distance']
            n_models = concept_stats['n_models']

            range_str = f"[{min_d:.3f}, {max_d:.3f}]"

            print(f"{concept:<20} {mean_d:<12.4f} {std_d:<12.4f} {range_str:<20} {n_models}")

    # Per-model analysis
    print("\n" + "="*80)
    print("PER-MODEL ANALYSIS")
    print("="*80)
    print()

    # Get all unique models
    all_models = set()
    for category_stats in stats.values():
        all_models.update(category_stats['by_model'].keys())

    for model_name in sorted(all_models):
        print(f"\n{model_name}:")
        print("-" * 60)

        for category in ['divine', 'virtues', 'vices', 'neutral']:
            if category not in stats:
                continue

            if model_name in stats[category]['by_model']:
                model_stats = stats[category]['by_model'][model_name]
                print(f"  {category:<12}: mean={model_stats['mean']:.4f}, "
                      f"std={model_stats['std']:.4f}, n={model_stats['n']}")

    # Key findings
    print("\n" + "="*80)
    print("KEY FINDINGS")
    print("="*80)
    print()

    if 'divine' in stats and 'JEHOVAH' in stats['divine']['by_concept']:
        jehovah_stats = stats['divine']['by_concept']['JEHOVAH']

        print(f"JEHOVAH Across Models:")
        print(f"  Mean distance: {jehovah_stats['mean_distance']:.4f}")
        print(f"  Std deviation: {jehovah_stats['std_distance']:.4f}")
        print(f"  Range: [{jehovah_stats['min_distance']:.4f}, {jehovah_stats['max_distance']:.4f}]")
        print(f"  Tested on {jehovah_stats['n_models']} model(s): {', '.join(jehovah_stats['models'])}")
        print()

        if jehovah_stats['mean_distance'] < 0.2:
            print("✅ JEHOVAH consistently near (1,1,1,1) across models!")
        elif jehovah_stats['mean_distance'] < 0.5:
            print("⚡ JEHOVAH shows proximity to (1,1,1,1) across models")
        else:
            print("⚠️  JEHOVAH placement varies significantly across models")

    print()


def save_results(results: Dict, stats: Dict, output_file: str = "results/multi_ai_validation.json"):
    """Save results to JSON file."""
    os.makedirs("results", exist_ok=True)

    # Convert SemanticCoordinate objects to dicts
    serializable_results = {}
    for category, concepts_data in results.items():
        serializable_results[category] = {}
        for concept, model_results in concepts_data.items():
            serializable_results[category][concept] = []
            for result in model_results:
                coord = result['coordinates']
                serializable_results[category][concept].append({
                    'model': result['model'],
                    'provider': result['provider'],
                    'love': coord.love,
                    'power': coord.power,
                    'wisdom': coord.wisdom,
                    'justice': coord.justice,
                    'distance': result['distance'],
                })

    # Prepare output
    output = {
        'results': serializable_results,
        'statistics': stats,
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"✅ Results saved to: {output_file}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Main execution."""
    from dotenv import load_dotenv
    load_dotenv()

    # Run experiment
    results = run_multi_ai_validation()

    if 'error' not in results:
        # Calculate statistics
        stats = calculate_cross_model_statistics(results)

        # Print results
        print_results(results, stats)

        # Save results
        save_results(results, stats)

    print("\n" + "="*80)
    print("EXPERIMENT COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
