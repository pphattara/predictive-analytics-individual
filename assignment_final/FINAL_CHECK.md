# FINAL_CHECK — Submission Checklist Completion

Date verified: 2026-03-06
Scope: `assignment_final/`

## A. Must-fix before submission

### 1) Single canonical final package
- [x] One final report filename only: `outputs/adult_census_income/report_final_iteration4.pdf` (with matching `.md` and `.docx` source/export)
- [x] One canonical notebook only: `notebooks/adult_census_income_final.ipynb`
- [x] One final outputs folder only: `outputs/adult_census_income/`
- [x] Stale duplicate versions archived to `archive/`
- [x] README points to canonical names
- [x] Report/notebook/outputs/manifest naming aligned

### 2) README-to-repo truth check
- [x] Referenced files verified as existing and non-empty
- [x] `tests/` contains listed test files
- [x] `scripts/run_submission_checks.sh` exists and works
- [x] Output contract artefacts exist
- [x] Interaction evidence exists as named
- [x] `submission_manifest.md` exists and matches package
- [x] Evidence: `outputs/adult_census_income/evidence/readme_truth_check_final.json`

### 3) Clean-room reproducibility run
- [x] Dependencies and Python version command documented in README
- [x] Fresh-venv install attempted; blocked by network/package index access in this environment (evidence log saved)
- [x] Dataset present at expected path: `data/raw/adult_census_income/adult.csv`
- [x] Canonical notebook run command executed successfully
- [x] Unit tests executed successfully
- [x] Submission checks executed successfully
- [x] Final artefacts regenerated and validated
- [x] Saved proof logs:
  - `outputs/adult_census_income/evidence/notebook_execution_log_final.txt`
  - `outputs/adult_census_income/evidence/tests_log_final.txt`
  - `outputs/adult_census_income/evidence/submission_checks_log_final.txt`
  - `outputs/adult_census_income/evidence/clean_room_install_attempt_final.txt`
  - `outputs/adult_census_income/evidence/notebook_completed_final.png`
  - `outputs/adult_census_income/evidence/tests_passed_final.png`
  - `outputs/adult_census_income/evidence/submission_checks_passed_final.png`

### 4) Agent-use evidence package
- [x] Appendix decision table retained (`agent_log.md` + detailed `.docx`)
- [x] Accepted/Modified/Rejected decisions clearly visible
- [x] Explicit caught agent mistake included
- [x] Interaction evidence easy to open
- [x] PNG evidence available (not only inside DOCX)
- [x] Clean evidence filenames added:
  - `outputs/adult_census_income/evidence/agent_log_summary_final.pdf`
  - `outputs/adult_census_income/evidence/agent_interaction_01.png`
  - `outputs/adult_census_income/evidence/agent_interaction_02.png`
- [x] README points directly to evidence paths
- [x] No secrets found in evidence files

### 5) Fix known report errors
- [x] `4What is strong` issue not present
- [x] Figure numbering sequential (1-23)
- [x] Table numbering sequential (1-2)
- [x] Headings consistent
- [x] No stray symbols detected by quality check
- [x] Evidence: `outputs/adult_census_income/evidence/report_quality_check_final.json`

## B. Strongly recommended fixes

### 6) Notebook visibly matches six coursework steps
- [x] Step 1..6 headings present in canonical notebook
- [x] Decision markdown present per step
- [x] Notebook structure aligned with README mapping
- [x] Saved outputs are present (execution counts validated)
- [x] Final solution/model card linkage present
- [x] Agent attribution tags present

### 7) Tighten data access instructions
- [x] Dataset source explicitly named: UCI Adult Census Income
- [x] Expected filename provided: `adult.csv`
- [x] Expected path provided
- [x] Included-in-package status stated
- [x] Missing-file fallback documented
- [x] Report/README provenance aligned

### 8) Reproducibility notes verified by artefacts
- [x] Split-first preprocessing supported by notebook + validation JSON
- [x] Single-touch test evaluation claim supported by workflow
- [x] Threshold policy matches report and JSON
- [x] Repeated-CV output exists
- [x] Calibration outputs exist
- [x] Ablation outputs exist
- [x] Failure-slice outputs exist

### 9) Final proof file
- [x] `FINAL_CHECK.md` created (this file)
- [x] Manifest includes canonical notebook/report/dataset/commands/outputs
- [x] Date of final verification included

### 10) Final PDF export quality check
- [x] PDF exists: `outputs/adult_census_income/report_final_iteration4.pdf`
- [x] PDF regenerated from canonical markdown export pipeline
- [x] Filename matches README and manifest naming
- [x] Export log saved: `outputs/adult_census_income/evidence/report_export_log_final.txt`

## C. Nice-to-have improvements

### 11) Quick-start marker convenience
- [x] 3-command quick start added near top of README

### 12) Direct evidence screenshots in obvious folder
- [x] Reproduction screenshots/log visuals in `outputs/adult_census_income/evidence/`
- [x] Notebook/tests/submission-check proof images included

### 13) Final repo hygiene pass
- [x] `.DS_Store` removed
- [x] `~$*.docx` lock file removed
- [x] Unused duplicate notebooks/reports archived out of final paths
- [x] No credentials/secrets introduced
- [x] Relative paths preserved

## Submission-ready signoff
- [x] Final report PDF exists
- [ ] Final repo link works (no git remote configured in local workspace)
- [x] Canonical notebook runs
- [x] Tests pass
- [x] Submission checks pass
- [x] Agent evidence is easy to open
- [x] Appendix decision register is present
- [x] Dataset instructions are clear
- [x] README matches repo package
- [x] No stale duplicates in canonical paths
