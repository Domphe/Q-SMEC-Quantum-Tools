import os
import json
from pathlib import Path
from typing import List, Dict, Any

ROOT = Path(__file__).resolve().parents[2] if '__file__' in globals() else Path.cwd().parents[0]
SCAN_ROOT = Path('G:/My Drive/Databases')
OUT_DIR = ROOT / 'expert' / 'sources' / 'processed'
REPORT_PATH = ROOT / 'expert' / 'sources' / 'discovery_report.json'

SUPPORTED_EXT = {'.json', '.jsonl', '.csv', '.sqlite', '.db'}


def discover_files(base: Path) -> List[Path]:
    files = []
    for dirpath, dirnames, filenames in os.walk(base):
        for name in filenames:
            p = Path(dirpath) / name
            if p.suffix.lower() in SUPPORTED_EXT:
                files.append(p)
    return files


def normalize_record_from_path(p: Path) -> Dict[str, Any]:
    rel = p.as_posix().replace('G:/My Drive/', '')
    src_id = f"src.local.{rel.replace('/', '.').replace(' ', '_')}"
    record = {
        "id": src_id[:200],
        "type": "dataset" if p.suffix.lower() in {'.csv', '.sqlite', '.db'} else "other",
        "title": p.stem,
        "authors": [],
        "year": 0,
        "publisher": "local",
        "provenance": "local_filesystem",
        "url": p.as_uri() if p.exists() else "",
        "domains": ["quantum_chemistry"],
        "trust_tier": "C",
        "open_access": True,
        "notes": f"Discovered at {p.as_posix()}",
        "last_verified": "2025-12-01"
    }
    return record


def main():
    SCAN_ROOT.mkdir(parents=True, exist_ok=True)
    files = discover_files(SCAN_ROOT)
    print(f"[DISCOVERY] Found {len(files)} files under {SCAN_ROOT}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_records = []
    for p in files:
        try:
            rec = normalize_record_from_path(p)
            out_records.append(rec)
        except Exception as e:
            print(f"[WARN] Failed to normalize {p}: {e}")

    # Write discovery report
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps({
        "scan_root": SCAN_ROOT.as_posix(),
        "count": len(files),
        "files": [f.as_posix() for f in files[:1000]]
    }, indent=2), encoding='utf-8')

    # Persist normalized records as one JSON per file
    for rec in out_records:
        fname = rec['id'].replace('src.local.', '').replace('.', '_') + '.json'
        out_path = OUT_DIR / fname
        out_path.write_text(json.dumps({"raw_text": "", "facts": [], "equations": [], "citations": [], "quality": {"score": 0}, "meta": rec}, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f"[OK] Wrote {len(out_records)} normalized records to {OUT_DIR}")
    print(f"[OK] Discovery report at {REPORT_PATH}")


if __name__ == '__main__':
    main()
