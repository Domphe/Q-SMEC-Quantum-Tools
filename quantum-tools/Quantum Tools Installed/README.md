# Quantum Tools Installed Environment

## Overview

This directory contains the complete Python virtual environment with 50+ quantum computing, machine learning, and scientific computing packages installed and validated.

**Size:** 3.3GB  
**Files:** 85,765 packages and dependencies  
**Migration Date:** January 15, 2026  

## Installed Packages

### Quantum Computing Frameworks
- **Qiskit 2.1.2** - IBM quantum circuits and simulators
- **Cirq 1.6.1** - Google quantum circuit library
- **PennyLane 0.43.1** - Quantum machine learning framework
- **Amazon Braket SDK** - Multi-vendor quantum access
- **Qiskit Aer** - High-performance quantum simulator
- **Qiskit IBM Runtime** - Cloud backend support

### Chemistry & Materials
- **PySCF 2.11.0** - Quantum chemistry computational methods
- **ASE 3.27.0** - Atomic simulations environment
- **PyMatgen** - Materials science toolkit
- **tblite 0.5.0** - Fast tight-binding (XTB) calculations

### Machine Learning & Deep Learning
- **TensorFlow 2.20.0** - Deep learning framework
- **PyTorch 2.9.1** - Neural network library
- **Scikit-Learn 1.7.2** - ML algorithms
- **Optuna** - Hyperparameter optimization

### Scientific Computing Stack
- **NumPy 2.3.5** - Numerical computing
- **SciPy 1.16.3** - Scientific functions
- **Pandas 2.2.2** - Data manipulation
- **Matplotlib 3.10.7** - Scientific plotting
- **Seaborn 0.13.2** - Statistical visualization
- **Plotly 6.5.1** - Interactive plots

### Interactive Development
- **Jupyter Lab 4.5.0** - Full Jupyter Lab environment
- **Jupyter Notebook 7.5.2** - Classic notebooks
- **IPython 9.9.0** - Enhanced Python shell

## Quick Start

### Activate the Environment (Linux/WSL)

```bash
# From anywhere
source /mnt/e/Data1/Q-SMEC-Client-Databases/.venv/bin/activate

# Or directly from Quantum-Tools
source /mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum\ Tools\ Installed/.venv/bin/activate

# Or from the Quantum-Tools directory
cd /mnt/e/Data1/Q-SMEC-Quantum-Tools
source ./quantum-tools/Quantum\ Tools\ Installed/.venv/bin/activate
```

### Activate the Environment (Windows)

```cmd
E:\Data1\Q-SMEC-Client-Databases\.venv\Scripts\activate
```

### Launch Jupyter Lab

```bash
# Activate the environment first
source /mnt/e/Data1/Q-SMEC-Client-Databases/.venv/bin/activate

# Then launch
jupyter lab
```

### Verify Installation

```python
# Test import of core quantum packages
python3 << 'EOF'
import sys
print(f"Python: {sys.version}")

# Quantum frameworks
import qiskit
print(f"Qiskit: {qiskit.__version__}")

import cirq
print(f"Cirq: {cirq.__version__}")

import pennylane as qml
print(f"PennyLane: {qml.__version__}")

# ML frameworks
import tensorflow as tf
print(f"TensorFlow: {tf.__version__}")

import torch
print(f"PyTorch: {torch.__version__}")

# Scientific stack
import numpy as np
print(f"NumPy: {np.__version__}")

import pandas as pd
print(f"Pandas: {pd.__version__}")

print("\n✓ All quantum packages verified!")
EOF
```

## Symlink Information

This environment is also accessible via a symlink at:
```
/mnt/e/Data1/Q-SMEC-Client-Databases/.venv
```

This symlink provides backward compatibility for any scripts or workflows that reference the old location.

## Directory Structure

```
Quantum Tools Installed/
├── .venv/
│   ├── Lib/
│   │   └── site-packages/          # All installed packages
│   │       ├── qiskit/
│   │       ├── cirq/
│   │       ├── pennylane/
│   │       ├── tensorflow/
│   │       ├── torch/
│   │       ├── numpy/
│   │       ├── pandas/
│   │       ├── matplotlib/
│   │       ├── jupyter/
│   │       └── ... (500+ packages)
│   ├── Scripts/                    # Entry point scripts
│   │   ├── jupyter
│   │   ├── jupyter-lab
│   │   ├── ipython
│   │   └── ... (30+ executables)
│   ├── Include/
│   ├── bin/ (on Linux)
│   └── pyvenv.cfg
└── README.md                       # This file
```

