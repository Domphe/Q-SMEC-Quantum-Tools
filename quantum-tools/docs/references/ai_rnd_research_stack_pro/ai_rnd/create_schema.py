import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def create_schema():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.execute("""
    CREATE TABLE IF NOT EXISTS country (
        country_id INTEGER PRIMARY KEY AUTOINCREMENT,
        iso_code TEXT UNIQUE NOT NULL,
        name TEXT UNIQUE NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS organization (
        org_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        domain TEXT,
        org_type TEXT,
        country_id INTEGER,
        website TEXT,
        notes TEXT,
        FOREIGN KEY (country_id) REFERENCES country (country_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS project (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT
    );
    """)
    
    # Insert a default project
    cur.execute("INSERT OR IGNORE INTO project (project_id, name, description, status) VALUES (1, 'Default Project', 'Default project for initial research', 'active');")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS technology (
        tech_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        trl INTEGER,
        mrl INTEGER,
        notes TEXT
    );
    """)
    
    # Insert technologies
    cur.execute("INSERT OR IGNORE INTO technology (tech_id, name) VALUES (1, '20KW Drone Motor');")
    cur.execute("INSERT OR IGNORE INTO technology (tech_id, name) VALUES (2, 'Monochromatic Hard X-ray Laser');")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS project_technology (
        project_id INTEGER,
        tech_id INTEGER,
        PRIMARY KEY (project_id, tech_id),
        FOREIGN KEY (project_id) REFERENCES project (project_id),
        FOREIGN KEY (tech_id) REFERENCES technology (tech_id)
    );
    """)
    
    # Link technologies to default project
    cur.execute("INSERT OR IGNORE INTO project_technology (project_id, tech_id) VALUES (1, 1);")
    cur.execute("INSERT OR IGNORE INTO project_technology (project_id, tech_id) VALUES (1, 2);")


    cur.execute("""
    CREATE TABLE IF NOT EXISTS document (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        title TEXT,
        doc_type TEXT,
        link TEXT,
        created_on TEXT,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES project (project_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS interaction (
        interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        date TEXT,
        mode TEXT,
        participants TEXT,
        summary TEXT,
        action_items TEXT,
        FOREIGN KEY (project_id) REFERENCES project (project_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS compliance_regime (
        regime_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        authority TEXT,
        notes TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS export_classification (
        class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tech_id INTEGER,
        regime_id INTEGER,
        category_code TEXT,
        status TEXT,
        date_classified TEXT,
        FOREIGN KEY (tech_id) REFERENCES technology (tech_id),
        FOREIGN KEY (regime_id) REFERENCES compliance_regime (regime_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS approval_gate (
        gate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT,
        criteria TEXT,
        approved_by TEXT,
        approved_on TEXT,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES project (project_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS funding_program (
        program_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        sponsor TEXT,
        country_id INTEGER,
        url TEXT,
        notes TEXT,
        FOREIGN KEY (country_id) REFERENCES country (country_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS grant_call (
        call_id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id INTEGER,
        call_code TEXT,
        title TEXT,
        open_date TEXT,
        close_date TEXT,
        trl_min INTEGER,
        trl_max INTEGER,
        budget_eur REAL,
        url TEXT,
        notes TEXT,
        FOREIGN KEY (program_id) REFERENCES funding_program (program_id)
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS risk (
        risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        category TEXT,
        description TEXT,
        likelihood INTEGER,
        impact INTEGER,
        mitigation TEXT,
        owner_person_id INTEGER,
        status TEXT,
        FOREIGN KEY (project_id) REFERENCES project (project_id)
    );
    """)

    conn.commit()
    conn.close()
    print("[schema] Database schema created and default data inserted.")

if __name__ == "__main__":
    create_schema()
