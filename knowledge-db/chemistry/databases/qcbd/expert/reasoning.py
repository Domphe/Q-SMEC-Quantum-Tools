"""Expert reasoning metrics for quantum chemistry & physics entities.
Extends simple scalar metrics with composite scores and graceful missing-field handling.
"""
from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
import os, json, sqlite3

QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
SQLITE_DB = QCBD_ROOT / 'qc_graph.db'
BASE_GRAPH = QCBD_ROOT / 'qc_knowledge_graph_full.json'

def _num(val, default=0.0):
    try:
        if val is None: return default
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str) and val.strip(): return float(val)
    except Exception: return default
    return default

def method_metrics(method: Dict[str, Any]) -> Dict[str, Any]:
    cost = _num(method.get('computational_cost', method.get('cost')), 0.0)
    acc = _num(method.get('accuracy_level', method.get('accuracy')), 0.0)
    scaling = (method.get('scaling') or 'unknown').lower()
    scaling_score = 4
    for pat, score in [('n^7',1),('n^6',2),('n^5',3),('n^4',5),('linear',8)]:
        if pat in scaling: scaling_score = score; break
    efficiency = acc / (cost if cost else 1.0)
    composite = efficiency * (0.6 + 0.4 * (scaling_score/8.0))
    return {
        'id': method.get('id'),
        'name': method.get('name'),
        'efficiency_score': round(efficiency,3),
        'composite_score': round(composite,3),
        'cost': cost,
        'accuracy': acc,
        'scaling': scaling,
        'scaling_score': scaling_score
    }

def basis_set_quality(basis: Dict[str, Any]) -> Dict[str, Any]:
    acc = _num(basis.get('accuracy_level'),0.0)
    cost = _num(basis.get('computational_cost'),0.0)
    ratio = acc / (cost if cost else 1.0)
    return {
        'id': basis.get('id'),
        'name': basis.get('name'),
        'accuracy': acc,
        'cost': cost,
        'acc_cost_ratio': round(ratio,3)
    }

def _load_methods() -> List[Dict[str, Any]]:
    if SQLITE_DB.exists():
        conn = sqlite3.connect(str(SQLITE_DB)); conn.row_factory = sqlite3.Row
        cur = conn.cursor(); cur.execute("SELECT properties FROM nodes WHERE label='Method'")
        rows = cur.fetchall(); methods=[]
        for r in rows:
            try: methods.append(json.loads(r['properties']))
            except Exception: pass
        conn.close();
        if methods: return methods
    if BASE_GRAPH.exists():
        try:
            data = json.loads(BASE_GRAPH.read_text(encoding='utf-8'))
            return data.get('Methods', [])
        except Exception: return []
    return []

def ranked_methods(limit=5) -> List[Dict[str, Any]]:
    ms = _load_methods()
    scored = [method_metrics(m) for m in ms]
    return sorted(scored, key=lambda x: x['composite_score'], reverse=True)[:limit]

if __name__ == '__main__':
    for m in ranked_methods():
        print(f"{m['name']}: composite={m['composite_score']} efficiency={m['efficiency_score']} cost={m['cost']} acc={m['accuracy']}")
