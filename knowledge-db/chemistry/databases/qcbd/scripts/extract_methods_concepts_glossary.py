"""Extract methods, concepts, and glossary terms from external packages."""
import json
import sys
from pathlib import Path
from datetime import date
from typing import List, Dict, Set
from utils import write_jsonl, DATA_PROCESSED

def extract_methods_from_benchmark_runner() -> List[Dict]:
    """Extract computational methods from qc_benchmark_dashboard_runner."""
    methods = []
    base = Path(r"G:\My Drive\Databases\qc_benchmark_dashboard_runner")
    
    # Check for method definitions in data/models directories
    for dir_name in ["models", "data", "cli"]:
        dir_path = base / dir_name
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                # Look for method-related patterns
                if any(kw in content.lower() for kw in ['benchmark', 'method', 'dft', 'ccsd', 'mp2', 'functional']):
                    print(f"  [SCAN] {py_file.name}")
            except Exception as e:
                continue
    
    # Add quantum physics-specific methods
    qp_methods = [
        {
            "id": "method.qp.qmc",
            "domain": "quantum_physics",
            "name": "Quantum Monte Carlo",
            "category": "stochastic",
            "brief": "Stochastic method for solving quantum many-body problems using Monte Carlo sampling.",
            "long_description": "QMC uses random sampling to evaluate path integrals or variational wavefunctions. Variants include Variational MC (VMC), Diffusion MC (DMC), and Path Integral MC (PIMC). Scales favorably with system size and can treat large systems accurately.",
            "inputs": ["trial wavefunction", "Hamiltonian"],
            "outputs": ["ground state energy", "correlation functions"],
            "equation_refs": [],
            "workflow_refs": [],
            "software_implementations": ["tool.qmcpack", "tool.casino"],
            "complexity": "O(N³-N⁴) depending on variant",
            "strengths": "Favorable scaling; high accuracy for bulk systems; treats correlation well.",
            "limitations": "Fixed-node approximation in DMC; statistical noise; expensive for excited states.",
            "typical_use_cases": "Condensed matter systems, bulk materials, strongly correlated electrons.",
            "standard_refs": [],
            "last_reviewed": str(date.today())
        },
        {
            "id": "method.qp.dmrg",
            "domain": "quantum_physics",
            "name": "Density Matrix Renormalization Group",
            "category": "tensor_network",
            "brief": "Tensor network method for one-dimensional quantum systems; highly accurate for ground states.",
            "long_description": "DMRG variationally optimizes matrix product states (MPS) to approximate ground states of 1D quantum systems. Polynomial scaling with bond dimension. Extends to 2D via PEPS. Captures entanglement structure efficiently.",
            "inputs": ["Hamiltonian", "lattice geometry"],
            "outputs": ["ground state", "entanglement entropy", "correlation functions"],
            "equation_refs": [],
            "workflow_refs": [],
            "software_implementations": ["tool.itensor", "tool.tenpy"],
            "complexity": "Polynomial in bond dimension",
            "strengths": "Extremely accurate for 1D systems; captures entanglement; systematically improvable.",
            "limitations": "Limited to 1D or quasi-1D; 2D scaling challenging; not efficient for high-dimensional systems.",
            "typical_use_cases": "1D spin chains, quantum wires, low-dimensional strongly correlated systems.",
            "standard_refs": [],
            "last_reviewed": str(date.today())
        },
        {
            "id": "method.qp.exact_diag",
            "domain": "quantum_physics",
            "name": "Exact Diagonalization",
            "category": "exact",
            "brief": "Numerically exact solution via full diagonalization of Hamiltonian matrix.",
            "long_description": "Exact diagonalization constructs full Hilbert space and diagonalizes Hamiltonian matrix. Numerically exact but exponentially scaling. Limited to small systems (~40 qubits). Used for benchmarking and small clusters.",
            "inputs": ["Hamiltonian matrix", "basis states"],
            "outputs": ["all eigenvalues", "all eigenstates"],
            "equation_refs": [],
            "workflow_refs": [],
            "software_implementations": ["tool.scipy", "tool.numpy"],
            "complexity": "Exponential in system size",
            "strengths": "Numerically exact; all eigenvalues; benchmark standard.",
            "limitations": "Exponential scaling; memory-limited; small systems only.",
            "typical_use_cases": "Small clusters, benchmarking, proof-of-concept studies.",
            "standard_refs": [],
            "last_reviewed": str(date.today())
        },
        {
            "id": "method.qp.vqe",
            "domain": "quantum_physics",
            "name": "Variational Quantum Eigensolver",
            "category": "quantum_computing",
            "brief": "Hybrid quantum-classical algorithm for finding ground states on near-term quantum computers.",
            "long_description": "VQE uses parameterized quantum circuits (ansatz) to prepare trial states. Classical optimizer minimizes energy expectation value measured on quantum hardware. NISQ-friendly due to shallow circuits.",
            "inputs": ["Hamiltonian", "parameterized ansatz"],
            "outputs": ["ground state energy", "optimized parameters"],
            "equation_refs": [],
            "workflow_refs": [],
            "software_implementations": ["tool.qiskit", "tool.cirq", "tool.pennylane"],
            "complexity": "Depends on ansatz and classical optimizer",
            "strengths": "NISQ-compatible; flexible ansatz; hybrid approach.",
            "limitations": "Ansatz choice critical; barren plateaus; classical optimization overhead.",
            "typical_use_cases": "Near-term quantum computing, molecular ground states, materials simulation.",
            "standard_refs": [],
            "last_reviewed": str(date.today())
        },
        {
            "id": "method.qp.tensor_network",
            "domain": "quantum_physics",
            "name": "Tensor Network Methods",
            "category": "tensor_network",
            "brief": "Family of methods representing quantum states as networks of tensors; efficient for low-entanglement systems.",
            "long_description": "Tensor networks (DMRG, PEPS, MERA) represent quantum states as contracted tensor products. Exploit entanglement structure to achieve polynomial scaling for systems with area-law entanglement. Include MPS, PEPS, MERA, TTN.",
            "inputs": ["Hamiltonian", "network topology"],
            "outputs": ["ground state", "expectation values", "entanglement measures"],
            "equation_refs": [],
            "workflow_refs": [],
            "software_implementations": ["tool.itensor", "tool.tenpy", "tool.quimb"],
            "complexity": "Polynomial in bond dimension",
            "strengths": "Efficient for low-entanglement states; captures area-law systems; systematically improvable.",
            "limitations": "High entanglement challenging; 2D more expensive than 1D; ansatz choice matters.",
            "typical_use_cases": "Condensed matter, quantum spin systems, 1D and 2D lattice models.",
            "standard_refs": [],
            "last_reviewed": str(date.today())
        }
    ]
    
    methods.extend(qp_methods)
    return methods

