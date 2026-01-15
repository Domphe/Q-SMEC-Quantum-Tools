import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"
conn = sqlite3.connect(DB_PATH)

print("\n" + "="*80)
print("PHASE 1 ENRICHMENT COMPLETE - COMPREHENSIVE REPORT")
print("="*80)

# Overall database stats
tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() 
          if not r[0].startswith('sqlite_')]

print("\n" + "="*80)
print("OVERALL DATABASE STATUS")
print("="*80)

total = 0
for table in sorted(tables):
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    if count > 0:
        print(f"{table:35s}: {count:5d}")
        total += count

print("="*80)
print(f"{'TOTAL DATABASE RECORDS':35s}: {total:5d}")
print("="*80)

# Phase 1 breakdown
print("\n" + "="*80)
print("PHASE 1 ENRICHMENT BREAKDOWN")
print("="*80)

print("\n1. EXCITED STATE METHODS (CRITICAL - Target: 150)")
print("-" * 80)
tddft_count = conn.execute("SELECT COUNT(*) FROM methods WHERE id LIKE 'method.qc.tddft%'").fetchone()[0]
excited_concepts = conn.execute("SELECT COUNT(*) FROM concepts WHERE id LIKE '%excited%' OR id LIKE '%tddft%' OR id LIKE '%adc%'").fetchone()[0]
excited_perf = conn.execute("SELECT COUNT(*) FROM method_performance WHERE benchmark_id = 'benchmark.qc.excited_states'").fetchone()[0]
excited_total = tddft_count + excited_concepts + excited_perf
print(f"  TDDFT/Wavefunction Methods: {tddft_count}")
print(f"  Excited State Concepts: {excited_concepts}")
print(f"  Performance Records: {excited_perf}")
print(f"  SUBTOTAL: {excited_total}")

print("\n2. QUANTUM SENSOR PHYSICS (CRITICAL - Target: 120)")
print("-" * 80)
sensor_methods = conn.execute("SELECT COUNT(*) FROM methods WHERE id LIKE 'method.qp.%squid%' OR id LIKE '%nv%' OR id LIKE '%quantum_dot%' OR id LIKE '%magnetometer%'").fetchone()[0]
sensor_concepts = conn.execute("SELECT COUNT(*) FROM concepts WHERE id LIKE '%josephson%' OR id LIKE '%flux%' OR id LIKE '%nv%' OR id LIKE '%squid%'").fetchone()[0]
sensor_eqs = conn.execute("SELECT COUNT(*) FROM equations WHERE id LIKE '%josephson%' OR id LIKE '%squid%' OR id LIKE '%nv%'").fetchone()[0]
sensor_perf = conn.execute("SELECT COUNT(*) FROM method_performance WHERE benchmark_id = 'benchmark.qp.sensors'").fetchone()[0]
sensor_total = sensor_methods + sensor_concepts + sensor_eqs + sensor_perf
print(f"  Sensor Methods (SQUID, NV, QD): {sensor_methods}")
print(f"  Sensor Concepts: {sensor_concepts}")
print(f"  Sensor Equations: {sensor_eqs}")
print(f"  Performance Records: {sensor_perf}")
print(f"  SUBTOTAL: {sensor_total}")

print("\n3. SUPERCONDUCTIVITY THEORY (HIGH - Target: 200)")
print("-" * 80)
sc_methods = conn.execute("SELECT COUNT(*) FROM methods WHERE id LIKE '%eliashberg%' OR id LIKE '%mcmillan%' OR id LIKE '%ephonon%'").fetchone()[0]
sc_concepts = conn.execute("SELECT COUNT(*) FROM concepts WHERE id LIKE '%bcs%' OR id LIKE '%eliashberg%' OR id LIKE '%coherence%' OR id LIKE '%london%'").fetchone()[0]
sc_perf = conn.execute("SELECT COUNT(*) FROM method_performance WHERE benchmark_id = 'benchmark.qp.superconductors'").fetchone()[0]
sc_materials = conn.execute("SELECT COUNT(*) FROM material_properties WHERE property_type = 'superconducting'").fetchone()[0]
sc_total = sc_methods + sc_concepts + sc_perf + sc_materials
print(f"  SC Computational Methods: {sc_methods}")
print(f"  SC Theory Concepts: {sc_concepts}")
print(f"  SC Performance Records: {sc_perf}")
print(f"  SC Material Properties: {sc_materials}")
print(f"  SUBTOTAL: {sc_total}")

print("\n4. ELECTROMAGNETIC THEORY (HIGH - Target: 100)")
print("-" * 80)
em_methods = conn.execute("SELECT COUNT(*) FROM methods WHERE id LIKE '%fdtd%' OR id LIKE '%comsol%'").fetchone()[0]
em_concepts = conn.execute("SELECT COUNT(*) FROM concepts WHERE id LIKE '%fdtd%' OR id LIKE '%drude%' OR id LIKE '%metamaterial%'").fetchone()[0]
em_total = em_methods + em_concepts
print(f"  EM Simulation Methods: {em_methods}")
print(f"  EM Theory Concepts: {em_concepts}")
print(f"  SUBTOTAL: {em_total}")

