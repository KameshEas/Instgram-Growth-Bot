"""A/B testing framework for tracking prompt variant performance.

Enables data-driven optimization by comparing prompt variants and tracking
which ones produce better results (engagement, quality scores, user preference).
"""

import json
import sqlite3
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class TestStatus(Enum):
    """Status of an A/B test."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class VariantResult:
    """Result from a single prompt variant."""
    variant_id: str
    test_id: str
    user_id: int
    original_prompt: str
    variant_prompt: str
    quality_score: float
    user_rating: Optional[int] = None  # 1-5 stars
    engagement_score: Optional[float] = None  # 0-100
    impressions: int = 0
    saves: int = 0
    shares: int = 0
    comments: int = 0
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "variant_id": self.variant_id,
            "test_id": self.test_id,
            "user_id": self.user_id,
            "original_prompt": self.original_prompt,
            "variant_prompt": self.variant_prompt,
            "quality_score": self.quality_score,
            "user_rating": self.user_rating,
            "engagement_score": self.engagement_score,
            "impressions": self.impressions,
            "saves": self.saves,
            "shares": self.shares,
            "comments": self.comments,
            "timestamp": self.timestamp.isoformat(),
        }


class ABTestingFramework:
    """Framework for running A/B tests on prompt variants."""

    DB_PATH = Path("data/ab_tests.db")

    def __init__(self):
        """Initialize A/B testing framework."""
        self.db_path = self.DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for test tracking."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ab_tests (
                    test_id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    test_name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    original_prompt TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    ended_at TEXT,
                    hypothesis TEXT,
                    metadata TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_variants (
                    variant_id TEXT PRIMARY KEY,
                    test_id TEXT NOT NULL,
                    strategy TEXT NOT NULL,
                    variant_prompt TEXT NOT NULL,
                    description TEXT,
                    control BOOLEAN DEFAULT FALSE,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(test_id) REFERENCES ab_tests(test_id)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS variant_results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    variant_id TEXT NOT NULL,
                    test_id TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    quality_score REAL,
                    user_rating INTEGER,
                    engagement_score REAL,
                    impressions INTEGER,
                    saves INTEGER,
                    shares INTEGER,
                    comments INTEGER,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(variant_id) REFERENCES test_variants(variant_id),
                    FOREIGN KEY(test_id) REFERENCES ab_tests(test_id)
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_test_id ON ab_tests(test_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_variant_test ON test_variants(test_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_result_variant ON variant_results(variant_id)
            """)

            conn.commit()

    def create_test(
        self,
        test_id: str,
        test_name: str,
        category: str,
        original_prompt: str,
        hypothesis: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new A/B test.

        Args:
            test_id: Unique test identifier
            test_name: Human-readable test name
            category: Prompt category being tested
            original_prompt: Original prompt (control)
            hypothesis: Test hypothesis
            metadata: Additional test metadata

        Returns:
            Test creation result
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO ab_tests
                    (test_id, status, test_name, category, original_prompt, created_at, hypothesis, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    test_id,
                    TestStatus.ACTIVE.value,
                    test_name,
                    category,
                    original_prompt,
                    datetime.now().isoformat(),
                    hypothesis,
                    json.dumps(metadata or {}),
                ))
                conn.commit()

            logger.info(f"[AB_TEST] Created test: {test_id}")
            return {
                "status": "success",
                "test_id": test_id,
                "message": f"Test '{test_name}' created successfully",
            }
        except Exception as e:
            logger.error(f"[AB_TEST] Failed to create test: {e}")
            return {"status": "error", "error": str(e)}

    def add_variant(
        self,
        test_id: str,
        variant_id: str,
        strategy: str,
        variant_prompt: str,
        description: str = "",
        is_control: bool = False,
    ) -> Dict[str, Any]:
        """Add a variant to a test.

        Args:
            test_id: Test ID to add variant to
            variant_id: Unique variant identifier
            strategy: Enhancement strategy used (e.g., 'cinematic', 'detailed')
            variant_prompt: The variant prompt text
            description: Human-readable description
            is_control: Whether this is the control variant

        Returns:
            Variant creation result
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO test_variants
                    (variant_id, test_id, strategy, variant_prompt, description, control, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    variant_id,
                    test_id,
                    strategy,
                    variant_prompt,
                    description,
                    is_control,
                    datetime.now().isoformat(),
                ))
                conn.commit()

            logger.info(f"[AB_TEST] Added variant {variant_id} to test {test_id}")
            return {
                "status": "success",
                "variant_id": variant_id,
                "message": f"Variant added to test {test_id}",
            }
        except Exception as e:
            logger.error(f"[AB_TEST] Failed to add variant: {e}")
            return {"status": "error", "error": str(e)}

    def record_result(self, result: VariantResult) -> Dict[str, Any]:
        """Record a test result.

        Args:
            result: VariantResult with test outcome

        Returns:
            Recording result
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO variant_results
                    (variant_id, test_id, user_id, quality_score, user_rating,
                     engagement_score, impressions, saves, shares, comments, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    result.variant_id,
                    result.test_id,
                    result.user_id,
                    result.quality_score,
                    result.user_rating,
                    result.engagement_score,
                    result.impressions,
                    result.saves,
                    result.shares,
                    result.comments,
                    result.timestamp.isoformat(),
                ))
                conn.commit()

            return {"status": "success", "message": "Result recorded"}
        except Exception as e:
            logger.error(f"[AB_TEST] Failed to record result: {e}")
            return {"status": "error", "error": str(e)}

    def get_test_results(
        self,
        test_id: str,
        min_samples: int = 5,
    ) -> Dict[str, Any]:
        """Get statistical results for a test.

        Args:
            test_id: Test ID to analyze
            min_samples: Minimum samples per variant for statistical significance

        Returns:
            Test results and statistical analysis
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get test info
                test = conn.execute(
                    "SELECT * FROM ab_tests WHERE test_id = ?",
                    (test_id,)
                ).fetchone()

                if not test:
                    return {"status": "error", "error": f"Test {test_id} not found"}

                # Get variants
                variants = conn.execute(
                    "SELECT * FROM test_variants WHERE test_id = ?",
                    (test_id,)
                ).fetchall()

                # Get results per variant
                results_data = {}
                for variant in variants:
                    variant_id = variant[0]
                    results = conn.execute(
                        "SELECT * FROM variant_results WHERE variant_id = ?",
                        (variant_id,)
                    ).fetchall()

                    results_data[variant_id] = results

            # Calculate statistics
            stats = self._calculate_statistics(results_data, min_samples)

            return {
                "status": "success",
                "test_id": test_id,
                "test_name": test[2],
                "variant_count": len(variants),
                "statistics": stats,
                "winner": self._determine_winner(stats),
                "sample_counts": {
                    v[0]: len(results_data.get(v[0], []))
                    for v in variants
                },
            }
        except Exception as e:
            logger.error(f"[AB_TEST] Failed to get results: {e}")
            return {"status": "error", "error": str(e)}

    def _calculate_statistics(
        self,
        results_data: Dict[str, List],
        min_samples: int,
    ) -> Dict[str, Any]:
        """Calculate statistics for test results."""
        stats = {}

        for variant_id, results in results_data.items():
            if not results or len(results) < min_samples:
                stats[variant_id] = {
                    "sample_count": len(results),
                    "status": "insufficient_samples",
                    "note": f"Need at least {min_samples} samples",
                }
                continue

            # Extract metrics (indices based on DB schema)
            quality_scores = [r[4] for r in results if r[4] is not None]
            engagement_scores = [r[6] for r in results if r[6] is not None]
            user_ratings = [r[5] for r in results if r[5] is not None]

            stats[variant_id] = {
                "sample_count": len(results),
                "status": "valid",
                "quality_score": {
                    "mean": sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                    "samples": len(quality_scores),
                },
                "engagement_score": {
                    "mean": sum(engagement_scores) / len(engagement_scores) if engagement_scores else 0,
                    "samples": len(engagement_scores),
                },
                "user_rating": {
                    "mean": sum(user_ratings) / len(user_ratings) if user_ratings else 0,
                    "samples": len(user_ratings),
                },
            }

        return stats

    def _determine_winner(self, stats: Dict[str, Any]) -> Optional[str]:
        """Determine winning variant based on metrics."""
        valid_variants = {
            v: s for v, s in stats.items()
            if s.get("status") == "valid"
        }

        if not valid_variants:
            return None

        # Score variants: 40% quality, 40% engagement, 20% rating
        scores = {}
        for variant_id, stat in valid_variants.items():
            score = (
                stat["quality_score"]["mean"] * 0.4 +
                stat["engagement_score"]["mean"] * 0.4 +
                stat["user_rating"]["mean"] * 20  # Scale 0-5 to 0-100
            )
            scores[variant_id] = score

        if not scores:
            return None

        return max(scores, key=scores.get)

    def get_winning_variants(
        self,
        category: str,
        limit: int = 5,
    ) -> Dict[str, Any]:
        """Get top-performing variants for a category.

        Args:
            category: Content category
            limit: Number of top variants to return

        Returns:
            List of winning variants and their strategies
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Find completed tests for this category
                tests = conn.execute(
                    "SELECT test_id FROM ab_tests WHERE category = ? AND status = ?",
                    (category, TestStatus.COMPLETED.value)
                ).fetchall()

                if not tests:
                    return {
                        "status": "success",
                        "category": category,
                        "winning_variants": [],
                        "note": "No completed tests found",
                    }

                # Collect results for winning variants
                winning = []
                for test_id, in tests:
                    result = self.get_test_results(test_id)
                    if result.get("winner"):
                        winner_id = result["winner"]
                        winner_info = conn.execute(
                            "SELECT strategy, variant_prompt FROM test_variants WHERE variant_id = ?",
                            (winner_id,)
                        ).fetchone()

                        winning.append({
                            "variant_id": winner_id,
                            "test_id": test_id,
                            "strategy": winner_info[0],
                            "quality_score": result["statistics"][winner_id]["quality_score"]["mean"],
                        })

                # Sort by quality score and limit
                winning.sort(key=lambda x: x["quality_score"], reverse=True)

                return {
                    "status": "success",
                    "category": category,
                    "winning_variants": winning[:limit],
                }
        except Exception as e:
            logger.error(f"[AB_TEST] Failed to get winning variants: {e}")
            return {"status": "error", "error": str(e)}
