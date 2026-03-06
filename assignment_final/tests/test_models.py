"""Unit tests for src/models.py — baseline model factory and experiment record."""
import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.models import baseline_model, ExperimentRecord


class TestBaselineModel(unittest.TestCase):
    def test_classification_returns_dummy_classifier(self):
        from sklearn.dummy import DummyClassifier
        model = baseline_model("classification")
        self.assertIsInstance(model, DummyClassifier)

    def test_classification_uses_most_frequent_strategy(self):
        model = baseline_model("classification")
        self.assertEqual(model.strategy, "most_frequent")

    def test_regression_returns_dummy_regressor(self):
        from sklearn.dummy import DummyRegressor
        model = baseline_model("regression")
        self.assertIsInstance(model, DummyRegressor)

    def test_regression_uses_mean_strategy(self):
        model = baseline_model("regression")
        self.assertEqual(model.strategy, "mean")

    def test_classification_model_is_fittable(self):
        import numpy as np
        model = baseline_model("classification")
        X = np.zeros((10, 2))
        y = np.array([0, 1, 0, 1, 0, 1, 0, 0, 0, 0])
        model.fit(X, y)
        preds = model.predict(X)
        self.assertEqual(len(preds), 10)
        # most_frequent → all predictions should be 0
        self.assertTrue((preds == 0).all())

    def test_regression_model_is_fittable(self):
        import numpy as np
        model = baseline_model("regression")
        X = np.zeros((10, 2))
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 1.0, 2.0, 3.0, 4.0, 5.0])
        model.fit(X, y)
        preds = model.predict(X)
        self.assertEqual(len(preds), 10)
        self.assertAlmostEqual(preds[0], np.mean(y), places=5)


class TestExperimentRecord(unittest.TestCase):
    def _make_record(self):
        return ExperimentRecord(
            experiment_id="test_001",
            dataset="adult_census_income",
            model_family="tree_hgb_tuned",
            pipeline_variant="robust",
            cv_mean=0.869,
            cv_std=0.003,
            test_metric=0.862,
            notes="Test record",
        )

    def test_record_fields_accessible(self):
        rec = self._make_record()
        self.assertEqual(rec.experiment_id, "test_001")
        self.assertEqual(rec.dataset, "adult_census_income")
        self.assertAlmostEqual(rec.cv_mean, 0.869)

    def test_record_is_frozen(self):
        rec = self._make_record()
        with self.assertRaises(Exception):
            rec.cv_mean = 0.999  # frozen dataclass should raise

    def test_record_cv_mean_in_valid_range(self):
        rec = self._make_record()
        self.assertGreaterEqual(rec.cv_mean, 0.0)
        self.assertLessEqual(rec.cv_mean, 1.0)


if __name__ == "__main__":
    unittest.main()
