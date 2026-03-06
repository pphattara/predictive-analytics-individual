"""Feature engineering contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

import pandas as pd


@dataclass(frozen=True)
class FeatureDecision:
    name: str
    formula: str
    rationale: str


def build_feature_set(dataset_name: str, frame: Any) -> tuple[Any, Dict[str, FeatureDecision]]:
    """Return transformed frame and documented feature decisions."""
    if dataset_name != "adult_census_income":
        raise NotImplementedError(f"Feature pipeline not implemented for dataset: {dataset_name}")

    transformed = frame.copy()
    decisions: Dict[str, FeatureDecision] = {}

    # Lightweight deterministic features used for optional downstream analysis.
    if {"capital.gain", "capital.loss"}.issubset(transformed.columns):
        transformed["capital.net"] = transformed["capital.gain"] - transformed["capital.loss"]
        decisions["capital.net"] = FeatureDecision(
            name="capital.net",
            formula="capital.gain - capital.loss",
            rationale="Net capital movement captures combined gain/loss signal in one numeric feature.",
        )

    if {"hours.per.week", "age"}.issubset(transformed.columns):
        safe_age = transformed["age"].replace(0, pd.NA)
        transformed["hours_per_age"] = (transformed["hours.per.week"] / safe_age).fillna(0.0)
        decisions["hours_per_age"] = FeatureDecision(
            name="hours_per_age",
            formula="hours.per.week / age",
            rationale="Age-normalized work intensity offers a stable interaction-style signal.",
        )

    decisions["core_feature_retention"] = FeatureDecision(
        name="core_feature_retention",
        formula="identity(frame)",
        rationale="Original Adult Census columns are retained to preserve interpretability and comparability.",
    )

    return transformed, decisions
