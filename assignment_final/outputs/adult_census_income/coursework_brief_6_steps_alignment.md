# Coursework Brief (End-to-End Steps) Alignment

This file follows the exact six headings from the coursework brief and maps each to completed evidence in this repo.

## 1. Obtain a dataset and frame the predictive problem
- Dataset chosen: Adult Census Income (`data/raw/adult_census_income/adult.csv`).
- Prediction type: binary classification (`income`: `>50K` vs `<=50K`).
- Success metrics and constraints defined in `outputs/adult_census_income/problem_statement.md`:
  - weighted F1 target >= 0.82
  - positive-class recall >= 0.75
  - calibration-readiness for threshold policy
  - interpretability and fairness-sensitive review constraints
- Assumptions and limitations documented in problem statement and deployment-risk note.
- Agent tooling expectation satisfied:
  - plan + verification split documented in `outputs/adult_census_income/agent_log.md`.

## 2. Explore the data to gain insights
- Concise visual EDA completed in notebook and exported:
  - `target_distribution.png`
  - `numeric_distributions.png`
  - `categorical_cardinality.png`
  - `missingness_summary.png`
  - `feature_target_checks.png`
- Insights addressed distributions, missingness, class imbalance, outlier-heavy numeric fields, and potential pitfalls.
- Data quality/pitfalls identified and converted into preprocessing actions in notebook markdown (“insight -> preprocessing action”).
- Agent tooling expectation satisfied:
  - EDA outputs were validated and corrected against direct data checks.

## 3. Prepare the data
- Reproducible split-first preprocessing pipeline implemented:
  - 70/15/15 stratified split, `random_state=42`
  - numeric: median imputation + robust scaling
  - categorical: most-frequent imputation + unknown-safe one-hot
- Validation checks completed and saved (`preprocessing_validation.json`):
  - no NaN after transformation: train=True, val=True, test=True
  - feature dimensional consistency: 104 / 104 / 104
  - split discipline and class-balance preservation verified
- Agent tooling expectation satisfied:
  - suggested preprocessing steps were documented and verified before acceptance.

## 4. Explore different models and shortlist the best ones
- Baseline established: Dummy + Logistic baseline.
- Multiple model families compared with 5-fold stratified CV:
  - Logistic Regression
  - Random Forest
  - HistGradientBoosting
  - MLPClassifier (modern approach)
- Evidence-based shortlisting outputs:
  - `model_comparison_cv.csv`
  - `ablation_results.csv`
- Choice justification uses CV mean/std + ablation evidence, not single-run results.
- Agent tooling expectation satisfied:
  - model and pipeline suggestions were experimentally verified.

## 5. Fine-tune and evaluate
- Tuning strategy applied:
  - CV-based model selection
  - explicit threshold tuning on validation set
- Robust evaluation completed:
  - confusion matrix, PR curve, ROC curve, calibration curve (`outputs/adult_census_income/figures/module2/`)
  - failure slices + worst cases (`module3_failure_slices.csv`, `module3_worst_cases.csv`)
  - threshold stress testing (`module3_threshold_stress.csv`)
  - interpretability via permutation importance (`module3_permutation_importance.csv`)
- Final test metrics at selected threshold 0.36:
  - weighted F1=0.8622
  - PR-AUC=0.8282
  - ROC-AUC=0.9259
  - recall-positive=0.7840
  - calibration error=0.0139
- Agent tooling expectation satisfied (explicit caught mistake):
  - corrected agent-led emphasis on raw accuracy by enforcing imbalance-aware metrics and threshold policy analysis.

## 6. Present the final solution
- Final model selection and rationale documented in:
  - `threshold_policy.json`
  - `evaluation_report.json`
- Limitations, risks, and next steps documented in:
  - `outputs/adult_census_income/module3_deployment_risk.md`
- Model-card style summary available in report draft (`report_sections_draft.md`):
  - intended use / out-of-scope use
  - data provenance and constraints
  - evaluation summary and caveats
- Agent decision appendix maintained in:
  - `outputs/adult_census_income/agent_log.md`

## Submission-Ready Note
Use this six-step structure as the spine of your final report and keep these exact headings in your notebook/report to match brief expectations.
