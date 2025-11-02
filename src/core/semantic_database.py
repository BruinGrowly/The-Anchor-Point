"""
Semantic Database
=================

Database system for storing and querying semantic coordinates.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Tuple
from pathlib import Path
import pandas as pd

from .semantic_coordinates import SemanticCoordinate, AnchorPoint


class SemanticDatabase:
    """
    SQLite database for storing semantic coordinates and metadata.
    """

    def __init__(self, db_path: str = "data/semantic_database.db"):
        """
        Initialize the database.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self._create_tables()

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Main concepts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS concepts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                concept TEXT NOT NULL UNIQUE,
                love REAL NOT NULL,
                power REAL NOT NULL,
                wisdom REAL NOT NULL,
                justice REAL NOT NULL,
                distance_to_anchor REAL NOT NULL,
                source TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Experiments table for tracking different measurement methods
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS experiments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                method TEXT,
                parameters TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Measurements table for linking concepts to experiments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                experiment_id INTEGER NOT NULL,
                concept_id INTEGER NOT NULL,
                love REAL NOT NULL,
                power REAL NOT NULL,
                wisdom REAL NOT NULL,
                justice REAL NOT NULL,
                distance_to_anchor REAL NOT NULL,
                FOREIGN KEY (experiment_id) REFERENCES experiments(id),
                FOREIGN KEY (concept_id) REFERENCES concepts(id)
            )
        """)

        # Create indexes for faster queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_distance
            ON concepts(distance_to_anchor)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_concept
            ON concepts(concept)
        """)

        self.conn.commit()

    def add_concept(self, coord: SemanticCoordinate, metadata: Optional[Dict] = None) -> int:
        """
        Add a semantic coordinate to the database.

        Args:
            coord: SemanticCoordinate to add
            metadata: Optional metadata dictionary

        Returns:
            ID of the inserted concept
        """
        cursor = self.conn.cursor()

        metadata_json = json.dumps(metadata) if metadata else None

        cursor.execute("""
            INSERT OR REPLACE INTO concepts
            (concept, love, power, wisdom, justice, distance_to_anchor, source, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            coord.concept,
            coord.love,
            coord.power,
            coord.wisdom,
            coord.justice,
            coord.distance_to_anchor(),
            coord.source,
            metadata_json
        ))

        self.conn.commit()
        return cursor.lastrowid

    def add_concepts_bulk(self, coords: List[SemanticCoordinate]) -> int:
        """
        Add multiple concepts efficiently.

        Args:
            coords: List of SemanticCoordinates

        Returns:
            Number of concepts added
        """
        cursor = self.conn.cursor()

        data = [
            (c.concept, c.love, c.power, c.wisdom, c.justice,
             c.distance_to_anchor(), c.source, None)
            for c in coords
        ]

        cursor.executemany("""
            INSERT OR REPLACE INTO concepts
            (concept, love, power, wisdom, justice, distance_to_anchor, source, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)

        self.conn.commit()
        return len(coords)

    def get_concept(self, concept_name: str) -> Optional[SemanticCoordinate]:
        """
        Retrieve a concept by name.

        Args:
            concept_name: Name of the concept

        Returns:
            SemanticCoordinate if found, None otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT concept, love, power, wisdom, justice, source
            FROM concepts
            WHERE concept = ?
        """, (concept_name,))

        row = cursor.fetchone()
        if row:
            return SemanticCoordinate(
                concept=row[0],
                love=row[1],
                power=row[2],
                wisdom=row[3],
                justice=row[4],
                source=row[5]
            )
        return None

    def get_closest_to_anchor(self, n: int = 10) -> List[SemanticCoordinate]:
        """
        Get the n concepts closest to the Anchor Point.

        Args:
            n: Number of concepts to retrieve

        Returns:
            List of closest concepts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT concept, love, power, wisdom, justice, source
            FROM concepts
            ORDER BY distance_to_anchor ASC
            LIMIT ?
        """, (n,))

        return [
            SemanticCoordinate(
                concept=row[0],
                love=row[1],
                power=row[2],
                wisdom=row[3],
                justice=row[4],
                source=row[5]
            )
            for row in cursor.fetchall()
        ]

    def get_all_concepts(self) -> List[SemanticCoordinate]:
        """
        Retrieve all concepts from the database.

        Returns:
            List of all SemanticCoordinates
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT concept, love, power, wisdom, justice, source
            FROM concepts
        """)

        return [
            SemanticCoordinate(
                concept=row[0],
                love=row[1],
                power=row[2],
                wisdom=row[3],
                justice=row[4],
                source=row[5]
            )
            for row in cursor.fetchall()
        ]

    def get_statistics(self) -> Dict[str, float]:
        """
        Get statistical summary of all concepts.

        Returns:
            Dictionary of statistics
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as count,
                AVG(distance_to_anchor) as mean_distance,
                MIN(distance_to_anchor) as min_distance,
                MAX(distance_to_anchor) as max_distance,
                AVG(love) as mean_love,
                AVG(power) as mean_power,
                AVG(wisdom) as mean_wisdom,
                AVG(justice) as mean_justice
            FROM concepts
        """)

        row = cursor.fetchone()
        return {
            'count': row[0],
            'mean_distance': row[1],
            'min_distance': row[2],
            'max_distance': row[3],
            'mean_love': row[4],
            'mean_power': row[5],
            'mean_wisdom': row[6],
            'mean_justice': row[7]
        }

    def search_concepts(self, pattern: str) -> List[SemanticCoordinate]:
        """
        Search for concepts matching a pattern.

        Args:
            pattern: SQL LIKE pattern (use % as wildcard)

        Returns:
            List of matching concepts
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT concept, love, power, wisdom, justice, source
            FROM concepts
            WHERE concept LIKE ?
            ORDER BY distance_to_anchor ASC
        """, (pattern,))

        return [
            SemanticCoordinate(
                concept=row[0],
                love=row[1],
                power=row[2],
                wisdom=row[3],
                justice=row[4],
                source=row[5]
            )
            for row in cursor.fetchall()
        ]

    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export all concepts to a pandas DataFrame.

        Returns:
            DataFrame with all concepts and their coordinates
        """
        return pd.read_sql_query("""
            SELECT concept, love, power, wisdom, justice,
                   distance_to_anchor, source, created_at
            FROM concepts
            ORDER BY distance_to_anchor ASC
        """, self.conn)

    def create_experiment(self, name: str, description: str,
                         method: str, parameters: Dict) -> int:
        """
        Create a new experiment record.

        Args:
            name: Experiment name
            description: Experiment description
            method: Method used (e.g., 'hash_sha256', 'manual_assignment')
            parameters: Experiment parameters

        Returns:
            Experiment ID
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO experiments (name, description, method, parameters)
            VALUES (?, ?, ?, ?)
        """, (name, description, method, json.dumps(parameters)))

        self.conn.commit()
        return cursor.lastrowid

    def add_measurement(self, experiment_id: int, coord: SemanticCoordinate) -> int:
        """
        Add a measurement to an experiment.

        Args:
            experiment_id: ID of the experiment
            coord: SemanticCoordinate measured

        Returns:
            Measurement ID
        """
        # First ensure concept exists
        concept_id = self.add_concept(coord)

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO measurements
            (experiment_id, concept_id, love, power, wisdom, justice, distance_to_anchor)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            experiment_id,
            concept_id,
            coord.love,
            coord.power,
            coord.wisdom,
            coord.justice,
            coord.distance_to_anchor()
        ))

        self.conn.commit()
        return cursor.lastrowid

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
