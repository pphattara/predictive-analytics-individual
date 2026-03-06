"""Feature engineering contract."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class FeatureDecision:
    name: str
    formula: str
    rationale: str


def build_feature_set(dataset_name: str, frame: Any) -> tuple[Any, Dict[str, FeatureDecision]]:
    """Return transformed frame and documented feature decisions."""
    raise NotImplementedError(f"Feature pipeline not implemented for dataset: {dataset_name}")

