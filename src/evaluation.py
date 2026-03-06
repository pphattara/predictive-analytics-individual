"""Evaluation contracts for classification and regression workflows."""

from __future__ import annotations

from typing import Dict

from sklearn.metrics import (
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_recall_curve,
    r2_score,
    roc_auc_score,
)


CLASSIFICATION_METRICS = [
    "f1_weighted",
    "auc_pr",
    "roc_auc",
    "recall_positive",
    "calibration_error",
]

REGRESSION_METRICS = [
    "rmse",
    "mae",
    "r2",
    "mape",
    "residual_diagnostics_summary",
]


def classification_report_dict(y_true, y_pred, y_prob) -> Dict[str, float]:
    """Compute core classification metrics contract."""
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    auc_pr = float(abs((recall[:-1] - recall[1:]).dot(precision[:-1])))
    return {
        "f1_weighted": float(f1_score(y_true, y_pred, average="weighted")),
        "auc_pr": auc_pr,
        "roc_auc": float(roc_auc_score(y_true, y_prob)),
    }


def regression_report_dict(y_true, y_pred) -> Dict[str, float]:
    """Compute core regression metrics contract."""
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    return {
        "rmse": float(rmse),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }

