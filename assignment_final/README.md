# Predictive Analytics Coursework Workspace

This package contains the final Adult Census Income submission for MSIN0097 Predictive Analytics.
The project predicts `income` (`>50K` vs `<=50K`) using a reproducible notebook-first workflow.
Canonical notebook: `notebooks/adult_census_income_final.ipynb`. Canonical report source:
`outputs/adult_census_income/report_final_iteration4.md`.

## Quick Start (3 Commands)

```bash
python3 -m pip install -r requirements.txt
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
./scripts/run_submission_checks.sh
```

## 1. Project Overview

- Task type: binary classification (`income` target, positive class `>50K`)
- Dataset: UCI Adult Census Income (`data/raw/adult_census_income/adult.csv`)
- Canonical notebook (single execution source): `notebooks/adult_census_income_final.ipynb`
- Canonical outputs folder: `outputs/adult_census_income/`
- Canonical report files:
  - `outputs/adult_census_income/report_final_iteration4.md`
  - `outputs/adult_census_income/report_final_iteration4.docx`
  - `outputs/adult_census_income/report_final_iteration4.pdf`

## 2. Assessment Mapping (6 Coursework Steps)

| Coursework requirement | Evidence location in this repo |
|---|---|
| Step 1: Obtain dataset and frame predictive problem | Notebook `## 1` (`1.1`, `1.2`), `outputs/adult_census_income/problem_statement.md`, report section `## 1. Introduction` |
| Step 2: Explore data to gain insights | Notebook `## 2.*`, EDA figures in `outputs/adult_census_income/figures/` (including leakage/missingness/outlier visuals) |
| Step 3: Prepare data | Notebook `## 3.*`, `outputs/adult_census_income/metrics/preprocessing_validation.json`, processed splits in `data/processed/adult_census_income/` |
| Step 4: Explore models and shortlist | Notebook `## 4.*`, `outputs/adult_census_income/metrics/model_comparison_cv.csv`, `outputs/adult_census_income/metrics/ablation_results.csv` |
| Step 5: Fine-tune and evaluate | Notebook `## 5.*`, `outputs/adult_census_income/metrics/evaluation_report.json`, `outputs/adult_census_income/metrics/threshold_policy.json`, evaluation figures under `outputs/adult_census_income/figures/module2/` and `outputs/adult_census_income/figures/module3/` |
| Step 6: Present final solution | Notebook `## 6.*`, `outputs/adult_census_income/metrics/final_solution_bundle.json`, report section `## 5. Model Card`, final report files (`.md/.docx/.pdf`) |
| Agent usage log + decision register | Notebook `### 6.3`, `### 6.4`, `### 6.5`; `outputs/adult_census_income/agent_log.md`, `outputs/adult_census_income/agent_log_detailed.docx`, `outputs/adult_census_income/agent_chat_screenshot.docx`, `outputs/adult_census_income/interaction_log_images/` |

## 3. Repository Structure

```text
assignment_final/
├── notebooks/
│   └── adult_census_income_final.ipynb
├── data/
│   ├── raw/adult_census_income/adult.csv
│   └── processed/adult_census_income/
├── outputs/
│   └── adult_census_income/
├── src/
├── tests/
├── scripts/
├── requirements.txt
└── README.md
```

## 4. Data Access

- Expected raw file: `data/raw/adult_census_income/adult.csv`
- This package currently includes `adult.csv` at that exact path.
- Source: UCI Adult Census Income dataset.
- If missing, re-download the UCI Adult Census Income dataset and place the CSV file as:
  `data/raw/adult_census_income/adult.csv`
- Processed files are written to: `data/processed/adult_census_income/`

## 5. Environment Setup

```bash
python3 -m pip install -r requirements.txt
python3 --version
```

## 6. Reproduction Steps

Primary portable notebook execution (no machine-specific kernel name):

```bash
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400
```

Optional fallback if your environment requires an explicit named kernel:

```bash
python3 -m ipykernel install --user --name msin0097
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_final.ipynb --inplace --ExecutePreprocessor.timeout=5400 --ExecutePreprocessor.kernel_name=msin0097
```

## 7. Tests and What They Validate

Run tests:

```bash
python3 -u -m unittest tests/test_preprocessing.py tests/test_models.py tests/test_evaluation.py tests/test_pipeline_smoke.py -v
```

Validation meaning by file:

- `tests/test_preprocessing.py`: checks split-config defaults, Adult preprocessor factory behavior, and transformed split NaN/dimension integrity assertions.
- `tests/test_models.py`: checks baseline model factory contracts and `ExperimentRecord` structure/immutability.
- `tests/test_evaluation.py`: checks classification/regression metric schema, required keys, and valid value ranges.
- `tests/test_pipeline_smoke.py`: checks required submission artifacts, JSON schema/range integrity, final bundle schema, and hygiene rules (no `.DS_Store`, no `~$*.docx` lock files).

