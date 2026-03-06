"""Preprocessing contract for all candidate datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler


@dataclass(frozen=True)
class SplitConfig:
    train_size: float = 0.70
    val_size: float = 0.15
    test_size: float = 0.15
    random_state: int = 42
    stratify: bool = True


def build_preprocessor(dataset_name: str) -> Any:
    """Return a leak-safe preprocessing pipeline for a dataset."""
    if dataset_name != "adult_census_income":
        raise NotImplementedError(f"Preprocessor not implemented for dataset: {dataset_name}")

    numeric_features = [
        "age",
        "fnlwgt",
        "education.num",
        "capital.gain",
        "capital.loss",
        "hours.per.week",
    ]
    categorical_features = [
        "workclass",
        "education",
        "marital.status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "native.country",
    ]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ]
    )


def validate_transformed_splits(X_train: Any, X_val: Any, X_test: Any) -> None:
    """Validate post-transform split integrity."""
    for name, matrix in (("train", X_train), ("val", X_val), ("test", X_test)):
        if hasattr(matrix, "isna"):
            has_nan = bool(matrix.isna().any().any())
        else:
            import numpy as np

            has_nan = bool(np.isnan(matrix).any())
        assert not has_nan, f"NaN detected in {name} split"

    train_cols = X_train.shape[1]
    assert train_cols == X_val.shape[1] == X_test.shape[1], "Feature count mismatch across splits"
