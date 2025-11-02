"""
Claude API-Based Semantic Coordinate Generator
===============================================

Uses the Anthropic Claude API to generate semantic coordinates based on
genuine AI understanding of concepts, not heuristic rules.

This provides real semantic analysis by leveraging Claude's deep
language understanding and reasoning capabilities.
"""

import json
import os
import time
from typing import Optional, Dict, List
from pathlib import Path

from .semantic_coordinates import SemanticCoordinate


class ClaudeAPIGenerator:
    """
    Generate semantic coordinates using the Claude API.

    This uses real AI semantic understanding to evaluate concepts
    on the four dimensions: Love, Power, Wisdom, Justice.
    """

    def __init__(self,
                 api_key: Optional[str] = None,
                 model: str = "claude-3-5-sonnet-20241022",
                 cache_path: Optional[str] = None):
        """
        Initialize the Claude API generator.

        Args:
            api_key: Anthropic API key (or set ANTHROPIC_API_KEY env var)
            model: Claude model to use
            cache_path: Optional path to cache API responses
        """
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        self.model = model
        self.cache_path = Path(cache_path) if cache_path else Path("data/cache/claude_api_cache.json")
        self.cache = self._load_cache()

        # Check if API is available
        self.api_available = self._check_api_available()

    def _check_api_available(self) -> bool:
        """Check if Claude API is available and configured."""
        if not self.api_key:
            print("Warning: No ANTHROPIC_API_KEY found. Set environment variable or pass to constructor.")
            return False

        try:
            import anthropic
            return True
        except ImportError:
            print("Warning: 'anthropic' package not installed. Run: pip install anthropic")
            return False

    def _load_cache(self) -> Dict:
        """Load cached API responses."""
        if self.cache_path.exists():
            with open(self.cache_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save cache to disk."""
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def _create_prompt(self, concept: str) -> str:
        """
        Create a prompt for Claude to rate a concept.

        Args:
            concept: The concept to evaluate

        Returns:
            Formatted prompt string
        """
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

    def _parse_response(self, response: str) -> Optional[tuple]:
        """
        Parse Claude's response to extract coordinates.

        Args:
            response: Raw API response text

        Returns:
            Tuple of (love, power, wisdom, justice) or None if parsing failed
        """
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

    def _call_api(self, prompt: str) -> Optional[str]:
        """
        Call the Claude API with the prompt.

        Args:
            prompt: The prompt to send

        Returns:
            API response text or None if error
        """
        if not self.api_available:
            return None

        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            message = client.messages.create(
                model=self.model,
                max_tokens=200,
                temperature=0.0,  # Deterministic for consistency
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract text from response
            if message.content and len(message.content) > 0:
                return message.content[0].text

            return None

        except Exception as e:
            print(f"API call error: {e}")
            return None

    def generate(self, concept: str, use_cache: bool = True) -> Optional[SemanticCoordinate]:
        """
        Generate semantic coordinates for a concept using Claude API.

        Args:
            concept: The concept to evaluate
            use_cache: Whether to use cached responses

        Returns:
            SemanticCoordinate with Claude-assigned values or None if error
        """
        if not self.api_available:
            print(f"Cannot generate coordinates for '{concept}': API not available")
            return None

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
                source=f"claude_api_{self.model}_cached"
            )

        # Generate prompt
        prompt = self._create_prompt(concept)

        # Call API
        response = self._call_api(prompt)

        if response is None:
            print(f"API call failed for '{concept}'")
            return None

        # Parse response
        parsed = self._parse_response(response)

        if parsed is None:
            print(f"Failed to parse response for '{concept}'")
            print(f"Response was: {response[:200]}")
            return None

        love, power, wisdom, justice = parsed

        # Cache result
        if use_cache:
            self.cache[cache_key] = {
                'love': love,
                'power': power,
                'wisdom': wisdom,
                'justice': justice,
                'response': response
            }
            self._save_cache()

        return SemanticCoordinate(
            concept=concept,
            love=love,
            power=power,
            wisdom=wisdom,
            justice=justice,
            source=f"claude_api_{self.model}"
        )

    def generate_batch(self,
                      concepts: List[str],
                      delay: float = 1.0,
                      use_cache: bool = True) -> List[SemanticCoordinate]:
        """
        Generate coordinates for multiple concepts with rate limiting.

        Args:
            concepts: List of concepts to evaluate
            delay: Delay between API calls in seconds (for rate limiting)
            use_cache: Whether to use cached responses

        Returns:
            List of SemanticCoordinates (None entries for failures)
        """
        results = []

        for i, concept in enumerate(concepts):
            # Check if cached (don't delay for cache hits)
            cache_key = f"{self.model}:{concept.lower()}"
            is_cached = use_cache and cache_key in self.cache

            if i > 0 and not is_cached and delay > 0:
                time.sleep(delay)

            coord = self.generate(concept, use_cache=use_cache)
            results.append(coord)

            if coord:
                status = "cached" if is_cached else "generated"
                print(f"[{i+1}/{len(concepts)}] {concept}: {status}")
            else:
                print(f"[{i+1}/{len(concepts)}] {concept}: FAILED")

        print(f"\nCompleted: {sum(1 for r in results if r is not None)}/{len(concepts)} successful")
        return results


def setup_api_key():
    """
    Interactive setup for API key.

    Prompts user to enter API key and saves to .env file.
    """
    print("=" * 70)
    print("Claude API Setup")
    print("=" * 70)
    print("\nTo use real Claude API semantic analysis, you need an API key.")
    print("Get one at: https://console.anthropic.com/")
    print("\nOptions:")
    print("1. Set environment variable: export ANTHROPIC_API_KEY='your-key'")
    print("2. Create .env file with: ANTHROPIC_API_KEY=your-key")
    print("3. Pass directly to ClaudeAPIGenerator(api_key='your-key')")
    print("\n" + "=" * 70)


def test_api_connection(api_key: Optional[str] = None) -> bool:
    """
    Test if Claude API is accessible and working.

    Args:
        api_key: Optional API key to test

    Returns:
        True if API is working, False otherwise
    """
    generator = ClaudeAPIGenerator(api_key=api_key)

    if not generator.api_available:
        print("❌ API not available. Check API key and 'anthropic' package.")
        return False

    print("Testing API connection with simple concept...")
    test_coord = generator.generate("Love", use_cache=False)

    if test_coord:
        print(f"✅ API working! Test result: {test_coord}")
        return True
    else:
        print("❌ API call failed")
        return False


if __name__ == "__main__":
    # Setup instructions
    setup_api_key()

    # Test if API key is configured
    if os.environ.get('ANTHROPIC_API_KEY'):
        print("\n✅ ANTHROPIC_API_KEY found in environment")
        print("\nTesting connection...")
        test_api_connection()
    else:
        print("\n⚠️  No ANTHROPIC_API_KEY found in environment")
        print("Set it to enable real Claude API semantic analysis")