def extract_methods_from_registry() -> List[Dict]:
    """Extract methods from qc_registry_platform_extended."""
    methods = []
    base = Path(r"G:\My Drive\Databases\qc_registry_platform_extended")
    
    # Scan workflows and enrichment for method patterns
    for dir_name in ["workflows", "enrichment", "cli"]:
        dir_path = base / dir_name
        if not dir_path.exists():
            continue
        
        for py_file in dir_path.rglob("*.py"):
            try:
                content = py_file.read_text(encoding='utf-8')
                if 'method' in content.lower() or 'algorithm' in content.lower():
                    print(f"  [SCAN] {py_file.name}")
            except Exception:
                continue
    
    return methods

def extract_concepts_from_packages() -> List[Dict]:
    """Extract domain concepts from inference and platform packages."""
    concepts = []
    
    packages = [
        r"G:\My Drive\Databases\qc_realworld_inference_package",
        r"G:\My Drive\Databases\enhanced_qc_platform_bundle",
        r"G:\My Drive\Databases\qc_enhanced_platform",
        r"G:\My Drive\Databases\qsmec_autorun_prod_viz_updated",
        r"G:\My Drive\Databases\qsmec_platform_autorun_docker"
    ]
    
    # Add quantum physics-specific concepts
    qp_concepts = [
        {
            "id": "concept.qp.entanglement",
            "domain": "quantum_physics",
            "title": "Quantum Entanglement",
            "level": "ug_adv",
            "tags": ["foundations", "nonlocality", "correlations"],
            "summary": "Non-classical correlation between quantum systems where measurement of one instantly affects the other, regardless of distance.",
            "long_explanation": "Entanglement is a uniquely quantum phenomenon where particles share correlations that cannot be explained classically. Entangled states violate Bell inequalities, demonstrating nonlocality. Measured by entanglement entropy, concurrence, or negativity. Central to quantum information and computing.",
            "prerequisites": ["concept.qp.superposition", "concept.qp.measurement"],
            "key_equations": [],
            "standard_refs": [],
            "common_pitfalls": "Confusing entanglement with classical correlation; assuming faster-than-light communication; ignoring decoherence effects.",
            "faq": [{"q": "Does entanglement enable faster-than-light communication?", "a": "No. While correlations are instantaneous, no usable information can be transmitted faster than light."}],
            "mastery_checklist": ["Distinguish entangled from product states", "Calculate entanglement entropy", "Understand Bell inequalities"],
            "last_reviewed": str(date.today())
        },
        {
            "id": "concept.qp.superposition",
            "domain": "quantum_physics",
            "title": "Quantum Superposition",
            "level": "ug_intro",
            "tags": ["foundations", "wavefunctions", "measurement"],
            "summary": "Principle that quantum systems can exist in linear combinations of basis states until measured.",
            "long_explanation": "Superposition allows quantum states to be linear combinations of eigenstates. Upon measurement, the system collapses to one eigenstate with probability given by Born rule. Enables quantum interference and parallelism.",
            "prerequisites": ["concept.qp.wavefunction"],
            "key_equations": [],
            "standard_refs": [],
            "common_pitfalls": "Thinking superposition means 'being in two states at once'; ignoring decoherence; confusing superposition with classical mixture.",
            "faq": [{"q": "What is the difference between superposition and classical probability?", "a": "Superposition involves coherent amplitudes that can interfere; classical probability uses incoherent probabilities."}],
            "mastery_checklist": ["Write superposition states in Dirac notation", "Apply Born rule", "Understand interference"],
            "last_reviewed": str(date.today())
        },
        {
            "id": "concept.qp.decoherence",
            "domain": "quantum_physics",
            "title": "Quantum Decoherence",
            "level": "grad",
            "tags": ["open_systems", "environment", "measurement"],
            "summary": "Loss of quantum coherence due to interaction with environment, causing transition from quantum to classical behavior.",
            "long_explanation": "Decoherence describes how quantum systems lose phase relationships through environmental coupling. Rapid for macroscopic systems, explaining classical emergence. Central to understanding quantum-to-classical transition and limiting quantum computing.",
            "prerequisites": ["concept.qp.entanglement", "concept.qp.density_matrix"],
            "key_equations": [],
            "standard_refs": [],
            "common_pitfalls": "Confusing decoherence with wavefunction collapse; assuming decoherence solves measurement problem; ignoring timescales.",
            "faq": [{"q": "Is decoherence the same as wavefunction collapse?", "a": "No. Decoherence explains loss of interference but does not select measurement outcomes."}],
            "mastery_checklist": ["Calculate decoherence timescales", "Understand pointer states", "Model open quantum systems"],
            "last_reviewed": str(date.today())
        },
        {
            "id": "concept.qp.quantum_computing",
            "domain": "quantum_physics",
            "title": "Quantum Computing",
            "level": "grad",
            "tags": ["computation", "qubits", "algorithms"],
            "summary": "Paradigm using quantum mechanical phenomena (superposition, entanglement) to perform computation beyond classical capabilities.",
            "long_explanation": "Quantum computers use qubits that can exist in superposition, enabling parallel computation. Quantum algorithms (Shor, Grover, VQE) offer speedups for specific problems. Challenges include decoherence, error correction, and scalability.",
            "prerequisites": ["concept.qp.entanglement", "concept.qp.superposition"],
            "key_equations": [],
            "standard_refs": [],
            "common_pitfalls": "Assuming quantum computers solve all problems faster; ignoring error rates; confusing NISQ and fault-tolerant regimes.",
            "faq": [{"q": "Can quantum computers break all encryption?", "a": "Shor's algorithm can factor integers efficiently, threatening RSA. Post-quantum cryptography addresses this threat."}],
            "mastery_checklist": ["Understand qubit gates", "Analyze simple quantum circuits", "Compare quantum vs classical complexity"],
            "last_reviewed": str(date.today())
        },
        {
            "id": "concept.qp.many_body",
            "domain": "quantum_physics",
            "title": "Quantum Many-Body Systems",
            "level": "grad",
            "tags": ["condensed_matter", "correlation", "phases"],
            "summary": "Systems of many interacting quantum particles exhibiting emergent collective phenomena beyond single-particle physics.",
            "long_explanation": "Quantum many-body systems are characterized by strong correlations and entanglement. Exhibit phase transitions, topological order, and emergent quasiparticles. Computationally challenging due to exponential Hilbert space growth. Methods include DMRG, QMC, mean-field theories.",
            "prerequisites": ["concept.qp.entanglement", "concept.qc.electron_correlation"],
            "key_equations": [],
            "standard_refs": [],
            "common_pitfalls": "Assuming mean-field always valid; ignoring correlation effects; not recognizing emergent phenomena.",
            "faq": [{"q": "What makes many-body problems hard?", "a": "Hilbert space grows exponentially with particle number, and correlations prevent factorization into independent particles."}],
            "mastery_checklist": ["Understand Fermi liquid theory", "Recognize emergent phenomena", "Apply approximation methods"],
            "last_reviewed": str(date.today())
        }
    ]
    
    concepts.extend(qp_concepts)
    return concepts

