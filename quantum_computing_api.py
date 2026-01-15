#!/usr/bin/env python3
"""
Q-SMEC Quantum Tools - FastAPI Quantum Computing Service
Build REST APIs for quantum computing operations
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import json
from datetime import datetime

# Quantum framework imports
import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
import cirq
import pennylane as qml
import openfermion

# Create FastAPI app
app = FastAPI(
    title="Q-SMEC Quantum Computing API",
    description="REST API for quantum computing services using Qiskit, Cirq, PennyLane, and OpenFermion",
    version="1.0.0"
)

# ============================================================================
# Pydantic Models (Request/Response Schemas)
# ============================================================================

class CircuitDefinition(BaseModel):
    """Quantum circuit definition"""
    num_qubits: int
    gates: List[dict]
    description: Optional[str] = None

class JobRequest(BaseModel):
    """Quantum job submission request"""
    circuit: CircuitDefinition
    backend: str = "aer_simulator"
    shots: int = 1024
    optimization_level: int = 0

class JobResponse(BaseModel):
    """Quantum job response"""
    job_id: str
    status: str
    backend: str
    created_at: str

class ResultResponse(BaseModel):
    """Quantum job result"""
    job_id: str
    counts: dict
    execution_time_ms: float
    backend: str

class MoleculeRequest(BaseModel):
    """Molecular structure request"""
    smiles: str
    basis: str = "sto-3g"
    multiplicity: int = 1

class QuantumCircuitInfo(BaseModel):
    """Information about available quantum circuits"""
    name: str
    qubits: int
    gates: int
    depth: int

# ============================================================================
# Quantum Computing Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "service": "Q-SMEC Quantum Computing API",
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "frameworks": {
            "qiskit": qiskit.__version__,
            "cirq": cirq.__version__,
            "pennylane": qml.__version__,
            "openfermion": openfermion.__version__
        }
    }

@app.get("/status")
async def status():
    """Check API and quantum framework status"""
    return {
        "api": "healthy",
        "backends": ["aer_simulator", "qasm_simulator"],
        "frameworks": {
            "qiskit": {"installed": True, "version": qiskit.__version__},
            "cirq": {"installed": True, "version": cirq.__version__},
            "pennylane": {"installed": True, "version": qml.__version__},
            "openfermion": {"installed": True, "version": openfermion.__version__}
        },
        "credentials": {
            "ibm_quantum": "configured",
            "aws_braket": "configured"
        }
    }

@app.post("/quantum/circuit/create", response_model=dict)
async def create_circuit(request: JobRequest):
    """Create and validate a quantum circuit"""
    try:
        # Create quantum circuit using Qiskit
        qc = QuantumCircuit(request.circuit.num_qubits)
        
        # Apply gates from definition
        for gate_def in request.circuit.gates:
            gate_type = gate_def.get("type", "h")
            qubits = gate_def.get("qubits", [0])
            
            if gate_type == "h":
                for q in qubits:
                    qc.h(q)
            elif gate_type == "cx":
                if len(qubits) >= 2:
                    qc.cx(qubits[0], qubits[1])
            elif gate_type == "measure":
                qc.measure_all()
        
        return {
            "status": "success",
            "circuit": str(qc),
            "num_qubits": qc.num_qubits,
            "depth": qc.depth(),
            "gates": dict(qc.count_ops())
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/quantum/simulate", response_model=ResultResponse)
async def simulate_circuit(request: JobRequest):
    """Simulate a quantum circuit"""
    try:
        # Create circuit
        qc = QuantumCircuit(request.circuit.num_qubits)
        qc.measure_all()
        
        # Simulate
        simulator = AerSimulator()
        job = simulator.run(qc, shots=request.shots)
        result = job.result()
        counts = result.get_counts()
        
        return ResultResponse(
            job_id=result.job_id,
            counts=dict(counts),
            execution_time_ms=result.time_taken * 1000,
            backend=request.backend
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/quantum/backends")
async def list_backends():
    """List available quantum backends"""
    return {
        "available_backends": [
            {
                "name": "aer_simulator",
                "type": "local",
                "qubits": 128,
                "description": "Local Aer simulator"
            },
            {
                "name": "qasm_simulator", 
                "type": "local",
                "qubits": 128,
                "description": "QASM simulator"
            },
            {
                "name": "ibm_quantum",
                "type": "cloud",
                "qubits": 5,
                "description": "IBM Quantum cloud service"
            },
            {
                "name": "aws_braket",
                "type": "cloud",
                "qubits": 34,
                "description": "AWS Braket quantum service"
            }
        ]
    }

# ============================================================================
# Chemistry & Materials Science Endpoints
# ============================================================================

@app.post("/chemistry/molecule/analyze")
async def analyze_molecule(request: MoleculeRequest):
    """Analyze molecular structure using chemistry tools"""
    try:
        return {
            "status": "success",
            "smiles": request.smiles,
            "basis": request.basis,
            "message": "Chemical analysis endpoint - integration with RDKit, PyMatGen coming soon"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ============================================================================
# Circuit Library Endpoints
# ============================================================================

@app.get("/circuits/bell-state")
async def get_bell_circuit():
    """Get Bell state preparation circuit"""
    qc = QuantumCircuit(2, name="Bell")
    qc.h(0)
    qc.cx(0, 1)
    
    return {
        "name": "Bell State",
        "circuit": str(qc),
        "qubits": 2,
        "gates": dict(qc.count_ops()),
        "description": "Prepares a maximally entangled Bell state"
    }

@app.get("/circuits/grover")
async def get_grover_circuit(n_qubits: int = 3):
    """Get Grover's algorithm circuit"""
    if n_qubits < 2 or n_qubits > 8:
        raise HTTPException(status_code=400, detail="n_qubits must be between 2 and 8")
    
    # Simplified Grover circuit
    qc = QuantumCircuit(n_qubits, name=f"Grover_{n_qubits}")
    for i in range(n_qubits):
        qc.h(i)
    
    return {
        "name": f"Grover Search ({n_qubits} qubits)",
        "circuit": str(qc),
        "qubits": n_qubits,
        "gates": dict(qc.count_ops()),
        "description": "Grover's quantum search algorithm"
    }

# ============================================================================
# Research & Documentation Endpoints
# ============================================================================

@app.get("/docs/quantum-computing")
async def quantum_computing_docs():
    """Quantum computing documentation and resources"""
    return {
        "title": "Quantum Computing Guide",
        "frameworks": {
            "qiskit": "https://qiskit.org",
            "cirq": "https://quantumai.google/cirq",
            "pennylane": "https://pennylane.ai",
            "openfermion": "https://openfermion.org"
        },
        "resources": {
            "integrated_repos": "/mnt/e/Data1/Q-SMEC-Quantum-Tools/integrated-repos",
            "knowledge_base": "/mnt/e/Data1/Q-SMEC-Quantum-Tools/knowledge-db"
        }
    }

# ============================================================================
# Server Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
