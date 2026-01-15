"""Context pack builder for LLM consumption.
Enriches with concept matches and ranking metadata.
"""
from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
import json, os
from expert.query_api import list_methods, suggest

QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
BASE_GRAPH = QCBD_ROOT / 'qc_knowledge_graph_full.json'

def _load_graph() -> Dict[str, Any]:
    if not BASE_GRAPH.exists(): return {}
    try: return json.loads(BASE_GRAPH.read_text(encoding='utf-8'))
    except Exception: return {}

def build_context(query: str, top: int = 5) -> Dict[str, Any]:
    graph = _load_graph()
    concepts = graph.get('Concepts', [])
    concept_hits = [c for c in concepts if query.lower() in (c.get('name','') + ' ' + c.get('long_explanation','')).lower()][:top]
    method_suggestions = suggest(query, limit=top)
    method_index = {m['id']: m for m in list_methods()}
    enriched_methods = [method_index[m['id']] for m in method_suggestions if m['id'] in method_index]
    return {
        'query': query,
        'concepts': [{'id': c['id'], 'name': c['name'], 'short_definition': c.get('short_definition')} for c in concept_hits],
        'methods': enriched_methods,
        'summary': f"Matched {len(concept_hits)} concepts and {len(enriched_methods)} methods for query '{query}'.",
        'metadata': {
            'version': '0.2',
            'source': 'expert-layer',
            'total_concepts': len(concepts),
            'total_methods': len(graph.get('Methods', []))
        }
    }

if __name__ == '__main__':
    import pprint
    pprint.pprint(build_context('electron correlation'))