## Common Tasks

### Run a Quantum Circuit (Qiskit)

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create Bell state
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])

# Simulate
sim = AerSimulator()
result = sim.run(qc).result()
counts = result.get_counts()
print("Measurement counts:", counts)
```

### Create Quantum Circuit (Cirq)

```python
import cirq

q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit(
    cirq.H(q0),
    cirq.CNOT(q0, q1),
    cirq.measure(q0, q1)
)
simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=1000)
print(result)
```

### Use PennyLane

```python
import pennylane as qml
from pennylane import numpy as np

dev = qml.device('default.qubit', wires=2)

@qml.qnode(dev)
def circuit(params):
    qml.RX(params[0], wires=0)
    qml.RY(params[1], wires=1)
    qml.CNOT(wires=[0, 1])
    return qml.expval(qml.PauliZ(1))

params = np.array([0.1, 0.2])
print(circuit(params))
```

### Run TensorFlow Model

```python
import tensorflow as tf
from tensorflow import keras

# Build model
model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(784,)),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
print(model.summary())
```

### Use PyTorch

```python
import torch
import torch.nn as nn

class QuantumNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 64)
        self.fc2 = nn.Linear(64, 2)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        return self.fc2(x)

model = QuantumNet()
print(model)
```

## Environment Variables (Optional)

If you need to set environment variables before activation:

### Linux/WSL

```bash
export PYTHONPATH="/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv/lib/python3.12/site-packages:${PYTHONPATH}"
export PATH="/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv/bin:${PATH}"
```

### Windows (PowerShell)

```powershell
$env:PYTHONPATH = "E:\Data1\Q-SMEC-Quantum-Tools\quantum-tools\Quantum Tools Installed\.venv\Lib\site-packages;$env:PYTHONPATH"
$env:PATH = "E:\Data1\Q-SMEC-Quantum-Tools\quantum-tools\Quantum Tools Installed\.venv\Scripts;$env:PATH"
```

## Troubleshooting

### Module Import Errors

If you get "ModuleNotFoundError", ensure:
1. Virtual environment is activated: `which python3` should show the venv path
2. You're using the correct Python: `python3 --version` should show 3.12.x
3. Reinstall if needed: `pip install --upgrade [package_name]`

### Slow TensorFlow/PyTorch Startup

This is normal - large ML frameworks have initial overhead on first import. Subsequent imports are fast.

### Jupyter Not Found

```bash
# Activate environment and reinstall
source /mnt/e/Data1/Q-SMEC-Client-Databases/.venv/bin/activate
pip install --upgrade jupyter jupyterlab
```

### Permission Errors (WSL/Linux)

If you get permission errors, the virtual environment should handle this. If not:

```bash
chmod -R u+w /mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum\ Tools\ Installed/.venv
```

## Migration Information

**Original Location:** `/mnt/e/Data1/Q-SMEC-Client-Databases/.venv`  
**New Location:** `/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv`  
**Migration Date:** January 15, 2026, 12:23 UTC  
**Migration Tool:** `migrate_quantum_venv.py`  
**Files Migrated:** 85,765  
**Total Size:** 3.09GB  
**Migration Time:** 59.2 minutes  
**Verification:** ✅ Passed - all files verified via comparison  

## Backward Compatibility

A symlink has been maintained at the original location for backward compatibility:

```
/mnt/e/Data1/Q-SMEC-Client-Databases/.venv
  ↓ (symlink to)
/mnt/e/Data1/Q-SMEC-Quantum-Tools/quantum-tools/Quantum Tools Installed/.venv
```

This means scripts using the old path will continue to work without modification.

## Next Steps

1. **Activate the environment:** See Quick Start section above
2. **Explore examples:** Check `/Quantum Models/` and `/Quantum Simulations/` for notebooks
3. **Create your own:** Start building quantum applications with Jupyter Lab
4. **Integrate with projects:** Use this venv in your Q-SMEC projects

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review individual package documentation (Qiskit, Cirq, TensorFlow, etc.)
3. Examine migration logs in: `/mnt/e/Data1/Q-SMEC-VSC-Operations/tools/migrate_quantum_venv.py`

---

**Last Updated:** January 15, 2026  
**Status:** ✅ Installed, Tested, and Ready to Use