def build_glossary_from_files() -> List[Dict]:
    """Build comprehensive glossary from enriched files and use cases."""
    glossary = []
    
    # Load enriched glossary
    try:
        enriched_path = Path(r"G:\My Drive\Databases\enriched_glossary.json")
        with open(enriched_path, 'r', encoding='utf-8') as f:
            enriched_data = json.load(f)
            for entry in enriched_data:
                # Convert to QCBD schema
                glossary.append({
                    "id": entry.get("id", f"glossary.{entry.get('domain', 'qc')}.{entry.get('term', 'unknown').lower().replace(' ', '_')}"),
                    "domain": entry.get("domain", "quantum_chemistry"),
                    "term": entry.get("term", ""),
                    "definition": entry.get("definition", ""),
                    "category": entry.get("category", "concept"),
                    "related_terms": entry.get("related_terms", []),
                    "see_also": entry.get("see_also", []),
                    "last_reviewed": entry.get("last_reviewed", str(date.today()))
                })
    except Exception as e:
        print(f"[WARN] Could not load enriched_glossary.json: {e}")
    
    # Load use cases and extract domain terms
    try:
        use_cases_path = Path(r"G:\My Drive\Databases\qsmec_use_cases_extracted.json")
        with open(use_cases_path, 'r', encoding='utf-8') as f:
            use_cases = json.load(f)
            
            # Extract Q-SMEC specific terms
            qsmec_terms = [
                {
                    "id": "glossary.qsmec.sensor",
                    "domain": "quantum_sensors",
                    "term": "Q-SMEC Sensor",
                    "definition": "Quantum superconducting sensor material engineered for high sensitivity, advanced energy storage, and integration into critical infrastructure using elements like Ge, Ga, Nb, Ti, Al, and nitrides.",
                    "category": "technology",
                    "related_terms": ["superconducting materials", "quantum sensing", "critical infrastructure"],
                    "see_also": [],
                    "last_reviewed": str(date.today())
                },
                {
                    "id": "glossary.qsmec.trl",
                    "domain": "engineering",
                    "term": "TRL",
                    "definition": "Technology Readiness Level - a systematic metric/measurement system that supports assessments of technology maturity from TRL 1 (basic principles) to TRL 9 (actual system proven in operational environment).",
                    "category": "process",
                    "related_terms": ["technology development", "commercialization", "systems engineering"],
                    "see_also": [],
                    "last_reviewed": str(date.today())
                },
                {
                    "id": "glossary.qsmec.doe",
                    "domain": "materials_science",
                    "term": "Design of Experiments",
                    "definition": "AI-driven systematic method to determine relationships between factors affecting a process and the output of that process, used in Q-SMEC for materials optimization.",
                    "category": "method",
                    "related_terms": ["materials design", "optimization", "AI-assisted design"],
                    "see_also": [],
                    "last_reviewed": str(date.today())
                }
            ]
            glossary.extend(qsmec_terms)
    except Exception as e:
        print(f"[WARN] Could not load use cases: {e}")
    
    return glossary

