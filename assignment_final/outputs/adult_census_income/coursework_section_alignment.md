# Coursework Section Alignment (Adult Census Income)

This document aligns our Iteration 1 analysis to the coursework brief sections discovered in `MSIN0097_ Predictive Analytics 25-26 Individual Coursework.pdf`.

## Section A: Core Information
- Module: MSIN0097 Predictive Analytics (Individual Coursework)
- Active project: Adult Census Income classification (`income`: `>50K` vs `<=50K`)
- Evidence files:
  - `notebooks/adult_census_income_analysis.ipynb`
  - `outputs/adult_census_income/problem_statement.md`
  - `outputs/adult_census_income/agent_log.md`

## Section B: Coursework Brief and Requirements

### Overview
- We completed an end-to-end workflow across Module 1-3:
  - Module 1: Framing + EDA + preprocessing
  - Module 2: Modelling + core evaluation
  - Module 3: Deep evaluation + interpretability + deployment risk

### Required Methods (Course Alignment)
- Framing: Completed (`problem_statement.md`).
- EDA: Completed with saved visuals (`outputs/adult_census_income/figures/`).
- Split-first preprocessing: Completed and validated.
  - Split sizes: train=22792, val=4884, test=4885
  - Post-transform NaN checks: train=True, val=True, test=True
- Systematic modelling + CV + ablations: Completed.
  - Model comparison: `model_comparison_cv.csv`
  - Ablations: `ablation_results.csv`
- Evaluation and error analysis: Completed.
  - Core metrics and curves: `evaluation_report.json`, `figures/module2/`
  - Failure slices + worst cases: `module3_failure_slices.csv`, `module3_worst_cases.csv`
- Interpretability: Completed with permutation importance (`module3_permutation_importance.csv`).
- Threshold policy and stress test: Completed (`threshold_policy.json`, `module3_threshold_stress.csv`).

### Required Artefacts (What You Must Submit)
- Notebook analysis: Complete (`notebooks/adult_census_income_analysis.ipynb`).
- Outputs (figures/metrics/models): Complete under `outputs/adult_census_income/`.
- Agent decision register/log: Complete and updated through Module 3.
- Code modularity: Present in `src/` and `scripts/`.

### Suggested Project Format (2000-word report)
- We mapped your results into the required sections in:
  - `outputs/adult_census_income/report_sections_draft.md`

### Coursework Brief (End-to-End Steps)
- Dataset selection and framing: Done.
- EDA and preprocessing rationale: Done.
- Modelling, ablation, selection, and final evaluation: Done.
- Risk-aware deployment discussion: Done.

### Agent Tooling: Allowed, Expected, and Documentation
- Agent usage log includes accepted/modified/rejected decisions.
- Module 2 and Module 3 entries document corrections and verification decisions.

## Section C: Module Learning Outcomes Coverage
- Data understanding and preparation: demonstrated.
- Predictive modelling and selection: demonstrated.
- Evaluation, interpretation, and critical reflection: demonstrated.
- Communication of evidence-based findings: ready for final report drafting.

## Section D: Assessment Criteria Fit (Rubric-Oriented)
- EDA quality: strong (decision-linked visuals).
- Methodology rigor: strong (split-first, CV, ablations, threshold policy).
- Evaluation depth: strong (core metrics + slices + interpretability + stress tests).
- Reproducibility/documentation: good (artifacts saved), but can still improve with environment pinning file.

## Section E: Groupwork Instructions
- Not applicable (individual coursework).

## Section F: Additional Information
- Submission-safe recommendation: keep this alignment file and the report draft alongside the notebook for final assembly.

## Remaining Gaps Before Final Submission
1. Final polished 2000-word narrative with citations and figure callouts.
2. Pinned dependency file (`requirements.txt` or `environment.yml`) if required by marker expectations.
3. Final proofreading against word-count and reference policy in the brief.

## Canonical Final Metric Snapshot
- Threshold: **0.3600**
- Test weighted F1: **0.8622**
- Test PR-AUC: **0.8282**
- Test ROC-AUC: **0.9259**
- Test recall (`>50K`): **0.7840**
- Test calibration error (ECE): **0.0139**
