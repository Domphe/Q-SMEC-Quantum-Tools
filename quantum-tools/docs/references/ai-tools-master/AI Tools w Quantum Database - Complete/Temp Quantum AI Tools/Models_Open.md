# Models — Open (from QOSF Awesome Quantum Software)

Source: Open-Source Quantum Software Projects (QOSF) README extracted on 2026-01-07.

Note: This source is a curated list of open-source software. “Paid” entries are not expected here. This document groups libraries and SDKs primarily used to build and train quantum models (algorithms, QML, and full‑stack SDKs), distinct from pure simulators.

---

## Quantum full‑stack libraries

### C
- [Qiskit](https://www.ibm.com/quantum/qiskit) — SDK for working with quantum computers at the level of extended quantum circuits, operators, and primitives. (supported by IBM).

### C++
- [avaloni](https://github.com/avalon-lang/avaloni) — Programming language (interpreter) for classical-quantum hybrid computers.
- [CUDA-Q](https://github.com/NVIDIA/cuda-quantum) — Platform for accelerated quantum-classical applications on GPUs, CPUs and QPUs.
- [qpp](https://github.com/softwareQinc/qpp) — Quantum++ is a modern C++ general purpose quantum computing library, composed solely of template header files.
- [Qristal](https://github.com/qbrilliance/qristal) — Quantum Brilliance's hybrid quantum-classical C++/Python development platform ([docs](https://qristal.readthedocs.io); [core module](https://github.com/qbrilliance/qristal-core)).
- [staq](https://github.com/softwareqinc/staq) — Full stack quantum processing toolkit ([arXiv paper](https://arxiv.org/abs/1912.06070)).
- [XACC](https://github.com/ORNL-QCI/xacc) — Extreme-scale programming model for quantum acceleration within high-performance computing ([arXiv paper](https://arxiv.org/abs/1710.01794)).

### Python
- [blueqat](https://github.com/Blueqat/Blueqat) — Quantum computing SDK.
- [bosonic-qiskit](https://github.com/C2QA/bosonic-qiskit) — Simulate hybrid boson-qubit systems within Qiskit, implemented as a part of the Co-design Center for Quantum Advantage (C2QA) of the National Quantum Initiative.
- [Braket](https://github.com/amazon-braket/amazon-braket-sdk-python) — [Amazon's](https://aws.amazon.com/braket/) fully managed quantum computing service for building quantum algorithms.
- [Cirq](https://github.com/quantumlib/Cirq) — Framework for creating, editing, and invoking Noisy Intermediate Scale Quantum (NISQ) circuits.
- [CUDA-Q](https://github.com/NVIDIA/cuda-quantum) — Platform for accelerated quantum-classical applications on GPUs, CPUs and QPUs.
- [Forest](https://github.com/rigetticomputing/pyquil) — [Rigetti](https://www.rigetti.com/)'s software library for writing, simulating, compiling and executing quantum programs.
- [Ket](https://quantumket.org) — Embedded programming language that introduces the ease of Python to quantum programming.
- [Ocean](https://github.com/dwavesystems/dwave-ocean-sdk) — [D-Wave System](https://www.dwavesys.com/home)'s suite of tools for solving hard problems with quantum computers.
- [OpenQL](https://github.com/QE-Lab/OpenQL) — Compiler framework with algorithm libraries, optimizer, scheduler, QEC, mapping, micro-code generator.
- [PennyLane](https://pennylane.ai) — Cross-platform Python library for differentiable programming of quantum computers.
- [Perceval](https://github.com/Quandela/Perceval) — [Quandela](https://www.quandela.com)'s software library for programming realistic photonic quantum computers.
- [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ) — Hardware-agnostic framework with compiler and simulator with emulation capabilities.
- [PyQudit](https://github.com/Ordoptimus/pyqudit) — Python package for generalized and universal versions of quantum gates in N-dimensions.
- [pytket](https://docs.quantinuum.com/tket/) — Quantum computing toolkit for building, compiling, and executing quantum circuits (developed by Quantinuum).
- [Qadence](https://github.com/pasqal-io/qadence) — [Pasqal](https://www.pasqal.com)'s package for building differentiable digital and digital-analog quantum programs realizable on neutral atom devices.
- [quantumcat](https://github.com/artificial-brain/quantumcat/) — Cross-platform open-source high-level quantum computing library focused on building applications.
- [Qibo](https://github.com/qiboteam/qibo) — An open-source framework for quantum simulation, self-hosted quantum hardware control and calibration.
- [Qiskit](https://www.ibm.com/quantum/qiskit) — SDK for working with quantum computers at the level of extended quantum circuits, operators, and primitives. (supported by IBM).
- [Qrisp](https://qrisp.eu/) — A high-level programming language and framework for creating and compiling quantum algorithms ([GitHub](https://github.com/eclipse-qrisp/Qrisp)).
- [Qristal](https://github.com/qbrilliance/qristal) — Quantum Brilliance's hybrid quantum-classical C++/Python development platform ([docs](https://qristal.readthedocs.io); [core module](https://github.com/qbrilliance/qristal-core)).
- [quantum-os](https://github.com/quantumos-org/quantum-os) — Operating system based on Linux kernel for quantum computing.
- [Strawberry Fields](https://github.com/xanaduai/strawberryfields) — [Xanadu](https://www.xanadu.ai)'s software library for photonic quantum computing.
- [Tangelo](https://github.com/goodchemistryco/Tangelo) and [Tangelo-Examples](https://github.com/goodchemistryco/Tangelo-Examples/) — Toolkit for quantum chemistry simulation workflows on quantum computers, maintained by [SandboxAQ](https://www.sandboxaq.com/).
- [TensorCircuit](https://github.com/tencent-quantum-lab/tensorcircuit) — Tensor network based quantum software framework for the NISQ era.
- [Tequila](https://github.com/aspuru-guzik-group/tequila) — Extensible Quantum Information and Learning Architecture developed by Alan Aspuru-Guzik's group (UofT).

### Q#
- [Q#](https://www.microsoft.com/en-us/quantum/development-kit) — Microsoft's quantum programming language with Visual Studio integration.

### Silq
- [Silq](https://silq.ethz.ch/) — High-level quantum programming language with safe uncomputation and intuitive semantics.

---

## Quantum algorithms and QML

### C++
- [XACC VQE](https://github.com/ornl-qci/xacc-vqe) — Variational quantum eigensolver built on [XACC](https://github.com/ORNL-QCI/xacc) for distributed, and shared memory systems.

### HTML
- [myQShor](https://github.com/Michaelvll/myQShor) — Quantum implementation of Shor's algorithm.

### Julia
- [QAOA.jl](https://github.com/FZJ-PGI-12/QAOA.jl) — Implementation the Quantum Approximate Optimization Algorithm (QAOA) in Julia.
- [QuantumTomography.jl](https://github.com/BBN-Q/QuantumTomography.jl) — Julia package to perform quantum state and process tomography.

### Python
- [Adapt](https://github.com/BBN-Q/Adapt) — Algorithms for adaptive refinement of measurements.
- [Arline Quantum](https://github.com/ArlineQ/arline_quantum) — Library with implementation of quantum gates and hardware, a part of [Arline Benchmarks](https://github.com/ArlineQ/arline_benchmarks) project.
- [Boson Sampling](https://github.com/IffTech/Boson-Sampling) — Library to calculate interferometer output probabilities given Fock state inputs.
- [FermiLib](https://github.com/ProjectQ-Framework/FermiLib) — Software for analyzing fermionic quantum simulation algorithms with [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ).
- [Grove](https://github.com/rigetticomputing/grove) — Quantum algorithms implemented using [Rigetti](https://www.rigetti.com/)'s [pyQuil](https://github.com/rigetticomputing/pyquil).
- [G/SG Morph](https://github.com/IffTech/GSG-Morph) — Quantum annealing algorithms for Graph/Subgraph Isomorphism.
- [MQT QAO](https://github.com/cda-tum/mqt-qao) — Automatic Framework for Solving Optimization Problems with Quantum Computers via the [`mqt.qao`](https://pypi.org/p/mqt.qao) Python package.
- [MQT QUBOMaker](https://github.com/cda-tum/mqt-qubomaker) — Automated QUBO formulation via the [`mqt.qubomaker`](https://pypi.org/p/mqt.qubomaker) Python package.
- [OpenFermion](https://github.com/quantumlib/OpenFermion) — Compiling and analyzing quantum algorithm for quantum chemistry simulations.
- [OpenQAOA](https://github.com/entropicalabs/openqaoa) — Multi-backend SDK to create, customise and execute QAOA on NISQ devices and simulators.
- [Paddle Quantum](https://github.com/PaddlePaddle/Quantum) — Quantum machine learning platform to construct & train quantum neural networks, developed by Baidu.
- [PyZFS](https://github.com/hema-ted/pyzfs) — Package to compute zero-field-splitting tensors for molecules and spin quantum bits in semiconductors.
- [QFog](https://github.com/artiste-qb-net/quantum-fog) — Framework for analyzing both classical and quantum Bayesian Networks.
- [QGrad](https://github.com/qgrad/qgrad) — Integrates automatic differentiation tools (e.g., JAX) with QuTiP and related packages.
- [Qiskit Nature](https://github.com/Qiskit/qiskit-nature) — Quantum Chemistry including ground state, excited states and dipole moment calculations.
- [QPanda](https://github.com/OriginQ/QPanda-2) — Framework to build, run, and optimize quantum algorithms.
- [Qualtran](https://qualtran.readthedocs.io/en/latest/) — Library for expressing and analyzing Fault Tolerant Quantum algorithms.
- [Quantum_Edward](https://github.com/artiste-qb-net/Quantum_Edward) — Python tools for supervised learning by Quantum Neural Networks.
- [QuantumFlow](https://github.com/rigetti/quantumflow) — Quantum Algorithms Development Toolkit allowing for backpropagation with QAOA.
- [Quantum TSP](https://github.com/mstechly/quantum_tsp_tutorials) — Tutorials on solving Travelling Salesman Problem using quantum computing (QAOA).
- [Qudit Team](https://github.com/q-inho/QuditsTeam-1) — Extend Qiskit versatility to higher dimensional quantum states.
- [ReCirq](https://github.com/quantumlib/ReCirq) — Modules for running quantum computing applications and experiments through [Cirq](https://github.com/quantumlib/Cirq).
- [spin_qudit_tomography](https://github.com/perlinm/spin_qudit_tomography) — Spin tomography using qudits.
- [Tensorflow Quantum](https://www.tensorflow.org/quantum) — Library for hybrid quantum-classical machine learning.
- [pyRiemann-qiskit](https://github.com/pyRiemann/pyRiemann-qiskit) — ML and quantum programming based on pyRiemann and Qiskit.
- [VQF](https://github.com/mstechly/vqf) — Variational Quantum Factoring algorithm (in pyQuil).
- [WebMark](https://github.com/ohtu2021-kvantti/WebMark) — Web platform for benchmarking quantum computing algorithms.
- [XACC Examples](https://github.com/ORNL-QCI/xacc-examples) — Example code using [XACC](https://github.com/ORNL-QCI/xacc).
- [XACC QChem](https://github.com/ORNL-QCI/xacc-qchem-benchmarks) — QPU Benchmarks for Quantum Chemistry via XACC, Psi4 and OpenFermion.

### Q#
- [Quantum Katas](https://github.com/Microsoft/QuantumKatas) — Programming exercises for learning Q# and quantum computing.

---

Notes:
- Items above are open-source projects; service backends (e.g., cloud QPU access) may be paid, but the SDKs listed are open.
- For pure circuit/state simulators, see the companion document “Simulations — Open”.
