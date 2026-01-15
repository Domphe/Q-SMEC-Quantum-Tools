import sqlite3
import os

# Define the path for the database
db_folder = r"G:\My Drive\Databases"
db_file = os.path.join(db_folder, "strategic_partners.db")

# Ensure the directory exists
os.makedirs(db_folder, exist_ok=True)

# Grant data
cordis_grant_data = [
    (
        1,
        "laser femtosecond",
        "https://cordis.europa.eu/search?q=laser%20femtosecond",
        "Stub record created by harvester; replace with API-parsed fields in deployment."
    )
]

us_grant_data = [
    (
        2,
        "UAV motor",
        "https://www.grants.gov/grantsws/rest/opportunities/search?keywords=UAV%20motor",
        "Stub record created by harvester; replace with API-parsed fields in deployment."
    )
]

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the cordis_grants table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cordis_grants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id INTEGER,
        query TEXT,
        url TEXT,
        notes TEXT
    )
    """)

    # Create the us_grants table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS us_grants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        program_id INTEGER,
        keyword TEXT,
        url TEXT,
        notes TEXT
    )
    """)

    # Insert data into the cordis_grants table
    for grant in cordis_grant_data:
        cursor.execute("SELECT 1 FROM cordis_grants WHERE program_id = ? AND query = ?", (grant[0], grant[1]))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO cordis_grants (program_id, query, url, notes)
            VALUES (?, ?, ?, ?)
            """, grant)

    # Insert data into the us_grants table
    for grant in us_grant_data:
        cursor.execute("SELECT 1 FROM us_grants WHERE program_id = ? AND keyword = ?", (grant[0], grant[1]))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO us_grants (program_id, keyword, url, notes)
            VALUES (?, ?, ?, ?)
            """, grant)

    # Commit the changes and close the connection
    conn.commit()
    print(f"Database '{db_file}' updated with grant information successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if conn:
        conn.close()
        print("Database connection closed.")
