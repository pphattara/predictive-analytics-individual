# Predicting Annual Income with the Adult Census Dataset
## MSIN0097 Predictive Analytics — Individual Coursework

---

## 1. Introduction

Accurate income classification enables workforce policy analysts and HR teams to direct
interventions toward individuals most likely to benefit — those earning ≤$50K annually.
Without a reliable classifier, resource allocation relies on broad demographic assumptions
rather than evidence-based targeting. This project trains a binary classifier on the Adult
Census Income dataset (Kohavi, 1996; 32,561 records, 14 features, target: income ≤50K
vs >50K) to support that decision. The dataset is publicly representative but carries
known sampling and label bias; all outputs are intended as decision support, not automated
judgement.

Class imbalance is the dominant structural challenge: 24,720 records (75.9%) are ≤50K,
giving an imbalance ratio of 3.15:1 (Figure 1). Success criteria were fixed before
modelling: weighted F1 ≥ 0.82, positive-class recall ≥ 0.75, and calibrated
probabilities for threshold-based policy. The final tuned HistGradientBoosting classifier
achieves weighted F1 = 0.862 on the held-out test set — a 5.0% relative gain over the
logistic regression baseline (F1 = 0.821) — while meeting both the recall (0.784) and
calibration (ECE = 0.014) constraints.

---

## 2. Methodology

### EDA-Driven Decisions

EDA was structured to produce design decisions, not descriptive summaries. Numeric
distributions (Figure 2) revealed extreme right-skew in capital.gain and capital.loss:
91.7% and 95.3% of records respectively carry zero values, with long tails driven by
large asset transactions. This motivated RobustScaler over StandardScaler — a choice
stress-tested by ablation (Table 2: standard_scaler variant CV F1 = 0.8688 = reference,
confirming the tree is invariant to monotone scaling, but the conservative choice is
retained for pipeline consistency across family comparisons).

Missingness (Figure 3) is concentrated in occupation (5.66%), workclass (5.64%), and
native.country (1.79%). All three are Missing At Random: occupation and workclass
missingness correlates with self-employed and unemployed subcategories where census
responses are structurally unavailable. This ruled out row deletion — which would remove
5.6% of records and distort the class distribution — in favour of most-frequent
imputation within a training-only pipeline.

The leakage detection chart (Figure 4) confirmed no numeric feature carries point-biserial
correlation ≥ 0.9 against the target, ruling out proxy leakage. The correlation heatmap
(Figure 5) identified education.num and education as highly correlated, motivating an
ablation to test dropping the redundant text column. Bivariate distributions (Figure 6)
confirmed marital.status and capital.gain as the strongest class-separating features —
consistent with the permutation importance results (Figure 18). IQR outlier rates
(Figure 7) reached 27.7% for hours.per.week; Isolation Forest (Figure 8) flagged 3.0%
of records as anomalous. Both were retained after confirming no single outlier dominated
the target signal.

### Preprocessing Pipeline

Data was split 70/15/15 (train/val/test) with stratification on the target and
random_state=42, before any preprocessing was applied. A scikit-learn ColumnTransformer
applied median imputation and RobustScaling to six numeric features, and most-frequent
imputation with one-hot encoding (handle_unknown='ignore') to eight categorical features,
yielding 104 transformed features. Training-only fit was verified by three post-split
assertions: zero NaN values across all splits, consistent feature counts (104 across
train/val/test), and preserved class balance confirmed post-stratification.

### Model Selection Logic

Four families were compared to cover the linear-to-nonlinear spectrum and include a
modern architecture: Logistic Regression (linear, interpretable floor), Random Forest
(ensemble, variance reduction), HistGradientBoosting (native missing-value handling,
tabular scale), and MLPClassifier with 64×32 hidden layers and early stopping (modern
neural approach). All candidates used identical 5-fold stratified CV with fixed seed,
scoring weighted F1, ROC-AUC, AUC-PR, and positive-class recall.

### Ablation Design and Hyperparameter Tuning

Seven ablations tested one change at a time on the winning HistGradientBoosting family
(Table 2). Hypotheses: (1) education.num and education text are redundant — tested by
dropping each; (2) fnlwgt adds signal — tested by dropping it; (3) robust vs standard
scaling matters under tree structure; (4) capital features carry the dominant signal —
tested by removing both. Following ablation, the winning family underwent
RandomizedSearchCV over 20 candidate configurations with 3-fold CV. Search space:
learning_rate ∈ {0.03, 0.05, 0.08, 0.10, 0.15}, max_leaf_nodes ∈ {15, 31, 63, 127},
min_samples_leaf ∈ {10, 20, 40, 60}, l2_regularization ∈ {0.0, 0.01, 0.05, 0.1},
max_iter ∈ {200, 300, 400}. Best configuration: learning_rate=0.08, max_leaf_nodes=31,
min_samples_leaf=10, l2_regularization=0.1, max_iter=300 (CV F1 = 0.8691). Threshold
was then tuned on the validation split under the constraint recall_positive ≥ 0.75,
selecting 0.36 (validation F1 = 0.858, recall = 0.757). The test set was touched exactly
once after this freeze.

