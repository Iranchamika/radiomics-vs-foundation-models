# Data dictionary

Column-level documentation for every CSV in this folder. Numbers in brackets are the file's row count (data rows, excluding header).

---

## `12_Final_Included_Corpus.csv` [28 rows]

The final corpus of head-to-head FM-vs-radiomics comparisons.

| Column | Type | Notes |
|---|---|---|
| Order | int | 1–28, manuscript ordering (matches Table 1) |
| PMID | str | PubMed identifier, links to references.bib via `pmid{PMID}` key |
| Year | int | Publication year |
| Modality | str | CT, MRI, PET/CT, X-ray, Ultrasound, etc. |
| Anatomical_Region | str | Free-text anatomy (e.g. "Pancreas", "Brain (meningioma)") |
| Task_Type | str | Classification, prognosis, survival, etc. |
| Cohort_Train | str | Training cohort size (leading integer used in Table 1) |
| Cohort_Internal_Test | str | Internal test cohort size |
| Cohort_External_Test | str | External test cohort size (0 if absent) |
| External_Validation | str | Y/N — external validation cohort present |
| FM_Name | str | Foundation-model architecture (e.g. ResNet50, BiomedCLIP) |
| FM_Pretraining | str | Pretraining corpus (ImageNet, PMC-15M, RadImageNet, MedicalNet, etc.) |
| FM_Tier | str | Domain (medical/biomedical) vs ImageNet — drives the headline subgroup |
| Radiomics_Package | str | PyRadiomics, 3D Slicer, in-house, etc. |
| ML_Head | str | Downstream classifier (LR, SVM, RF, XGBoost, MLP, etc.) |
| FM_Arm_Metric | str | Primary discrimination metric (AUC unless noted) |
| FM_Arm_Value | float | FM-arm metric value |
| Rad_Arm_Value | float | Radiomics-arm metric value |
| Metric_Difference | float | FM − radiomics (positive favours FM) |
| PROBAST_Rating | str | Overall PROBAST risk of bias: High / Unclear / Low |
| (+ 13 further columns) | mixed | Segmentation method, blinding, calibration reporting, cross-validation scheme, etc. |

## `15_RQS_Item_Scores.csv` [28 rows]

Per-study Radiomics Quality Score (Lambin et al. 2017). Columns: `PMID`, then `RQS_1` to `RQS_16` (signed integer scores per item).

## `16_CLAIM_Item_Scores.csv` [28 rows]

Per-study CLAIM checklist (Mongan et al. 2020). Columns: `PMID`, then `CLAIM_1` to `CLAIM_42` (binary 0/1 with NR/NA codes).

## `17_PROBAST_Signaling.csv` [28 rows]

Per-study PROBAST signalling-question responses (Wolff et al. 2019). Four domains × 2–6 signalling questions plus overall risk-of-bias rating.

## `28_Kappa_Sample_25.csv` [25 rows]

Inter-rater reliability sample. Columns: `PMID`, `AI_Decision` (INCLUDE / EXCLUDE / MAYBE), `Reviewer_Final` (INCLUDE / EXCLUDE), `Agreement` (boolean).

## `29_Kappa_Results.csv`

Cohen's κ point estimate and 95% CI from the n = 25 sample. Used in §2.4 of the manuscript.

## `31_Exclusion_Reasons_Detail.csv` [46 rows]

Full-text exclusion taxonomy. Columns: `PMID`, `Year`, `Title`, `Primary_Exclusion_Reason`, `FAIL_Flags` (pipe-separated PASS/FAIL markers from the structured extraction form).

## `09a_PubMed_AI_Prescreen.csv` [245 rows]

Stage 1 AI pre-screen output. Columns: `PMID`, `Title`, `Abstract`, `AI_Decision`, `AI_Reasoning`.

## `10_Stage2_MAYBE_Sample.csv`

Stage 2 reviewer adjudication of the AI's MAYBE candidates.

## `11_Stage3_Remaining_MAYBEs.csv`

Stage 3 reconciliation log — all MAYBE-classified records resolved to INCLUDE/EXCLUDE by full-text review.

## `07_Pilot_Adjudication.csv`

Pilot kappa calibration on the first 20 abstracts (used to confirm the protocol before scaling to the full search).

## `references.bib`

BibTeX, PMID-keyed (`pmid{PMID}`). 28 entries matching the final corpus.
