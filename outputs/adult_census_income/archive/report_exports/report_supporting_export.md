# Predicting Annual Income with the Adult Census Dataset
## MSIN0097 Predictive Analytics — Individual Coursework

---

## 1. Introduction

This project predicts whether an individual earns `>50K` per year using the Adult Census
Income dataset. The intended stakeholder is a workforce policy or HR analytics team that
needs **priority ranking** rather than a perfect deterministic rule. A binary classifier is
appropriate because the operational decision is whether an individual likely belongs in a
higher-income segment, not exact income estimation.

The dataset contains 32,561 records and 14 predictors (Kohavi, 1996; Dua and Graff, 2019).
The target is imbalanced: 75.9% `<=50K` and 24.1% `>50K` (Figure 1), so raw accuracy is not a
safe primary metric. Before any modelling, success criteria were fixed as:

- weighted F1 `>= 0.82`
- positive-class recall (`>50K`) `>= 0.75`
- calibration quality suitable for threshold-based policy decisions

The final model is a tuned HistGradientBoosting classifier with operating threshold `0.36`.
On the untouched test set, it achieves weighted F1 `0.862`, recall `0.784`, PR-AUC `0.828`,
ROC-AUC `0.926`, and calibration error (ECE) `0.014`. Relative to the logistic baseline,
this is a +0.041 absolute F1 gain, or approximately +5.0% relative improvement.

This report follows the coursework six-step structure and documents both model evidence and
agent-assisted decision verification.

---

## 2. Methodology

### 2.1 EDA-driven design decisions

EDA was run to drive decisions, not just describe data.

Numeric distributions (Figure 2) show extreme right-skew in `capital.gain` and
`capital.loss` with dominant zero mass and long positive tails. This motivated robust,
leak-safe preprocessing and explicit outlier diagnostics.

Missingness is concentrated in `occupation` (5.66%), `workclass` (5.64%), and
`native.country` (1.79%) (Figure 3). Figure 20 adds a mechanism classification map
(MCAR/MAR/MNAR heuristic labels) and makes the caveat explicit: the labels are practical
working assumptions, not proven causal mechanisms. The implication remains the same:
row deletion is riskier than imputation because it removes signal and may amplify class/slice
imbalance.

Leakage checks were made explicit. Figure 4 shows no numeric feature with absolute
point-biserial correlation near the 0.9 suspicion threshold. Figure 5 (correlation heatmap)
highlights redundancy between `education` and `education.num`, later tested via ablation.
Figure 6 confirms separation signal for features linked to household structure and capital,
while Figures 7-8 show outlier concentration without a single dominant leakage-like feature.
The IQR plot (Figure 7) indicates high rates for `hours.per.week`, but the Isolation Forest
scatter (Figure 8) confirms these points are distributed rather than concentrated into a
single pathological subgroup. That finding supported retaining outliers and handling them
through robust preprocessing plus downstream threshold stress testing, rather than hard
trimming rules that could disproportionately remove minority slices.

To satisfy the visual-verification requirement, Figure 21 documents one explicit agent-plot
correction: a raw-missing-count chart was replaced with normalized percentages because raw
counts can mis-prioritize columns. This correction was retained as evidence of human review,
not silently overwritten.

### 2.2 Data preparation and leakage discipline

Data was split **before** preprocessing using stratified 70/15/15 with `random_state=42`.
All transformers were fit only on training data. The preprocessing pipeline uses:

- numeric: median imputation + `RobustScaler`
- categorical: most-frequent imputation + one-hot encoding (`handle_unknown='ignore'`)

Post-transform assertions verified:

- no NaN values in train/val/test transformed matrices
- consistent feature dimensions across all splits
- preserved class balance after stratification

This split-first discipline, together with pipeline encapsulation, prevents target leakage and
keeps CV/test estimates trustworthy.

### 2.3 Model shortlist, ablation, and tuning protocol

The shortlist intentionally spans linear, tree-ensemble, and neural families:

- Logistic Regression (interpretable linear floor)
- Random Forest
- HistGradientBoosting
- MLPClassifier (64x32, early stopping)

A majority baseline (`DummyClassifier`) establishes the minimum bar.
All candidates were evaluated with `StratifiedKFold(n_splits=5, shuffle=True,
random_state=42)` and consistent scoring (`f1_weighted`, PR-AUC, ROC-AUC,
positive recall).

Ablation design used one-change-at-a-time variants on the winning family:
class-weight removal, scaler swap, `fnlwgt` drop, education-field redundancy checks,
and capital-feature removal.

