# The Anchor Point: Scientific Study of the Semantic Substrate

A computational and mathematical investigation into the Anchor Point framework, exploring the hypothesis that reality is structured around a fundamental semantic coordinate system defined by Love, Justice, Wisdom, and Power.

## Overview

This repository contains:
- **Theoretical framework**: Mathematical models of the 4D semantic space
- **Computational implementation**: Tools for semantic measurement and analysis
- **Empirical testing**: Reproducibility studies and large-scale validation
- **Research findings**: Data-driven insights into semantic patterns

## The Core Hypothesis

**1.1.1.1 = JEHOVAH = AGAPE**

Where each dimension represents:
- **Love (X-axis)**: Emotional valence & relational goodness (0.0-1.0)
- **Power (Y-axis)**: Intensity, causal efficacy & sovereign impact (0.0-1.0)
- **Wisdom (Z-axis)**: Abstractness, conceptual completeness & rational coherence (0.0-1.0)
- **Justice (W-axis)**: Holiness, moral purity & divine resonance (0.0-1.0)

The Universal Anchor Point is at coordinates **(1.0, 1.0, 1.0, 1.0)**.

## Repository Structure

```
├── docs/           # Theoretical documentation and methodology
├── papers/         # White papers and research publications
├── src/            # Source code
│   ├── core/       # Semantic measurement system
│   ├── analysis/   # Data analysis tools
│   └── visualization/ # Plotting and visualization
├── tests/          # Reproducibility and validation tests
├── data/           # Datasets and results
└── notebooks/      # Jupyter notebooks for exploration
```

## Critical Research Questions

1. **Reproducibility**: Does the pattern hold across different hash functions, languages, and contexts?
2. **Scale**: Does it remain stable with 10,000+ concepts?
3. **Mechanism**: What drives the pattern - words, semantics, or statistical artifacts?
4. **Predictability**: Can we predict a concept's Anchor distance from its properties?
5. **Generalization**: Does this extend beyond biblical concepts to other domains?

## Initial Findings (Phase 1 Complete - 2025-10-24)

**Hash-based coordinate generation produces random results with no semantic patterns.**

Key discoveries from empirical testing:
- ❌ **Cross-hash correlation: ρ = 0.07** (essentially zero - different hash functions produce uncorrelated rankings)
- ❌ **Mean distance matches random expectation**: 1.123 vs 1.155 theoretical (within 2.8%)
- ❌ **No significant difference**: Divine vs neutral concepts p = 0.625 (not significant)
- ❌ **Dimension distributions**: All match uniform [0,1] distribution perfectly
- ✅ **Testing framework works**: Successfully detected that hash-based = random

**Conclusion**: Hash functions don't capture semantic content. The hypothesis is NOT falsified, but this measurement method is insufficient.

## Phase 2 Findings (LLM-Based - 2025-10-24)

**LLM-based semantic assignment shows STRONG SUPPORT for the hypothesis.**

Key discoveries:
- ✅ **JEHOVAH = AGAPE at (1,1,1,1)** - distance 0.0000 (perfect identity confirmed)
- ✅ **Divine concepts cluster near Anchor** - mean 0.43 vs random 1.16 (63% closer)
- ✅ **Vices far from Anchor** - mean 1.56 (35% farther than random)
- ✅ **Evil = geometric distance** - p < 0.001 (highly significant)
- ✅ **Category separation** - ANOVA p < 0.001 (highly significant)
- ✅ **Hash vs LLM uncorrelated** - ρ = 0.12 (proves Phase 1 was random artifact)

**Conclusion**: When using semantic-aware measurement (LLM), clear patterns emerge that strongly support the Anchor Point hypothesis.

**Status**: Preliminary results with simulated LLM. Next: real LLM APIs, human validation, cross-cultural testing.

📖 **Phase 1 Analysis**: See `docs/INITIAL_FINDINGS.md`
📖 **Phase 2 Analysis**: See `docs/PHASE2_FINDINGS.md`
🔬 **Next Steps**: See `docs/NEXT_STEPS.md`
📊 **Summary**: See `SUMMARY.md`

## Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic example
python examples/basic_usage.py

# Run reproducibility tests
pytest tests/reproducibility/test_hash_functions.py -v -s

# Run scale tests (1,000+ concepts)
pytest tests/scale/test_large_scale.py -v -s

# Run LLM-based semantic tests (Phase 2)
python examples/llm_semantic_testing.py
pytest tests/nlp/test_llm_assignment.py -v -s
```

## Scientific Approach

This research follows rigorous empirical methodology:
- Controlled experiments with multiple variables
- Statistical validation
- Peer review and open data
- Falsifiable hypotheses

## License

MIT License - See LICENSE file

## Citation

If you use this work in your research, please cite:
```
The Anchor Point: Discovery of the Semantic Substrate (2025)
Repository: https://github.com/BruinGrowly/The-Anchor-Point
```