---

## 3. Results

### Model Comparison

**Table 1. Five-fold stratified CV results across all model families.**

| Model                  | CV F1 (mean ± std) | AUC-PR | ROC-AUC | CV Recall+ |
|------------------------|--------------------|--------|---------|------------|
| Majority baseline      | 0.655 —            | 0.241  | 0.500   | 0.000      |
| Logistic Regression    | 0.821 ± 0.005      | 0.766  | 0.907   | 0.851      |
| Random Forest          | 0.851 ± 0.008      | 0.766  | 0.904   | 0.618      |
| MLP (64×32)            | 0.851 ± 0.002      | 0.778  | 0.911   | 0.629      |
| HGB (untuned)          | 0.869 ± 0.003      | 0.827  | 0.927   | 0.657      |
| **HGB (tuned)**        | **0.869 ± 0.003**  |**0.830**|**0.929**| **0.661** |

HGB (tuned) leads on weighted F1, AUC-PR, and ROC-AUC (Figure 9). Logistic Regression
achieves the highest CV recall (0.851) but at the cost of weighted F1 — it operates near
a precision floor the tuned model clears with threshold selection. Random Forest and MLP
tie at 0.851, but Random Forest's higher standard deviation (0.008 vs 0.002) signals less
stable fold-to-fold generalisation.

### Ablation Findings

**Table 2. One-change-at-a-time ablation results on HistGradientBoosting.**

| Variant               | CV F1 (mean ± std) | Change vs reference |
|-----------------------|--------------------|---------------------|
| drop_education_text   | 0.8693 ± 0.0028    | +0.06pp             |
| reference             | 0.8688 ± 0.0028    | —                   |
| no_class_weight       | 0.8688 ± 0.0028    | 0.00pp              |
| standard_scaler       | 0.8688 ± 0.0028    | 0.00pp              |
| drop_fnlwgt           | 0.8681 ± 0.0031    | −0.07pp             |
| drop_education_num    | 0.8681 ± 0.0025    | −0.07pp             |
| **no_capital_features**| **0.8381 ± 0.0032**| **−3.08pp**       |

The dominant finding is the capital features ablation (Figure 10): removing capital.gain
and capital.loss collapses F1 by 3.1pp — confirming these sparse, right-skewed features
carry the strongest discriminative signal despite their extreme distributions. Dropping
the education text column (keeping education.num) marginally improves F1 (+0.06pp),
confirming the ordinal encoding subsumes the text label's information.

### Best Model Test Evaluation

Final evaluation on the held-out test set (n=4,885, untouched during training and tuning):

| Metric              | Value  | Success criterion |
|---------------------|--------|-------------------|
| Weighted F1         | 0.862  | ≥ 0.82 ✓          |
| AUC-PR              | 0.828  | —                 |
| ROC-AUC             | 0.926  | —                 |
| Recall (>50K)       | 0.784  | ≥ 0.75 ✓          |
| Precision (>50K)    | 0.679  | —                 |
| Calibration (ECE)   | 0.014  | Required ✓         |

The confusion matrix (Figure 12) shows 252 false negatives and 385 false positives at
threshold 0.36. The PR curve (Figure 13) confirms AUC-PR = 0.828; the ROC curve
(Figure 14) shows strong rank discrimination (AUC = 0.926). The calibration curve
(Figure 15) shows near-diagonal predicted probabilities (ECE = 0.014), confirming
probability outputs are reliable inputs to threshold-based policy decisions. Learning
curves (Figure 11) show train F1 decaying from 0.995 at 3,646 samples to 0.890 at 18,233,
while validation F1 plateaus at 0.869 by 14,586 samples — the converging gap confirms
the model is not data-limited at current training size.

### Failure Mode Analysis

