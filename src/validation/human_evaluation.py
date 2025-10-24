"""
Human Evaluation Protocol
==========================

Tools and templates for conducting human evaluation studies
to validate semantic coordinate assignments.
"""

import json
from typing import List, Dict, Optional
from pathlib import Path
import csv


class HumanEvaluationProtocol:
    """
    Manage human evaluation studies for semantic coordinates.
    """

    def __init__(self, study_name: str, output_dir: str = "data/human_eval"):
        """
        Initialize evaluation protocol.

        Args:
            study_name: Name of this evaluation study
            output_dir: Directory to store evaluation data
        """
        self.study_name = study_name
        self.output_dir = Path(output_dir) / study_name
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_evaluation_sheet(self,
                                  concepts: List[str],
                                  output_format: str = 'csv') -> str:
        """
        Generate evaluation sheet for human evaluators.

        Args:
            concepts: List of concepts to evaluate
            output_format: 'csv' or 'json'

        Returns:
            Path to generated file
        """
        if output_format == 'csv':
            return self._generate_csv(concepts)
        elif output_format == 'json':
            return self._generate_json(concepts)
        else:
            raise ValueError(f"Unknown format: {output_format}")

    def _generate_csv(self, concepts: List[str]) -> str:
        """Generate CSV evaluation sheet."""
        output_path = self.output_dir / "evaluation_sheet.csv"

        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                'Evaluator_ID',
                'Concept',
                'Love_0_10',
                'Power_0_10',
                'Wisdom_0_10',
                'Justice_0_10',
                'Confidence_0_10',
                'Notes'
            ])

            # Template rows
            for concept in concepts:
                writer.writerow([
                    'EVALUATOR_001',  # To be filled
                    concept,
                    '',  # Love rating
                    '',  # Power rating
                    '',  # Wisdom rating
                    '',  # Justice rating
                    '',  # Confidence
                    ''   # Notes
                ])

        return str(output_path)

    def _generate_json(self, concepts: List[str]) -> str:
        """Generate JSON evaluation template."""
        output_path = self.output_dir / "evaluation_template.json"

        template = {
            'study_name': self.study_name,
            'evaluator_id': 'EVALUATOR_001',
            'instructions': self._get_instructions(),
            'concepts': [
                {
                    'concept': concept,
                    'love': None,
                    'power': None,
                    'wisdom': None,
                    'justice': None,
                    'confidence': None,
                    'notes': ''
                }
                for concept in concepts
            ]
        }

        with open(output_path, 'w') as f:
            json.dump(template, f, indent=2)

        return str(output_path)

    def _get_instructions(self) -> Dict:
        """Get evaluation instructions."""
        return {
            'overview': 'Rate each concept on four dimensions using a scale from 0 to 10',
            'dimensions': {
                'love': {
                    'name': 'LOVE (Emotional Valence & Relational Goodness)',
                    'scale': {
                        0: 'Maximum hatred, destruction, anti-relational',
                        5: 'Neutral, neither loving nor hateful',
                        10: 'Perfect selfless love (AGAPE), maximally life-giving'
                    }
                },
                'power': {
                    'name': 'POWER (Intensity, Causal Efficacy & Sovereign Impact)',
                    'scale': {
                        0: 'Complete impotence, no causal effect',
                        5: 'Moderate power, some influence',
                        10: 'Omnipotent, absolute causal sovereignty'
                    }
                },
                'wisdom': {
                    'name': 'WISDOM (Abstractness, Conceptual Completeness & Rational Coherence)',
                    'scale': {
                        0: 'Complete foolishness, incoherence, maximum error',
                        5: 'Partial understanding, mixed truth and error',
                        10: 'Perfect wisdom, the Logos, complete truth'
                    }
                },
                'justice': {
                    'name': 'JUSTICE (Holiness, Moral Purity & Divine Resonance)',
                    'scale': {
                        0: 'Maximum corruption, absolute moral evil',
                        5: 'Morally neutral or mixed',
                        10: 'Perfect holiness, absolute righteousness'
                    }
                }
            },
            'confidence': 'Rate your confidence in your evaluation (0=guessing, 10=certain)',
            'tips': [
                'Consider the inherent meaning and associations of the concept',
                'Think about how it relates to ultimate reality and goodness',
                'Evaluate its moral, relational, and metaphysical character',
                'Be honest and thoughtful - there are no wrong answers',
                'Use the full scale (0-10) - avoid clustering around 5'
            ]
        }

    def load_evaluations(self, file_path: str) -> List[Dict]:
        """
        Load completed evaluations from file.

        Args:
            file_path: Path to evaluation file (CSV or JSON)

        Returns:
            List of evaluation dictionaries
        """
        file_path = Path(file_path)

        if file_path.suffix == '.csv':
            return self._load_csv(file_path)
        elif file_path.suffix == '.json':
            return self._load_json(file_path)
        else:
            raise ValueError(f"Unknown file type: {file_path.suffix}")

    def _load_csv(self, file_path: Path) -> List[Dict]:
        """Load evaluations from CSV."""
        evaluations = []

        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Love_0_10']:  # Skip empty rows
                    evaluations.append({
                        'evaluator_id': row['Evaluator_ID'],
                        'concept': row['Concept'],
                        'love': float(row['Love_0_10']) / 10.0,  # Normalize to [0,1]
                        'power': float(row['Power_0_10']) / 10.0,
                        'wisdom': float(row['Wisdom_0_10']) / 10.0,
                        'justice': float(row['Justice_0_10']) / 10.0,
                        'confidence': float(row['Confidence_0_10']) / 10.0 if row['Confidence_0_10'] else None,
                        'notes': row.get('Notes', '')
                    })

        return evaluations

    def _load_json(self, file_path: Path) -> List[Dict]:
        """Load evaluations from JSON."""
        with open(file_path, 'r') as f:
            data = json.load(f)

        evaluations = []
        for concept_data in data['concepts']:
            if concept_data['love'] is not None:  # Skip unevaluated
                evaluations.append({
                    'evaluator_id': data['evaluator_id'],
                    'concept': concept_data['concept'],
                    'love': concept_data['love'] / 10.0,  # Normalize to [0,1]
                    'power': concept_data['power'] / 10.0,
                    'wisdom': concept_data['wisdom'] / 10.0,
                    'justice': concept_data['justice'] / 10.0,
                    'confidence': concept_data.get('confidence', None),
                    'notes': concept_data.get('notes', '')
                })

        return evaluations

    def aggregate_evaluations(self, evaluations: List[Dict]) -> Dict[str, Dict]:
        """
        Aggregate evaluations across multiple evaluators.

        Args:
            evaluations: List of evaluation dictionaries

        Returns:
            Dictionary mapping concepts to aggregated ratings
        """
        import numpy as np
        from collections import defaultdict

        concept_ratings = defaultdict(lambda: {
            'love': [],
            'power': [],
            'wisdom': [],
            'justice': [],
            'confidence': []
        })

        # Collect all ratings
        for eval_data in evaluations:
            concept = eval_data['concept']
            concept_ratings[concept]['love'].append(eval_data['love'])
            concept_ratings[concept]['power'].append(eval_data['power'])
            concept_ratings[concept]['wisdom'].append(eval_data['wisdom'])
            concept_ratings[concept]['justice'].append(eval_data['justice'])
            if eval_data['confidence'] is not None:
                concept_ratings[concept]['confidence'].append(eval_data['confidence'])

        # Aggregate with mean and std
        aggregated = {}
        for concept, ratings in concept_ratings.items():
            aggregated[concept] = {
                'love_mean': np.mean(ratings['love']),
                'love_std': np.std(ratings['love']),
                'power_mean': np.mean(ratings['power']),
                'power_std': np.std(ratings['power']),
                'wisdom_mean': np.mean(ratings['wisdom']),
                'wisdom_std': np.std(ratings['wisdom']),
                'justice_mean': np.mean(ratings['justice']),
                'justice_std': np.std(ratings['justice']),
                'n_evaluators': len(ratings['love']),
                'confidence_mean': np.mean(ratings['confidence']) if ratings['confidence'] else None
            }

        return aggregated

    def calculate_inter_rater_reliability(self, evaluations: List[Dict]) -> Dict:
        """
        Calculate inter-rater reliability (Cronbach's alpha).

        Args:
            evaluations: List of evaluation dictionaries

        Returns:
            Reliability metrics
        """
        import numpy as np
        from collections import defaultdict

        # Group by concept
        concept_ratings = defaultdict(lambda: {
            'love': [],
            'power': [],
            'wisdom': [],
            'justice': []
        })

        for eval_data in evaluations:
            concept = eval_data['concept']
            concept_ratings[concept]['love'].append(eval_data['love'])
            concept_ratings[concept]['power'].append(eval_data['power'])
            concept_ratings[concept]['wisdom'].append(eval_data['wisdom'])
            concept_ratings[concept]['justice'].append(eval_data['justice'])

        # Calculate Cronbach's alpha for each dimension
        def cronbachs_alpha(ratings_matrix):
            """Calculate Cronbach's alpha for a matrix of ratings."""
            items = np.array(ratings_matrix)
            item_vars = items.var(axis=0, ddof=1)
            total_var = items.sum(axis=1).var(ddof=1)
            n_items = items.shape[1]
            alpha = (n_items / (n_items - 1)) * (1 - item_vars.sum() / total_var)
            return alpha

        reliability = {}

        for dimension in ['love', 'power', 'wisdom', 'justice']:
            # Build matrix: concepts x evaluators
            matrix = []
            for concept in sorted(concept_ratings.keys()):
                matrix.append(concept_ratings[concept][dimension])

            matrix = np.array(matrix).T  # Transpose to evaluators x concepts

            if matrix.shape[0] > 1:  # Need at least 2 evaluators
                alpha = cronbachs_alpha(matrix)
                reliability[dimension] = {
                    'cronbachs_alpha': alpha,
                    'n_evaluators': matrix.shape[0],
                    'n_concepts': matrix.shape[1]
                }

        return reliability


