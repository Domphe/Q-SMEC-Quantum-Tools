import sqlite3
from datetime import datetime

DB_PATH = "exports/export_log.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS export_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            format TEXT,
            session TEXT,
            num_entries INTEGER,
            path TEXT
        )
        """)
        conn.commit()

def log_export(format, session, num_entries, path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        INSERT INTO export_log (timestamp, format, session, num_entries, path)
        VALUES (?, ?, ?, ?, ?)
        """, (datetime.utcnow().isoformat(), format, session, num_entries, str(path)))
        conn.commit()
