import sqlite3
from pathlib import Path

db_path = Path('g:/My Drive/Databases/QCBD/db/qc_qp_expert.db')
conn = sqlite3.connect(db_path)

print("="*70)
print("QCBD DATABASE COMPREHENSIVE SUMMARY - December 3, 2025")
print("="*70)
print()

# Table counts
tables = ['sources', 'concepts', 'methods', 'equations', 'workflows', 
          'software_tools', 'datasets', 'use_cases', 'glossary']
          
print("DATABASE RECORD COUNTS:")
print("-"*70)
total = 0
for table in tables:
    count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    print(f"  {table:20s}: {count:5d} records")
    total += count
print("-"*70)
print(f"  {'TOTAL':20s}: {total:5d} records")
print()

# Concepts breakdown
print("CONCEPTS BREAKDOWN BY DOMAIN:")
print("-"*70)
concepts = conn.execute("SELECT domain, COUNT(*) FROM concepts GROUP BY domain").fetchall()
for domain, count in concepts:
    print(f"  {domain:30s}: {count:3d} concepts")
print()

# Methods breakdown
print("METHODS BREAKDOWN BY DOMAIN:")
print("-"*70)
methods = conn.execute("SELECT domain, COUNT(*) FROM methods GROUP BY domain").fetchall()
for domain, count in methods:
    print(f"  {domain:30s}: {count:3d} methods")
print()

# Equations breakdown
print("EQUATIONS BREAKDOWN BY DOMAIN:")
print("-"*70)
equations = conn.execute("SELECT domain, COUNT(*) FROM equations GROUP BY domain").fetchall()
for domain, count in equations:
    print(f"  {domain:30s}: {count:3d} equations")
print()

# Software tools breakdown
print("SOFTWARE TOOLS BREAKDOWN BY DOMAIN:")
print("-"*70)
tools = conn.execute("SELECT domain, COUNT(*) FROM software_tools GROUP BY domain").fetchall()
for domain, count in tools:
    print(f"  {domain:30s}: {count:3d} tools")
print()

# Glossary breakdown
print("GLOSSARY BREAKDOWN BY DOMAIN:")
print("-"*70)
glossary = conn.execute("SELECT domain, COUNT(*) FROM glossary GROUP BY domain").fetchall()
for domain, count in glossary:
    print(f"  {domain:30s}: {count:3d} terms")
print()

# Use cases breakdown
print("USE CASES BREAKDOWN BY SECTOR:")
print("-"*70)
use_cases = conn.execute("SELECT sector, COUNT(*) FROM use_cases GROUP BY sector ORDER BY COUNT(*) DESC").fetchall()
for sector, count in use_cases:
    print(f"  {sector:40s}: {count:3d} use cases")
print()

# Datasets/Benchmarks
print("DATASETS/BENCHMARKS:")
print("-"*70)
datasets_count = conn.execute("SELECT COUNT(*) FROM datasets WHERE json LIKE '%benchmark%'").fetchone()[0]
molecules_count = conn.execute("SELECT COUNT(*) FROM datasets WHERE json LIKE '%smiles%'").fetchone()[0]
print(f"  Benchmark datasets                      : {datasets_count:3d}")
print(f"  Benchmark molecules with SMILES         : {molecules_count:3d}")
print()

print("="*70)
print("Q-SMEC EXPANSION SUMMARY:")
print("="*70)
print("✓ Added 15 Q-SMEC concepts (bondon density, NEP, SNR, FOM, THz sensing,")
print("  metamaterials, PBA, quantum magnetometry, TRL, SWAP-C, CMMC, FedRAMP, ITAR)")
print()
print("✓ Added 10 Q-SMEC methods (DFT for superconductors, band structure,")
print("  BoltzTraP, FDTD, THz-TDS, SQUID, sensor optimization, PUF, QKD, ML fusion)")
print()
print("✓ Added 15 Q-SMEC equations (NEP, SNR, FOM, McMillan, Seebeck, ZT,")
print("  complex permittivity, RCS, impedance, plasma frequency, Nernst, Drude)")
print()
print("✓ Added 42 Q-SMEC glossary terms (all major acronyms and technical terms)")
print()
print("✓ Added 10 Q-SMEC software tools (VASP, Wien2k, BoltzTraP, CST, COMSOL,")
print("  OpenEMS, MEEP, Materials Project, AFLOW, Phonopy)")
print()
print("✓ Added 6 Q-SMEC workflows (material screening, metamaterial design,")
print("  sensor design, THz characterization, thermoelectric, PBA battery)")
print()
print("✓ Maintained 35 Q-SMEC use cases across 11 DHS sectors")
print()
print("✓ Maintained 30 benchmark molecules with SMILES notation")
print()
print("="*70)

conn.close()
