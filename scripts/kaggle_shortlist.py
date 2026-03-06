#!/usr/bin/env python3
"""Build a Kaggle top-10 shortlist constrained to 10k-70k rows."""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


MIN_ROWS = 10_000
MAX_ROWS = 70_000
TARGET_CLASSIFICATION = 7
TARGET_REGRESSION = 3
TOP_N = 10
MAX_CANDIDATES_TO_VERIFY = 120

SEARCH_TERMS: Sequence[str] = (
    "health classification",
    "loan default",
    "bank marketing",
    "employee attrition",
    "customer churn",
    "insurance charges regression",
    "house prices",
    "retail sales forecasting",
    "credit risk",
    "education performance",
    "heart disease",
    "stroke prediction",
    "hospital readmission",
    "fraud detection",
    "telecom churn",
)

BLACKLIST_PATTERNS: Sequence[str] = (
    "titanic",
    "iris",
    "mnist",
    "digit-recognizer",
    "house-prices-advanced-regression-techniques",
)

TARGET_HINTS: Sequence[str] = (
    "target",
    "label",
    "class",
    "churn",
    "default",
    "outcome",
    "loan_status",
    "stroke",
    "heart",
    "survived",
    "is_fraud",
    "fraud",
    "price",
    "charges",
    "salary",
    "sales",
    "revenue",
    "score",
    "risk",
    "y",
)


@dataclass
class Candidate:
    dataset_slug: str
    title: str
    kaggle_url: str
    source_search: str
    task_type: str
    verified_rows: int
    target_column: str
    feature_overview: str
    why_proper_for_coursework: str
    risks_or_caveats: str
    fit_score: int
    score_breakdown: Dict[str, int] = field(default_factory=dict)


def _kaggle_bin() -> str:
    cli = os.environ.get("KAGGLE_BIN")
    if cli:
        return cli
    user_bin = Path.home() / "Library/Python/3.13/bin/kaggle"
    if user_bin.exists():
        return str(user_bin)
    return "kaggle"


def _kaggle_env(config_dir: Path) -> Dict[str, str]:
    env = os.environ.copy()
    env["KAGGLE_CONFIG_DIR"] = str(config_dir)
    return env