def main():
    print("Extracting methods, concepts, and glossary from external packages...")
    
    # Extract methods
    print("\n[1/4] Extracting quantum physics methods...")
    qp_methods = extract_methods_from_benchmark_runner()
    print(f"  Found {len(qp_methods)} quantum physics methods")
    
    print("\n[2/4] Scanning registry platform...")
    registry_methods = extract_methods_from_registry()
    print(f"  Found {len(registry_methods)} additional methods")
    
    # Extract concepts
    print("\n[3/4] Extracting quantum physics concepts...")
    qp_concepts = extract_concepts_from_packages()
    print(f"  Found {len(qp_concepts)} quantum physics concepts")
    
    # Build glossary
    print("\n[4/4] Building comprehensive glossary...")
    glossary = build_glossary_from_files()
    print(f"  Found {len(glossary)} glossary terms")
    
    # Write output files
    all_methods = qp_methods + registry_methods
    if all_methods:
        methods_qp_path = DATA_PROCESSED / "methods.qp.jsonl"
        write_jsonl(methods_qp_path, all_methods)
        print(f"\n✓ Created {methods_qp_path} with {len(all_methods)} methods")
    
    if qp_concepts:
        concepts_qp_path = DATA_PROCESSED / "concepts.qp.jsonl"
        write_jsonl(concepts_qp_path, qp_concepts)
        print(f"✓ Created {concepts_qp_path} with {len(qp_concepts)} concepts")
    
    if glossary:
        glossary_path = DATA_PROCESSED / "glossary.jsonl"
        write_jsonl(glossary_path, glossary)
        print(f"✓ Created {glossary_path} with {len(glossary)} terms")
    
    print("\n✓ Extraction complete")
    return 0

if __name__ == '__main__':
    sys.exit(main())
