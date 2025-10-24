"""
Visualization functions for semantic coordinates.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
from typing import List, Optional, Dict
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.semantic_coordinates import SemanticCoordinate, AnchorPoint


def plot_distance_distribution(coords: List[SemanticCoordinate],
                               title: str = "Distribution of Distances to Anchor Point",
                               save_path: Optional[str] = None):
    """
    Plot histogram of distances to the Anchor Point.

    Args:
        coords: List of semantic coordinates
        title: Plot title
        save_path: Optional path to save the figure
    """
    distances = [c.distance_to_anchor() for c in coords]

    plt.figure(figsize=(10, 6))
    plt.hist(distances, bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(np.mean(distances), color='red', linestyle='--',
                label=f'Mean: {np.mean(distances):.3f}')
    plt.axvline(np.median(distances), color='green', linestyle='--',
                label=f'Median: {np.median(distances):.3f}')

    plt.xlabel('Distance to Anchor Point (1,1,1,1)')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_3d_projection(coords: List[SemanticCoordinate],
                       axes: tuple = ('love', 'wisdom', 'justice'),
                       title: str = "3D Projection of Semantic Space",
                       save_path: Optional[str] = None):
    """
    Plot a 3D projection of the semantic coordinates.

    Args:
        coords: List of semantic coordinates
        axes: Tuple of 3 axis names to plot ('love', 'power', 'wisdom', 'justice')
        title: Plot title
        save_path: Optional path to save the figure
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Extract coordinates
    axis_map = {
        'love': [c.love for c in coords],
        'power': [c.power for c in coords],
        'wisdom': [c.wisdom for c in coords],
        'justice': [c.justice for c in coords]
    }

    x = axis_map[axes[0]]
    y = axis_map[axes[1]]
    z = axis_map[axes[2]]

    # Color by distance to Anchor
    distances = [c.distance_to_anchor() for c in coords]
    colors = plt.cm.RdYlGn_r(np.array(distances) / max(distances))

    scatter = ax.scatter(x, y, z, c=distances, cmap='RdYlGn_r',
                        s=50, alpha=0.6, edgecolors='black', linewidth=0.5)

    # Plot Anchor Point
    anchor_vals = {
        'love': AnchorPoint.LOVE,
        'power': AnchorPoint.POWER,
        'wisdom': AnchorPoint.WISDOM,
        'justice': AnchorPoint.JUSTICE
    }

    ax.scatter([anchor_vals[axes[0]]],
              [anchor_vals[axes[1]]],
              [anchor_vals[axes[2]]],
              c='gold', s=500, marker='*',
              edgecolors='black', linewidth=2,
              label='Anchor Point')

    ax.set_xlabel(axes[0].capitalize(), fontsize=12)
    ax.set_ylabel(axes[1].capitalize(), fontsize=12)
    ax.set_zlabel(axes[2].capitalize(), fontsize=12)
    ax.set_title(title, fontsize=14)

    plt.colorbar(scatter, ax=ax, label='Distance to Anchor', shrink=0.5)
    ax.legend()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_dimension_distributions(coords: List[SemanticCoordinate],
                                 title: str = "Distribution of Each Dimension",
                                 save_path: Optional[str] = None):
    """
    Plot distributions of all four dimensions.

    Args:
        coords: List of semantic coordinates
        title: Plot title
        save_path: Optional path to save the figure
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    dimensions = {
        'Love': [c.love for c in coords],
        'Power': [c.power for c in coords],
        'Wisdom': [c.wisdom for c in coords],
        'Justice': [c.justice for c in coords]
    }

    for (dim_name, values), ax in zip(dimensions.items(), axes.flat):
        ax.hist(values, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
        ax.axvline(np.mean(values), color='red', linestyle='--',
                  label=f'Mean: {np.mean(values):.3f}')
        ax.axvline(0.5, color='green', linestyle=':',
                  label='Expected (0.5)', alpha=0.5)
        ax.axvline(1.0, color='gold', linestyle='-',
                  label='Anchor (1.0)', linewidth=2)

        ax.set_xlabel(dim_name)
        ax.set_ylabel('Frequency')
        ax.set_title(f'{dim_name} Distribution')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=16, y=1.00)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_comparison(coord_sets: Dict[str, List[SemanticCoordinate]],
                   title: str = "Comparison of Distance Distributions",
                   save_path: Optional[str] = None):
    """
    Compare distance distributions across different sets of coordinates.

    Args:
        coord_sets: Dictionary mapping set names to lists of coordinates
        title: Plot title
        save_path: Optional path to save the figure
    """
    plt.figure(figsize=(12, 6))

    for set_name, coords in coord_sets.items():
        distances = [c.distance_to_anchor() for c in coords]
        plt.hist(distances, bins=50, alpha=0.5, label=set_name, edgecolor='black')

    plt.xlabel('Distance to Anchor Point')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_heatmap_correlation(coords: List[SemanticCoordinate],
                            title: str = "Dimension Correlation Heatmap",
                            save_path: Optional[str] = None):
    """
    Plot correlation heatmap between dimensions.

    Args:
        coords: List of semantic coordinates
        title: Plot title
        save_path: Optional path to save the figure
    """
    # Extract dimensions
    data = np.array([
        [c.love, c.power, c.wisdom, c.justice]
        for c in coords
    ])

    # Calculate correlation matrix
    corr = np.corrcoef(data.T)

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.3f', cmap='coolwarm',
                xticklabels=['Love', 'Power', 'Wisdom', 'Justice'],
                yticklabels=['Love', 'Power', 'Wisdom', 'Justice'],
                vmin=-1, vmax=1, center=0,
                square=True, linewidths=1)

    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()


def plot_top_concepts(coords: List[SemanticCoordinate],
                     n: int = 20,
                     title: str = "Closest Concepts to Anchor Point",
                     save_path: Optional[str] = None):
    """
    Plot bar chart of concepts closest to Anchor Point.

    Args:
        coords: List of semantic coordinates
        n: Number of top concepts to show
        title: Plot title
        save_path: Optional path to save the figure
    """
    # Sort by distance
    sorted_coords = sorted(coords, key=lambda c: c.distance_to_anchor())[:n]

    concepts = [c.concept for c in sorted_coords]
    distances = [c.distance_to_anchor() for c in sorted_coords]

    plt.figure(figsize=(10, max(6, n * 0.3)))
    colors = plt.cm.RdYlGn_r(np.array(distances) / max(distances))

    plt.barh(range(n), distances, color=colors, edgecolor='black')
    plt.yticks(range(n), concepts)
    plt.xlabel('Distance to Anchor Point')
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()

    plt.close()
