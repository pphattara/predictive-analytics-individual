"""Unit tests for src/preprocessing.py — split validation and pipeline contracts."""
import sys
import os
import unittest
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.preprocessing import validate_transformed_splits, SplitConfig, build_preprocessor


class TestSplitConfig(unittest.TestCase):
    def test_default_ratios_sum_to_one(self):
        cfg = SplitConfig()
        self.assertAlmostEqual(cfg.train_size + cfg.val_size + cfg.test_size, 1.0)

    def test_default_seed(self):
        cfg = SplitConfig()
        self.assertEqual(cfg.random_state, 42)

    def test_stratify_on_by_default(self):
        cfg = SplitConfig()
        self.assertTrue(cfg.stratify)


class TestBuildPreprocessor(unittest.TestCase):
    def test_returns_column_transformer_for_adult(self):
        from sklearn.compose import ColumnTransformer

        pre = build_preprocessor("adult_census_income")
        self.assertIsInstance(pre, ColumnTransformer)

    def test_raises_for_unknown_dataset(self):
        with self.assertRaises(NotImplementedError):
            build_preprocessor("unknown_dataset")


class TestValidateTransformedSplits(unittest.TestCase):
    def _clean_splits(self):
        rng = np.random.default_rng(42)
        return (
            rng.random((100, 5)),
            rng.random((20, 5)),
            rng.random((20, 5)),
        )

    def test_passes_on_clean_splits(self):
        X_train, X_val, X_test = self._clean_splits()
        # Should not raise
        validate_transformed_splits(X_train, X_val, X_test)

    def test_raises_on_nan_in_train(self):
        X_train, X_val, X_test = self._clean_splits()
        X_train[0, 0] = np.nan
        with self.assertRaises(AssertionError):
            validate_transformed_splits(X_train, X_val, X_test)

    def test_raises_on_nan_in_val(self):
        X_train, X_val, X_test = self._clean_splits()
        X_val[3, 2] = np.nan
        with self.assertRaises(AssertionError):
            validate_transformed_splits(X_train, X_val, X_test)

    def test_raises_on_nan_in_test(self):
        X_train, X_val, X_test = self._clean_splits()
        X_test[1, 4] = np.nan
        with self.assertRaises(AssertionError):
            validate_transformed_splits(X_train, X_val, X_test)

    def test_passes_with_dataframe_inputs(self):
        rng = np.random.default_rng(0)
        df_train = pd.DataFrame(rng.random((50, 3)), columns=["a", "b", "c"])
        df_val   = pd.DataFrame(rng.random((10, 3)), columns=["a", "b", "c"])
        df_test  = pd.DataFrame(rng.random((10, 3)), columns=["a", "b", "c"])
        validate_transformed_splits(df_train, df_val, df_test)

    def test_raises_on_nan_in_dataframe(self):
        rng = np.random.default_rng(1)
        df_train = pd.DataFrame(rng.random((50, 3)), columns=["a", "b", "c"])
        df_train.iloc[5, 1] = np.nan
        df_val   = pd.DataFrame(rng.random((10, 3)), columns=["a", "b", "c"])
        df_test  = pd.DataFrame(rng.random((10, 3)), columns=["a", "b", "c"])
        with self.assertRaises(AssertionError):
            validate_transformed_splits(df_train, df_val, df_test)


if __name__ == "__main__":
    unittest.main()
