# Reproducibility notes

Practical notes for re-running the pipeline end-to-end.

## Environment

- **Python**: 3.10 or 3.11 recommended. 3.12 should work but is untested.
- **R**: 4.2 or later. Required packages: `meta`, `metafor`, `dplyr`, `ggplot2`, `readr`. Install with:
  ```r
  install.packages(c("meta", "metafor", "dplyr", "ggplot2", "readr"))
  ```
- **LaTeX** (only needed if you want to compile `outputs/table1.tex` or `outputs/prisma_checklist.tex` into a PDF): TeX Live 2023+ or MiKTeX, with `longtable`, `pdflscape`, `booktabs`, `array`.

## Order of operations

The scripts are numbered in their intended run order, but they are independent — you can re-run any one without re-running the others, as long as `data/12_Final_Included_Corpus.csv` and the relevant quality-appraisal CSVs are present.

```bash
mkdir outputs

# 1. Headline meta-analysis (Δ AUC pooled, subgroups, sensitivity analyses)
Rscript scripts/19_meta_analysis.R
# → outputs/meta_analysis_results.csv, outputs/subgroup_summary.csv

# 2. Forest plot (Figure 2)
Rscript scripts/20_forest_plot.R
# → outputs/forest_plot.pdf, outputs/forest_plot.png

# 3. Quality-appraisal figures
python scripts/21_rqs_heatmap.py            # → outputs/rqs_heatmap.{png,pdf}
python scripts/22_claim_heatmap.py          # → outputs/claim_heatmap.{png,pdf}
python scripts/23_probast_traffic_light.py  # → outputs/probast_traffic_light.{png,pdf}

# 4. PRISMA 2020 flow diagram (Figure 1)
python scripts/24_prisma_flow.py            # → outputs/prisma_2020_flow.{png,pdf}

# 5. Manuscript-ready LaTeX tables
python scripts/32_table1_generator.py       # → outputs/table1.tex  (Table 1, landscape longtable)
python scripts/33_prisma_checklist_generator.py
                                            # → outputs/prisma_checklist.tex (Appendix A)
```

## Why some numbers differ between an "exact" reproduction and the manuscript

Three reasons you may see small discrepancies (typically in the 3rd decimal place):

1. **Hanley-McNeil SE(AUC)** assumes balanced classes when prevalence is not reported. We used the balanced-class form for 14/28 studies that did not report prevalence. If you have access to per-study prevalence and want an exact reproduction, edit `19_meta_analysis.R` to pass observed prevalence.
2. **DerSimonian-Laird τ²** is point-estimated. Different implementations (e.g. `meta` vs `metafor`) can disagree on the third decimal place of pooled estimates. The manuscript uses `meta::metagen(method.tau = "DL", hakn = TRUE)`.
3. **Knapp-Hartung** is enabled (`hakn = TRUE`). Disabling it widens the CI but does not change the point estimate.

## Cohen's κ caveat

The κ = 0.41 (95% CI 0.08–0.75) for the AI triage classifier vs human reviewer is the lowest-confidence number in the paper. The wide CI reflects the n = 25 calibration sample. We deliberately kept the AI as a triage-only filter — every AI INCLUDE was re-reviewed, and every AI MAYBE went through two further human stages. The final corpus is human-determined.

## Updating the bibliography

`data/references.bib` is PMID-keyed. To add a new paper:

1. Run `python scripts/30_fetch_pubmed_authors.py PMID1 PMID2 ...` to fetch the BibTeX-formatted entries.
2. Append the output to `data/references.bib`.
3. Re-run `python scripts/32_table1_generator.py` to refresh Table 1.

## Known limitations

- PubMed-only search. We considered Embase, Scopus and Web of Science but lacked institutional access to all three. Sensitivity analysis suggests the corpus is unlikely to have grown by more than 5–10 studies under a multi-database search; the BiomedCLIP-tier signal is strong enough to be robust to a 10-study addition.
- No grey literature search. Conference abstracts (RSNA, MICCAI, ISMRM) often report preliminary FM-vs-radiomics comparisons that don't survive to peer-reviewed publication.
- Single-reviewer extraction at Stage 4 (data extraction). The PRISMA-recommended dual-extraction was infeasible for a solo independent researcher. The 28-field structured form (`supplementary/Supplementary_File_3_Extraction_Form.pdf`) plus subsequent reconciliation pass (`supplementary/Supplementary_File_4_Reconciliation_Log.pdf`) is the mitigation.
