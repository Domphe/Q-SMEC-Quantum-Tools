"""Snapshot & diff utilities for expert knowledge graph.

Snapshots allow tracking evolution of ontology & method metadata.
Diff reports highlight added / removed top-level entities and count deltas.
"""

from __future__ import annotations

import datetime
import json
import os
from pathlib import Path
from typing import Any, Dict

# Use C: drive path (G: drive doesn't exist)
QCBD_ROOT = Path(os.environ.get("QCBD_ROOT")) if os.environ.get("QCBD_ROOT") else None
if not QCBD_ROOT:
    # Try common paths in priority order
    for candidate in [
        r"C:\Users\domph\My Drive (s.dely@niketllc.com)\Databases\QCBD",
        Path(__file__).parent.parent,
    ]:
        candidate_path = Path(candidate)
        if candidate_path.exists():
            QCBD_ROOT = candidate_path
            break
if not QCBD_ROOT:
    QCBD_ROOT = Path(__file__).parent.parent

SNAPSHOT_DIR = QCBD_ROOT / "expert" / "snapshots"
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def _load_graph() -> Dict[str, Any]:
    from expert.load_expert_graph import load_graph

    return load_graph()


def create_snapshot(name: str | None = None) -> Path:
    g = _load_graph()
    ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    fname = f"snapshot_{name + '_' if name else ''}{ts}.json"
    path = SNAPSHOT_DIR / fname
    with open(path, "w", encoding="utf-8") as f:
        json.dump(g, f, indent=2)
    return path


def diff_snapshots(a: Path, b: Path) -> Dict[str, Any]:
    def load(p: Path) -> Dict[str, Any]:
        return json.loads(p.read_text(encoding="utf-8"))

    ga, gb = load(a), load(b)
    keys = sorted(set(ga.keys()) | set(gb.keys()))
    report = {"a": a.name, "b": b.name, "changes": []}
    for k in keys:
        va, vb = ga.get(k), gb.get(k)
        if isinstance(va, list) and isinstance(vb, list):
            if len(va) != len(vb):
                report["changes"].append(
                    {
                        "key": k,
                        "a_count": len(va),
                        "b_count": len(vb),
                        "delta": len(vb) - len(va),
                    }
                )
        elif va != vb:
            report["changes"].append({"key": k, "changed": True})
    return report


if __name__ == "__main__":
    snap = create_snapshot()
    print("Created snapshot:", snap)
