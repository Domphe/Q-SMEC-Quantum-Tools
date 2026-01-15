
import sqlite3
from .config import DB_PATH

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def upsert_org(conn, name, domain=None, org_type=None, iso_code=None, website=None, notes=None):
    cur = conn.cursor()
    country_id = None
    if iso_code:
        c = cur.execute("SELECT country_id FROM country WHERE iso_code=?", (iso_code,)).fetchone()
        if c is None:
            cur.execute("INSERT INTO country(iso_code,name) VALUES(?,?)", (iso_code, iso_code))
            country_id = cur.lastrowid
        else:
            country_id = c[0]
    cur.execute("SELECT org_id FROM organization WHERE name=?", (name,))
    row = cur.fetchone()
    if row:
        org_id = row[0]
        cur.execute(
            "UPDATE organization SET domain=COALESCE(?,domain), org_type=COALESCE(?,org_type), country_id=COALESCE(?,country_id), website=COALESCE(?,website), notes=COALESCE(?,notes) WHERE org_id=?",
            (domain, org_type, country_id, website, notes, org_id)
        )
    else:
        cur.execute(
            "INSERT INTO organization(name,domain,org_type,country_id,website,notes) VALUES(?,?,?,?,?,?)",
            (name, domain, org_type, country_id, website, notes)
        )
        org_id = cur.lastrowid
    conn.commit()
    return org_id

def log_interaction(conn, project_id, mode, participants, summary, action_items):
    from datetime import datetime, timezone
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO interaction(project_id, date, mode, participants, summary, action_items) VALUES(?,?,?,?,?,?)",
        (project_id, datetime.now(timezone.utc).isoformat(), mode, participants, summary, action_items)
    )
    conn.commit()
