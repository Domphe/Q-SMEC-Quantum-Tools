"""Secure Query API for expert layer.
Provides listing, filtering, ranking, comparison, and suggestion utilities.
"""
from __future__ import annotations
from typing import List, Dict, Any, Optional, Callable
import sqlite3, json, os
from pathlib import Path
from expert.reasoning import method_metrics

QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
DB_PATH = QCBD_ROOT / 'qc_graph.db'
BASE_GRAPH = QCBD_ROOT / 'qc_knowledge_graph_full.json'

def _connect():
    return sqlite3.connect(str(DB_PATH))

def _load_methods_sqlite() -> List[Dict[str, Any]]:
    if not DB_PATH.exists():
        return []
    conn = _connect(); conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id,name,properties FROM nodes WHERE label='Method' ORDER BY name")
    rows = cur.fetchall(); conn.close()
    out=[]
    for r in rows:
        try:
            props = json.loads(r['properties']) if r['properties'] else {}
        except Exception:
            props = {}
        props['id'] = r['id']; props['name'] = r['name']
        out.append(props)
    return out

def _load_methods_json() -> List[Dict[str, Any]]:
    if not BASE_GRAPH.exists():
        return []
    try:
        data = json.loads(BASE_GRAPH.read_text(encoding='utf-8'))
        return data.get('Methods', [])
    except Exception:
        return []

def list_methods(limit: Optional[int]=None) -> List[Dict[str, Any]]:
    methods = _load_methods_sqlite() or _load_methods_json()
    if limit: methods = methods[:limit]
    return [{**m, **method_metrics(m)} for m in methods]

def filter_methods(min_accuracy: float=0.0, max_cost: Optional[float]=None, tags: Optional[List[str]]=None) -> List[Dict[str, Any]]:
    out=[]
    for m in list_methods():
        acc = m.get('accuracy') or m.get('accuracy_level') or 0
        cost = m.get('cost') or m.get('computational_cost') or 0
        if acc < min_accuracy: continue
        if max_cost is not None and cost and cost > max_cost: continue
        if tags:
            present = set(m.get('tags', []))
            if not all(t in present for t in tags):
                continue
        out.append(m)
    return out

def rank_methods(score_fn: Optional[Callable[[Dict[str, Any]], float]]=None, limit: int=10) -> List[Dict[str, Any]]:
    methods = list_methods()
    if not score_fn:
        score_fn = lambda m: m['composite_score']
    ranked = sorted(methods, key=score_fn, reverse=True)
    return ranked[:limit]

def method_detail(method_id: str) -> Dict[str, Any]:
    for m in list_methods():
        if m['id'] == method_id:
            return m
    return {}

def compare(method_ids: List[str]) -> List[Dict[str, Any]]:
    idx = {m['id']: m for m in list_methods()}
    rows=[]
    for mid in method_ids:
        m = idx.get(mid);
        if not m: continue
        rows.append({
            'id': mid,
            'name': m.get('name'),
            'accuracy': m.get('accuracy'),
            'cost': m.get('cost'),
            'efficiency_score': m.get('efficiency_score'),
            'scaling': m.get('scaling'),
            'tags': m.get('tags', [])
        })
    return rows

def suggest(goal: str, max_cost: Optional[float]=None, limit: int=5) -> List[Dict[str, Any]]:
    goal_low = goal.lower(); candidates=[]
    for m in list_methods():
        blob = ' '.join([m.get('long_explanation',''), ' '.join(m.get('tags', []))]).lower()
        score = sum(1 for tok in goal_low.split() if tok in blob)
        if goal_low in blob: score += 5
        cost = m.get('cost') or 0
        if max_cost is not None and cost and cost > max_cost: continue
        candidates.append({'id': m['id'], 'name': m['name'], 'match_score': score, 'cost': cost})
    return sorted(candidates, key=lambda x: x['match_score'], reverse=True)[:limit]

if __name__ == '__main__':
    print("Top Ranked Methods:")
    for r in rank_methods(limit=5):
        print(r['name'], r['composite_score'])
    print("\nFilter accuracy>=5 cost<=5:")
    for f in filter_methods(min_accuracy=5, max_cost=5):
        print(f['name'], f['accuracy'], f['cost'])
    print("\nSuggest 'electron correlation':")
    for s in suggest('electron correlation'): print(s)