Failure is not uniformly distributed. Figure 16 shows that Own-child relationship
(recall = 0.333, n = 736) and the 16–25 age band (recall = 0.364, n = 825) are
systematically under-recalled: the model misses two-thirds of true high-earners in
these groups. Figure 17 shows the highest overall error rates among Wife (31.8%, n = 239)
and Husband (24.8%, n = 1,998) relationship subgroups. Permutation importance (Figure 18)
confirms marital.status is the single most important feature (importance = 0.058 ± 0.004),
followed by capital.gain (0.051 ± 0.003). The model's reliance on household structure
creates a structural fairness risk for non-traditional households.

---

## 4. Discussion

### Limitations and Deployment Risks

The most immediate deployment risk is subgroup recall disparity. Young adults (16–25)
and dependents (Own-child) have recall rates below 0.40: the model misses 60% of
high-earners in these groups. Any deployment directing financial interventions would
systematically exclude them. Governance must include a subgroup recall floor — for example,
recall ≥ 0.60 for all subgroups with n ≥ 100 — with mandatory review when that floor
is breached.

Threshold sensitivity is a second operational risk. The stress test (Figure 19) shows
that a 0.05 shift from the operating threshold of 0.36 (to 0.31 or 0.41) changes recall
by approximately 4–5 percentage points — material for policy boundaries. Threshold 0.36
must be treated as a live operational parameter, not a fixed design constant, and reviewed
whenever class prevalence shifts materially.

Distribution shift is a latent risk. The Adult Census data reflects 1994 income
distributions; deployment against current workforce data will encounter shifted prevalence,
changed occupation categories, and altered capital gain distributions. Calibration error
(ECE = 0.014) provides a monitoring anchor: a statistically significant increase signals
covariate shift before it degrades top-line F1.

### Critical Reflection on Agent Tooling

Agent delegation accelerated the boilerplate phases — pipeline scaffolding, CV harness
construction, and figure generation — reliably and with minimal correction. The most
effective verification strategy was running CV metrics independently after each agent
suggestion before accepting: this caught the accuracy-first model-ranking error
immediately. Accuracy (≈ 0.820 for logistic regression) ranked the same as weighted F1
numerically but carried the wrong policy implication for an imbalanced dataset where the
positive class is the decision-relevant one. Catching this required reading the metric
definition, not just the number.

The most costly agent failure was the deployment recommendation: the agent suggested a
static threshold of 0.50 without considering the recall constraint or stress testing
under prevalence shifts. Fixing this required explicitly sweeping 61 thresholds (Figure 19)
and reading the policy implications of the precision-recall trade-off — work the agent
could not have directed without human framing. The key lesson is that agent outputs are
plausible starting points, not verified conclusions. Accepting scaffolding is appropriate;
accepting domain-level recommendations without validation is not.

### Next Steps

Three targeted improvements would reduce identified risks. First, collect additional
records from the 16–25 and Own-child subgroups — a targeted oversample of 2,000–3,000
records from these cohorts would directly address the recall gap without model architecture
changes. Second, implement a calibration monitoring pipeline that recomputes ECE weekly
against live predictions, triggering retraining when ECE exceeds 0.03. Third, test a
fairness-constrained post-processing variant (Equalized Odds) to quantify the precision
cost of enforcing recall parity across relationship and age subgroups before accepting
the current trade-off in production.

---

## 5. Model Card

**Model name:** HistGradientBoosting Classifier (tuned), Adult Census Income v4

**Intended use:** Decision support for workforce policy analysts identifying households
likely to earn ≤$50K annually. Outputs are probability scores and binary classifications
for resource allocation planning. Requires human review before any consequential action.

**Out-of-scope uses:** Automated high-stakes decisions (loan approval, hiring, benefits
eligibility) without human oversight. Not validated for populations outside the 1994 US
Census demographic profile. Not suitable if workforce composition has shifted materially
from the training distribution.

**Training data:** UCI Adult Census Income dataset (Kohavi, 1996). 32,561 records,
14 features, 1994 US Census. Known limitations: historical sampling bias, potential
label noise in income banding, underrepresentation of self-employed categories.

**Evaluation:** Test weighted F1 = 0.862, AUC-PR = 0.828, ROC-AUC = 0.926,
recall (>50K) = 0.784, calibration ECE = 0.014. Performance degrades for Own-child
relationship subgroup (recall = 0.333) and 16–25 age band (recall = 0.364).

**Ethical considerations:** marital.status is the highest-importance feature, which may
encode protected household structures. The model disproportionately misclassifies
non-traditional household members. Outputs must not be used to discriminate in employment,
credit, or benefits decisions.

**Caveats:** Threshold (0.36) must be reviewed if class prevalence shifts by more than
5 percentage points. Retrain required if weekly ECE exceeds 0.03. Not validated on
post-1994 data.