Run one-command submission checks:

```bash
./scripts/run_submission_checks.sh
```

## 8. Output Contract / Expected Artefacts

Core metrics/models/report:

- `outputs/adult_census_income/metrics/model_comparison_cv.csv`
- `outputs/adult_census_income/metrics/ablation_results.csv`
- `outputs/adult_census_income/metrics/evaluation_report.json`
- `outputs/adult_census_income/metrics/threshold_policy.json`
- `outputs/adult_census_income/metrics/hyperparameter_tuning_summary.json`
- `outputs/adult_census_income/models/best_model_module2.pkl`
- `outputs/adult_census_income/report_final_iteration4.md`
- `outputs/adult_census_income/report_final_iteration4.docx`
- `outputs/adult_census_income/report_final_iteration4.pdf`

Iteration 5 robustness:

- `outputs/adult_census_income/metrics/repeated_cv_stability.csv`
- `outputs/adult_census_income/metrics/mlp_training_curve.csv`
- `outputs/adult_census_income/metrics/tuning_robustness_summary.json`
- `outputs/adult_census_income/metrics/final_solution_bundle.json`

Deep evaluation:

- `outputs/adult_census_income/metrics/module3_deep_evaluation.json`
- `outputs/adult_census_income/metrics/module3_failure_slices.csv`
- `outputs/adult_census_income/metrics/module3_permutation_importance.csv`
- `outputs/adult_census_income/metrics/module3_threshold_stress.csv`
- `outputs/adult_census_income/metrics/module3_worst_cases.csv`

Interaction evidence:

- `outputs/adult_census_income/agent_log.md`
- `outputs/adult_census_income/agent_log_detailed.docx`
- `outputs/adult_census_income/agent_chat_screenshot.docx`
- `outputs/adult_census_income/interaction_log_images/`
- `outputs/adult_census_income/evidence/agent_log_summary_final.pdf`
- `outputs/adult_census_income/evidence/agent_interaction_01.png`
- `outputs/adult_census_income/evidence/agent_interaction_02.png`

Reproducibility evidence:

- `outputs/adult_census_income/evidence/notebook_execution_log_final.txt`
- `outputs/adult_census_income/evidence/tests_log_final.txt`
- `outputs/adult_census_income/evidence/submission_checks_log_final.txt`
- `outputs/adult_census_income/evidence/clean_room_install_attempt_final.txt`
- `outputs/adult_census_income/evidence/notebook_completed_final.png`
- `outputs/adult_census_income/evidence/tests_passed_final.png`
- `outputs/adult_census_income/evidence/submission_checks_passed_final.png`

This inventory is aligned with:
`outputs/adult_census_income/submission_manifest.md`.

## 9. How to Verify Successful Reproduction

A successful reproduction should:

- execute `notebooks/adult_census_income_final.ipynb` end-to-end without manual edits,
- pass all unit and smoke tests,
- return success (`exit 0`) for `./scripts/run_submission_checks.sh`,
- produce the required artifacts above as non-empty files,
- show final selected threshold and test metrics in
  `outputs/adult_census_income/metrics/evaluation_report.json`.

## 10. Reproducibility Notes

- Fixed random seed (`42`) is used across split/modeling workflow.
- Split-first discipline is enforced before preprocessing transformations.
- Test set is single-touch after model and threshold freeze.
- Reported artifacts are generated through notebook execution and saved outputs.

## 11. Agent-Use and Attribution

Notebook code cells include one of:

- `[Agent-generated]`
- `[Modified-from-agent]`
- `[Scratch-written]`

Agent-use evidence locators:

- Notebook sections `### 6.3`, `### 6.4`, `### 6.5`
- `outputs/adult_census_income/agent_log.md`
- `outputs/adult_census_income/agent_log_detailed.docx`
- `outputs/adult_census_income/agent_chat_screenshot.docx`
- `outputs/adult_census_income/interaction_log_images/`

Caught agent mistake example:

- An accuracy-first ranking suggestion was rejected for this imbalanced task and replaced by weighted F1 + PR-AUC + recall + calibration criteria.

## 12. Troubleshooting

- Missing data file: place `adult.csv` at `data/raw/adult_census_income/adult.csv`.
- Kernel mismatch: use the optional named-kernel setup in Section 6.
- Missing figures/artifacts: re-run notebook from a clean kernel, then run submission checks.
- Failing tests: run `./scripts/run_submission_checks.sh` first, then inspect failing test module output.
