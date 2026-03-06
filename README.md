# Predictive Analytics Coursework Workspace

This repository contains the Adult Census Income project for MSIN0097 Predictive Analytics, structured around the six coursework end-to-end steps.

## Canonical Notebook

- Active/canonical notebook: `notebooks/adult_census_income_iteration4_six_steps.ipynb`
- Previous version (legacy): `notebooks/adult_census_income_iteration3_six_steps.ipynb`

## Data Access

- Raw dataset expected at: `data/raw/adult_census_income/adult.csv`
- Processed outputs are written to: `data/processed/adult_census_income/`
- Main artefacts are written to: `outputs/adult_census_income/`

## Environment Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run Instructions

### Execute canonical notebook end-to-end

```bash
jupyter nbconvert --to notebook --execute notebooks/adult_census_income_iteration4_six_steps.ipynb --inplace --ExecutePreprocessor.timeout=5400 --ExecutePreprocessor.kernel_name=vscode-env
```

### Run existing tests

```bash
python3 -u -m unittest tests/test_skill_router.py tests/test_kaggle_shortlist.py tests/test_blueprints_contract.py -v
```

## Output Contract (Adult)

After notebook execution, key files should exist:

- `outputs/adult_census_income/metrics/model_comparison_cv.csv`
- `outputs/adult_census_income/metrics/ablation_results.csv`
- `outputs/adult_census_income/metrics/evaluation_report.json`
- `outputs/adult_census_income/metrics/hyperparameter_tuning_summary.json`
- `outputs/adult_census_income/metrics/module3_deep_evaluation.json`
- `outputs/adult_census_income/models/best_model_module2.pkl`
- `outputs/adult_census_income/figures/module2/*.png`
- `outputs/adult_census_income/figures/module3/*.png`
- `outputs/adult_census_income/report_final_iteration4.pdf`

## Attribution Policy

Notebook code cells include one of these tags:

- `[Agent-generated]`
- `[Modified-from-agent]`
- `[Scratch-written]`

Current Iteration 4 notebook is tagged with explicit attribution comments in each code cell header.

## Notes

- Do not commit secrets/credentials.
- If notebook kernel name differs locally, adjust `--ExecutePreprocessor.kernel_name` accordingly.
