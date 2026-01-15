"""Load and merge base QC knowledge graph with domain extension."""

from pathlib import Path
import json
from typing import Dict, Any
import os

QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
BASE_GRAPH = QCBD_ROOT / 'qc_knowledge_graph_full.json'
EXT_GRAPH = QCBD_ROOT / 'qc_domain_extension.json'
ALT_EXT_GRAPH = QCBD_ROOT / 'expert' / 'domain_extension.json'
PHYSICS_EXT = QCBD_ROOT / 'expert' / 'physics_extension.json'


def load_graph() -> Dict[str, Any]:
    if not BASE_GRAPH.exists():
        raise FileNotFoundError(f"Base graph missing: {BASE_GRAPH}")
    with open(BASE_GRAPH, 'r', encoding='utf-8') as f:
        base = json.load(f)
    
    INLINE_EXTENSION = {
        "Hamiltonians": [
            {"id": "hamiltonian_electronic_non_relativistic_inline", "name": "Electronic Hamiltonian (NR)", "description": "Fallback inline non-relativistic electronic Hamiltonian."}
        ],
        "BasisSets": [
            {"id": "basisset_minimal_inline", "name": "Minimal Inline Basis", "type": "Minimal", "description": "Fallback inline minimal basis placeholder."}
        ],
        "ManyBodyMethods": [
            {"id": "mb_inline_dmft", "name": "Inline DMFT", "description": "Fallback placeholder for DMFT."}
        ]
    }

    candidate = None
    if EXT_GRAPH.exists():
        candidate = EXT_GRAPH
    if (candidate is None or not candidate.read_text(encoding='utf-8').strip()) and ALT_EXT_GRAPH.exists():
        candidate = ALT_EXT_GRAPH
    ext = {}
    physics_ext = {}
    if candidate:
        raw = candidate.read_text(encoding='utf-8')
        if not raw.strip():
            print(f"Warning: extension file empty: {candidate}")
        else:
            try:
                ext = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"Extension JSON decode error in {candidate}: {e}. First 120 chars: {raw[:120]!r}")
    else:
        ext = {}

    # If extension ended up empty, apply inline fallback
    if not any(isinstance(v, list) and v for v in ext.values()):
        print("Info: applying inline expert extension fallback")
        ext = INLINE_EXTENSION

    if PHYSICS_EXT.exists():
        pr = PHYSICS_EXT.read_text(encoding='utf-8')
        if pr.strip():
            try:
                physics_ext = json.loads(pr)
            except json.JSONDecodeError as e:
                print(f"Physics extension decode error: {e}")
    
    # Merge new entity collections if not already present
    merged = dict(base)
    added_types = []
    for key, value in ext.items():
        if key.startswith('metadata_'):
            continue
        if isinstance(value, list):
            if key not in merged:
                merged[key] = value
                added_types.append(key)
            else:
                # Append while avoiding duplicate IDs
                existing_ids = {e['id'] for e in merged[key] if isinstance(e, dict) and 'id' in e}
                for entry in value:
                    if entry.get('id') not in existing_ids:
                        merged[key].append(entry)
                added_types.append(key)

    for key, value in physics_ext.items():
        if key.startswith('metadata_'):
            continue
        if isinstance(value, list):
            if key not in merged:
                merged[key] = value
                added_types.append(key)
            else:
                existing_ids = {e['id'] for e in merged[key] if isinstance(e, dict) and 'id' in e}
                for entry in value:
                    if entry.get('id') not in existing_ids:
                        merged[key].append(entry)
                added_types.append(key)
    
    # Extend metadata
    meta = merged.get('metadata', {})
    ext_meta = ext.get('metadata_extension', {})
    phys_meta = physics_ext.get('metadata_extension', {})
    combined_domains = list({*(ext_meta.get('domain', []) or []), *(phys_meta.get('domain', []) or [])})
    meta['expert_layer'] = {
        'domains': combined_domains,
        'version': ext_meta.get('version', phys_meta.get('version', '0.0.0')),
        'added_entity_types': list(set(ext_meta.get('added_entity_types', []) + phys_meta.get('added_entity_types', [])))
    }
    merged['metadata'] = meta
    
    return merged


def summarize_graph(graph: Dict[str, Any]) -> Dict[str, Any]:
    summary = {}
    for key, value in graph.items():
        if isinstance(value, list):
            summary[key] = len(value)
    return summary


def main():
    graph = load_graph()
    summary = summarize_graph(graph)
    print("=== Expert Graph Summary ===")
    for k, v in sorted(summary.items()):
        print(f"{k}: {v}")
    print("\nExpert layer domains:", graph['metadata'].get('expert_layer', {}).get('domains'))

if __name__ == '__main__':
    main()