def _run(cmd: Sequence[str], *, env: Dict[str, str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _has_credentials(config_dir: Path) -> bool:
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True
    cfg = config_dir / "kaggle.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text(encoding="utf-8"))
            return bool(data.get("username")) and bool(data.get("key"))
        except json.JSONDecodeError:
            return False
    return False


def _validate_auth(kaggle_cmd: str, env: Dict[str, str], cwd: Path) -> None:
    test_cmd = [kaggle_cmd, "datasets", "list", "-s", "tabular", "-p", "1", "-v"]
    result = _run(test_cmd, env=env, cwd=cwd)
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        details = stderr if stderr else stdout
        raise RuntimeError(
            "Kaggle auth validation failed.\n"
            f"Command: {' '.join(test_cmd)}\n"
            f"Details: {details}\n\n"
            "Remediation:\n"
            "1) Create .kaggle/kaggle.json in this project with:\n"
            '   {"username":"<your_kaggle_username>","key":"<your_kaggle_key>"}\n'
            "2) Run: chmod 600 .kaggle/kaggle.json\n"
            "3) Re-run this script."
        )


def _parse_csv_output(raw: str) -> List[Dict[str, str]]:
    if not raw.strip():
        return []
    reader = csv.DictReader(io.StringIO(raw))
    return [row for row in reader]


def _discover_candidates(kaggle_cmd: str, env: Dict[str, str], cwd: Path) -> List[Dict[str, str]]:
    discovered: Dict[str, Dict[str, str]] = {}
    for term in SEARCH_TERMS:
        for page in (1, 2, 3):
            cmd = [
                kaggle_cmd,
                "datasets",
                "list",
                "-s",
                term,
                "--file-type",
                "csv",
                "--sort-by",
                "votes",
                "-p",
                str(page),
                "-v",
            ]
            result = _run(cmd, env=env, cwd=cwd)
            if result.returncode != 0:
                continue
            rows = _parse_csv_output(result.stdout)
            for row in rows:
                ref = (row.get("ref") or "").strip()
                title = (row.get("title") or ref).strip()
                if not ref:
                    continue
                lowered = ref.lower()
                if any(pattern in lowered for pattern in BLACKLIST_PATTERNS):
                    continue
                if ref not in discovered:
                    discovered[ref] = {"ref": ref, "title": title, "search": term}
    return list(discovered.values())


def _find_tabular_files(base_dir: Path) -> List[Path]:
    allowed = {".csv", ".tsv", ".parquet"}
    files: List[Path] = []
    for path in base_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() in allowed:
            files.append(path)
    files.sort(key=lambda p: p.stat().st_size, reverse=True)
    return files


def _load_frame(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path, low_memory=False)
    if suffix == ".tsv":
        return pd.read_csv(path, sep="\t", low_memory=False)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file type: {path}")


def _guess_target_column(df: pd.DataFrame) -> Optional[str]:
    lowered = {col.lower(): col for col in df.columns}
    for hint in TARGET_HINTS:
        for low_name, original in lowered.items():
            if low_name == hint or low_name.endswith(f"_{hint}") or hint in low_name:
                return original
    # Conservative fallback: avoid index-like or id-only names.
    fallback_cols = [c for c in df.columns if not re.search(r"\b(id|index)\b", str(c).lower())]
    if fallback_cols:
        return fallback_cols[-1]
    return None


def _infer_task_type(series: pd.Series, n_rows: int) -> str:
    non_null = series.dropna()
    if non_null.empty:
        return "classification"
    nunique = non_null.nunique()
    if series.dtype == "O" or str(series.dtype).startswith("category"):
        return "classification"
    if pd.api.types.is_bool_dtype(series):
        return "classification"
    if nunique <= 20 and (nunique / max(n_rows, 1)) <= 0.15:
        return "classification"
    return "regression"


def _feature_overview(df: pd.DataFrame, target_col: str) -> str:
    feature_df = df.drop(columns=[target_col], errors="ignore")
    numeric_cols = feature_df.select_dtypes(include=["number"]).columns
    categorical_cols = [c for c in feature_df.columns if c not in numeric_cols]
    missing_rate = feature_df.isna().mean().mean() if not feature_df.empty else 0.0
    return (
        f"{feature_df.shape[1]} features "
        f"({len(numeric_cols)} numeric, {len(categorical_cols)} categorical), "
        f"avg missingness {missing_rate:.1%}"
    )


def _score_candidate(df: pd.DataFrame, target_col: str, task_type: str) -> Tuple[int, Dict[str, int]]:
    feature_df = df.drop(columns=[target_col], errors="ignore")
    num_cols = feature_df.select_dtypes(include=["number"]).columns
    cat_cols = [c for c in feature_df.columns if c not in num_cols]
    avg_missing = float(feature_df.isna().mean().mean()) if not feature_df.empty else 0.0
    n_features = int(feature_df.shape[1])

    richness = 0
    richness += 40 if len(num_cols) > 2 else 20
    richness += 30 if len(cat_cols) > 1 else 10
    richness += 30 if 0.01 <= avg_missing <= 0.35 else 10
    richness = min(100, richness)

    modeling = 0
    modeling += 35 if n_features >= 10 else 15
    modeling += 30 if task_type == "classification" else 25
    modeling += 35 if feature_df.isna().any().any() else 20
    modeling = min(100, modeling)

    realism = 75
    reportability = 80 if n_features >= 8 else 60
    novelty = 85

    weighted = (
        0.30 * richness
        + 0.25 * modeling
        + 0.20 * realism
        + 0.15 * reportability
        + 0.10 * novelty
    )

    breakdown = {
        "methodological_richness": richness,
        "modelling_evaluation_potential": modeling,
        "problem_realism": realism,
        "reportability": reportability,
        "novelty": novelty,
    }
    return int(round(weighted)), breakdown


def _why_text(task_type: str, feature_overview: str, target_col: str, score: int) -> str:
    return (
        f"Suitable for a full supervised pipeline with clear target `{target_col}`. "
        f"Data profile: {feature_overview}. "
        f"Supports robust EDA, leakage-safe preprocessing, baseline vs advanced model comparison, "
        f"and explainability/failure-mode analysis. Fit score: {score}/100."
    )


def _risk_text(df: pd.DataFrame, target_col: str, task_type: str) -> str:
    target = df[target_col]
    if task_type == "classification":
        counts = target.value_counts(dropna=False)
        if len(counts) > 1:
            ratio = counts.max() / max(counts.min(), 1)
            if ratio >= 3:
                return f"Class imbalance risk (max/min ratio {ratio:.2f}); use stratification and imbalance-aware metrics."
        return "Potential label noise and class boundary overlap; verify with confusion-matrix and subgroup error analysis."
    skew = target.dropna().skew() if pd.api.types.is_numeric_dtype(target) else 0.0
    if abs(float(skew)) > 1:
        return f"Target appears skewed (skew={float(skew):.2f}); consider robust losses or target transformation."
    return "Regression residual diagnostics and heteroscedasticity checks are required before deployment claims."


def _verify_candidate(
    kaggle_cmd: str,
    env: Dict[str, str],
    cwd: Path,
    cache_dir: Path,
    ref: str,
    title: str,
    source_search: str,
) -> Optional[Candidate]:
    safe_ref = ref.replace("/", "__")
    work = cache_dir / safe_ref
    work.mkdir(parents=True, exist_ok=True)

    download_cmd = [kaggle_cmd, "datasets", "download", "-d", ref, "-p", str(work), "--unzip", "-q"]
    download = _run(download_cmd, env=env, cwd=cwd)
    if download.returncode != 0:
        return None

    tabular_files = _find_tabular_files(work)
    if not tabular_files:
        return None

    for file in tabular_files:
        try:
            df = _load_frame(file)
        except Exception:
            continue
        rows = int(df.shape[0])
        if rows < MIN_ROWS or rows > MAX_ROWS:
            continue
        target_col = _guess_target_column(df)
        if not target_col or target_col not in df.columns:
            continue
        task_type = _infer_task_type(df[target_col], rows)
        feature_overview = _feature_overview(df, target_col)
        fit_score, breakdown = _score_candidate(df, target_col, task_type)
        why = _why_text(task_type, feature_overview, target_col, fit_score)
        risks = _risk_text(df, target_col, task_type)
        return Candidate(
            dataset_slug=ref,
            title=title,
            kaggle_url=f"https://www.kaggle.com/datasets/{ref}",
            source_search=source_search,
            task_type=task_type,
            verified_rows=rows,
            target_column=target_col,
            feature_overview=feature_overview,
            why_proper_for_coursework=why,
            risks_or_caveats=risks,
            fit_score=fit_score,
            score_breakdown=breakdown,
        )
    return None


def _select_top10(valid: List[Candidate]) -> List[Candidate]:
    classification = sorted(
        [c for c in valid if c.task_type == "classification"],
        key=lambda c: c.fit_score,
        reverse=True,
    )
    regression = sorted(
        [c for c in valid if c.task_type == "regression"],
        key=lambda c: c.fit_score,
        reverse=True,
    )

    selected = classification[:TARGET_CLASSIFICATION] + regression[:TARGET_REGRESSION]
    if len(selected) < TOP_N:
        leftovers = sorted(
            [c for c in valid if c not in selected],
            key=lambda c: c.fit_score,
            reverse=True,
        )
        selected.extend(leftovers[: TOP_N - len(selected)])

    selected = sorted(selected, key=lambda c: c.fit_score, reverse=True)[:TOP_N]
    return selected


def _write_csv(path: Path, rows: List[Candidate]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = []
    for idx, item in enumerate(rows, start=1):
        data.append(
            {
                "rank": idx,
                "dataset_slug": item.dataset_slug,
                "kaggle_url": item.kaggle_url,
                "task_type": item.task_type,
                "verified_rows": item.verified_rows,
                "target_column": item.target_column,
                "feature_overview": item.feature_overview,
                "why_proper_for_coursework": item.why_proper_for_coursework,
                "risks_or_caveats": item.risks_or_caveats,
                "fit_score": item.fit_score,
            }
        )
    pd.DataFrame(data).to_csv(path, index=False)


def _starter_prompt(item: Candidate) -> str:
    if item.task_type == "classification":
        return (
            f"Predict `{item.target_column}` for a stakeholder decision workflow, "
            f"optimize recall/precision trade-off, and document class-imbalance controls."
        )
    return (
        f"Predict `{item.target_column}` as a continuous outcome, benchmark baseline RMSE, "
        "and justify robust preprocessing + residual diagnostics."
    )


def _write_markdown(path: Path, rows: List[Candidate]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    class_count = sum(1 for r in rows if r.task_type == "classification")
    reg_count = sum(1 for r in rows if r.task_type == "regression")

    lines: List[str] = []
    lines.append("# Kaggle Top-10 Shortlist (10k-70k rows)")
    lines.append("")
    lines.append(f"- Composition: {class_count} classification, {reg_count} regression")
    lines.append("- Source: Kaggle (row counts locally verified)")
    lines.append("")
    lines.append("| Rank | Dataset | Task | Verified Rows | Target | Fit Score |")
    lines.append("|---:|---|---|---:|---|---:|")
    for i, item in enumerate(rows, start=1):
        lines.append(
            f"| {i} | [{item.dataset_slug}]({item.kaggle_url}) | {item.task_type} | "
            f"{item.verified_rows:,} | `{item.target_column}` | {item.fit_score} |"
        )
    lines.append("")
    lines.append("## Why Each Dataset Is Proper For This Project")
    lines.append("")
    for i, item in enumerate(rows, start=1):
        lines.append(f"### {i}. {item.dataset_slug}")
        lines.append(f"- **Why proper:** {item.why_proper_for_coursework}")
        lines.append(f"- **Project relevance:** {item.feature_overview}")
        lines.append(f"- **Risks/Caveats:** {item.risks_or_caveats}")
        lines.append("")

    lines.append("## Best 3 Starter Options")
    lines.append("")
    for i, item in enumerate(rows[:3], start=1):
        lines.append(f"{i}. **{item.dataset_slug}**: {_starter_prompt(item)}")

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Kaggle top-10 shortlist.")
    parser.add_argument(
        "--output-md",
        default="outputs/kaggle_shortlist_top10.md",
        help="Path to markdown shortlist output.",
    )
    parser.add_argument(
        "--output-csv",
        default="outputs/kaggle_shortlist_top10.csv",
        help="Path to CSV shortlist output.",
    )
    parser.add_argument(
        "--config-dir",
        default=".kaggle",
        help="Kaggle config directory (contains kaggle.json).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    cwd = Path.cwd()
    output_md = cwd / args.output_md
    output_csv = cwd / args.output_csv
    config_dir = (cwd / args.config_dir).resolve()
    config_dir.mkdir(parents=True, exist_ok=True)

    kaggle_cmd = _kaggle_bin()
    env = _kaggle_env(config_dir)

    if not _has_credentials(config_dir):
        print(
            "Missing Kaggle credentials.\n"
            f"Checked env vars and {config_dir / 'kaggle.json'}.\n"
            "Add credentials, then rerun:\n"
            "  mkdir -p .kaggle\n"
            "  cat > .kaggle/kaggle.json <<'JSON'\n"
            '  {"username":"<your_kaggle_username>","key":"<your_kaggle_key>"}\n'
            "  JSON\n"
            "  chmod 600 .kaggle/kaggle.json",
            file=sys.stderr,
        )
        return 2

    try:
        _validate_auth(kaggle_cmd, env, cwd)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 3

    candidates = _discover_candidates(kaggle_cmd, env, cwd)
    if not candidates:
        print("No candidates discovered from Kaggle list queries.", file=sys.stderr)
        return 4

    verified: List[Candidate] = []
    cache_dir = cwd / ".cache" / "kaggle_shortlist"
    cache_dir.mkdir(parents=True, exist_ok=True)

    for idx, item in enumerate(candidates, start=1):
        if idx > MAX_CANDIDATES_TO_VERIFY:
            break
        cand = _verify_candidate(
            kaggle_cmd=kaggle_cmd,
            env=env,
            cwd=cwd,
            cache_dir=cache_dir,
            ref=item["ref"],
            title=item["title"],
            source_search=item["search"],
        )
        if cand is not None:
            verified.append(cand)
        # Early stop once pool is sufficient to satisfy 7/3 composition.
        cls = sum(1 for c in verified if c.task_type == "classification")
        reg = sum(1 for c in verified if c.task_type == "regression")
        if cls >= 12 and reg >= 8:
            break

    if len(verified) < TOP_N:
        print(
            f"Only {len(verified)} verified candidates found in row range [{MIN_ROWS}, {MAX_ROWS}].",
            file=sys.stderr,
        )
        return 5

    selected = _select_top10(verified)
    _write_csv(output_csv, selected)
    _write_markdown(output_md, selected)

    print(f"Wrote: {output_md}")
    print(f"Wrote: {output_csv}")
    print(
        f"Selected {len(selected)} datasets "
        f"({sum(1 for s in selected if s.task_type == 'classification')} classification / "
        f"{sum(1 for s in selected if s.task_type == 'regression')} regression)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
