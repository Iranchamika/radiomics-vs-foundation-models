r"""
33_prisma_checklist_generator.py
Generate the PRISMA 2020 27-item checklist as a LaTeX longtable, with the
"Reported on page/section" column mapped to the systematic review manuscript.

PRISMA 2020 reference:
  Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an
  updated guideline for reporting systematic reviews. BMJ. 2021;372:n71.
  doi:10.1136/bmj.n71

Writes:
  - outputs/prisma_checklist.tex   (\input-able from main.tex)

Run on Windows:
    cd .
    python 33_prisma_checklist_generator.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_TEX = ROOT / "outputs" / "prisma_checklist.tex"

# PRISMA 2020 checklist: (Section, Item #, Checklist item description, Reported on page/section)
# All 27 items unpacked into the 42 line items the official .docx file uses.
items = [
    # ----------------- TITLE -----------------
    ("TITLE", "1",
     "Identify the report as a systematic review.",
     r"Page 1 (Title); identifies the work as a ``systematic review and meta-analysis''."),

    # ----------------- ABSTRACT -----------------
    ("ABSTRACT", "2",
     "See the PRISMA 2020 for Abstracts checklist (Page et al., 2021).",
     r"Page 1--2 (Abstract): structured Background/Methods/Results/Conclusions; reports objectives, eligibility, sources, synthesis methods, $k=28$, pooled $\Delta$AUC with 95\% CI, heterogeneity, and limitations."),

    # ----------------- INTRODUCTION -----------------
    ("INTRODUCTION", "3 -- Rationale",
     "Describe the rationale for the review in the context of existing knowledge.",
     r"\S1 Introduction: states the gap between handcrafted radiomics and pretrained foundation-model embeddings; absence of pooled head-to-head evidence."),

    ("INTRODUCTION", "4 -- Objectives",
     "Provide an explicit statement of the objective(s) or question(s) the review addresses.",
     r"\S1 Introduction (final paragraph): the review's PICO question and primary objective."),

    # ----------------- METHODS -----------------
    ("METHODS", "5 -- Eligibility criteria",
     "Specify the inclusion and exclusion criteria for the review and how studies were grouped for the syntheses.",
     r"\S2.1 Eligibility criteria; full PICO formulation in PROSPERO record CRD420261393443."),

    ("METHODS", "6 -- Information sources",
     "Specify all databases, registers, websites, organisations, reference lists and other sources searched or consulted to identify studies. Specify the date when each source was last searched or consulted.",
     r"\S2.2: PubMed/MEDLINE searched 15 May 2026; no additional databases or grey literature (limitation acknowledged in \S5.4)."),

    ("METHODS", "7 -- Search strategy",
     "Present the full search strategies for all databases, registers and websites, including any filters and limits used.",
     r"\S2.2 (summary) and Supplementary File 2 (full Boolean search string)."),

    ("METHODS", "8 -- Selection process",
     "Specify the methods used to decide whether a study met the inclusion criteria of the review, including how many reviewers screened each record and each report retrieved, whether they worked independently, and if applicable, details of automation tools used in the process.",
     r"\S2.3 Selection process: single human reviewer (WAICK) with AI triage (Claude Sonnet 4.6) as initial sorting step. Inter-rater $\kappa = 0.41$ (95\% CI 0.08--0.75) on a stratified sample of 25 records; AI-EXCLUDE confirmed 10/10."),

    ("METHODS", "9 -- Data collection process",
     "Specify the methods used to collect data from reports, including how many reviewers collected data from each report, whether they worked independently, any processes for obtaining or confirming data from study investigators, and if applicable, details of automation tools used in the process.",
     r"\S2.4 Data extraction: 28-field standardised extraction form (Supplementary File 3); single human extractor with AI assistance against the pre-specified schema; every extracted field independently verified against the source PDF before entry into the corpus."),

    ("METHODS", "10a -- Data items: outcomes",
     "List and define all outcomes for which data were sought. Specify whether all results that were compatible with each outcome domain in each study were sought (e.g., for all measures, time points, analyses), and if not, the methods used to decide which results to collect.",
     r"\S2.4 and \S2.6: primary outcome = per-arm AUC (or C-index for survival tasks); for studies reporting multiple FM arms, the best-performing arm was the comparator."),

    ("METHODS", "10b -- Data items: other variables",
     "List and define all other variables for which data were sought (e.g., participant and intervention characteristics, funding sources). Describe any assumptions made about any missing or unclear information.",
     r"\S2.4: cohort sizes, modality, anatomy, task, FM identity and pretraining, FM usage mode, radiomics package and feature families, ML classifier, statistical comparison, code/data availability, funding, COI. Missing fields recorded as ``NR''."),

    ("METHODS", "11 -- Study risk of bias assessment",
     "Specify the methods used to assess risk of bias in the included studies, including details of the tool(s) used, how many reviewers assessed each study and whether they worked independently, and if applicable, details of automation tools used in the process.",
     r"\S2.5 Quality appraisal: RQS (16 items, 36 points; radiomics arm), CLAIM (42 items; FM arm), PROBAST (20 signalling questions across 4 domains; study level). Single rater with intra-rater consistency monitoring; 5 inter-phase flags resolved by PDF re-verification (Supplementary File 4)."),

    ("METHODS", "12 -- Effect measures",
     "Specify for each outcome the effect measure(s) (e.g., risk ratio, mean difference) used in the synthesis or presentation of results.",
     r"\S2.6: per-study $\Delta$AUC = AUC$_{\text{FM}}$ -- AUC$_{\text{Rad}}$; per-arm SE(AUC) from Hanley--McNeil approximation; per-study SE($\Delta$AUC) under conservative independent-arms assumption."),

    ("METHODS", "13a -- Synthesis methods: eligibility for synthesis",
     "Describe the processes used to decide which studies were eligible for each synthesis (e.g., tabulating the study intervention characteristics and comparing against the planned groups for each synthesis).",
     r"\S2.6: all 28 included studies eligible for the primary meta-analysis."),

    ("METHODS", "13b -- Synthesis methods: preparation of data",
     "Describe any methods required to prepare the data for presentation or synthesis, such as handling of missing summary statistics, or data conversions.",
     r"\S2.6: AUCs reported with 95\% CIs converted to SE(AUC) directly; otherwise Hanley--McNeil approximation with balanced-class assumption when prevalence was not reported."),

    ("METHODS", "13c -- Synthesis methods: tabulation and visualisation",
     "Describe any methods used to tabulate or visually display results of individual studies and syntheses.",
     r"\S2.6 + Figures: forest plot (Figure 2); RQS heatmap (Figure 3); PROBAST traffic-light (Figure 4); CLAIM heatmap (Supplementary Figure S1); Table 1 per-study characteristics."),

    ("METHODS", "13d -- Synthesis methods: pooled effect computation",
     "Describe any methods used to synthesise results and provide a rationale for the choice(s). If meta-analysis was performed, describe the model(s), method(s) to identify the presence and extent of statistical heterogeneity, and software package(s) used.",
     r"\S2.6: random-effects DerSimonian--Laird with Knapp--Hartung adjustment; \texttt{metafor} R package; heterogeneity quantified via $I^2$, $\tau^2$, Cochran Q."),

    ("METHODS", "13e -- Synthesis methods: heterogeneity exploration",
     "Describe any methods used to explore possible causes of heterogeneity among study results (e.g., subgroup analysis, meta-regression).",
     r"\S2.6: pre-specified subgroup analyses by FM class (domain-pretrained vs ImageNet-CNN), modality (CT/MRI/US), and external validation status."),

    ("METHODS", "13f -- Synthesis methods: sensitivity analyses",
     "Describe any sensitivity analyses conducted to assess robustness of the synthesised results.",
     r"\S2.6 + Table 2: five pre-specified sensitivity analyses (High-RQS only $\geq 12$; AUC-only; external-validation-only; exclusion of weak-radiomics-arm outlier; PROBAST Unclear/Low only)."),

    ("METHODS", "14 -- Reporting bias assessment",
     "Describe any methods used to assess risk of bias due to missing results in a synthesis (arising from reporting biases).",
     r"\S2.7: small $k$ precluded reliable funnel-plot symmetry or Egger's regression; reporting-bias risk assessed narratively against the distribution of $\Delta$AUC sign and magnitude versus methodological quality (RQS, PROBAST)."),

    ("METHODS", "15 -- Certainty assessment",
     "Describe any methods used to assess certainty (or confidence) in the body of evidence for an outcome.",
     r"\S2.7: modified GRADE approach incorporating risk of bias, inconsistency ($I^2$), indirectness, imprecision, publication bias."),

    # ----------------- RESULTS -----------------
    ("RESULTS", "16a -- Study selection",
     "Describe the results of the search and selection process, from the number of records identified in the search to the number of studies included in the review, ideally using a flow diagram.",
     r"\S3.1 Search and selection + Figure 1 PRISMA 2020 flow diagram: 245 records identified $\rightarrow$ 170 excluded at title/abstract $\rightarrow$ 75 sought for retrieval $\rightarrow$ 1 not retrieved $\rightarrow$ 74 assessed at full text $\rightarrow$ 46 excluded $\rightarrow$ 28 included."),

    ("RESULTS", "16b -- Excluded reports",
     "Cite studies that might appear to meet the inclusion criteria, but which were excluded, and explain why they were excluded.",
     r"\S3.1 and Supplementary File 5: full-text exclusion taxonomy (n = 46) with primary reason per record."),

    ("RESULTS", "17 -- Study characteristics",
     "Cite each included study and present its characteristics.",
     r"\S3.2 Study characteristics + Table 1 (per-study characteristics, landscape supplementary longtable, 28 rows $\times$ 15 columns)."),

    ("RESULTS", "18 -- Risk of bias in studies",
     "Present assessments of risk of bias for each included study.",
     r"\S3.5 Quality appraisal + Figure 3 (RQS heatmap) + Figure 4 (PROBAST traffic-light) + Supplementary Figure S1 (CLAIM heatmap). Item-level scores in Supplementary Tables 2--4."),

    ("RESULTS", "19 -- Results of individual studies",
     "For all outcomes, present, for each study: (a) summary statistics for each group (where appropriate) and (b) an effect estimate and its precision (e.g. confidence/credible interval), ideally using structured tables or plots.",
     r"Table 1 (per-study FM and radiomics values + $\Delta$AUC) + Figure 2 (forest plot with per-study 95\% CIs)."),

    ("RESULTS", "20a -- Results of syntheses: study characteristics",
     "For each synthesis, briefly summarise the characteristics and risk of bias among contributing studies.",
     r"\S3.2 and \S3.5: 28 studies, 5 imaging modalities, 17 anatomical sites, $k = 11$ external validation, 89\% PROBAST High risk of bias."),

    ("RESULTS", "20b -- Results of syntheses: pooled estimates",
     "Present results of all statistical syntheses conducted. If meta-analysis was done, present for each the summary estimate and its precision (e.g. confidence/credible interval) and measures of statistical heterogeneity. If comparing groups, describe the direction of the effect.",
     r"\S3.3 Primary meta-analysis: pooled $\Delta$AUC $= +0.051$ (95\% CI $+0.013$ to $+0.089$; $p = 0.010$; $I^2 = 58\%$; $\tau^2 = 0.0048$). Direction favours foundation-model arm."),

    ("RESULTS", "20c -- Results of syntheses: heterogeneity exploration",
     "Present results of all investigations of possible causes of heterogeneity among study results.",
     r"\S3.4 Subgroup and sensitivity analyses + Table 2: domain-pretrained FM $\Delta$AUC $= +0.120$ (95\% CI $+0.066$ to $+0.174$; $I^2 = 0\%$) vs ImageNet-CNN $\Delta$AUC $= +0.024$ (CI overlapping zero; $I^2 = 64\%$)."),

    ("RESULTS", "20d -- Results of syntheses: sensitivity analyses",
     "Present results of all sensitivity analyses conducted to assess the robustness of the synthesised results.",
     r"\S3.4 + Table 2: every pre-specified sensitivity analysis preserved direction and statistical significance of the primary result."),

    ("RESULTS", "21 -- Reporting biases",
     "Present assessments of risk of bias due to missing results (arising from reporting biases) for each synthesis assessed.",
     r"\S3.6: narrative assessment of publication-bias risk; small $k$ precluded reliable funnel-plot or Egger's test."),

    ("RESULTS", "22 -- Certainty of evidence",
     "Present assessments of certainty (or confidence) in the body of evidence for each outcome assessed.",
     r"\S3.6: modified-GRADE rating per outcome (overall, domain-pretrained subgroup, ImageNet-CNN subgroup)."),

    # ----------------- DISCUSSION -----------------
    ("DISCUSSION", "23a -- General interpretation",
     "Provide a general interpretation of the results in the context of other evidence.",
     r"\S5.1 Summary of evidence: pooled $\Delta$AUC interpreted against existing radiomics-FM literature."),

    ("DISCUSSION", "23b -- Limitations of the evidence",
     "Discuss any limitations of the evidence included in the review.",
     r"\S5.4 Limitations: 89\% PROBAST High risk of bias, dominant drivers calibration-absence and univariate pre-filtering."),

    ("DISCUSSION", "23c -- Limitations of the review processes",
     "Discuss any limitations of the review processes used.",
     r"\S5.4: PubMed-only search; conservative independent-arms SE assumption; single-reviewer screening (mitigated by AI triage + intra-rater consistency monitoring)."),

    ("DISCUSSION", "23d -- Implications",
     "Discuss implications of the results for practice, policy, and future research.",
     r"\S5.5 Implications for future research: prospective head-to-head pre-registration; calibration reporting; segmenter-blinding declaration; regularised regression without univariate pre-filtering; taxonomy distinguishing domain-pretrained FMs from ImageNet-CNN transfer learning."),

    # ----------------- OTHER INFORMATION -----------------
    ("OTHER INFORMATION", "24a -- Registration",
     "Provide registration information for the review, including the register name and registration number, or state that the review was not registered.",
     r"Declarations: PROSPERO CRD420261393443."),

    ("OTHER INFORMATION", "24b -- Protocol availability",
     "Indicate where the review protocol can be accessed, or state that a protocol was not prepared.",
     r"Declarations: protocol accessible via the PROSPERO record (CRD420261393443)."),

    ("OTHER INFORMATION", "24c -- Protocol amendments",
     "Describe and explain any amendments to information provided at registration or in the protocol.",
     r"Declarations: no amendments to the registered protocol."),

    ("OTHER INFORMATION", "25 -- Support",
     "Describe sources of financial or non-financial support for the review, and the role of the funders or sponsors in the review.",
     r"Declarations -- Funding: this research received no external funding."),

    ("OTHER INFORMATION", "26 -- Competing interests",
     "Declare any competing interests of review authors.",
     r"Declarations -- Competing interests: the author declares no competing interests relevant to this work."),

    ("OTHER INFORMATION", "27 -- Availability of data, code, other materials",
     "Report which of the following are publicly available and where they can be found: template data collection forms; data extracted from included studies; data used for all analyses; analytic code; any other materials used in the review.",
     r"Declarations -- Availability of data and materials: extracted data and item-level scoring sheets in Supplementary Tables 1--4; meta-analysis source code (R/\texttt{metafor}) and figure code (Python/\texttt{matplotlib}) at a public GitHub repository at the time of publication."),
]


def esc(s):
    # The "Reported on..." column contains hand-authored LaTeX (with $...$ and
    # \S etc.), so it must NOT be re-escaped. Only the plain-text description
    # column gets escaped.
    if not s:
        return ""
    return (s.replace("&", r"\&")
             .replace("%", r"\%")
             .replace("#", r"\#")
             .replace("_", r"\_"))


lines = []
lines.append(r"% PRISMA 2020 27-item checklist -- generated by 33_prisma_checklist_generator.py")
lines.append(r"% Cite as: Page MJ et al. BMJ 2021;372:n71 (doi:10.1136/bmj.n71)")
lines.append(r"")
lines.append(r"\clearpage")
lines.append(r"\section*{Supplementary Appendix A: PRISMA 2020 Checklist}")
lines.append(r"\addcontentsline{toc}{section}{Supplementary Appendix A: PRISMA 2020 Checklist}")
lines.append(r"")
lines.append(r"This appendix maps each of the 27 PRISMA 2020 reporting items (with sub-items, 42 line items) to the manuscript section, table, or figure where it is reported. Citation: Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. \emph{BMJ}. 2021;372:n71. \texttt{doi:10.1136/bmj.n71}.")
lines.append(r"")
lines.append(r"\begin{footnotesize}")
lines.append(r"\setlength{\tabcolsep}{4pt}")
lines.append(r"\renewcommand{\arraystretch}{1.25}")
lines.append(r"")
lines.append(r"\sloppy")
lines.append(r"\begin{longtable}{@{}L{1.8cm} L{2.8cm} L{4.8cm} L{5.5cm}@{}}")
lines.append(r"\caption{PRISMA 2020 27-item checklist with cross-references to the manuscript.}\label{tab:prisma_checklist}\\")
lines.append(r"\toprule")
lines.append(r"\textbf{Section} & \textbf{Item \#} & \textbf{Checklist item} & \textbf{Reported in} \\")
lines.append(r"\midrule")
lines.append(r"\endfirsthead")
lines.append(r"\multicolumn{4}{c}{\emph{Table~\ref{tab:prisma_checklist} continued from previous page}}\\")
lines.append(r"\toprule")
lines.append(r"\textbf{Section} & \textbf{Item \#} & \textbf{Checklist item} & \textbf{Reported in} \\")
lines.append(r"\midrule")
lines.append(r"\endhead")
lines.append(r"\midrule")
lines.append(r"\multicolumn{4}{r}{\emph{continued on next page}}\\")
lines.append(r"\endfoot")
lines.append(r"\bottomrule")
lines.append(r"\endlastfoot")

last_section = None
for section, item, desc, reported in items:
    # Print section label only on first row of each section
    sec_cell = section if section != last_section else ""
    last_section = section
    lines.append(f"{esc(sec_cell)} & {esc(item)} & {esc(desc)} & {reported} \\\\")

lines.append(r"\end{longtable}")
lines.append(r"\end{footnotesize}")
lines.append(r"")

OUT_TEX.parent.mkdir(parents=True, exist_ok=True)
OUT_TEX.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT_TEX}")
print(f"  {len(items)} checklist line items -> 1 longtable")