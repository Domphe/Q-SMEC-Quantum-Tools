import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

tables = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

print("\n" + "="*80)
print("QCBD DATABASE DEEP ANALYSIS REPORT")
print("="*80)

print("\n1. DATABASE COVERAGE")
print("-" * 80)
total = 0
for table in tables:
    if table == 'sqlite_sequence': continue
    count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table:30s}: {count:5d}")
    total += count
print(f"  {'TOTAL':30s}: {total:5d}")

print("\n2. EXPERT QC/QP RECOMMENDATIONS")
print("-" * 80)

recommendations = [
    ("CRITICAL", "Excited State Methods", 150, ["TDDFT functionals (CAM-B3LYP, LC-wPBE, M06-2X)", "ADC(2), ADC(3) for UV-Vis spectra", "EOM-CCSD for high-accuracy excited states", "Citations: Casida (2012), Laurent & Jacquemin (2013), Dreuw (2015)"]),
    ("CRITICAL", "Quantum Sensor Physics", 120, ["SQUID fundamentals: Josephson equations, flux quantization", "NV centers: spin Hamiltonian, ODMR, magnetometry", "Quantum dot sensors: Coulomb blockade, charge sensing", "Citations: Clarke & Braginski (2004), Doherty (2013), Budker (2007)"]),
    ("HIGH", "Superconductivity Theory", 200, ["BCS theory: gap equation, coherence length", "Eliashberg equations: a2F(w), McMillan formula", "DFT for Tc: DFPT electron-phonon coupling", "Database: Materials Project, SuperCon (NIST)", "Citations: Bardeen (1957), Sanna (2018), Drozdov (2015)"]),
    ("HIGH", "Electromagnetic Theory", 100, ["FDTD method: Yee algorithm, PML boundaries", "Complex permittivity: Drude-Lorentz models", "Metamaterials: negative index, effective medium", "Citations: Taflove & Hagness (2005), Smith (2004)"]),
    ("MEDIUM", "Thermoelectric Transport", 80, ["BoltzTraP: Boltzmann transport theory", "ZT optimization: Seebeck, conductivity, thermal", "Database: TEDesignLab, Materials Project", "Citations: Madsen & Singh (2006), Lindsay (2010)"])
]

total_recs = 0
for priority, area, count, details in recommendations:
    print(f"\n[{priority}] {area} (~{count} records)")
    for detail in details:
        print(f"  - {detail}")
    total_recs += count

print(f"\n3. PHASE 1 SUMMARY")
print("-" * 80)
print(f"  Total Estimated Records: ~{total_recs}")
print(f"  Timeline: 8-12 weeks for full Phase 1")
print(f"  Database Growth: {total} -> ~{total + total_recs} (+{100*total_recs/total:.0f}%)")

print("\n4. KEY LITERATURE REFERENCES")
print("-" * 80)
print("""  Excited States:
  - Casida & Huix-Rotllant, Ann. Rev. Phys. Chem., 2012, 63, 287
  - Laurent & Jacquemin, Int. J. Quantum Chem., 2013, 113, 2019
  
  Superconductivity:
  - Bardeen et al., Phys. Rev., 1957, 108, 1175 (BCS)
  - Sanna et al., J. Phys. Soc. Jpn., 2018, 87, 041012
  
  Sensors:
  - Clarke & Braginski, The SQUID Handbook, 2004
  - Doherty et al., Phys. Rep., 2013, 528, 1
  
  Databases:
  - Materials Project: https://materialsproject.org/
  - SuperCon: http://supercon.nims.go.jp/
  - GMTKN55: Goerigk et al., PCCP, 2017, 19, 32184""")

conn.close()
print("\n" + "="*80 + "\n")
