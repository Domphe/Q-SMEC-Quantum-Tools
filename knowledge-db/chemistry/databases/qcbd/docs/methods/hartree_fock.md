# Hartree-Fock Method

## Overview

The **Hartree-Fock (HF)** method is the foundation of ab initio quantum chemistry. It solves the electronic Schrödinger equation by approximating the N-electron wavefunction as a single Slater determinant, treating electron-electron repulsion in a mean-field approximation.

**Entity ID:** `method_hartree_fock`  
**Computational Cost:** Low to Medium  
**Accuracy Level:** Medium  
**Best for:** Initial guess generation, qualitative molecular orbital analysis, small molecules

---

## Theoretical Basis

### The Hartree-Fock Approximation

HF makes two key approximations:

1. **Born-Oppenheimer Approximation:** Nuclei are fixed (no nuclear motion)
2. **Independent Particle Model:** Each electron moves in the average field of all other electrons

The HF energy is:

$$E_{HF} = \sum_i^{N/2} 2h_{ii} + \sum_i^{N/2} \sum_j^{N/2} (2J_{ij} - K_{ij})$$

Where:
- $h_{ii}$ = one-electron integrals (kinetic + nuclear attraction)
- $J_{ij}$ = Coulomb integrals (electron-electron repulsion)
- $K_{ij}$ = Exchange integrals (from antisymmetry)

---

## When to Use HF

### ✅ Good For:
- **Qualitative MO analysis** - Understanding orbital structure
- **Initial geometries** - Fast optimization for starting structures
- **Systems dominated by exchange** - Closed-shell organic molecules
- **Educational purposes** - Learning quantum chemistry concepts
- **Generating initial guess** - For correlated methods (MP2, CCSD(T))

### ❌ Not Suitable For:
- **Dispersion-dominated systems** - No London dispersion forces
- **Strongly correlated systems** - Bond breaking, radicals, transition metals
- **Quantitative energetics** - Typical errors: 5-10 kcal/mol for reaction energies
- **Noncovalent interactions** - Underestimates π-π stacking by orders of magnitude

---

## Variants

### Restricted Hartree-Fock (RHF)
- **Use case:** Closed-shell systems (all electrons paired)
- **Spin:** Singlet states only
- **Efficiency:** Fastest HF variant

### Unrestricted Hartree-Fock (UHF)
- **Use case:** Open-shell systems (unpaired electrons)
- **Spin:** Any spin multiplicity
- **Caveat:** Suffers from spin contamination

### Restricted Open-Shell Hartree-Fock (ROHF)
- **Use case:** Open-shell systems requiring pure spin states
- **Advantage:** No spin contamination
- **Disadvantage:** Slower convergence than UHF

---

## Computational Details

### Scaling
- **Formal scaling:** O(N⁴) with number of basis functions
- **Practical scaling:** O(N²·⁷) with efficient algorithms (DIIS, direct SCF)

### Memory Requirements
- **Conventional:** Stores full 4-index electron repulsion integral (ERI) tensor ~ O(N⁴)
- **Direct SCF:** Recomputes ERIs on-the-fly ~ O(N²) memory

### Typical Timings (Single-point, def2-TZVP)
- **Benzene (42 electrons):** < 1 second
- **Naphthalene (68 electrons):** ~5 seconds
- **Buckminsterfullerene (360 electrons):** ~10 minutes

---

## Accuracy Benchmarks

### G2/97 Test Set (Atomization Energies)
- **MAE:** 87 kcal/mol
- **RMSE:** 102 kcal/mol
- **Interpretation:** HF systematically underestimates binding

### S22 Noncovalent Interactions
- **Hydrogen bonding:** MAE = 1.2 kcal/mol (underestimates)
- **Dispersion:** MAE = 2.8 kcal/mol (severely underestimates)
- **Mixed:** MAE = 1.5 kcal/mol

### Reaction Barriers
- **Typical error:** -5 to -10 kcal/mol (barriers too low)
- **Why:** Missing electron correlation

---

## Software Implementation

