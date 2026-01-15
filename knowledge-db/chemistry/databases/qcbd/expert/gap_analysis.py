"""Gap analysis utilities.

Heuristics:
 - Check for presence of recommended ontology sections
 - Identify if basis sets exist without associated accuracy metadata
 - Placeholder for cross-method benchmark coverage
"""
from __future__ import annotations
from typing import Dict, Any, List
from expert.load_expert_graph import load_graph

RECOMMENDED_KEYS = [
    'BenchmarkSets',  # expected collection of standardized benchmark datasets
    'ThermochemicalData',
    'ExcitedStateMethods'
]

def analyze() -> Dict[str, Any]:
    g = load_graph()
    missing = [k for k in RECOMMENDED_KEYS if k not in g]
    basis_sets = g.get('BasisSets', []) or g.get('Parameters', [])
    basis_missing_accuracy: List[str] = []
    for b in basis_sets:
        if isinstance(b, dict) and 'accuracy_level' not in b and 'effects_on_accuracy' not in b:
            basis_missing_accuracy.append(b.get('name','unknown'))
    return {
        'missing_sections': missing,
        'basis_sets_missing_accuracy_metadata': basis_missing_accuracy[:25]
    }

if __name__ == '__main__':
    import json
    print(json.dumps(analyze(), indent=2))
