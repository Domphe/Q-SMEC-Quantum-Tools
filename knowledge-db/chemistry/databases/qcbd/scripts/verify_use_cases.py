import sqlite3
import json

conn = sqlite3.connect('db/qc_qp_expert.db')
cur = conn.cursor()

# Count use cases
cur.execute("SELECT COUNT(*) FROM use_cases")
count = cur.fetchone()[0]
print(f"Total Q-SMEC use cases: {count}")

# Get use cases by sector
cur.execute("SELECT sector, COUNT(*) FROM use_cases GROUP BY sector ORDER BY COUNT(*) DESC")
print("\nUse cases by sector:")
print("-" * 80)
for row in cur.fetchall():
    sector, cnt = row
    print(f"  {sector:40} {cnt:3} use cases")

# Show sample use cases with key details
cur.execute("""
    SELECT id, name, sector, json 
    FROM use_cases 
    LIMIT 10
""")

print("\n\nFirst 10 use cases:")
print("-" * 80)
for row in cur.fetchall():
    uc_id, name, sector, json_data = row
    data = json.loads(json_data)
    market = data.get('market_size_billion', 'N/A')
    cagr = data.get('cagr_percent', 'N/A')
    trl = data.get('trl_target', 'N/A')
    print(f"  {name}")
    print(f"    Sector: {sector}")
    print(f"    Market: ${market}B | CAGR: {cagr}% | TRL: {trl}")
    print()

# Get high-value use cases (>$10B market)
cur.execute("SELECT name, json FROM use_cases")
high_value = []
for row in cur.fetchall():
    name, json_data = row
    data = json.loads(json_data)
    market = data.get('market_size_billion', 0)
    if market >= 10:
        high_value.append((name, market, data.get('cagr_percent', 0)))

print("\nHigh-value use cases (>$10B market):")
print("-" * 80)
for name, market, cagr in sorted(high_value, key=lambda x: x[1], reverse=True):
    print(f"  {name:45} ${market:5.1f}B | CAGR: {cagr:3}%")

conn.close()
