# Pretrained foundation-model embeddings vs handcrafted radiomics — analysis code and data

[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE-data)
[![PROSPERO](https://img.shields.io/badge/PROSPERO-CRD420261393443-orange.svg)](https://www.crd.york.ac.uk/prospero/)
[![DOI](https://zenodo.org/badge/1245520162.svg)](https://doi.org/10.5281/zenodo.20502586)

Reproducibility package for the systematic review and meta-analysis

> **Pretrained foundation-model embeddings versus handcrafted radiomics for medical image classification and prognostic tasks: a systematic review and meta-analysis**

PROSPERO registration: **CRD420261393443**. Manuscript currently under peer review at *Insights into Imaging*.

## What is in this repository

This repository contains the analysis scripts, screening logs, extracted-data tables, and supplementary materials needed to reproduce every figure and number in the manuscript. The manuscript text itself is held back until acceptance; once the paper is published, a link to the open-access version will be added here and the repository will be Zenodo-archived for a permanent DOI.

```
.
├── scripts/                Analysis pipeline (Python + R)
├── data/                   Screening logs, final corpus, quality-appraisal scores, bibliography
├── supplementary/          PRISMA-recommended supplementary PDFs (search strategy, extraction form, exclusion taxonomy)
├── docs/                   Statistical synthesis workflow notes
├── outputs/                Created at runtime — figures and tables write here (gitignored)
├── requirements.txt        Python dependencies
├── CITATION.cff            How to cite this repository
└── LICENSE / LICENSE-data  MIT for code, CC BY 4.0 for data
```

## Headline result (preview)

Across 28 head-to-head studies where both paradigms were applied to the same patient cohort and the same clinical task, foundation-model embeddings outperformed handcrafted radiomics by **Δ AUC = +0.051 (95% CI +0.013 to +0.089; p = 0.010)**. The effect is concentrated in domain-pretrained foundation models (BiomedCLIP, RadImageNet, MedicalNet): pooled **Δ AUC = +0.120 (95% CI +0.066 to +0.174; I² = 0%)**. ImageNet-pretrained CNN feature extractors did not show a significant advantage (Δ AUC = +0.024, CI crossed zero, I² = 64%). Full numbers, subgroup analyses and sensitivity analyses are in the manuscript and reproducible from `scripts/19_meta_analysis.R`.

## Quickstart — reproduce the analyses

Requires Python 3.10+ and R 4.2+.

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt
mkdir outputs

# Random-effects meta-analysis (DerSimonian-Laird + Knapp-Hartung)
Rscript scripts/19_meta_analysis.R

# Forest plot
Rscript scripts/20_forest_plot.R

# Quality-appraisal figures
python scripts/21_rqs_heatmap.py
python scripts/22_claim_heatmap.py
python scripts/23_probast_traffic_light.py

# PRISMA 2020 flow diagram (Figure 1)
python scripts/24_prisma_flow.py

# Per-study characteristics table (LaTeX longtable, Table 1)
python scripts/32_table1_generator.py

# PRISMA 27-item checklist (Supplementary Appendix A)
python scripts/33_prisma_checklist_generator.py
```

All outputs are written to `outputs/`, which is created at runtime and not tracked in git.

## Script catalogue

| Script | Language | Purpose |
|---|---|---|
| `19_meta_analysis.R` | R | Random-effects DerSimonian-Laird meta-analysis with Knapp-Hartung adjustment; subgroup pooling by foundation-model tier, modality, task type; sensitivity analyses |
| `20_forest_plot.R` | R | Forest plot (Figure 2) |
| `21_rqs_heatmap.py` | Python | 28 × 16 Radiomics Quality Score heatmap |
| `22_claim_heatmap.py` | Python | 28 × 42 CLAIM checklist heatmap |
| `23_probast_traffic_light.py` | Python | PROBAST domain-level risk-of-bias visualisation |
| `24_prisma_flow.py` | Python | PRISMA 2020 four-box flow diagram (Figure 1) |
| `25_characteristics_table.py` | Python | Supplementary Table 1 generator |
| `30_fetch_pubmed_authors.py` | Python | Helper — resolve first-author surnames from PMIDs |
| `32_table1_generator.py` | Python | Manuscript Table 1 (per-study characteristics longtable) |
| `33_prisma_checklist_generator.py` | Python | Supplementary Appendix A — PRISMA 27-item checklist with page references |

## Data files

| File | Rows | Description |
|---|---|---|
| `data/12_Final_Included_Corpus.csv` | 28 | Final included corpus with 33 extracted fields per study (modality, anatomy, cohort sizes, foundation-model details, radiomics package, ML head, primary metric, FM/radiomics values, Δ, PROBAST rating) |
| `data/15_RQS_Item_Scores.csv` | 28 | Per-study Radiomics Quality Score (16 items) |
| `data/16_CLAIM_Item_Scores.csv` | 28 | Per-study CLAIM (Checklist for Artificial Intelligence in Medical imaging) scores (42 items) |
| `data/17_PROBAST_Signaling.csv` | 28 | PROBAST signalling-question responses |
| `data/28_Kappa_Sample_25.csv` | 25 | Inter-rater reliability sample (Cohen's κ, AI triage vs human reviewer) |
| `data/29_Kappa_Results.csv` | — | κ point estimate and 95% CI |
| `data/31_Exclusion_Reasons_Detail.csv` | 46 | Full-text exclusion taxonomy with per-PMID detail |
| `data/09a_PubMed_AI_Prescreen.csv` | 245 | Stage 1 AI pre-screen output |
| `data/10_Stage2_MAYBE_Sample.csv` | — | Stage 2 reviewer adjudication of MAYBE candidates |
| `data/11_Stage3_Remaining_MAYBEs.csv` | — | Stage 3 reconciliation log |
| `data/07_Pilot_Adjudication.csv` | — | Pilot kappa calibration (first 20 abstracts) |
| `data/references.bib` | 28 | BibTeX entries (PMID-keyed) for the 28 included studies |

A column-level data dictionary lives at `data/README.md`.

## Methodology in one paragraph

PubMed-only systematic search (2026-05-15), AI-assisted Stage 1 pre-screen with Cohen's κ = 0.41 (95% CI 0.08–0.75) against human reviewer ground truth, Stage 2 and Stage 3 human adjudication of MAYBE candidates, full-text retrieval (75 sought, 74 assessed, 1 not retrieved), full-text exclusion (n = 46, taxonomy in `data/31_Exclusion_Reasons_Detail.csv`), final inclusion n = 28. Quality appraisal applied RQS (Lambin 2017), CLAIM (Mongan 2020) and PROBAST (Wolff 2019) to every included study. Meta-analysis used the Hanley-McNeil SE(AUC) approximation under an independent-arms assumption (conservative), DerSimonian-Laird random-effects pooling with Knapp-Hartung small-sample CI adjustment, prespecified subgroup analyses (foundation-model pretraining tier, modality, task type, validation status) and five prespecified sensitivity analyses.

## Licensing

- **Code** (`scripts/`, `requirements.txt`, top-level config): MIT licence — see [`LICENSE`](LICENSE).
- **Data and documentation** (`data/`, `docs/`, `supplementary/`, `README.md`): Creative Commons Attribution 4.0 International — see [`LICENSE-data`](LICENSE-data). The 28 included primary studies remain copyrighted by their original publishers; this repository contains extracted summary data, not the source articles.

## Citing this work

Until the manuscript is accepted, please cite the repository directly using the metadata in [`CITATION.cff`](CITATION.cff). After acceptance the manuscript will be the preferred citation and a Zenodo DOI will be minted for this repository.

## Caveats and reproducibility notes

- The Hanley-McNeil SE(AUC) approximation assumes balanced classes when prevalence was not reported. For studies that did report prevalence, the exact form was used. The independent-arms variance approximation (var(Δ) = var_FM + var_Rad) is conservative; the paired variance is smaller. Sensitivity of the headline pooled Δ to this assumption is reported in §3.5 of the manuscript.
- κ for the AI triage classifier is moderate (0.41) and is the lowest-confidence number in the paper. Stage 2 and Stage 3 human adjudication absorb the AI's false-negatives; the final corpus is human-determined, not AI-determined.
- PRISMA flow counts are reconciled (245 → 170 → 75 → 1 → 74 → 46 → 28). The reconciliation log is at `supplementary/Supplementary_File_4_Reconciliation_Log.pdf`.

## Contact

Repository maintainer: W. A. I. C. Kumarananda — `iran.wanniarachchige@student.adelaide.edu.au`.

Issues, corrections and reproducibility questions: please open a GitHub issue rather than emailing.
