# Simulations — Open (from QOSF Awesome Quantum Software)

Source: Open-Source Quantum Software Projects (QOSF) README extracted on 2026-01-07.

This document collects open-source quantum simulators and closely related packages (analog Hamiltonian control and annealing toolkits) from the source list.

---

## Quantum simulators

### Assembly

- [Quplexity](https://github.com/MrGilli/Quplexity) — Modular toolkit for QC simulators written in ARM(64) and x86 Assembly.

### C

- [QuaC](https://github.com/0tt3r/QuaC) — Parallel time-dependent open quantum systems solver.
- [QuEST](https://github.com/aniabrown/QuEST) — Quantum Exact Simulation Toolkit, high-performance multicore simulator of universal quantum circuits.
- [TNQVM](https://github.com/ornl-qci/tnqvm) — Tensor Network QPU Simulator for Eclipse [XACC](https://github.com/ORNL-QCI/xacc).

### Common Lisp

- [QVM](https://github.com/rigetti/qvm) — Rigetti's high-performance quantum virtual machine.

### Coq

- [QWIRE](https://github.com/jpaykin/QWIRE) — Quantum circuit language and formal verification tool.

### C++

- [Huawei HiQsimulator](https://github.com/Huawei-HiQ/HiQsimulator) — Single-amplitude, full-amplitude and error-correction circuit simulation engine.
- [Intel Quantum Simulator](https://github.com/intel/intel-qs) — Distributed qubit register quantum simulator using OpenMP and MPI.
- [MQT DDSIM](https://github.com/cda-tum/mqt-ddsim) — Quantum circuit simulator using decision diagrams; Python interface and Qiskit backend via [`mqt.ddsim`](https://pypi.org/p/mqt.ddsim).
- [PennyLane Lightning](https://github.com/PennyLaneAI/pennylane-lightning) — Fast state-vector simulator written in C++; GPU support.
- [qFlex](https://github.com/ngnrsaa/qflex) — Flexible high-performance simulator for verifying and benchmarking quantum circuits.
- [Qiskit Aer](https://github.com/Qiskit/qiskit-aer) — High performance simulator for quantum circuits including noise models (IBM).
- [QCEAD](https://github.com/llens/QuantumComputingEvolutionaryAlgorithmDesign) — Simulate and use parallel evolutionary techniques to design algorithms.
- [QCSim](https://github.com/aromanro/QCSim) — Quantum computing simulator with many algorithms as examples and tests.
- [QPlayer](https://github.com/eQuantumOS/QPlayer) — Light-weight, scalable and fast quantum Schrödinger simulator.
- [Qrack](https://github.com/vm6502q/qrack) — Comprehensive qubit and gate implementation for universal virtual quantum processors.
- [qSim](https://github.com/haykkh/qSim) — High level, elementary simulation library.
- [qsim](https://github.com/quantumlib/qsim) — GPU-enabled C++ and Python library for fast state-vector simulation of quantum circuits.
- [Quantum++](https://github.com/softwareqinc/qpp) — High-performance general purpose quantum simulator (supports qudits).
- [tweedledum](https://github.com/boschmitt/tweedledum) — Library for synthesis, compilation, and optimization of quantum circuits.

### F#

- [Liqui|>](http://stationq.github.io/Liquid/) — Toolsuite for quantum simulation developed by Microsoft QuArC.

### GoLang

- [Q](https://github.com/itsubaki/q) — Quantum Computation Simulator written purely in GoLang.

### Java

- [Strange](https://github.com/redfx-quantum/strange) — Java API to create Quantum Programs and simulate them.

### JavaScript

- [jsquil](https://github.com/mapmeld/jsquil) — JavaScript interface for writing Quil programs.
- [Quantum Circuit Simulator](https://github.com/perak/quantum-circuit) — Simulates 20+ qubits in browser or on Node.js.
- [Quirk](https://github.com/Strilanc/Quirk) — Drag-and-drop quantum circuit simulator in your browser.
- [Quantum JavaScript (Q.js)](https://quantumjavascript.app/) — Drag-and-drop circuit editor and simulator with documented API.
- [Quantum-computing-playground](https://github.com/gwroblew/Quantum-Computing-Playground) — Browser-based IDE to run, visualize and debug quantum programs.
- [Quantum tensors](https://github.com/Quantum-Game/quantum-tensors) — JS/TS package for sparse tensor operations on complex numbers for quantum computing.

### Julia

- [BosonSampling.jl](https://github.com/benoitseron/BosonSampling.jl) — Efficient simulation of multiphoton interference.
- [Cliffords.jl](https://github.com/BBN-Q/Cliffords.jl) — Efficient calculation of Clifford circuits in Julia.
- [IonSim.jl](https://github.com/HaeffnerLab/IonSim.jl) — Simulate dynamics of trapped ions interacting with laser light.
- [KadanoffBaym.jl](https://github.com/NonequilibriumDynamics/KadanoffBaym.jl) — Adaptive many-body time evolution of non-equilibrium Green functions.
- [PauliStrings.jl](https://github.com/nicolasloizeau/PauliStrings.jl) — Many-body simulations in the Pauli strings representation.
- [QSimulator.jl](https://github.com/BBN-Q/QSimulator.jl) — Unitary and Lindbladian evolution.
- [QuantumInfo.jl](https://github.com/BBN-Q/QuantumInfo.jl) — Quantum information calculations.
- [QuantumOptics.jl](https://qojulia.org/) — Framework to simulate open quantum systems.
- [RandomQuantum.jl](https://github.com/BBN-Q/RandomQuantum.jl) — Random quantum states and processes.
- [Yao.jl](https://github.com/QuantumBFS/Yao.jl) — Extensible, efficient quantum algorithm design framework.

### Python

- [Dynamiqs](https://www.dynamiqs.org/) — High-performance quantum systems simulation with JAX.
- [Graphix](https://github.com/TeamGraphix/graphix) — MBQC compiler, simulator and QPU interface.
- [Horqrux](https://github.com/pasqal-io/horqrux) — Jax-based state vector simulator tailored for QML from Pasqal.
- [Interlin-q](https://github.com/Interlin-q/Interlin-q) — Quantum network simulator for distributed quantum systems.
- [MentPy](https://github.com/BestQuark/mentpy) — Create and simulate MBQC programs.
- [MISTIQS](https://github.com/USCCACS/MISTIQS) — Tooling for many-body dynamics simulations.
- [Piquasso](https://github.com/Budapest-Quantum-Computing-Group/piquasso) — Photonic quantum computing simulator in Python/C++.
- [PIQS](https://github.com/nathanshammah/piqs) — Open quantum dynamics of identical qubits.
- [PyQTorch](https://github.com/pasqal-io/pyqtorch) — PyTorch-based state vector simulator for QML from Pasqal.
- [QCircuits](https://github.com/grey-area/qcircuits) — Student-friendly circuit simulator.
- [QCompute](https://github.com/baidu/QCompute) — Baidu SDK for designing circuits and simulating.
- [Qibo](https://github.com/qiboteam/qibo) — Framework for quantum simulation with JIT acceleration.
- [qsim](https://github.com/quantumlib/qsim) — GPU-enabled simulation library (C++/Python bindings).
- [QTop](https://github.com/jacobmarks/QTop) — Simulation and visualization of topological quantum computers.
- [quantum-computing](https://github.com/QuantumSystems/quantum-computing) — Functionally complete simulator for universal QC in Python.
- [Quditto](https://github.com/Networks-it-uc3m/Quditto) — QKD Network emulator with ETSI GS QKD 014 compliance.
- [QuForge](https://github.com/tiago939/QuForge) — Qudit simulation package.
- [quimb](https://github.com/jcmgray/quimb) — Quantum information and many-body calculations with tensor networks.
- [Quintuple](https://github.com/corbett/QuantumComputing) — Simulating IBM’s 5-qubit processor.
- [QuPy](https://github.com/ken-nakanishi/qupy) — Circuit simulator for both CPU and GPU.
- [QuSpin](https://github.com/weinbe58/QuSpin) — Exact diagonalization and dynamics of many-body systems.
- [QuTiP](http://qutip.org/) — Simulations of open quantum systems.
- [SeQuencing](https://github.com/sequencing-dev/sequencing) — Construct and simulate quantum control sequences using QuTiP.
- [SimulaQron](https://github.com/StephanieWehner/SimulaQron) — Application-level quantum network simulator.
- [SOQCS](https://github.com/SOQCSAdmin/SOQCS) — Non-ideal quantum optical circuits (Python and C++ APIs).
- [Stim](https://github.com/quantumlib/Stim) — Fast stabilizer circuit simulator.
- [SQUANCH](https://github.com/att-innovate/squanch) — Distributed simulation framework for quantum networks and channels.
- [QuNetSim](https://github.com/tqsd/QuNetSim) — Quantum network simulation framework.
- [The Walrus](https://github.com/xanaduAI/thewalrus) — Gaussian Boson Sampling library from Xanadu.
- [gdsfactory](https://gdsfactory.github.io/gdsfactory/) and [plugins](https://gdsfactory.github.io/gplugins) — Design and simulation of photonics/analog/quantum circuits.

### Rust

- [QCGPU](https://github.com/QCGPU/qcgpu-rust) — GPU-accelerated simulation library (arXiv:1805.00988).
- [Quriust](https://github.com/ScipioneParmigiano/quriust) — Blazing fast Rust library for circuit simulation.
- [RustQIP](https://github.com/Renmusxd/RustQIP) — Rust QC library leveraging graph building for efficient simulations.

### Swift

- [SwiftQuantumComputing](https://github.com/indisoluble/SwiftQuantumComputing) — Circuit simulator with a bit of genetic programming.

---

## Quantum Analog Hamiltonian

- [Bloqade](https://github.com/QuEraComputing/Bloqade.jl) — Julia package for quantum computation/simulation on neutral-atom architecture.
- [Pulser](https://github.com/pasqal-io/Pulser) — Python library for pulse-level/analog control of neutral atom devices.

---

## Quantum annealing

### C++

- [C-to-D-Wave](https://github.com/lanl/c2dwave) — Compile a very small subset of C to a D-Wave Hamiltonian.

### Go

- [edif2qmasm](https://github.com/lanl/edif2qmasm/) — Compile Verilog/VHDL and other HDLs to a D-Wave Hamiltonian.
- [QA Prolog](https://github.com/lanl/QA-Prolog) — Compile a subset of Prolog to a D-Wave Hamiltonian.

### Julia

- [QAOA.jl](https://github.com/FZJ-PGI-12/QAOA.jl) — Simulate quantum annealing and mean-field quantum annealing in Julia.

### Python

- [chimera_embedding](https://github.com/dwavesystems/chimera-embedding) — Generate native-structured embeddings for Chimera graphs.
- [dimod](https://github.com/dwavesystems/dimod) — Shared API for Ising and QUBO problems.
- [dwavebinarycsp](https://github.com/dwavesystems/dwavebinarycsp) — Map CSPs with binary variables to BQMs.
- [dwave-cloud-client](https://github.com/dwavesystems/dwave-cloud-client) — Minimal REST client for D‑Wave Solver API.
- [dwave_neal](https://github.com/dwavesystems/dwave-neal) — Simulated annealing sampler.
- [dwave_networkx](https://github.com/dwavesystems/dwave_networkx) — Exploration and analysis of network graphs.
- [dwave-system](https://github.com/dwavesystems/dwave-system) — Easy incorporation of D‑Wave quantum annealers as samplers in the [Ocean](https://ocean.dwavesys.com/) stack.
- [embedding_utilities](https://github.com/dwavesystems/dwave_embedding_utilities) — Mapping samples between original and embedded graph.
- [micro_client_sapi_dimod](https://github.com/dwavesystems/dwave_micro_client_dimod) — [dimod](https://github.com/dwavesystems/dimod) wrapper for the D-Wave Micro Client.
- [minorminer](https://github.com/dwavesystems/minorminer) — Heuristic tool for minor graph embedding.
- [penaltymodel](https://github.com/dwavesystems/penaltymodel) — Utilities and interfaces for penalty models.
- [QMASM](https://github.com/lanl/qmasm/) — Quantum macro assembler for D-Wave systems.
- [qubo-nn](https://github.com/instance01/qubo-nn/) — Classifying, auto-encoding and reverse-engineering QUBO matrices.
- [qubovert](https://github.com/jtiosue/qubovert) — Formulating and simulated annealing of Ising, QUBO, and higher-order problems with constraints.

### Python, C & Matlab

- [Qbsolv](https://github.com/dwavesystems/qbsolv) — QUBO solver with D‑Wave or classical tabu solver backend.

---

Notes:
- All entries are open-source as per the source list.
- Some projects interface with commercial QPUs/services (which may be paid), but the simulator tooling itself is open-source.
