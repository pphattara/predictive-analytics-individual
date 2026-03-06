"""Preprocessing contract for all candidate datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SplitConfig:
    train_size: float = 0.70
    val_size: float = 0.15
    test_size: float = 0.15
    random_state: int = 42
    stratify: bool = True


def build_preprocessor(dataset_name: str) -> Any:
    """Return a leak-safe preprocessing pipeline for a dataset.

    Implementations should be dataset-specific and fitted only on training data.
    """
    raise NotImplementedError(f"Preprocessor not implemented for dataset: {dataset_name}")


def validate_transformed_splits(X_train: Any, X_val: Any, X_test: Any) -> None:
    """Validate post-transform split integrity.

    Required checks:
    - no NaN values remain
    - feature counts match across splits
    """
    for name, matrix in (("train", X_train), ("val", X_val), ("test", X_test)):
        if hasattr(matrix, "isna"):
            has_nan = bool(matrix.isna().any().any())
        else:
            import numpy as np

            has_nan = bool(np.isnan(matrix).any())
        assert not has_nan, f"NaN detected in {name} split"

    train_cols = X_train.shape[1]
    assert train_cols == X_val.shape[1] == X_test.shape[1], "Feature count mismatch across splits"

