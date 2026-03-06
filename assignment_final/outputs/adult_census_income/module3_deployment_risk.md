# Module 3 Deployment Risk Statement

## Model Context
- Dataset: Adult Census Income
- Model family: tree_hgb_tuned
- Operating threshold: 0.36

## Key Risks Identified
1. **Subgroup disparity risk**: Some slices show lower positive-class recall, meaning the model can miss true `>50K` cases disproportionately.
2. **Threshold sensitivity risk**: Small threshold changes shift precision/recall materially; policy outcomes can drift without re-tuning.
3. **Distribution shift risk**: If applicant/workforce composition changes, current calibration and slice performance may no longer hold.

## Do-Not-Use Conditions
- Do not use for fully automated high-stakes decisions without human review.
- Do not use if monitored subgroup recall drops below governance limits.
- Do not use unchanged when prevalence shifts materially from training/test conditions.

## Monitoring Recommendations
- Track weekly: weighted F1, positive recall, calibration error, and subgroup recall.
- Trigger retraining/re-thresholding when subgroup recall or calibration degrades beyond policy tolerance.

## Lowest-Recall Slices (Current Test Snapshot)
```text
   group_col group_value  count  recall_positive
relationship   Own-child    736         0.333333
    age_band    [16, 25)    825         0.363636
relationship   Unmarried    508         0.432432
  hours_band     [0, 20)    256         0.500000
  hours_band    [20, 35)    565         0.500000
```

## Highest-Error Slices (Current Test Snapshot)
```text
   group_col      group_value  count  error_rate
relationship             Wife    239    0.317992
relationship          Husband   1998    0.247748
  hours_band        [60, 100)    382    0.222513
   workclass Self-emp-not-inc    388    0.213918
    age_band         [45, 55)    839    0.201430
```
