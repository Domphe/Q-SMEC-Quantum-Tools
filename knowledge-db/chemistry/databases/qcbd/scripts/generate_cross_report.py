import os
import json
from collections import defaultdict, Counter
from datetime import datetime

REPORTS_DIR = r"G:\\My Drive\\Databases\\QCBD\\reports"

# Find latest deep_summary file
summary_files = [f for f in os.listdir(REPORTS_DIR) if f.startswith("deep_summary_") and f.endswith(".json")]
if not summary_files:
    raise SystemExit("No deep_summary_*.json found. Run deep_inventory.py first.")
summary_files.sort(reverse=True)
summary_path = os.path.join(REPORTS_DIR, summary_files[0])

with open(summary_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    summaries = data.get("summaries", [])

# Aggregate keywords and roots
by_keyword = defaultdict(list)
by_root = defaultdict(list)

for item in summaries:
    path = item.get("path", "")
    summary = item.get("summary", {})
    kws = summary.get("keywords", [])
    # Determine root from path prefix
    root = None
    for candidate in [
        r"G:\\My Drive\\White Paper (Patent)",
        r"G:\\My Drive\\NDA Documents",
        r"G:\\My Drive\\Pitch Decks",
        r"G:\\My Drive\\Q-SMEC Overall DB",
    ]:
        if path.startswith(candidate):
            root = candidate
            break
    if root is None:
        root = "UNKNOWN"
    by_root[root].append(item)
    for kw in kws:
        by_keyword[kw].append(item)

# Keyword stats
kw_counts = {kw: len(items) for kw, items in by_keyword.items()}
kw_top = sorted(kw_counts.items(), key=lambda x: x[1], reverse=True)

# Build overlaps: keyword presence across roots
kw_roots = {}
for kw, items in by_keyword.items():
    roots = set()
    for it in items:
        p = it.get("path", "")
        if p.startswith(r"G:\\My Drive\\White Paper (Patent)"):
            roots.add("White Paper")
        elif p.startswith(r"G:\\My Drive\\NDA Documents"):
            roots.add("NDA Documents")
        elif p.startswith(r"G:\\My Drive\\Pitch Decks"):
            roots.add("Pitch Decks")
        elif p.startswith(r"G:\\My Drive\\Q-SMEC Overall DB"):
            roots.add("Overall DB")
    kw_roots[kw] = sorted(roots)

# Generate Markdown report
ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
report_md = [
    f"# Cross-Root Knowledge Report\n",
    f"Generated: {ts}\n",
    f"Source: {os.path.basename(summary_path)}\n",
    "\n",
    "## Summary\n",
    f"Total summarized docs: {len(summaries)}\n",
    "\n",
    "## Top Keywords\n",
]
for kw, cnt in kw_top[:25]:
    roots = ", ".join(kw_roots.get(kw, [])) or "(no root mapping)"
    report_md.append(f"- {kw}: {cnt} docs [{roots}]\n")

report_md.append("\n## Root Coverage\n")
for root, items in by_root.items():
    report_md.append(f"- {os.path.basename(root)}: {len(items)} summarized docs\n")

# Detailed sections for key Q-SMEC terms
sections = ["GaN", "AlN", "Ge", "Nb", "Ti", "graphene", "battery", "THz", "defect", "superconduct", "DFT", "HSE06", "QMC", "DOE"]
for kw in sections:
    items = by_keyword.get(kw, [])
    if not items:
        continue
    report_md.append(f"\n## {kw} References ({len(items)} docs)\n")
    for it in items[:50]:
        path = it.get("path", "")
        summ = it.get("summary", {})
        sample = summ.get("sample_head", [])
        sample_text = (" ".join(sample[:3])[:300] + "...") if sample else ""
        report_md.append(f"- {path}\n  - Sample: {sample_text}\n")

out_path = os.path.join(REPORTS_DIR, "cross_root_report.md")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("".join(report_md))

print(f"[WRITE] Cross-root report: {out_path}")
