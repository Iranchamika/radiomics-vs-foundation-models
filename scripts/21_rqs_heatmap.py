"""
21_rqs_heatmap.py
RQS heatmap: 28 papers x 16 items, colored by per-item score.
Run from cmd:  python "21_rqs_heatmap.py"
"""
import csv, io
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

BASE = Path(__file__).resolve().parent.parent
OUT  = BASE / "phase5_outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- load ----------
raw = (BASE / "data" / "15_RQS_Item_Scores.csv").read_bytes().decode("utf-8-sig").replace("\x00", "")
rows = list(csv.reader(io.StringIO(raw)))
header = rows[0]
data_rows = rows[1:29]

# columns 3..18 are RQS items 01..16; col 19 = Total; col 20 = Pct
item_labels = [
    "01 ImgProtocol", "02 MultiSeg", "03 Phantom", "04 MultiTime",
    "05 FeatRedux", "06 MultiVar", "07 BiologicCorr", "08 CutOff",
    "09 Discrim", "10 Calib", "11 ProspReg", "12 Validation",
    "13 GoldStd", "14 ClinUtil", "15 CostEff", "16 OpenScience",
]
paper_labels = [f"P{r[0]} ({r[1]})" for r in data_rows]
scores = np.array([[int(r[3 + i]) for i in range(16)] for r in data_rows])  # 28 x 16

# ---------- colormap ----------
# Range observed: -3 to +7. Custom diverging colormap:
#  -3: deep red, 0: light grey, +7: deep blue
cmap = mcolors.LinearSegmentedColormap.from_list(
    "rqs", [(0.0, "#8B0000"), (0.3, "#FFCCCC"), (0.4, "#F5F5F5"),
            (0.6, "#CCE5FF"), (1.0, "#003366")])

# ---------- plot ----------
fig, ax = plt.subplots(figsize=(10, 14))
vmin, vmax = -3, 7
im = ax.imshow(scores, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")

# Cell text annotations
for i in range(28):
    for j in range(16):
        v = scores[i, j]
        txt_color = "white" if (v >= 4 or v <= -2) else "black"
        ax.text(j, i, str(v), ha="center", va="center",
                fontsize=8, color=txt_color, fontweight="bold")

ax.set_xticks(range(16))
ax.set_xticklabels(item_labels, rotation=45, ha="right", fontsize=8)
ax.set_yticks(range(28))
ax.set_yticklabels(paper_labels, fontsize=8)

# Add Total + Pct as a row annotation to the right
for i, r in enumerate(data_rows):
    total, pct = r[19], r[20]
    ax.text(16.3, i, f"{total} / {pct}%", va="center", fontsize=8, color="black")

ax.text(16.3, -1.0, "Total / Pct", va="center", fontsize=8, fontweight="bold")

cbar = plt.colorbar(im, ax=ax, shrink=0.5, pad=0.12)
cbar.set_label("RQS item score", fontsize=10)

plt.title("Radiomics Quality Score (RQS) — per-item scores across 28 included papers",
          fontsize=12, pad=15)
plt.tight_layout()
plt.savefig(OUT / "rqs_heatmap.png", dpi=300, bbox_inches="tight")
plt.savefig(OUT / "rqs_heatmap.pdf", bbox_inches="tight")
plt.close()
print(f"Saved {OUT / 'rqs_heatmap.png'}")
print(f"Saved {OUT / 'rqs_heatmap.pdf'}")
