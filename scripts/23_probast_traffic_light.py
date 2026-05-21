"""
23_probast_traffic_light.py
PROBAST traffic-light: 28 papers x 4 domains, colored Low/High/Unclear.
Plus overall ROB and Applicability columns.
Run from cmd:  python "23_probast_traffic_light.py"
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

raw = (BASE / "data" / "17_PROBAST_Signaling.csv").read_bytes().decode("utf-8-sig").replace("\x00", "")
rows = list(csv.reader(io.StringIO(raw)))
header = rows[0]
data_rows = rows[1:29]

# Find column indices
def col(name):
    return header.index(name)

paper_labels = [f"P{r[0]} ({r[1]})" for r in data_rows]
column_labels = ["D1\nParticipants", "D2\nPredictors", "D3\nOutcome", "D4\nAnalysis",
                  "Overall\nROB", "D1 Appl", "D2 Appl", "D3 Appl", "Overall\nAppl"]

# Encode: Low=2, Unclear=1, High=0
def code(v):
    return {"Low": 2, "Unclear": 1, "High": 0}.get(v.strip(), 1)

c_d1 = col("D1_ROB"); c_d2 = col("D2_ROB"); c_d3 = col("D3_ROB"); c_d4 = col("D4_ROB")
c_orob = col("Overall_ROB")
c_d1a = col("D1_Appl"); c_d2a = col("D2_Appl"); c_d3a = col("D3_Appl")
c_oappl = col("Overall_Applicability")

matrix = np.array([[code(r[c]) for c in [c_d1, c_d2, c_d3, c_d4, c_orob, c_d1a, c_d2a, c_d3a, c_oappl]]
                   for r in data_rows])

# Colormap: green=Low, yellow=Unclear, red=High
cmap = mcolors.ListedColormap(["#E55D5D", "#F5DC6F", "#5DA85D"])
bounds = [-0.5, 0.5, 1.5, 2.5]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots(figsize=(11, 12))
im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="auto")

# Add text labels in each cell
text_map = {2: "L", 1: "U", 0: "H"}
for i in range(28):
    for j in range(9):
        v = matrix[i, j]
        ax.text(j, i, text_map[v], ha="center", va="center",
                fontsize=9, fontweight="bold",
                color="white" if v == 0 else "black")

# Add a separating line between ROB (cols 0-4) and Applicability (cols 5-8)
ax.axvline(x=4.5, color="black", linewidth=2)
# Separating line for Overall ROB column
ax.axvline(x=3.5, color="black", linewidth=1, alpha=0.5)
ax.axvline(x=7.5, color="black", linewidth=1, alpha=0.5)

ax.set_xticks(range(9))
ax.set_xticklabels(column_labels, rotation=0, fontsize=8)
ax.set_yticks(range(28))
ax.set_yticklabels(paper_labels, fontsize=8)

# Top labels
ax.text(1.5, -1.5, "Risk of Bias", ha="center", fontsize=11, fontweight="bold")
ax.text(6.5, -1.5, "Applicability", ha="center", fontsize=11, fontweight="bold")

legend_handles = [
    Patch(color="#5DA85D", label="Low (L)"),
    Patch(color="#F5DC6F", label="Unclear (U)"),
    Patch(color="#E55D5D", label="High (H)"),
]
ax.legend(handles=legend_handles, loc="upper center",
          bbox_to_anchor=(0.5, -0.04), ncol=3, frameon=False, fontsize=10)

plt.title("PROBAST Risk of Bias and Applicability — 28 papers",
          fontsize=12, pad=25)
plt.tight_layout()
plt.savefig(OUT / "probast_traffic_light.png", dpi=300, bbox_inches="tight")
plt.savefig(OUT / "probast_traffic_light.pdf", bbox_inches="tight")
plt.close()
print(f"Saved {OUT / 'probast_traffic_light.png'}")
print(f"Saved {OUT / 'probast_traffic_light.pdf'}")

# Print modal failure-mode tallies
print("\nPROBAST domain ROB tallies at n=28:")
domains = ["D1 Participants", "D2 Predictors", "D3 Outcome", "D4 Analysis"]
for j, d in enumerate(domains):
    col_vals = matrix[:, j]
    print(f"  {d}: Low={np.sum(col_vals==2)} | Unclear={np.sum(col_vals==1)} | High={np.sum(col_vals==0)}")
print(f"\n  Overall ROB:    Low={np.sum(matrix[:,4]==2)} | Unclear={np.sum(matrix[:,4]==1)} | High={np.sum(matrix[:,4]==0)}")
print(f"  Overall Appl:   Low={np.sum(matrix[:,8]==2)} | Unclear={np.sum(matrix[:,8]==1)} | High={np.sum(matrix[:,8]==0)}")
