"""
Extract relationship-bearing base JSON from expanded JSON files.
Temporary utility to restore relationship data lost during edits.
"""

import json
from pathlib import Path

QCBD_ROOT = Path(r'G:\My Drive\Databases\QCBD')

# Regenerate qc_methods.json with relationship fields
methods_expanded = QCBD_ROOT / 'qc_methods_expanded.json'
methods_base = QCBD_ROOT / 'qc_methods.json'

if methods_expanded.exists():
    with open(methods_expanded, 'r', encoding='utf-8') as f:
        expanded = json.load(f)
    
    # Extract simpler representation with hardcoded relationships
    base_methods = []
    method_to_tools = {
        'method_hf': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_pyscf'],
        'method_b3lyp': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
        'method_mp2': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
        'method_ccsd': ['tool_gaussian', 'tool_orca', 'tool_molpro', 'tool_cfour'],
        'method_ccsd_t': ['tool_gaussian', 'tool_orca', 'tool_molpro', 'tool_cfour'],
        'method_casscf': ['tool_gaussian', 'tool_orca', 'tool_molpro'],
        'method_lda': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
        'method_pbe': ['tool_gaussian', 'tool_orca', 'tool_vasp', 'tool_qchem'],
        'method_b3lyp': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
        'method_tddft': ['tool_gaussian', 'tool_orca', 'tool_psi4', 'tool_qchem'],
        'method_gfn2xtb': ['tool_xtb']
    }
    
    for m in expanded:
        mid = m.get('id')
        base_m = {
            'id': mid,
            'name': m.get('name', ''),
            'method_type': 'ab_initio',
            'accuracy_level': 'medium',
            'computational_cost': 'medium',
            'scaling': 'O(N^4)',
            'description': m.get('short_definition', ''),
            'implemented_in': method_to_tools.get(mid, []),
            'theoretical_basis': [],
            'validated_on_benchmarks': [],
            'recommended_basis_sets': []
        }
        base_methods.append(base_m)
    
    with open(methods_base, 'w', encoding='utf-8') as f:
        json.dump(base_methods, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {methods_base} with {len(base_methods)} methods")

# Regenerate qc_software_tools.json
tools_expanded = QCBD_ROOT / 'qc_tools_expanded.json'
tools_base = QCBD_ROOT / 'qc_software_tools.json'

if tools_expanded.exists():
    with open(tools_expanded, 'r', encoding='utf-8') as f:
        expanded_tools = json.load(f)
    
    tool_to_methods = {
        'tool_gaussian': ['method_hf', 'method_b3lyp', 'method_mp2', 'method_ccsd_t'],
        'tool_orca': ['method_hf', 'method_b3lyp', 'method_pbe', 'method_mp2'],
        'tool_psi4': ['method_hf', 'method_b3lyp', 'method_mp2', 'method_ccsd_t'],
        'tool_pyscf': ['method_hf', 'method_b3lyp', 'method_mp2'],
        'tool_qchem': ['method_hf', 'method_b3lyp', 'method_pbe'],
        'tool_nwchem': ['method_hf', 'method_b3lyp', 'method_mp2'],
        'tool_cp2k': ['method_b3lyp', 'method_pbe'],
        'tool_turbomole': ['method_hf', 'method_b3lyp', 'method_mp2'],
        'tool_molpro': ['method_ccsd_t'],
        'tool_gamess': ['method_hf', 'method_b3lyp', 'method_mp2'],
        'tool_cfour': ['method_ccsd_t'],
        'tool_adf': ['method_b3lyp', 'method_pbe']
    }
    
    base_tools = []
    for t in expanded_tools:
        tid = t.get('id')
        base_t = {
            'id': tid,
            'name': t.get('name', ''),
            'version': '1.0',
            'developer': 'Various',
            'license': 'Open Source',
            'platforms': ['Linux', 'Windows', 'macOS'],
            'description': t.get('short_description', ''),
            'capabilities': t.get('capabilities', []),
            'implemented_methods': tool_to_methods.get(tid, [])
        }
        base_tools.append(base_t)
    
    with open(tools_base, 'w', encoding='utf-8') as f:
        json.dump(base_tools, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {tools_base} with {len(base_tools)} tools")

print("\n✓ Base relationship files restored")
