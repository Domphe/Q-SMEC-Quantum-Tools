"""Check benchmark loading status in database."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get all tables
tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

print("Database Content Summary:")
print("=" * 60)
print(f"Tables: {', '.join(tables)}")
print(f"Total datasets: {c.execute('SELECT COUNT(*) FROM datasets').fetchone()[0]}")

# Check for Q-SMEC benchmarks
qsmec_results = c.execute("""
    SELECT id, domain, json
    FROM datasets 
    WHERE id LIKE '%superconductor%' 
       OR id LIKE '%thermoelectric%' 
       OR id LIKE '%permittivity%'
       OR id LIKE '%nep_sensor%'
       OR id LIKE '%snr_sensor%'
       OR id LIKE '%rcs_stealth%'
    LIMIT 10
""").fetchall()

print(f"\nQ-SMEC Benchmarks (sample): {len(qsmec_results)} found")
for row in qsmec_results[:3]:
    import json
    data = json.loads(row[2])
    name = data.get('name', 'N/A')
    print(f"  - {row[0]}: {name} ({row[1]})")

# Check for advanced QC/QP benchmarks
advanced_results = c.execute("""
    SELECT id, domain, json
    FROM datasets 
    WHERE id LIKE '%reaction_barriers%'
       OR id LIKE '%excited_states%'
       OR id LIKE '%s66x8%'
       OR id LIKE '%conformers%'
       OR id LIKE '%transition_metals%'
    LIMIT 10
""").fetchall()

print(f"\nAdvanced QC/QP Benchmarks (sample): {len(advanced_results)} found")
for row in advanced_results[:3]:
    import json
    data = json.loads(row[2])
    name = data.get('name', 'N/A')
    print(f"  - {row[0]}: {name} ({row[1]})")

# Get all benchmark domains
domains = c.execute("""
    SELECT DISTINCT domain, COUNT(*) 
    FROM datasets 
    GROUP BY domain
    ORDER BY COUNT(*) DESC
""").fetchall()

print(f"\nDataset Domains:")
for domain, count in domains:
    print(f"  - {domain}: {count}")

conn.close()
