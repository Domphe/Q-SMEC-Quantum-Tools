"""Lightweight semantic search over Methods using deterministic hash embeddings.

Design goals:
 - Zero external dependencies (pure standard library)
 - Deterministic, reproducible embeddings for offline environments
 - Graceful handling of missing / empty method lists
 - Optional persistence to SQLite (table: embeddings)

Vector construction:
 Each token is lowercased; sha256(token).hexdigest() -> int -> bucket index (mod DIM).
 Bucket value += 1 / (token_index + 1) to lightly weight early tokens.
 Cosine similarity used for ranking. All vectors kept dense length DIM.
"""
from __future__ import annotations
from typing import List, Dict, Any, Tuple
import hashlib, math, json, sqlite3, os
from pathlib import Path

DIM = 64
QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
SQLITE_DB = QCBD_ROOT / 'qc_graph.db'

def _tokenize(text: str) -> List[str]:
    if not text: return []
    # Replace punctuation with spaces, simple normalization
    for ch in ',;:\n\r\t()[]{}<>/\\' :
        text = text.replace(ch, ' ')
    return [t for t in text.lower().split(' ') if t]

def _embed(text: str) -> List[float]:
    tokens = _tokenize(text)
    vec = [0.0] * DIM
    for i, tok in enumerate(tokens):
        h = hashlib.sha256(tok.encode()).hexdigest()
        bucket = int(h, 16) % DIM
        vec[bucket] += 1.0 / (i + 1)
    # L2 normalize for cosine similarity stability
    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v / norm for v in vec]

def _load_methods() -> List[Dict[str, Any]]:
    # Reuse reasoning internal loader if available for consistency
    try:
        from expert import reasoning
        return reasoning._load_methods()  # type: ignore[attr-defined]
    except Exception:
        return []

def build_embeddings(persist: bool = True) -> Dict[str, List[float]]:
    methods = _load_methods()
    emb_map: Dict[str, List[float]] = {}
    if not methods:
        return emb_map
    for m in methods:
        mid = m.get('id') or m.get('name') or f"method_{len(emb_map)}"
        text = ' '.join([
            str(m.get('name','')),
            str(m.get('description','')),
            ' '.join(m.get('tags', []))
        ])
        emb_map[mid] = _embed(text)
    if persist and SQLITE_DB.exists():
        try:
            conn = sqlite3.connect(str(SQLITE_DB))
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS embeddings (method_id TEXT PRIMARY KEY, name TEXT, vector TEXT)")
            for m in methods:
                mid = m.get('id') or m.get('name')
                if not mid: continue
                name = m.get('name','')
                vec = json.dumps(emb_map[mid])
                cur.execute("INSERT OR REPLACE INTO embeddings(method_id,name,vector) VALUES (?,?,?)", (mid, name, vec))
            conn.commit(); conn.close()
        except Exception:
            pass
    return emb_map

def _cosine(a: List[float], b: List[float]) -> float:
    return sum(x*y for x,y in zip(a,b))

def search_methods(query: str, top_k: int = 5, ensure_built: bool = True) -> List[Dict[str, Any]]:
    if ensure_built:
        # Attempt load from SQLite first
        if SQLITE_DB.exists():
            try:
                conn = sqlite3.connect(str(SQLITE_DB)); cur = conn.cursor()
                cur.execute("SELECT method_id, name, vector FROM embeddings")
                rows = cur.fetchall(); conn.close()
                if rows:
                    method_vecs = [(r[0], r[1], json.loads(r[2])) for r in rows]
                else:
                    emb_map = build_embeddings(persist=True)
                    method_vecs = [(mid, '', vec) for mid, vec in emb_map.items()]
            except Exception:
                emb_map = build_embeddings(persist=False)
                method_vecs = [(mid, '', vec) for mid, vec in emb_map.items()]
        else:
            emb_map = build_embeddings(persist=False)
            # Need names for readability
            methods = _load_methods()
            name_lookup = {m.get('id') or m.get('name'): m.get('name') for m in methods}
            method_vecs = [(mid, name_lookup.get(mid,''), vec) for mid, vec in emb_map.items()]
    else:
        emb_map = build_embeddings(persist=False)
        methods = _load_methods()
        name_lookup = {m.get('id') or m.get('name'): m.get('name') for m in methods}
        method_vecs = [(mid, name_lookup.get(mid,''), vec) for mid, vec in emb_map.items()]

    if not method_vecs:
        return []
    q_vec = _embed(query)
    scored: List[Tuple[str,str,float]] = []
    for mid, name, vec in method_vecs:
        score = _cosine(q_vec, vec)
        scored.append((mid, name, score))
    ranked = sorted(scored, key=lambda x: x[2], reverse=True)[:top_k]
    return [{"method_id": mid, "name": name, "similarity": round(score,4)} for mid, name, score in ranked]

if __name__ == '__main__':
    print("Building embeddings...")
    build_embeddings(persist=True)
    print("Search examples:")
    for q in ["correlation", "density functional", "coupled cluster"]:
        print(q, '->', search_methods(q))
