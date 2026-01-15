# ORCA User Guide

## Overview

**ORCA** is a free-for-academic-use quantum chemistry package developed by Frank Neese and colleagues at the Max Planck Institute. Known for its excellent performance on transition metal systems, ORCA excels at DFT, multireference methods (CASSCF, NEVPT2), and spectroscopy calculations.

**Entity ID:** `tool_orca`  
**Current Version:** 5.0.4 (as of 2024)  
**License:** Free for academic use  
**Platforms:** Linux, macOS, Windows

---

## Key Strengths

- ✅ **Transition metal chemistry** - Excellent DFT and CASSCF for d/f-block
- ✅ **Spectroscopy** - UV-Vis, EPR, NMR, Mössbauer, X-ray absorption
- ✅ **Efficient parallel** - Excellent scaling on multi-core systems
- ✅ **User-friendly syntax** - Simple input files
- ✅ **Free for academics** - No license fees for universities
- ✅ **Active development** - Regular updates with new features

---

## Installation

### Download
1. Register at: https://orcaforum.kofo.mpg.de
2. Download ORCA binary for your platform
3. Extract to `/opt/orca` (Linux) or `C:\orca` (Windows)

### Environment Setup

**Linux/macOS:**
```bash
export ORCA_ROOT=/opt/orca
export PATH=$ORCA_ROOT:$PATH
export LD_LIBRARY_PATH=$ORCA_ROOT:$LD_LIBRARY_PATH
```

**Windows:**
```powershell
$env:ORCA_ROOT = "C:\orca"
$env:PATH += ";$env:ORCA_ROOT"
```

### Test Installation
```bash
orca --version
# Should output: ORCA 5.0.4 - RELEASED ...
```

---

## Basic Usage

### Input File Structure

ORCA uses simple keyword-based input:

```bash
# water_opt.inp
! B3LYP def2-TZVP Opt

* xyz 0 1
O   0.0000   0.0000   0.1173
H   0.0000   0.7572  -0.4692
H   0.0000  -0.7572  -0.4692
*
```

**Run:**
```bash
orca water_opt.inp > water_opt.out &
```

### Key Input Sections

#### 1. **Simple Keywords** (`!` line)
```bash
! B3LYP def2-TZVP            # Method and basis set
! Opt Freq                    # Tasks
! TightSCF RIJCOSX           # Convergence and acceleration
```

#### 2. **Geometry** (`* xyz` block)
```bash
* xyz charge multiplicity
C   0.0   0.0   0.0
H   0.0   0.0   1.09
*
```

#### 3. **Block Keywords** (`%block`)
```bash
%scf
  MaxIter 200
  ConvForced true
end

%pal nprocs 8 end  # Use 8 cores
```

---

## Common Calculations

### 1. Single-Point Energy
```bash
! B3LYP def2-TZVP

* xyzfile 0 1 geometry.xyz
```

### 2. Geometry Optimization
```bash
! B3LYP def2-TZVP Opt

%geom
  MaxIter 100
  Convergence Tight
end

* xyzfile 0 1 start_geom.xyz
```

### 3. Frequency Calculation
```bash
! B3LYP def2-TZVP Freq

* xyzfile 0 1 optimized.xyz
```

### 4. Transition State Search
```bash
! B3LYP def2-TZVP OptTS NumFreq

%geom
  Calc_Hess true    # Calculate Hessian at start
  Recalc_Hess 5     # Recalculate every 5 steps
end

* xyzfile 0 1 ts_guess.xyz
```

### 5. Excited States (TD-DFT)
```bash
! B3LYP def2-TZVP TDDFT

%tddft
  NRoots 10          # Calculate 10 excited states
  MaxDim 5           # Davidson expansion
end

* xyzfile 0 1 ground_state.xyz
```

---

## Method Selection

### DFT Functionals

**GGA:**
```bash
! BP86 def2-TZVP      # Becke-Perdew
! PBE def2-TZVP       # Perdew-Burke-Ernzerhof
```

**Hybrid:**
```bash
! B3LYP def2-TZVP     # 20% HF exchange
! PBE0 def2-TZVP      # 25% HF exchange
```

**Meta-GGA:**
```bash
! M06L def2-TZVP      # Local meta-GGA
! M06 def2-TZVP       # 27% HF exchange
! M06-2X def2-TZVP    # 54% HF exchange (main-group)
```

**Range-separated:**
```bash
! wB97X-D3 def2-TZVP  # With dispersion
```

### Dispersion Corrections

ORCA makes it easy:
```bash
! B3LYP D3BJ def2-TZVP    # Grimme's D3 with BJ damping
! PBE D4 def2-TZVP         # D4 correction
```

---

## Basis Sets

### Def2 Series (Recommended)
```bash
! def2-SVP      # Double-zeta (fast)
! def2-TZVP     # Triple-zeta (balanced)
! def2-TZVPP    # Triple-zeta + extra polarization
! def2-QZVPP    # Quadruple-zeta (high accuracy)
```