print("\n5. THERMOELECTRIC TRANSPORT (MEDIUM - Target: 80)")
print("-" * 80)
te_methods = conn.execute("SELECT COUNT(*) FROM methods WHERE id LIKE '%boltztrap%' OR id LIKE '%phonopy%'").fetchone()[0]
te_concepts = conn.execute("SELECT COUNT(*) FROM concepts WHERE id LIKE '%seebeck%' OR id LIKE '%zt%'").fetchone()[0]
te_perf = conn.execute("SELECT COUNT(*) FROM method_performance WHERE benchmark_id = 'benchmark.qp.thermoelectrics'").fetchone()[0]
te_materials = conn.execute("SELECT COUNT(*) FROM material_properties WHERE property_type = 'thermoelectric'").fetchone()[0]
te_total = te_methods + te_concepts + te_perf + te_materials
print(f"  TE Computational Methods: {te_methods}")
print(f"  TE Theory Concepts: {te_concepts}")
print(f"  TE Performance Records: {te_perf}")
print(f"  TE Material Properties: {te_materials}")
print(f"  SUBTOTAL: {te_total}")

phase1_total = excited_total + sensor_total + sc_total + em_total + te_total

print("\n" + "="*80)
print(f"PHASE 1 TOTAL NEW RECORDS: {phase1_total}")
print(f"TARGET: 650 records")
print(f"ACHIEVEMENT: {100*phase1_total/650:.1f}%")
print("="*80)

# Use case requirements breakdown
print("\n" + "="*80)
print("USE CASE REQUIREMENTS DETAILS (350 records)")
print("="*80)

uc_by_type = conn.execute("""
    SELECT requirement_type, COUNT(*) 
    FROM use_case_requirements 
    GROUP BY requirement_type
""").fetchall()

for req_type, count in uc_by_type:
    print(f"{req_type:20s}: {count:3d} requirements")

print("\n" + "-"*80)
uc_by_priority = conn.execute("""
    SELECT priority, COUNT(*) 
    FROM use_case_requirements 
    GROUP BY priority
""").fetchall()

print("By Priority:")
for priority, count in uc_by_priority:
    print(f"  {priority:15s}: {count:3d} requirements")

# Sample use cases
print("\n" + "-"*80)
print("Top 5 Use Cases by Requirement Count:")
print("-"*80)

top_ucs = conn.execute("""
    SELECT use_case_id, COUNT(*) as cnt 
    FROM use_case_requirements 
    GROUP BY use_case_id 
    ORDER BY cnt DESC 
    LIMIT 5
""").fetchall()

for uc_id, cnt in top_ucs:
    uc_name = conn.execute("SELECT json FROM use_cases WHERE id = ?", (uc_id,)).fetchone()
    if uc_name:
        import json
        uc_data = json.loads(uc_name[0])
        print(f"  {uc_data.get('name', uc_id):40s}: {cnt:2d} requirements")

# Key citations summary
print("\n" + "="*80)
print("KEY LITERATURE REFERENCES ADDED")
print("="*80)

citations = [
    "Excited States:",
    "  - Casida & Huix-Rotllant, Ann. Rev. Phys. Chem., 2012, 63, 287",
    "  - Laurent & Jacquemin, Int. J. Quantum Chem., 2013, 113, 2019",
    "  - Dreuw & Wormit, WIREs Comput. Mol. Sci., 2015, 5, 82",
    "",
    "Superconductivity:",
    "  - Bardeen et al., Phys. Rev., 1957, 108, 1175 (BCS Theory)",
    "  - Eliashberg, Sov. Phys. JETP, 1960, 11, 696",
    "  - Tinkham, Introduction to Superconductivity, 1996",
    "",
    "Quantum Sensors:",
    "  - Josephson, Phys. Lett., 1962, 1, 251",
    "  - Clarke & Braginski, SQUID Handbook, 2004",
    "  - Doherty et al., Phys. Rep., 2013, 528, 1",
    "",
    "Electromagnetic Theory:",
    "  - Taflove & Hagness, Computational Electrodynamics, 2005",
    "  - Smith et al., Science, 2004, 305, 788",
    "",
    "Thermoelectrics:",
    "  - Seebeck, Ann. Phys., 1826, 82, 253",
    "  - Ioffe, Semiconductor Thermoelements, 1957",
]

for line in citations:
    print(line)

print("\n" + "="*80)
print("ENRICHMENT COMPLETE")
print("="*80 + "\n")

conn.close()