### Available in:
- **Gaussian** - `# HF/def2-TZVP`
- **ORCA** - `! HF def2-TZVP`
- **Psi4** - `energy('scf/def2-tzvp')`
- **PySCF** - `mf = scf.RHF(mol)`
- **Q-Chem** - `METHOD = HF`
- **NWChem** - `task scf energy`
- **Molpro** - `{hf; wf,electrons,spin}`

### Convergence Options

**DIIS (Direct Inversion of Iterative Subspace):**
```python
# PySCF example
mf = scf.RHF(mol)
mf.diis = True
mf.diis_space = 8  # Number of DIIS vectors
```

**Level Shifting (for difficult SCF):**
```bash
# ORCA
! HF SlowConv
%scf
  Shift Shift 0.3 ErrOff 0.05 end
end
```

**Damping:**
```python
# Psi4
set damping_percentage 20
```

---

## Common Problems & Solutions

### Problem: SCF Not Converging

**Diagnostic:** Max iterations reached, energy oscillates

**Solutions:**
1. **Tighten integration grid** (DFT-specific, but analogous)
2. **Use level shift:** `Shift 0.5 0.0`
3. **Try damping:** Mix 70% new density + 30% old density
4. **Better initial guess:** `guess=core` or `guess=huckel`
5. **Check geometry:** May be far from minimum

### Problem: Wrong Number of Electrons

**Diagnostic:** Fractional occupation numbers, charge not matching

**Solution:**
```python
# PySCF - explicitly set charge and spin
mol.charge = 0
mol.spin = 0  # 2*S (0=singlet, 1=doublet, 2=triplet)
```

### Problem: Spin Contamination (UHF)

**Diagnostic:** ⟨S²⟩ >> S(S+1) after SCF

**Solutions:**
1. Switch to ROHF for pure spin
2. Use stability analysis: `stability_analysis='follow'`
3. Accept contamination and correct with projection (unreliable)

---

## Next Steps After HF

### Energy Corrections:
1. **MP2** - Add second-order perturbation correction (~70% of correlation)
2. **CCSD** - Iterative coupled cluster (expensive, accurate)
3. **CCSD(T)** - "Gold standard" with triples correction

### Improved Mean-Field:
1. **DFT (B3LYP, PBE0, ωB97X-D)** - Include correlation via functional
2. **Double-hybrid DFT** - Mix HF exchange with MP2 correlation

---

## Example Workflow

```python
# PySCF: Optimize benzene geometry with RHF
from pyscf import gto, scf, geomopt

mol = gto.M(
    atom='''
    C   0.000000   1.396000   0.000000
    C   1.209000   0.698000   0.000000
    C   1.209000  -0.698000   0.000000
    C   0.000000  -1.396000   0.000000
    C  -1.209000  -0.698000   0.000000
    C  -1.209000   0.698000   0.000000
    H   0.000000   2.479000   0.000000
    H   2.147000   1.240000   0.000000
    H   2.147000  -1.240000   0.000000
    H   0.000000  -2.479000   0.000000
    H  -2.147000  -1.240000   0.000000
    H  -2.147000   1.240000   0.000000
    ''',
    basis='def2-svp',
    symmetry=True
)

mf = scf.RHF(mol)
mf.kernel()

# Optimize geometry
mol_eq = geomopt.optimize(mf)
print(f"Optimized HF energy: {mol_eq.e_tot:.6f} Hartree")
```

---

## References

1. **Szabo & Ostlund** - *Modern Quantum Chemistry* (1989) - Classic HF theory textbook
2. **Helgaker, Jørgensen, Olsen** - *Molecular Electronic Structure Theory* (2000) - Comprehensive reference
3. **Jensen** - *Introduction to Computational Chemistry* (2017) - Practical guide

---

## Related Topics

- [DFT](dft.md) - More accurate mean-field method
- [Basis Sets](../concepts/basis_sets.md) - Choice affects HF quality
- [Electron Correlation](../concepts/electron_correlation.md) - What HF is missing
- [MP2](mp2.md) - Simplest post-HF method
- [Geometry Optimization](../workflows/geometry_optimization.md) - Using HF for structures
