import sqlite3
conn = sqlite3.connect('g:/My Drive/Databases/QCBD/qc_graph.db')
tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print('Tables:', [t[0] for t in tables])
for t in tables:
    print(f'\n{t[0]} columns:')
    cols = conn.execute(f'PRAGMA table_info({t[0]})').fetchall()
    for col in cols:
        print(f'  {col[1]} ({col[2]})')
