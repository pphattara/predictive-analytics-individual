"""Modeling interfaces and experiment logging schema."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class ExperimentRecord:
    experiment_id: str
    dataset: str
    model_family: str
    pipeline_variant: str
    cv_mean: float
    cv_std: float
    test_metric: float
    notes: str


def baseline_model(task_type: str) -> Any:
    """Return baseline estimator for classification or regression."""
    if task_type == "classification":
        from sklearn.dummy import DummyClassifier

        return DummyClassifier(strategy="most_frequent")
    from sklearn.dummy import DummyRegressor

    return DummyRegressor(strategy="mean")


def candidate_models(task_type: str) -> Dict[str, Any]:
    """Return candidate model families used in ablation and tuning."""
    from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
    from sklearn.linear_model import LogisticRegression, Ridge
    from sklearn.neural_network import MLPClassifier, MLPRegressor

    if task_type == "classification":
        return {
            "linear": LogisticRegression(max_iter=2000),
            "tree_ensemble": RandomForestClassifier(random_state=42),
            "neural": MLPClassifier(random_state=42, max_iter=500),
        }
    return {
        "linear": Ridge(random_state=42),
        "tree_ensemble": RandomForestRegressor(random_state=42),
        "neural": MLPRegressor(random_state=42, max_iter=500),
    }
