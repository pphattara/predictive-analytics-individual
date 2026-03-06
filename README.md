# MSIN0097 Predictive Analytics — Adult Census Income (Final)

This is the final marker-facing repository for the Adult Census Income coursework project.
The project predicts `income` (`>50K` vs `<=50K`) using one canonical notebook and reproducible saved artefacts.

## Quick Start (3 commands)

```bash
python3 -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
./scripts/run_submission_checks.sh
```

## Canonical Files

- Final report (submission file): `report_final.pdf`
- Canonical notebook: `notebooks/adult_census_income_final.ipynb`
- Final outputs folder: `outputs/adult_census_income/`
- Submission overview: `submission_manifest.md`

## Assessment Mapping (6 Coursework Steps)

| Coursework requirement | Evidence location |
|---|---|
| 1. Obtain dataset and frame problem | Notebook `## 1`, `outputs/adult_census_income/problem_statement.md`, report section `1. Introduction` |
| 2. Explore data | Notebook `## 2`, figures in `outputs/adult_census_income/figures/` |
| 3. Prepare data | Notebook `## 3`, `outputs/adult_census_income/metrics/preprocessing_validation.json` |
| 4. Explore models and shortlist | Notebook `## 4`, `metrics/model_comparison_cv.csv`, `metrics/ablation_results.csv` |
| 5. Fine-tune and evaluate | Notebook `## 5`, `metrics/evaluation_report.json`, `metrics/threshold_policy.json`, calibration/ROC/PR/confusion figures |
| 6. Present final solution | Notebook `## 6`, `metrics/final_solution_bundle.json`, model card in report |
| Agent usage + decision register | `outputs/adult_census_income/agent_log.md`, `outputs/adult_census_income/decision_register.pdf`, `outputs/adult_census_income/evidence/` |

## Repository Structure

```text
project-root/
├── README.md
├── requirements.txt
├── report_final.pdf
├── submission_manifest.md
├── notebooks/
│   └── adult_census_income_final.ipynb
├── data/
│   ├── raw/adult_census_income/adult.csv
│   └── processed/adult_census_income/
├── src/
├── tests/
├── scripts/
│   └── run_submission_checks.sh
└── outputs/
    └── adult_census_income/
```

## Data Access

- Dataset source: **UCI Adult Census Income**
- Expected filename: `adult.csv`
- Expected path: `data/raw/adult_census_income/adult.csv`
- Current package status: file included.
- If missing: download UCI Adult dataset and place it at the path above.

## Environment

```bash
python3 -m pip install -r requirements.txt
python3 --version
```

## Reproduction

```bash
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
python3 -u -m unittest tests/test_preprocessing.py tests/test_models.py tests/test_evaluation.py tests/test_pipeline_smoke.py -v
./scripts/run_submission_checks.sh
```

## Tests and Validation Meaning

- `tests/test_preprocessing.py`: split config, preprocessor contract, NaN/dimension checks.
- `tests/test_models.py`: baseline model factory and experiment record contract.
- `tests/test_evaluation.py`: classification/regression metric schema and ranges.
- `tests/test_pipeline_smoke.py`: artefact existence/schema + hygiene checks.

## Output Contract (Expected)

Core outputs:

- `outputs/adult_census_income/metrics/model_comparison_cv.csv`
- `outputs/adult_census_income/metrics/ablation_results.csv`
- `outputs/adult_census_income/metrics/evaluation_report.json`
- `outputs/adult_census_income/metrics/threshold_policy.json`
- `outputs/adult_census_income/metrics/final_solution_bundle.json`
- `outputs/adult_census_income/models/best_model_module2.pkl`
- `report_final.pdf` (canonical submission report at repo root)

Agent evidence outputs:

- `outputs/adult_census_income/agent_log.md`
- `outputs/adult_census_income/decision_register.pdf`
- `outputs/adult_census_income/evidence/`

Supporting report exports are archived under `outputs/adult_census_income/archive/report_exports/` and are not submission files.

## Reproducibility Notes

- Fixed random seed (`42`).
- Split-first preprocessing discipline.
- Test set single-touch after model/threshold freeze.
- Saved artefacts are generated from notebook execution.

## Agent Attribution

Notebook code cells are tagged with:

- `[Agent-generated]`
- `[Modified-from-agent]`
- `[Scratch-written]`

Caught agent mistake example:

- Accuracy-first recommendation was rejected for imbalance; final model selection uses weighted F1 + PR-AUC + recall + calibration.

## Troubleshooting

- Missing dataset: place `adult.csv` in `data/raw/adult_census_income/`.
- Kernel issues: recreate environment and rerun notebook from a clean kernel.
- Missing figures/metrics: rerun notebook, then run `./scripts/run_submission_checks.sh`.