Hyperparameter tuning used `RandomizedSearchCV` on HistGradientBoosting
(20 draws, 3-fold CV), with explicit search space and persisted best parameters.
This is not exhaustive global optimization, but it is principled and reproducible.

### 2.4 Fine-tuning and robustness checks

Threshold tuning was performed on validation data only under recall constraint
(`recall_positive >= 0.75`), then frozen at `0.36`.

Iteration 5 added two robustness upgrades:

- Figure 22: MLP training dynamics (loss/validation trajectories) to show convergence
  behaviour for the modern baseline
- Figure 23 + `repeated_cv_stability.csv`: repeated CV stability check using
  `RepeatedStratifiedKFold(5x3)` on the selected pipeline

The repeated-CV mean remains close to the base CV mean, supporting that model ranking was
not a single-split artifact.

---

## 3. Results

### 3.1 Cross-validated model comparison

**Table 1. Five-fold stratified CV results across shortlisted families**

| Model                  | CV F1 (mean ± std) | AUC-PR | ROC-AUC | Recall+ |
|------------------------|--------------------|--------|---------|---------|
| Majority baseline      | 0.655 —            | 0.241  | 0.500   | 0.000   |
| Logistic Regression    | 0.821 ± 0.005      | 0.766  | 0.907   | 0.851   |
| Random Forest          | 0.851 ± 0.008      | 0.766  | 0.904   | 0.618   |
| MLP (64x32)            | 0.851 ± 0.002      | 0.778  | 0.911   | 0.629   |
| HGB (untuned)          | 0.869 ± 0.003      | 0.827  | 0.927   | 0.657   |
| **HGB (tuned)**        | **0.869 ± 0.003**  |**0.830**|**0.929**| **0.661** |

The tuned HGB remains first on weighted F1 and ranking metrics (Figure 9). Improvement over
untuned HGB is intentionally reported as **small** (about +0.0007 F1 in the saved run):
tuning was justified as robustness and reproducibility evidence, not a dramatic uplift claim.

### 3.2 Ablation evidence

**Table 2. One-change-at-a-time ablations on HistGradientBoosting**

| Variant                 | CV F1 (mean ± std) | Change vs reference |
|-------------------------|--------------------|---------------------|
| drop_education_text     | 0.8693 ± 0.0028    | +0.06pp             |
| reference               | 0.8688 ± 0.0028    | —                   |
| no_class_weight         | 0.8688 ± 0.0028    | 0.00pp              |
| standard_scaler         | 0.8688 ± 0.0028    | 0.00pp              |
| drop_fnlwgt             | 0.8681 ± 0.0031    | −0.07pp             |
| drop_education_num      | 0.8681 ± 0.0025    | −0.07pp             |
| **no_capital_features** | **0.8381 ± 0.0032**| **−3.08pp**         |

The largest movement is capital-feature removal (Figure 10), confirming that sparse capital
signals are central to discrimination despite heavy skew and zero inflation.

### 3.3 Final test performance (single-touch)

Final evaluation was performed once on held-out test data after model and threshold freeze.

| Metric                | Value | Criterion |
|-----------------------|-------|-----------|
| Weighted F1           | 0.862 | >= 0.82 ✅ |
| PR-AUC                | 0.828 | —         |
| ROC-AUC               | 0.926 | —         |
| Recall (`>50K`)       | 0.784 | >= 0.75 ✅ |
| Precision (`>50K`)    | 0.679 | —         |
| Calibration (ECE)     | 0.014 | Required ✅ |

Figure 11 (learning curve) shows validation F1 flattening as sample size grows, which
suggests limited benefit from additional data under current feature set unless data quality
changes. Figure 12 (normalized confusion matrix) makes the error trade-off explicit at the
chosen threshold. Figure 13 (PR curve) shows strong positive-class ranking where precision
must be controlled under intervention budgets. Figure 14 (ROC curve) confirms high global
discrimination performance, which matters because prevalence can shift across cohorts.
Figure 15 confirms that predicted probabilities remain close to observed frequencies, so
score-based triage rules are more defensible than hard class labels alone.

Taken together, Figures 11-15 justify the final operating decision: the model is not
selected only because of F1, but because it jointly satisfies ranking quality, calibration,
and recall constraints under a clearly stated threshold policy.

### 3.4 Error and failure-mode analysis

Error is heterogeneous by subgroup. Figure 16 shows low recall in `Own-child` and younger
age-band slices. Figure 17 shows elevated error rates for selected relationship groups.
Figure 18 confirms model dependence on `marital.status` and capital features, creating a
plausible fairness and transferability risk.

