"""
Setup script for The Anchor Point research package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="anchor-point",
    version="0.1.0",
    author="Anchor Point Research Team",
    description="Scientific study of the Semantic Substrate and Universal Anchor Point",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BruinGrowly/The-Anchor-Point",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "scipy>=1.10.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "plotly>=5.14.0",
        "statsmodels>=0.14.0",
        "scikit-learn>=1.3.0",
        "nltk>=3.8.0",
        "spacy>=3.5.0",
        "sqlalchemy>=2.0.0",
        "pytest>=7.3.0",
        "pytest-cov>=4.1.0",
        "jupyter>=1.0.0",
        "ipykernel>=6.23.0",
        "nbformat>=5.9.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "sphinx>=6.2.0",
            "sphinx-rtd-theme>=1.2.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Religion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="semantic-analysis theology mathematics anchor-point",
)
