import re
import json
from pathlib import Path
from datetime import datetime

REPORT_PATH = Path("G:/My Drive/Databases/QCBD/reports/cross_root_report.md")
OUT_ENTITIES = Path("G:/My Drive/Databases/QCBD/reports/entity_inserts_proposals.json")
OUT_BRIEF = Path("G:/My Drive/Databases/QCBD/reports/next_steps_brief.md")


MATERIAL_KEYWORDS = [
    "GaN", "AlN", "graphene", "Nb", "Ti", "Ge", "PB", "PBA", "Prussian Blue",
]
METHOD_KEYWORDS = [
    "DFT", "HSE06", "THz", "DOE",
]
DATASET_MARKERS = [
    "benchmarks", "Benchmark", "Verified", "Gap Analysis",
]


def load_report():
    if not REPORT_PATH.exists():
        raise FileNotFoundError(f"Report not found: {REPORT_PATH}")
    return REPORT_PATH.read_text(encoding="utf-8", errors="ignore")


def extract_sections(md: str):
    sections = {}
    current = None
    for line in md.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
        elif current:
            sections[current].append(line)
    return sections


def gather_refs(lines):
    refs = []
    for i, line in enumerate(lines):
        if line.startswith("- ") and ":\\" in line:
            path = line[2:].strip()
            sample = None
            # Look ahead for sample line
            if i + 1 < len(lines) and lines[i + 1].strip().startswith("- Sample:"):
                sample = lines[i + 1].strip().replace("- Sample:", "").strip()
            refs.append({"path": path, "sample": sample})
    return refs


def find_entities(md: str):
    sections = extract_sections(md)
    entities = {"materials": {}, "methods": {}, "datasets": {}}

    # Keyword-driven extraction from Top Keywords sections and per-keyword references
    for sec_name, lines in sections.items():
        lower_name = sec_name.lower()
        refs = gather_refs(lines)
        # Materials
        for kw in MATERIAL_KEYWORDS:
            if kw.lower() in lower_name:
                entities["materials"].setdefault(kw, []).extend(refs)
        # Methods
        for kw in METHOD_KEYWORDS:
            if kw.lower() in lower_name:
                entities["methods"].setdefault(kw, []).extend(refs)
        # Datasets
        if any(m.lower() in lower_name for m in ["references", "top keywords", "root coverage"]):
            # Skip meta sections
            continue
        if any(marker.lower() in lower_name for marker in ["benchmarks", "verified", "gap analysis"]):
            entities["datasets"].setdefault(sec_name, []).extend(refs)

    # Scan entire doc for dataset markers to pick up additional references
    dataset_refs = []
    for m in re.finditer(r"-\s+G:\\\\My Drive\\[^\n]+", md):
        line = m.group(0)
        if any(dm.lower() in md[max(0, m.start()-200):m.end()+200].lower() for dm in DATASET_MARKERS):
            dataset_refs.append(line[2:].strip())
    if dataset_refs:
        entities["datasets"].setdefault("General Benchmarks", []).extend(
            [{"path": p, "sample": None} for p in dataset_refs]
        )

    return entities


def propose_registry_inserts(entities):
    proposals = {
        "generated_at": datetime.utcnow().isoformat(),
        "materials": [],
        "methods": [],
        "datasets": [],
    }

    def uniq_by_path(items):
        seen = set()
        out = []
        for it in items:
            p = it.get("path")
            if p and p not in seen:
                seen.add(p)
                out.append(it)
        return out

    for mat, refs in entities.get("materials", {}).items():
        proposals["materials"].append({
            "name": mat,
            "type": "material",
            "sources": uniq_by_path(refs),
        })
    for meth, refs in entities.get("methods", {}).items():
        proposals["methods"].append({
            "name": meth,
            "type": "method",
            "sources": uniq_by_path(refs),
        })
    for dname, refs in entities.get("datasets", {}).items():
        proposals["datasets"].append({
            "name": dname,
            "type": "dataset",
            "sources": uniq_by_path(refs),
        })
    return proposals


def write_next_steps_brief(entities):
    lines = []
    lines.append("# Targeted Next Steps")
    lines.append("")
    lines.append("## THz Detector Benchmarks")
    lines.append("- Collect and normalize THz metrics (NEP, responsivity, bandwidth, dynamic range) from referenced pitch decks and docx samples.")
    lines.append("- Cross-verify with peer-reviewed references indicated in 'peer-reviewed benchmarks' sources.")
    lines.append("- Map to QCBD sets: THz-Response, SCONF21 for optical/material coupling.")
    lines.append("")
    lines.append("## Prussian Blue (PB/PBA) Battery Targets")
    lines.append("- Extract energy density (Wh/kg), cycle life, rate capability and voltage profiles from Gap Analysis and Verified Benchmarks sections.")
    lines.append("- Align targets against Battery24 set; flag gaps where proposal exceeds current verified performance.")
    lines.append("- Create overlay charts in `reports/` with proposal vs. verified ranges.")
    lines.append("")
    lines.append("## Materials and Methods Inserts")
    lines.append("- Add materials: GaN, AlN, graphene, Nb, Ti, Ge, Prussian Blue/PBA to registry with linked sources.")
    lines.append("- Add methods: DFT, HSE06, THz measurement, DOE to methods table with provenance.")
    lines.append("- Associate dataset entries with source paths for reproducibility.")
    lines.append("")
    lines.append("## Immediate Actions")
    lines.append("- Approve proposed inserts JSON for ingestion into QCBD.")
    lines.append("- Schedule data extraction for THz and PB benchmarks; generate normalized CSVs.")
    lines.append("- Update materials taxonomy in docs with cross-root coverage summary.")

    OUT_BRIEF.write_text("\n".join(lines), encoding="utf-8")


def main():
    md = load_report()
    entities = find_entities(md)
    proposals = propose_registry_inserts(entities)
    OUT_ENTITIES.write_text(json.dumps(proposals, indent=2), encoding="utf-8")
    write_next_steps_brief(entities)
    print(f"[WRITE] Proposed inserts: {OUT_ENTITIES}")
    print(f"[WRITE] Next steps brief: {OUT_BRIEF}")


if __name__ == "__main__":
    main()
