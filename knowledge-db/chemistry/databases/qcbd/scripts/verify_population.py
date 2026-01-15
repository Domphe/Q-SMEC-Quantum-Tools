import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"
conn = sqlite3.connect(DB_PATH)

tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() 
          if not r[0].startswith('sqlite_')]

print("\n" + "="*60)
print("DATABASE POPULATION COMPLETE")
print("="*60)

total = 0
for table in sorted(tables):
    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table:35s}: {count:5d}")
    total += count

print("="*60)
print(f"{'TOTAL RECORDS':35s}: {total:5d}")
print("="*60)

print("\n" + "="*60)
print("NEWLY POPULATED TABLES")
print("="*60)
print(f"{'method_performance':35s}: {conn.execute('SELECT COUNT(*) FROM method_performance').fetchone()[0]:5d} records")
print(f"{'use_case_requirements':35s}: {conn.execute('SELECT COUNT(*) FROM use_case_requirements').fetchone()[0]:5d} records")
print(f"{'validation_results':35s}: {conn.execute('SELECT COUNT(*) FROM validation_results').fetchone()[0]:5d} records")

new_total = conn.execute('SELECT COUNT(*) FROM method_performance').fetchone()[0] + \
            conn.execute('SELECT COUNT(*) FROM use_case_requirements').fetchone()[0] + \
            conn.execute('SELECT COUNT(*) FROM validation_results').fetchone()[0]

print("="*60)
print(f"{'NEW RECORDS ADDED':35s}: {new_total:5d}")
print("="*60 + "\n")

conn.close()