Threshold sensitivity (Figure 19) shows that ±0.05 around `0.36` shifts recall by
approximately 4-5 percentage points, so threshold is an operational control, not a static
constant.

---

## 4. Discussion

### 4.1 What is strong

The pipeline is statistically disciplined (split-first, no leakage, test single-touch),
methodologically broad (baseline + multiple families + ablations), and operationally grounded
(calibration + threshold policy + subgroup diagnostics). This combination supports decision
support use better than leaderboard-only tuning.

### 4.2 Limitations

1. **Dataset age and shift risk:** Adult Census reflects 1994 distributions. Workforce
   composition and income structure have changed, so external validity is limited.
2. **Subgroup recall disparity:** some slices remain under-recalled, which is material for
   intervention or triage use cases.
3. **Feature semantics risk:** high-importance household-structure features may encode
   social structure effects that do not transfer safely across contexts.
4. **Tuning uplift magnitude:** hyperparameter tuning improved stability more than headline
   performance; this is honest but limits raw performance gains.

### 4.3 Verification strategies: what worked, what failed, why

This section captures metacognitive verification rather than a task log.

**Worked well (accepted):**
- CV scaffold and fixed-seed protocol suggestions were fast to validate and low-risk.
  Re-running CV reproduced metric bands closely, so these were accepted with minimal friction.

**Worked with modification (modified):**
- Missingness handling: an agent suggestion to drop missing rows was modified after checking
  that deletion would remove ~5.6% of records and distort class balance.
- Interpretability tooling: SHAP-first suggestion was replaced by permutation importance to
  stay within dependency constraints while preserving global feature diagnostics.

**Failed and required rejection (rejected):**
- Accuracy-first ranking on imbalanced data was rejected because it obscured positive-class
  recovery trade-offs.
- Static-threshold recommendation without stress testing was rejected; threshold sweep evidence
  showed material policy sensitivity.

The key pattern: agent output is efficient for scaffolding and boilerplate, but analytical
claims require explicit empirical verification before adoption.

### 4.4 Next steps

- Add subgroup-aware monitoring with hard governance floors (for example, minimum recall
  thresholds for slices above a minimum sample size).
- Recalibrate and re-threshold on newer data snapshots to mitigate temporal shift.
- Evaluate fairness-constrained post-processing and compare precision cost explicitly.

### 4.5 Operational guardrails before deployment

If this model were transitioned beyond coursework, three guardrails would be mandatory.
First, a monitoring dashboard should track weighted F1, recall (`>50K`), and ECE at a fixed
cadence, with explicit alert thresholds and a documented owner for intervention. Second,
subgroup monitoring should use both minimum sample-size rules and confidence intervals to
avoid over-reacting to noise in very small slices. Third, any threshold revision should be
logged as a policy change with pre/post impact simulation, not performed ad hoc by
individual analysts. These controls are simple but materially reduce the risk that a stable
offline model drifts into unsafe behavior in live use.

---

## 5. Model Card

**Model**: HistGradientBoosting Classifier (tuned) + threshold policy `0.36`  
**Intended use**: decision support for workforce/HR prioritization  
**Not for**: fully automated high-stakes decisions (hiring, credit, benefits)

**Data provenance**: UCI Adult Census Income, 32,561 rows, 14 features, historical US census
sample (Kohavi, 1996; Dua and Graff, 2019).

**Evaluation summary (test set)**:
- F1 weighted: 0.862
- PR-AUC: 0.828
- ROC-AUC: 0.926
- Recall (`>50K`): 0.784
- Calibration error (ECE): 0.014

**Caveats**:
- Under-recall in specific age/relationship slices.
- Threshold sensitivity around operational point.
- Temporal transferability risk due to dataset vintage.

---

## 6. References

Bergstra, J. and Bengio, Y. (2012) 'Random search for hyper-parameter optimization',
*Journal of Machine Learning Research*, 13(10), pp. 281-305.

Dua, D. and Graff, C. (2019) *UCI Machine Learning Repository*. Irvine, CA: University of
California, School of Information and Computer Science. Available at:
https://archive.ics.uci.edu (Accessed: 4 March 2026).

Kohavi, R. (1996) 'Scaling up the accuracy of Naive-Bayes classifiers: A decision-tree
hybrid'. In: *Proceedings of the Second International Conference on Knowledge Discovery and
Data Mining (KDD-96)*. Portland, OR: AAAI Press, pp. 202-207.

Pedregosa, F. *et al.* (2011) 'Scikit-learn: Machine Learning in Python', *Journal of
Machine Learning Research*, 12, pp. 2825-2830.
