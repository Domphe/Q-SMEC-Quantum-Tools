"""Check embeddings database status."""
import sqlite3
from pathlib import Path

EMBEDDINGS_DB = Path(__file__).parent.parent / "expert" / "embeddings.db"

conn = sqlite3.connect(EMBEDDINGS_DB)
c = conn.cursor()

# Count by type
counts = c.execute("""
    SELECT entity_type, COUNT(*) 
    FROM embeddings 
    GROUP BY entity_type 
    ORDER BY COUNT(*) DESC
""").fetchall()

print("Embeddings by type:")
for etype, count in counts:
    print(f"  {etype}: {count}")

# Sample use cases
use_cases = c.execute("""
    SELECT entity_id, name 
    FROM embeddings 
    WHERE entity_type = 'UseCases'
    LIMIT 10
""").fetchall()

print("\nSample Use Cases:")
for uid, name in use_cases:
    print(f"  - {uid}: {name}")

conn.close()
