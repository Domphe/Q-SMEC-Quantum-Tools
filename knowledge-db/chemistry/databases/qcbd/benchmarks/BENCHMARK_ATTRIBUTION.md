# QCDB Benchmark Data Attribution

This document provides full citations and licensing information for all benchmark datasets included in the QCBD knowledge base.

## Noncovalent Interaction Benchmarks

### S22 Dataset

**Citation:**

```
Jurecka, P.; Sponer, J.; Cerny, J.; Hobza, P.
"Benchmark database of accurate (MP2 and CCSD(T) complete basis set limit) 
interaction energies of small model complexes, DNA base pairs, and amino acid pairs"
Physical Chemistry Chemical Physics, 2006, 8, 1985-1993.
DOI: 10.1021/ct600281g
```

**License:** CC0-1.0 (Public Domain)

**Description:** 22 hydrogen-bonded and dispersion-bound molecular dimers with CCSD(T)/CBS reference energies.

**Data Source:** <http://www.begdb.com/>

---

### S66 Dataset

**Citation:**

```
Řezáč, J.; Riley, K. E.; Hobza, P.
"S66: A Well-balanced Database of Benchmark Interaction Energies Relevant to Biomolecular Structures"
Journal of Chemical Theory and Computation, 2011, 7(8), 2427-2438.
DOI: 10.1021/ct200523a
```

**License:** CC-BY-4.0

**Description:** 66 noncovalent dimers covering 8 interaction types with CCSD(T)/CBS reference energies.

**Categories:** Hydrogen bonds, π-π stacking, London dispersion, electrostatics

---

### S66x8 Dataset

**Citation:** Same as S66 (Řezáč et al., 2011)

**Description:** S66 dimers at 8 different intermolecular distances (0.9, 0.95, 1.0, 1.05, 1.1, 1.25, 1.5, 2.0 × equilibrium distance)

---

## Thermochemistry Benchmarks

### GMTKN55 Database

**Citation:**

```
Goerigk, L.; Hansen, A.; Bauer, C.; Ehrlich, S.; Najibi, A.; Grimme, S.
"A look at the density functional theory zoo with the advanced GMTKN55 
database for general main group thermochemistry, kinetics and noncovalent interactions"
Physical Chemistry Chemical Physics, 2017, 19, 32184-32215.
DOI: 10.1039/c7cp04913g
```

**License:** CC-BY-4.0

**Description:** 55 subsets with 1505 data points covering:

- Thermochemistry (atomization energies, ionization potentials, electron affinities)
- Reaction barriers
- Noncovalent interactions
- Conformational energies
- Isomerization energies

**Data Source:** <https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/GMTKN/gmtkn55>

---

### G2/97 Test Set

**Citation:**

```
Curtiss, L. A.; Raghavachari, K.; Redfern, P. C.; Pople, J. A.
"Assessment of Gaussian-2 and density functional theories for the computation 
of enthalpies of formation"
Journal of Chemical Physics, 1997, 106, 1063-1079.
DOI: 10.1063/1.473182
```

**License:** Public Domain

**Description:** 148 molecules with experimental atomization energies, ionization potentials, electron affinities, and proton affinities.

---

### G3/99 Test Set

**Citation:**

```
Curtiss, L. A.; Redfern, P. C.; Raghavachari, K.; Pople, J. A.
"Gaussian-3 theory using reduced Møller-Plesset order"
Journal of Chemical Physics, 1999, 110, 4703-4709.
DOI: 10.1063/1.478676
```

**License:** Public Domain

**Description:** Extended version of G2/97 with 222 molecules.

---

### HEAT298 Dataset

**Citation:**

```
Harding, M. E.; Vazquez, J.; Ruscic, B.; Wilson, A. K.; Gauss, J.; Stanton, J. F.
"High-accuracy extrapolated ab initio thermochemistry. III. Additional improvements 
and overview"
Journal of Chemical Physics, 2008, 128, 114111.
DOI: 10.1063/1.3009270
```

**License:** CC-BY-4.0

**Description:** 6 small molecules with sub-kJ/mol accuracy heats of formation using high-accuracy extrapolated CCSDTQ calculations.

**Systems:** H₂O, CH₄, CO, N₂, C₂H₂, CO₂

---

### W4-11 Dataset

**Citation:**

```
Karton, A.; Daon, S.; Martin, J. M. L.
"W4-11: A high-confidence benchmark dataset for computational thermochemistry 
derived from first-principles W4 data"
Chemical Physics Letters, 2011, 510, 165-178.
DOI: 10.1063/1.3609250
```

**License:** CC-BY-4.0

**Description:** 140 molecules with high-accuracy atomization energies from W4 theory.

---

## Water Cluster Benchmarks

### WATER27 Dataset

**Citation:**

```
Bryantsev, V. S.; Diallo, M. S.; van Duin, A. C. T.; Goddard, W. A.
"Evaluation of B3LYP, X3LYP, and M06-Class Density Functionals for Predicting 
the Binding Energies of Neutral, Protonated, and Deprotonated Water Clusters"
Journal of Chemical Theory and Computation, 2009, 5(4), 1016-1026.
DOI: 10.1021/ct300550x
```

**License:** CC-BY-4.0

**Description:** Water cluster binding energies with CCSD(T)/CBS reference values.

---

## Usage Guidelines

### Data Redistribution

All benchmark data in QCBD is redistributed in accordance with the original licenses:

- **CC0-1.0 (Public Domain):** No restrictions
- **CC-BY-4.0:** Requires attribution (provided above)
- **Public Domain:** No restrictions

### Citation Requirements

When using QCDB benchmark data in publications:

1. **Cite the original benchmark papers** (provided above)
2. **Cite QCDB:** "Q-SMEC Quantum Chemistry Database (QCDB), version 1.0.0, 2025"
3. **Acknowledge data sources:** "Benchmark data obtained from [source] via QCDB"

### Data Quality

All reference values in QCDB are:

- Directly sourced from original publications or official databases
- Verified against multiple sources when possible
- Accompanied by uncertainty estimates where available
- Documented with calculation details (method, basis set, geometry optimization protocol)

---

## Contact & Updates

For questions about benchmark data or to report issues:

- Repository: Internal Q-SMEC Development
- Email: Contact Q-SMEC Development Team
- Last Updated: December 1, 2025

---

## Disclaimer

While every effort has been made to ensure accuracy, users should:

1. Verify critical values against original sources
2. Understand the limitations of each benchmark
3. Report any discrepancies to the QCDB team

The QCDB team is not responsible for errors in the original benchmark data.
