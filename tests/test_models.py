"""Submission checks for saved model-selection outputs."""

from pathlib import Path
import json
import unittest

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "outputs" / "adult_census_income" / "metrics"


class TestModelSelectionArtifacts(unittest.TestCase):
    def setUp(self) -> None:
        self.model_comparison = pd.read_csv(METRICS / "model_comparison_cv.csv")
        self.ablations = pd.read_csv(METRICS / "ablation_results.csv")
        self.threshold_policy = json.loads((METRICS / "threshold_policy.json").read_text(encoding="utf-8"))

    def test_model_comparison_columns_present(self):
        required = {
            "experiment_id",
            "dataset",
            "model_family",
            "pipeline_variant",
            "cv_mean",
            "cv_std",
            "notes",
        }
        self.assertTrue(required.issubset(self.model_comparison.columns))

    def test_model_comparison_nonempty(self):
        self.assertGreater(len(self.model_comparison), 0)
        self.assertTrue((self.model_comparison["cv_mean"] >= 0).all())
        self.assertTrue((self.model_comparison["cv_mean"] <= 1).all())

    def test_ablation_results_nonempty(self):
        self.assertGreaterEqual(len(self.ablations), 4)
        self.assertIn("pipeline_variant", self.ablations.columns)
        self.assertIn("dropped_columns", self.ablations.columns)

    def test_threshold_policy_schema(self):
        for key in [
            "selected_model_family",
            "selected_variant",
            "threshold",
            "validation_f1_weighted_at_threshold",
            "validation_recall_positive_at_threshold",
            "validation_precision_positive_at_threshold",
            "rationale",
        ]:
            self.assertIn(key, self.threshold_policy)

    def test_threshold_in_valid_range(self):
        threshold = self.threshold_policy["threshold"]
        self.assertGreaterEqual(threshold, 0.0)
        self.assertLessEqual(threshold, 1.0)


if __name__ == "__main__":
    unittest.main()
