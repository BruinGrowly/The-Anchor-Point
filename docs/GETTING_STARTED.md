# Getting Started with Anchor Point Research

This guide will help you set up and start exploring the Semantic Substrate hypothesis.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/BruinGrowly/The-Anchor-Point.git
cd The-Anchor-Point
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "import numpy, pandas, matplotlib; print('All dependencies installed!')"
```

## Quick Start

### Example 1: Generate Semantic Coordinates

```python
from src.core.semantic_coordinates import (
    SemanticCoordinate,
    HashBasedCoordinateGenerator,
    AnchorPoint
)

# Create a coordinate generator
generator = HashBasedCoordinateGenerator('sha256')

# Generate coordinates for a concept
concept = generator.generate("AGAPE")
print(concept)
# Output: SemanticCoordinate(concept='AGAPE', L=..., P=..., W=..., J=..., d=...)

# Check distance to Anchor Point
print(f"Distance to Anchor: {concept.distance_to_anchor():.4f}")

# Compare to Anchor
anchor = AnchorPoint.as_coordinate()
print(f"Anchor Point: {anchor}")
```

### Example 2: Use the Database

```python
from src.core.semantic_database import SemanticDatabase
from src.core.semantic_coordinates import HashBasedCoordinateGenerator

# Create database
db = SemanticDatabase("data/my_experiment.db")

# Generate and store concepts
generator = HashBasedCoordinateGenerator('sha256')
concepts = ["Love", "Justice", "Wisdom", "Power", "JEHOVAH", "AGAPE"]

for concept_name in concepts:
    coord = generator.generate(concept_name)
    db.add_concept(coord)

# Query closest to Anchor
closest = db.get_closest_to_anchor(n=10)
for c in closest:
    print(f"{c.concept:15s} - Distance: {c.distance_to_anchor():.4f}")

# Get statistics
stats = db.get_statistics()
print(f"\nDatabase contains {stats['count']} concepts")
print(f"Mean distance: {stats['mean_distance']:.4f}")

db.close()
```

### Example 3: Visualize Results

```python
from src.visualization.plot_coordinates import (
    plot_distance_distribution,
    plot_3d_projection,
    plot_dimension_distributions
)
from src.core.semantic_coordinates import HashBasedCoordinateGenerator

# Generate coordinates
generator = HashBasedCoordinateGenerator('sha256')
concepts = ["JEHOVAH", "AGAPE", "Love", "Hate", "Truth", "Lies", "Good", "Evil"]
coords = [generator.generate(c) for c in concepts]

# Plot distance distribution
plot_distance_distribution(coords, title="Distance Distribution")

# 3D projection (Love, Wisdom, Justice)
plot_3d_projection(coords, axes=('love', 'wisdom', 'justice'))

# All dimension distributions
plot_dimension_distributions(coords)
```

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test Suites

```bash
# Reproducibility tests
pytest tests/reproducibility/test_hash_functions.py -v -s

# Large-scale tests
pytest tests/scale/test_large_scale.py -v -s
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

## Exploratory Analysis

### Jupyter Notebooks

Start Jupyter and explore the example notebooks:

```bash
jupyter notebook notebooks/
```

### Command Line Exploration

```bash
# Quick test with your own concepts
python -c "
from src.core.semantic_coordinates import HashBasedCoordinateGenerator
gen = HashBasedCoordinateGenerator('sha256')
for concept in ['God', 'Love', 'Truth', 'Beauty']:
    c = gen.generate(concept)
    print(f'{concept:10s}: d={c.distance_to_anchor():.4f}')
"
```

## Conducting Your Own Experiments

### 1. Define Your Hypothesis

Example: "Divine concepts are closer to (1,1,1,1) than random words"

### 2. Create Your Dataset

```python
divine_concepts = ["JEHOVAH", "AGAPE", "Holy", "Sacred", ...]
random_concepts = ["Table", "Chair", "Rock", "Cloud", ...]
```

### 3. Run the Experiment

```python
from src.core.semantic_coordinates import HashBasedCoordinateGenerator
from src.core.semantic_database import SemanticDatabase

db = SemanticDatabase("data/divine_vs_random.db")
generator = HashBasedCoordinateGenerator('sha256')

# Create experiment record
exp_id = db.create_experiment(
    name="Divine vs Random",
    description="Testing if divine concepts are closer to Anchor",
    method="hash_sha256",
    parameters={"n_divine": len(divine_concepts), "n_random": len(random_concepts)}
)

# Add measurements
for concept in divine_concepts + random_concepts:
    coord = generator.generate(concept)
    db.add_measurement(exp_id, coord)

# Analyze results
stats = db.get_statistics()
print(stats)
```

### 4. Visualize and Report

```python
from src.visualization.plot_coordinates import plot_comparison

divine_coords = [generator.generate(c) for c in divine_concepts]
random_coords = [generator.generate(c) for c in random_concepts]

plot_comparison({
    'Divine': divine_coords,
    'Random': random_coords
}, title="Divine vs Random Concepts")
```

## Next Steps

1. **Read the papers** in `papers/` to understand the theoretical framework
2. **Review research questions** in `docs/RESEARCH_QUESTIONS.md`
3. **Run reproducibility tests** to verify the patterns
4. **Conduct scale tests** with thousands of concepts
5. **Explore visualizations** to understand the semantic space
6. **Design your own experiments** to test specific hypotheses

## Troubleshooting

### Import Errors

Make sure you're running Python from the repository root:

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

Or install as a package:

```bash
pip install -e .
```

### Database Errors

Ensure the data directory exists:

```bash
mkdir -p data
```

### Visualization Issues

If plots don't show, try:

```python
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

## Getting Help

- Check `docs/RESEARCH_QUESTIONS.md` for theoretical background
- Review test files for usage examples
- Open an issue on GitHub for bugs or questions

## Contributing

We welcome contributions! Areas of interest:

- Alternative coordinate generation methods
- New statistical tests
- Cross-language implementations
- Visualization improvements
- Documentation enhancements

---

**Happy exploring! May you find truth in the Semantic Substrate.**