### With ECPs (Effective Core Potentials)
```bash
! def2-TZVP def2-ECP  # Automatically uses ECPs for heavy atoms
```

### Correlation-consistent
```bash
! cc-pVDZ
! cc-pVTZ
! aug-cc-pVTZ    # With diffuse functions
```

---

## Performance Optimization

### RIJCOSX Approximation
Speeds up hybrid DFT by ~10x:
```bash
! B3LYP def2-TZVP RIJCOSX def2/J
```

### Parallelization
```bash
%pal nprocs 16 end     # Use 16 CPU cores
```

### Memory Allocation
```bash
%maxcore 2000          # 2000 MB per core
```

---

## Multireference Methods

### CASSCF (Complete Active Space SCF)
```bash
! CASSCF def2-TZVP

%casscf
  nel 10          # 10 active electrons
  norb 10         # 10 active orbitals
  mult 3          # Triplet state
  nroots 3        # 3 states
end

* xyzfile 0 3 geometry.xyz
```

### NEVPT2 (Perturbation correction)
```bash
! CASSCF NEVPT2 def2-TZVP

%casscf
  nel 8
  norb 8
end

* xyzfile 0 1 geometry.xyz
```

---

## Spectroscopy

### EPR (Electron Paramagnetic Resonance)
```bash
! UKS B3LYP def2-TZVP

%eprnmr
  Nuclei = all C {aiso}  # All carbons, hyperfine coupling
  Nuclei = all H {aiso}
end

* xyz 0 2  # Doublet radical
C 0 0 0
...
*
```

### UV-Vis Spectrum
```bash
! B3LYP def2-TZVP TDDFT

%tddft
  NRoots 20
  MaxDim 5
end

* xyzfile 0 1 molecule.xyz
```

---

## Troubleshooting

### SCF Not Converging

**Error:** `SCF NOT CONVERGED AFTER MAX ITERATIONS`

**Solutions:**
```bash
%scf
  MaxIter 500
  ConvForced true     # Force convergence with damping
  Shift Shift 0.3 ErrOff 0.05 end
end
```

### Geometry Optimization Failing

**Error:** `GEOMETRY OPTIMIZATION FAILED TO CONVERGE`

**Solutions:**
```bash
%geom
  MaxIter 200
  Trust 0.1         # Smaller initial trust radius
  inhess almloef    # Better Hessian guess
end
```

### Insufficient Memory

**Error:** `NOT ENOUGH MEMORY`

**Solutions:**
```bash
%maxcore 4000        # Increase to 4 GB per core
```

Or use RIJCOSX approximation to reduce memory.

---

## Output File Parsing

### Extract Final Energy
```bash
grep "FINAL SINGLE POINT ENERGY" water_opt.out
# FINAL SINGLE POINT ENERGY      -76.342156841829
```

### Extract Optimized Geometry
```bash
# Last geometry in trajectory file
cat water_opt.xyz
```

### Extract Frequencies
```bash
grep "cm**-1" water_opt.out | grep -A100 "VIBRATIONAL FREQUENCIES"
```

---

## Example Workflows

### Complete Thermochemistry Workflow
```bash
# 1. Optimize geometry
! B3LYP D3BJ def2-TZVP Opt TightOPT
* xyz 0 1
...
*

# 2. Run with optimized geometry (after first job)
! B3LYP D3BJ def2-TZVP Freq
* xyzfile 0 1 geometry.xyz
```

### Transition State Characterization
```bash
# 1. Find TS
! B3LYP def2-TZVP OptTS NumFreq
%geom Calc_Hess true end
* xyz 0 1
...
*

# 2. Verify (should have exactly 1 imaginary frequency)
grep "***imaginary mode***" output.out

# 3. IRC (Intrinsic Reaction Coordinate)
! B3LYP def2-TZVP IRC
%irc
  MaxIter 50
  Direction both
end
* xyzfile 0 1 ts_optimized.xyz
```

---

## Best Practices

1. **Always optimize first** - Don't calculate properties on unoptimized structures
2. **Use RIJCOSX for hybrids** - 10x speedup with negligible error
3. **Include dispersion** - Use D3BJ or D4 for most systems
4. **Check convergence** - Look for "ORCA TERMINATED NORMALLY"
5. **Verify frequencies** - 0 imaginary = minimum, 1 imaginary = TS
6. **Archive outputs** - ORCA doesn't keep old outputs by default

---

## Resources

- **Manual:** https://www.faccts.de/docs/orca/5.0/manual/
- **Forum:** https://orcaforum.kofo.mpg.de
- **Tutorials:** https://www.youtube.com/@FrankNeese
- **Input Library:** https://sites.google.com/site/orcainputlibrary/

---

## Related Topics

- [DFT Methods](../methods/dft.md)
- [CASSCF](../methods/casscf.md)
- [Geometry Optimization Workflow](../workflows/geometry_optimization.md)
- [TD-DFT for Excited States](../methods/tddft.md)
