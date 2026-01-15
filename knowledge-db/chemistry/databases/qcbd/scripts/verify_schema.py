"""Verify expanded schema tables."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

tables = [row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]

print("Database Tables:")
print("=" * 60)

# Separate base tables from expanded schema
base_tables = ['sources', 'concepts', 'methods', 'equations', 'workflows', 
               'software_tools', 'datasets', 'glossary', 'benchmark_results', 
               'use_cases', 'sqlite_sequence']

expanded_tables = [t for t in tables if t not in base_tables]
base_present = [t for t in tables if t in base_tables]

print(f"\nBase Tables ({len(base_present)}):")
for t in sorted(base_present):
    count = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  - {t}: {count} records")

print(f"\nExpanded Schema Tables ({len(expanded_tables)}):")
for t in sorted(expanded_tables):
    count = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  - {t}: {count} records")

print(f"\nTotal Tables: {len(tables)}")

conn.close()
