"""
25_characteristics_table.py
Generate Supplementary Table 1: Characteristics of Included Studies.
Pulls condensed fields from 12_Final_Included_Corpus.csv and emits both
CSV (for editing in Excel) and a publication-style HTML for screenshots.

Run from cmd:  python "25_characteristics_table.py"
"""
import csv, io
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT  = BASE / "phase5_outputs"
OUT.mkdir(parents=True, exist_ok=True)

# ---------- load corpus ----------
raw = (BASE / "data" / "12_Final_Included_Corpus.csv").read_bytes().decode("utf-8-sig").replace("\x00","")
rows = list(csv.reader(io.StringIO(raw)))
header = rows[0]
data_rows = rows[1:29]

def col(name):
    return header.index(name)

# Build a condensed supplementary table
# Column choices for a typical "Characteristics of Studies" table:
suppl_columns = [
    ("Study", lambda r: f"P{r[0]} ({r[1]})"),
    ("Year", lambda r: r[3]),
    ("Modality", lambda r: r[col('Modality')]),
    ("Anatomy", lambda r: r[col('Anatomical_Region')]),
    ("Task", lambda r: r[col('Clinical_Task')][:60]),
    ("N (train/intTest/extTest)", lambda r: f"{r[col('Cohort_Train')]} / {r[col('Cohort_Internal_Test')]} / {r[col('Cohort_External_Test')]}"),
    ("Ext val", lambda r: r[col('External_Validation')]),
    ("FM", lambda r: r[col('FM_Name')]),
    ("FM pretraining", lambda r: r[col('FM_Pretraining')][:35]),
    ("FM usage", lambda r: r[col('FM_Usage_Mode')][:25]),
    ("Rad package", lambda r: r[col('Radiomics_Package')]),
    ("ML head", lambda r: r[col('ML_Head')][:25]),
    ("FM AUC", lambda r: r[col('FM_Arm_Value')]),
    ("Rad AUC", lambda r: r[col('Rad_Arm_Value')]),
    ("Delta AUC", lambda r: r[col('Metric_Difference')]),
    ("Stat test", lambda r: r[col('Stat_Comparison')][:30]),
    ("RQS /36", lambda r: r[col('RQS_Score')]),
    ("CLAIM %", lambda r: r[col('CLAIM_Score')]),
    ("PROBAST", lambda r: r[col('PROBAST_Rating')]),
    ("Code shared", lambda r: "Y" if (r[col('Code_Available')].startswith("http") or r[col('Code_Available')].startswith("https")) else "N"),
    ("Data shared", lambda r: "Y" if (r[col('Data_Available')].startswith("http") or r[col('Data_Available')].lower().find("request") >= 0) else "N"),
]

# ---------- CSV output ----------
csv_path = OUT / "characteristics_of_studies.csv"
with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow([h for h, _ in suppl_columns])
    for r in data_rows:
        w.writerow([fn(r) for _, fn in suppl_columns])
print(f"Saved {csv_path}")

# ---------- HTML output (publication-style) ----------
html_path = OUT / "characteristics_of_studies.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Supplementary Table 1: Characteristics of Included Studies</title>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; color: #222; }
  h1 { font-size: 18px; margin-bottom: 5px; }
  .subtitle { color: #666; font-size: 11px; margin-bottom: 20px; }
  table { border-collapse: collapse; font-size: 9.5px; width: 100%; }
  th, td { padding: 4px 6px; border: 1px solid #aaa; text-align: left; vertical-align: top; }
  th { background: #2C5282; color: white; font-weight: bold; }
  tr:nth-child(even) td { background: #F8FAFC; }
  tr:hover td { background: #FEF9C3; }
  .footer { color: #666; font-size: 10px; margin-top: 20px; font-style: italic; }
</style>
</head><body>
<h1>Supplementary Table 1: Characteristics of Included Studies (n = 28)</h1>
<div class="subtitle">Pretrained foundation-model embeddings vs handcrafted radiomics for medical image classification and prognostic tasks.<br/>PROSPERO CRD420261393443.</div>
<table>
<thead><tr>
""")
    for h, _ in suppl_columns:
        f.write(f"<th>{h}</th>")
    f.write("</tr></thead>\n<tbody>\n")
    for r in data_rows:
        f.write("<tr>")
        for _, fn in suppl_columns:
            v = fn(r)
            f.write(f"<td>{v}</td>")
        f.write("</tr>\n")
    f.write("""</tbody></table>
<div class="footer">
  RQS = Radiomics Quality Score (max 36, Lambin 2017). CLAIM = Checklist for AI in Medical Imaging (% adequately reported, Mongan 2020). PROBAST = Prediction model Risk Of Bias ASsessment Tool (Wolff 2019).<br/>
  Delta AUC = FM arm AUC - Radiomics arm AUC. Positive favors FM; negative favors Radiomics.
</div>
</body></html>
""")
print(f"Saved {html_path}")
print()
print(f"Total papers: {len(data_rows)}")
print("Open the .html in a browser for a screenshot-ready supplementary table.")
