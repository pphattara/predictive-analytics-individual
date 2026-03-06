"""Submission checks for saved preprocessing outputs."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "outputs" / "adult_census_income" / "metrics"


class TestPreprocessingArtifacts(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads((METRICS / "preprocessing_validation.json").read_text(encoding="utf-8"))

    def test_required_keys_present(self):
        for key in [
            "module",
            "dataset",
            "target",
            "no_nan_train",
            "no_nan_val",
            "no_nan_test",
            "feature_count_train",
            "feature_count_val",
            "feature_count_test",
            "split_sizes",
            "class_balance_by_split",
            "leakage_checks_passed",
        ]:
            self.assertIn(key, self.payload)

    def test_no_nan_flags_true(self):
        self.assertTrue(self.payload["no_nan_train"])
        self.assertTrue(self.payload["no_nan_val"])
        self.assertTrue(self.payload["no_nan_test"])

    def test_feature_counts_match(self):
        self.assertEqual(self.payload["feature_count_train"], self.payload["feature_count_val"])
        self.assertEqual(self.payload["feature_count_train"], self.payload["feature_count_test"])

    def test_split_sizes_positive(self):
        split_sizes = self.payload["split_sizes"]
        for key in ["train", "val", "test"]:
            self.assertIn(key, split_sizes)
            self.assertGreater(split_sizes[key], 0)

    def test_leakage_check_passed(self):
        self.assertTrue(self.payload["leakage_checks_passed"])


if __name__ == "__main__":
    unittest.main()
