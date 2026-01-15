from __future__ import annotations
import os
import sqlite3
from urllib.parse import urlparse

def connect(db_url: str) -> sqlite3.Connection:
    # Supports sqlite:///path.db only in v1. Expand to Postgres with SQLAlchemy if desired.
    if not db_url.startswith("sqlite:///"):
        raise ValueError("v1 supports only sqlite:///... for simplicity. Set DB_URL=sqlite:///data/agent.db")
    path = db_url.replace("sqlite:///","",1)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init(conn: sqlite3.Connection) -> None:
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS sources(
      source_id TEXT PRIMARY KEY,
      url TEXT NOT NULL,
      type TEXT NOT NULL,
      tags TEXT
    );

    CREATE TABLE IF NOT EXISTS fetches(
      url TEXT PRIMARY KEY,
      fetched_at TEXT NOT NULL,
      sha256 TEXT NOT NULL,
      content_type TEXT,
      title TEXT,
      publisher TEXT,
      raw_path TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS records(
      record_id TEXT PRIMARY KEY,
      source_id TEXT NOT NULL,
      url TEXT NOT NULL,
      title TEXT,
      fetched_at TEXT NOT NULL,
      text_path TEXT NOT NULL,
      FOREIGN KEY(source_id) REFERENCES sources(source_id)
    );

    CREATE TABLE IF NOT EXISTS entities(
      entity_id TEXT PRIMARY KEY,
      entity_type TEXT NOT NULL,
      name TEXT NOT NULL,
      aliases TEXT,
      attributes_json TEXT
    );

    CREATE TABLE IF NOT EXISTS entity_evidence(
      entity_id TEXT NOT NULL,
      url TEXT NOT NULL,
      sha256 TEXT NOT NULL,
      retrieved_at TEXT NOT NULL,
      PRIMARY KEY(entity_id,url),
      FOREIGN KEY(entity_id) REFERENCES entities(entity_id)
    );

    CREATE TABLE IF NOT EXISTS events(
      event_id TEXT PRIMARY KEY,
      event_type TEXT NOT NULL,
      occurred_on TEXT,
      location_json TEXT,
      outcomes_json TEXT,
      constraints TEXT
    );

    CREATE TABLE IF NOT EXISTS event_participants(
      event_id TEXT NOT NULL,
      entity_id TEXT NOT NULL,
      PRIMARY KEY(event_id, entity_id),
      FOREIGN KEY(event_id) REFERENCES events(event_id),
      FOREIGN KEY(entity_id) REFERENCES entities(entity_id)
    );
    """)
    conn.commit()
