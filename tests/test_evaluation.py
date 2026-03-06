"""Submission checks for saved evaluation outputs."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "outputs" / "adult_census_income" / "metrics"


class TestEvaluationArtifacts(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads((METRICS / "evaluation_report.json").read_text(encoding="utf-8"))

    def test_required_top_level_keys(self):
        for key in [
            "module",
            "dataset",
            "target",
            "positive_class",
            "split_sizes",
            "selection",
            "baseline_validation_metrics",
            "test_metrics",
        ]:
            self.assertIn(key, self.payload)

    def test_required_test_metrics_present(self):
        metrics = self.payload["test_metrics"]
        for key in ["f1_weighted", "auc_pr", "roc_auc", "recall_positive", "calibration_error"]:
            self.assertIn(key, metrics)
            self.assertIsNotNone(metrics[key])

    def test_probability_metrics_in_range(self):
        metrics = self.payload["test_metrics"]
        for key in ["f1_weighted", "auc_pr", "roc_auc", "recall_positive"]:
            self.assertGreaterEqual(metrics[key], 0.0)
            self.assertLessEqual(metrics[key], 1.0)
        self.assertGreaterEqual(metrics["calibration_error"], 0.0)

    def test_selection_threshold_in_range(self):
        threshold = self.payload["selection"]["threshold"]
        self.assertGreaterEqual(threshold, 0.0)
        self.assertLessEqual(threshold, 1.0)


if __name__ == "__main__":
    unittest.main()
