"""
24_prisma_flow.py
PRISMA 2020 flow diagram for the systematic review.

Inputs the screening counts manually (from the PRISMA flow structure of
PROSPERO CRD420261393443) and produces a publication-ready flow diagram
matching the PRISMA 2020 four-box vertical layout.

Run from cmd:  python "24_prisma_flow.py"

EDIT THE COUNTS BELOW to match your actual screening log. The counts shown
are derived from the Phase 4a workflow:
  - PubMed search 2026-05-15: 245 records
  - After Stage 1 AI pre-screen + Stage 2/3 reviewer adjudication:
    - 28 INCLUDED (final corpus)
    - Plus 4 unresolved MAYBEs and 1 paywalled paper documented separately
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent.parent / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- VERIFIED COUNTS FROM SCREENING LOGS (2026-05-19 reconciliation) ----------
# Reconciled to make arithmetic balance:
#   245 records identified -> 170 excluded at t/a -> 75 sought -> 1 not retrieved
#   -> 74 assessed at full text -> 46 excluded -> 28 included.
# Exclusion breakdown derived from 10_Stage2_MAYBE_Sample.csv + 11_Stage3_Remaining_MAYBEs.csv
# via the PASS/FAIL markers in FM_Named / Texture_Features / Per_Arm_Metrics / Modality_OK fields.
n_pubmed         = 245      # PubMed search hits (2026-05-15)
n_other_dbs      = 0        # No other databases searched (PubMed only)
n_duplicates     = 0        # PubMed internal dedup; no separate dedup step
n_records_screened = 245
n_excluded_titleabs = 170   # AI EXCLUDE at title/abstract (245 - 75)
n_to_fulltext    = 75       # AI INCLUDE/MAYBE advanced to full-text retrieval
n_not_retrieved  = 1        # Paywalled, ILL unsuccessful
n_fulltext_assessed = 74    # 75 sought - 1 not retrieved
n_excluded_fulltext = 46    # See breakdown below; verified from Stage 2 + Stage 3 logs
n_included       = 28       # Final corpus

# Full-text exclusion reason taxonomy (n=46, derived from structured PASS/FAIL fields in
# Phase 4a Stage 2 and Stage 3 screening logs). Primary-reason categorisation; some
# excludes had multiple FAIL flags and are assigned to the highest-priority reason.
exclusion_reasons = {
    # Short labels for the diagram (so cells fit a 3-unit box at fontsize 7.5).
    # The full taxonomy with per-PMID detail is in Supplementary File 5.
    "No qualifying pretrained FM": 23,
    "Fusion-only, no per-arm metrics": 11,
    "First-order radiomics only": 9,
    "Other protocol-nuance reasons": 2,
    "Off-scope modality": 1,
}

# ---------- Build the diagram ----------
fig, ax = plt.subplots(figsize=(10, 13))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis("off")

# Helper to draw a box
def draw_box(x, y, w, h, text, fc="#E8F0FB", ec="#2C5282", fontsize=9, fontweight="normal"):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                        boxstyle="round,pad=0.05,rounding_size=0.15",
                        linewidth=1.5, edgecolor=ec, facecolor=fc)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight, wrap=True)

# Helper to draw an arrow
def draw_arrow(x1, y1, x2, y2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle="-|>", mutation_scale=15,
                            linewidth=1.5, color="#2C5282")
    ax.add_patch(arrow)

# Title
ax.text(5, 13.5, "PRISMA 2020 Flow Diagram", fontsize=14, fontweight="bold", ha="center")
ax.text(5, 13.0, "Pretrained foundation-model embeddings vs handcrafted radiomics",
        fontsize=10, ha="center", style="italic")
ax.text(5, 12.65, "PROSPERO CRD420261393443", fontsize=9, ha="center", color="#666")

# Section labels (left side)
ax.text(0.3, 11.5, "Identification", fontsize=11, fontweight="bold", rotation=90, va="center")
ax.text(0.3, 8.5,  "Screening",      fontsize=11, fontweight="bold", rotation=90, va="center")
ax.text(0.3, 5.5,  "Eligibility",    fontsize=11, fontweight="bold", rotation=90, va="center")
ax.text(0.3, 2.5,  "Included",       fontsize=11, fontweight="bold", rotation=90, va="center")

# Box positions
# Identification
draw_box(4, 11.5, 4, 1.2,
         f"Records identified from:\nDatabase (PubMed): n = {n_pubmed}\nOther sources: n = {n_other_dbs}")
draw_box(8.0, 11.5, 3, 1.2,
         f"Records removed before\nscreening:\nDuplicates: n = {n_duplicates}", fc="#FFE9E9")
draw_arrow(6, 11.5, 6.5, 11.5)

# Arrow down to Screening
draw_arrow(4, 10.85, 4, 10.0)

# Screening
draw_box(4, 9.4, 4, 1.2,
         f"Records screened\nn = {n_records_screened}")
draw_box(8.0, 9.4, 3, 1.2,
         f"Records excluded\nat title/abstract:\nn = {n_excluded_titleabs}", fc="#FFE9E9")
draw_arrow(6, 9.4, 6.5, 9.4)

# Arrow down to fulltext retrieval
draw_arrow(4, 8.8, 4, 7.95)

draw_box(4, 7.3, 4, 1.2,
         f"Reports sought for retrieval\nn = {n_to_fulltext}")
draw_box(8.0, 7.3, 3, 1.2,
         f"Reports not retrieved:\nn = {n_not_retrieved}\n(paywall / unavailable)", fc="#FFE9E9")
draw_arrow(6, 7.3, 6.5, 7.3)

# Arrow down to Eligibility
draw_arrow(4, 6.7, 4, 5.85)

# Eligibility
draw_box(4, 5.2, 4, 1.2,
         f"Reports assessed for eligibility\nn = {n_fulltext_assessed}")

# Exclusion-reasons box (rich content)
# Drawn manually so the text can be left-aligned within the box (the draw_box
# helper centres text, which causes long lines to spill over both edges).
reason_text = "Reports excluded:\n" + "\n".join([f"- {r} (n={n})" for r, n in exclusion_reasons.items()])
_excl_box = FancyBboxPatch((8.0 - 3/2, 5.2 - 2.3/2), 3, 2.3,
                           boxstyle="round,pad=0.05,rounding_size=0.15",
                           linewidth=1.5, edgecolor="#2C5282", facecolor="#FFE9E9")
ax.add_patch(_excl_box)
ax.text(8.0 - 3/2 + 0.12, 5.2, reason_text,
        ha="left", va="center", fontsize=7.5, wrap=True)
draw_arrow(6, 5.2, 6.5, 5.2)

# Arrow down to Included
draw_arrow(4, 4.55, 4, 3.7)

# Included
draw_box(4, 3.0, 4, 1.2,
         f"Studies included in review\nn = {n_included}",
         fc="#D9F2D9", ec="#2E7D32", fontweight="bold")

# Footer note
ax.text(5, 0.5,
        "AI-assisted title/abstract pre-screen with reviewer adjudication.\n"
        "Cohen kappa = 0.41 (95% CI 0.08-0.75).",
        ha="center", fontsize=8, s