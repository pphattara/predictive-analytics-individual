"""Unit tests for src/evaluation.py — classification and regression metric contracts."""
import sys
import os
import unittest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.evaluation import (
    classification_report_dict,
    regression_report_dict,
    CLASSIFICATION_METRICS,
    REGRESSION_METRICS,
)


class TestClassificationReportDict(unittest.TestCase):
    def _binary_inputs(self):
        rng = np.random.default_rng(42)
        y_true = np.array([0, 1, 0, 1, 0, 1, 1, 0, 0, 1])
        y_pred = np.array([0, 1, 0, 0, 0, 1, 1, 0, 1, 1])
        y_prob = rng.uniform(0.0, 1.0, size=10)
        # make probabilities consistent with y_true direction
        y_prob = np.where(y_true == 1, rng.uniform(0.5, 1.0, 10), rng.uniform(0.0, 0.5, 10))
        return y_true, y_pred, y_prob

    def test_returns_required_keys(self):
        y_true, y_pred, y_prob = self._binary_inputs()
        result = classification_report_dict(y_true, y_pred, y_prob)
        for key in ("f1_weighted", "auc_pr", "roc_auc"):
            self.assertIn(key, result)

    def test_f1_in_valid_range(self):
        y_true, y_pred, y_prob = self._binary_inputs()
        result = classification_report_dict(y_true, y_pred, y_prob)
        self.assertGreaterEqual(result["f1_weighted"], 0.0)
        self.assertLessEqual(result["f1_weighted"], 1.0)

    def test_roc_auc_in_valid_range(self):
        y_true, y_pred, y_prob = self._binary_inputs()
        result = classification_report_dict(y_true, y_pred, y_prob)
        self.assertGreaterEqual(result["roc_auc"], 0.0)
        self.assertLessEqual(result["roc_auc"], 1.0)

    def test_perfect_classifier_f1_equals_one(self):
        y_true = np.array([0, 0, 0, 1, 1, 1])
        y_pred = np.array([0, 0, 0, 1, 1, 1])
        y_prob = np.array([0.1, 0.1, 0.1, 0.9, 0.9, 0.9])
        result = classification_report_dict(y_true, y_pred, y_prob)
        self.assertAlmostEqual(result["f1_weighted"], 1.0, places=5)

    def test_all_values_are_floats(self):
        y_true, y_pred, y_prob = self._binary_inputs()
        result = classification_report_dict(y_true, y_pred, y_prob)
        for v in result.values():
            self.assertIsInstance(v, float)


class TestRegressionReportDict(unittest.TestCase):
    def _regression_inputs(self):
        rng = np.random.default_rng(0)
        y_true = rng.normal(50000, 10000, 100)
        y_pred = y_true + rng.normal(0, 1000, 100)
        return y_true, y_pred

    def test_returns_required_keys(self):
        y_true, y_pred = self._regression_inputs()
        result = regression_report_dict(y_true, y_pred)
        for key in ("rmse", "mae", "r2"):
            self.assertIn(key, result)

    def test_rmse_positive(self):
        y_true, y_pred = self._regression_inputs()
        result = regression_report_dict(y_true, y_pred)
        self.assertGreater(result["rmse"], 0.0)

    def test_perfect_regression_rmse_zero(self):
        y_true = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        y_pred = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        result = regression_report_dict(y_true, y_pred)
        self.assertAlmostEqual(result["rmse"], 0.0, places=8)
        self.assertAlmostEqual(result["r2"], 1.0, places=8)


class TestMetricContracts(unittest.TestCase):
    def test_classification_metrics_list_contains_expected(self):
        required = {"f1_weighted", "auc_pr", "roc_auc", "recall_positive"}
        self.assertTrue(required.issubset(set(CLASSIFICATION_METRICS)))

    def test_regression_metrics_list_contains_expected(self):
        required = {"rmse", "mae", "r2"}
        self.assertTrue(required.issubset(set(REGRESSION_METRICS)))


if __name__ == "__main__":
    unittest.main()
