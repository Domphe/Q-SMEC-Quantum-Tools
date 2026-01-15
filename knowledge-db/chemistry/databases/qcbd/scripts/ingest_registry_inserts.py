"""Ingest proposed registry inserts (materials, methods, datasets) into SQLite DB."""
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from utils import DB_DIR

PROPOSALS = Path("G:/My Drive/Databases/QCBD/reports/entity_inserts_proposals.json")


def load_json(path: Path) -> Dict[str, Any]:
    import json
    return json.loads(path.read_text(encoding="utf-8"))


def upsert(conn: sqlite3.Connection, table: str, record_id: str, domain: str, payload: Dict[str, Any], extra: Dict[str, Any] | None = None) -> None:
    import json
    js = json.dumps(payload, ensure_ascii=False)
    if table == "glossary":
        term = payload.get("name", record_id)
        conn.execute(
            'INSERT OR REPLACE INTO glossary (id, domain, term, json) VALUES (?, ?, ?, ?)',
            (record_id, domain, term, js)
        )
    elif table == "datasets":
        conn.execute(
            'INSERT OR REPLACE INTO datasets (id, domain, json) VALUES (?, ?, ?)',
            (record_id, domain, js)
        )
    elif table == "methods":
        conn.execute(
            'INSERT OR REPLACE INTO methods (id, domain, json) VALUES (?, ?, ?)',
            (record_id, domain, js)
        )
    else:
        # Default to concepts table
        conn.execute(
            'INSERT OR REPLACE INTO concepts (id, domain, json) VALUES (?, ?, ?)',
            (record_id, domain, js)
        )


def norm_id(prefix: str, name: str) -> str:
    slug = ''.join(c.lower() if c.isalnum() else '-' for c in name).strip('-')
    return f"{prefix}:{slug}"


def main() -> int:
    if not PROPOSALS.exists():
        print(f"[SKIP] Proposals file not found: {PROPOSALS}")
        return 0

    data = load_json(PROPOSALS)
    db_path = DB_DIR / 'qc_qp_expert.db'
    conn = sqlite3.connect(db_path)
    inserted = 0
    try:
        ts = datetime.now().isoformat()

        # Materials -> concepts (domain='materials')
        for m in data.get('materials', []):
            payload = {
                "name": m.get("name"),
                "type": "material",
                "sources": m.get("sources", []),
                "provenance": {"generated_at": data.get("generated_at"), "ingested_at": ts}
            }
            upsert(conn, "concepts", norm_id("mat", m["name"]), "materials", payload)
            inserted += 1

        # Methods -> methods (domain='methods')
        for meth in data.get('methods', []):
            payload = {
                "name": meth.get("name"),
                "type": "method",
                "sources": meth.get("sources", []),
                "provenance": {"generated_at": data.get("generated_at"), "ingested_at": ts}
            }
            upsert(conn, "methods", norm_id("meth", meth["name"]), "methods", payload)
            inserted += 1

        # Datasets -> datasets (domain='benchmarks')
        for ds in data.get('datasets', []):
            payload = {
                "name": ds.get("name"),
                "type": "dataset",
                "sources": ds.get("sources", []),
                "provenance": {"generated_at": data.get("generated_at"), "ingested_at": ts}
            }
            upsert(conn, "datasets", norm_id("ds", ds["name"]), "benchmarks", payload)
            inserted += 1

        conn.commit()
        print(f"[INGEST] Registry inserts committed: {inserted} records")
        return 0
    except Exception as e:
        conn.rollback()
        print(f"ERROR: {e}")
        return 1
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
"""
Ingest proposed registry inserts into the SQLite DB.
Reads reports/entity_inserts_proposals.json and inserts into tables:
- concepts (materials, domain='materials')
- methods (methods, domain='methods')
- datasets (datasets, domain='benchmarks')
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path("G:/My Drive/Databases/QCBD")
DB_PATH = PROJECT_ROOT / 'db' / 'qc_qp_expert.db'
PROPOSALS = PROJECT_ROOT / 'reports' / 'entity_inserts_proposals.json'


def ensure_tables(conn: sqlite3.Connection):
    # Minimal check; tables created by build_db.py
    pass


def insert_concept(conn: sqlite3.Connection, name: str, domain: str, sources: list):
    rec = {
        "id": f"concept:{domain}:{name}",
        "name": name,
        "domain": domain,
        "sources": sources,
        "ingested_at": datetime.now().isoformat()
    }
    conn.execute(
        'INSERT OR REPLACE INTO concepts (id, domain, json) VALUES (?, ?, ?)',
        (rec["id"], domain, json.dumps(rec))
    )


def insert_method(conn: sqlite3.Connection, name: str, domain: str, sources: list):
    rec = {
        "id": f"method:{name}",
        "name": name,
        "domain": domain,
        "sources": sources,
        "ingested_at": datetime.now().isoformat()
    }
    conn.execute(
        'INSERT OR REPLACE INTO methods (id, domain, json) VALUES (?, ?, ?)',
        (rec["id"], domain, json.dumps(rec))
    )


def insert_dataset(conn: sqlite3.Connection, name: str, domain: str, sources: list):
    rec = {
        "id": f"dataset:{name}",
        "name": name,
        "benchmark_set": name,
        "domain": domain,
        "sources": sources,
        "ingested_at": datetime.now().isoformat()
    }
    conn.execute(
        'INSERT OR REPLACE INTO datasets (id, domain, json) VALUES (?, ?, ?)',
        (rec["id"], domain, json.dumps(rec))
    )


def main():
    if not PROPOSALS.exists():
        print(f"[SKIP] Proposals not found: {PROPOSALS}")
        return 0
    if not DB_PATH.exists():
        print(f"[ERROR] DB not found: {DB_PATH}")
        return 1

    data = json.loads(PROPOSALS.read_text(encoding='utf-8'))
    conn = sqlite3.connect(DB_PATH)
    try:
        ensure_tables(conn)
        m_count = 0
        meth_count = 0
        d_count = 0

        for m in data.get("materials", []):
            insert_concept(conn, m.get("name", "unknown"), "materials", m.get("sources", []))
            m_count += 1

        for meth in data.get("methods", []):
            insert_method(conn, meth.get("name", "unknown"), "methods", meth.get("sources", []))
            meth_count += 1

        for ds in data.get("datasets", []):
            insert_dataset(conn, ds.get("name", "unknown"), "benchmarks", ds.get("sources", []))
            d_count += 1

        conn.commit()
        print(f"[INGEST] concepts={m_count} methods={meth_count} datasets={d_count}")
        return 0
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Ingestion failed: {e}")
        return 1
    finally:
        conn.close()


if __name__ == '__main__':
    raise SystemExit(main())
