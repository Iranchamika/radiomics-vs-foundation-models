"""
22_claim_heatmap.py
CLAIM heatmap: 28 papers x 42 items, colored Y/N/NA.
Run from cmd:  python "22_claim_heatmap.py"
"""
import csv, io
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

BASE = Path(__file__).resolve().parent.parent
OUT  = BASE / "phase5_outputs"
OUT.mkdir(parents=True, exist_ok=True)

raw = (BASE / "data" / "16_CLAIM_Item_Scores.csv").read_bytes().decode("utf-8-sig").replace("\x00", "")
rows = list(csv.reader(io.StringIO(raw)))
data_rows = rows[1:29]

# cols 3..44 are items 01..42; col 47 = Pct
paper_labels = [f"P{r[0]} ({r[1]})" for r in data_rows]
item_labels = [f"{i:02d}" for i in range(1, 43)]

# Encode: Y=1, N=0, NA=-1
def code(v):
    return {"Y": 1, "N": 0, "NA": -1}.get(v.strip(), 0)

matrix = np.array([[code(r[3 + i]) for i in range(42)] for r in data_rows])  # 28 x 42

# Colormap: green = Y, red = N, grey = NA
cmap = mcolors.ListedColormap(["#888888", "#E55D5D", "#5DA85D"])
bounds = [-1.5, -0.5, 0.5, 1.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(16, 12))
im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")

# Add Pct annotation as last column
for i, r in enumerate(data_rows):
    ax.text(42.5, i, f"{r[46]}%", va="center", fontsize=7, color="black")
ax.text(42.5, -1.0, "%Reported", va="center", fontsize=7, fontweight="bold")

ax.set_xticks(range(42))
ax.set_xticklabels(item_labels, rotation=0, fontsize=7)
ax.set_yticks(range(28))
ax.set_yticklabels(paper_labels, fontsize=7)
ax.set_xlabel("CLAIM Item (01-42)", fontsize=10)

# Legend
legend_handles = [
    Patch(color="#5DA85D", label="Y (reported adequately)"),
    Patch(color="#E55D5D", label="N (missing/inadequate)"),
    Patch(color="#888888", label="NA (not applicable)"),
]
ax.legend(handles=legend_handles, loc="upper center",
          bbox_to_anchor=(0.5, -0.06), ncol=3, frameon=False, fontsize=9)

plt.title("CLAIM Checklist — 42 items x 28 papers", fontsize=12, pad=15)
plt.tight_layout()
plt.savefig(OUT / "claim_heatmap.png", dpi=300, bbox_inches="tight")
plt.savefig(OUT / "claim_heatmap.pdf", bbox_inches="tight")
plt.close()
print(f"Saved {OUT / 'claim_heatmap.png'}")
print(f"Saved {OUT / 'claim_heatmap.pdf'}")

# Also print item-level "% N" tally for the manuscript text
n_count = np.sum(matrix == 0, axis=0)
print("\nItems failed by >50% of papers (N count >=15):")
for i in range(42):
    if n_count[i] >= 15:
        print(f"  CLAIM_{i+1:02d}: N in {n_count[i]} / 28 papers ({n_count[i]/28*100:.0f}%)")
