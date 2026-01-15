"""Query database to verify arXiv ingestion."""
import sqlite3
from pathlib import Path
from utils import DB_DIR

db_path = DB_DIR / 'qc_qp_expert.db'
conn = sqlite3.connect(db_path)

# Count arXiv records
cursor = conn.execute("SELECT COUNT(*) FROM sources WHERE id LIKE 'src.arxiv.%'")
arxiv_count = cursor.fetchone()[0]
print(f"✓ Found {arxiv_count} arXiv preprints in database")

# Sample a few records
cursor = conn.execute("SELECT id, title, doi FROM sources WHERE id LIKE 'src.arxiv.%' LIMIT 5")
print(f"\nSample arXiv records:")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1][:60]}{'...' if len(row[1]) > 60 else ''}")

# Count by source type
cursor = conn.execute("""
    SELECT 
        CASE 
            WHEN id LIKE 'src.arxiv.%' THEN 'arXiv'
            WHEN id LIKE 'src.crossref.%' THEN 'Crossref'
            ELSE 'Other'
        END as source_type,
        COUNT(*) as count
    FROM sources
    GROUP BY source_type
""")
print(f"\nSources by type:")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
print(f"\n✓ Database verification complete")