def generate_recruitment_text() -> str:
    """Generate text for recruiting human evaluators."""
    return """
CALL FOR EVALUATORS: Semantic Coordinate Research Study

We are conducting research on how people understand and evaluate concepts
across four fundamental dimensions: Love, Power, Wisdom, and Justice.

WHAT YOU'LL DO:
- Rate approximately 50-100 concepts on these four dimensions
- Takes 20-30 minutes
- No special knowledge required - just your honest intuitions
- All data anonymized

COMPENSATION:
- $20 gift card for completion
- Contribute to novel research in semantic analysis

ELIGIBILITY:
- 18+ years old
- Fluent in English
- No background in theology required

TO PARTICIPATE:
Email: anchor.point.study@example.com
Subject: "Evaluator Volunteer"

This research explores how human semantic understanding maps to
geometric space, with applications in AI, philosophy, and ethics.

IRB Approved: [Study Number]
Principal Investigator: [Name]
"""


if __name__ == "__main__":
    # Example usage
    protocol = HumanEvaluationProtocol("pilot_study_001")

    concepts = ["Love", "Hatred", "Justice", "Wisdom", "Power", "Evil", "JEHOVAH", "AGAPE"]

    # Generate evaluation sheet
    csv_path = protocol.generate_evaluation_sheet(concepts, format='csv')
    print(f"Evaluation sheet generated: {csv_path}")

    # Generate instructions
    print("\nEvaluation Instructions:")
    print("=" * 70)
    print(json.dumps(protocol._get_instructions(), indent=2))
