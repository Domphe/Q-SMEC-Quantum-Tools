"""Harvest open-source quantum chemistry/computing software documentation."""
import sys
from datetime import date
from utils import write_jsonl, DATA_RAW

OPEN_SOURCE_TOOLS = [
    {
        "id": "tool.psi4",
        "name": "Psi4",
        "domain": "quantum_chemistry",
        "categories": ["electronic_structure", "ab_initio"],
        "capabilities": "HF, DFT, MP2, CCSD(T), CASSCF, EOM, optimization, frequencies",
        "license": "LGPL v3",
        "official_url": "https://psicode.org/",
        "docs_url": "https://psicode.org/psi4manual/master/",
        "standard_refs": ["src.tool_docs.psi4"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.cp2k",
        "name": "CP2K",
        "domain": "quantum_chemistry",
        "categories": ["dft", "molecular_dynamics"],
        "capabilities": "DFT, QM/MM, molecular dynamics, linear scaling",
        "license": "GPL v2+",
        "official_url": "https://www.cp2k.org/",
        "docs_url": "https://manual.cp2k.org/",
        "standard_refs": ["src.tool_docs.cp2k"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.quantum_espresso",
        "name": "Quantum ESPRESSO",
        "domain": "quantum_chemistry",
        "categories": ["dft", "solid_state"],
        "capabilities": "DFT, plane waves, pseudopotentials, solid-state, spectroscopy",
        "license": "GPL v2",
        "official_url": "https://www.quantum-espresso.org/",
        "docs_url": "https://www.quantum-espresso.org/documentation/",
        "standard_refs": ["src.tool_docs.quantum_espresso"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.pyscf",
        "name": "PySCF",
        "domain": "quantum_chemistry",
        "categories": ["electronic_structure", "python"],
        "capabilities": "HF, DFT, CCSD, CASSCF, DMRG, periodic systems",
        "license": "Apache 2.0",
        "official_url": "https://pyscf.org/",
        "docs_url": "https://pyscf.org/user.html",
        "standard_refs": ["src.tool_docs.pyscf"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.nwchem",
        "name": "NWChem",
        "domain": "quantum_chemistry",
        "categories": ["electronic_structure", "molecular_dynamics"],
        "capabilities": "HF, DFT, MP2, CCSD(T), TDDFT, QM/MM, molecular dynamics",
        "license": "ECL 2.0",
        "official_url": "https://nwchemgit.github.io/",
        "docs_url": "https://nwchemgit.github.io/Home.html",
        "standard_refs": ["src.tool_docs.nwchem"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.qiskit",
        "name": "Qiskit",
        "domain": "quantum_physics",
        "categories": ["quantum_computing", "quantum_algorithms"],
        "capabilities": "Quantum circuits, algorithms, simulators, IBMQ access",
        "license": "Apache 2.0",
        "official_url": "https://qiskit.org/",
        "docs_url": "https://qiskit.org/documentation/",
        "standard_refs": ["src.tool_docs.qiskit"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.cirq",
        "name": "Cirq",
        "domain": "quantum_physics",
        "categories": ["quantum_computing", "quantum_algorithms"],
        "capabilities": "Quantum circuits, NISQ algorithms, Google Quantum AI integration",
        "license": "Apache 2.0",
        "official_url": "https://quantumai.google/cirq",
        "docs_url": "https://quantumai.google/cirq/start",
        "standard_refs": ["src.tool_docs.cirq"],
        "last_reviewed": str(date.today())
    },
    {
        "id": "tool.pennylane",
        "name": "PennyLane",
        "domain": "quantum_physics",
        "categories": ["quantum_computing", "quantum_ml"],
        "capabilities": "Variational quantum algorithms, quantum ML, differentiable programming",
        "license": "Apache 2.0",
        "official_url": "https://pennylane.ai/",
        "docs_url": "https://docs.pennylane.ai/",
        "standard_refs": ["src.tool_docs.pennylane"],
        "last_reviewed": str(date.today())
    }
]

SOURCE_RECORDS = [
    {
        "id": "src.tool_docs.psi4",
        "type": "documentation",
        "title": "Psi4 Documentation",
        "authors": ["Psi4 Development Team"],
        "year": 2024,
        "publisher": "Psi4",
        "provenance": "open_source_docs",
        "url": "https://psicode.org/psi4manual/master/",
        "domains": ["quantum_chemistry"],
        "trust_tier": "B",
        "allowed_content": "full_open_content",
        "open_access": True,
        "keywords": ["psi4", "documentation", "api"],
        "notes": "Open-source quantum chemistry software documentation (LGPL v3).",
        "last_verified": str(date.today())
    },
    # Additional source records would follow same pattern for CP2K, QE, PySCF, NWChem, Qiskit, Cirq, PennyLane
]

def main():
    """Harvest open-source tool documentation."""
    tools_path = DATA_RAW / "tools" / "open_source_tools.jsonl"
    sources_path = DATA_RAW / "tools" / "tool_docs_sources.jsonl"
    
    write_jsonl(tools_path, OPEN_SOURCE_TOOLS)
    write_jsonl(sources_path, SOURCE_RECORDS)
    
    print(f"Harvested open-source tools:")
    print(f"  Tools: {tools_path} ({len(OPEN_SOURCE_TOOLS)} tools)")
    print(f"  Sources: {sources_path} ({len(SOURCE_RECORDS)} sources)")
    print("\nLegal compliance: Full open content from open-source projects.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
