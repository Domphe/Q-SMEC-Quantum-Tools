import sqlite3
import os

# Define the path for the database
db_folder = r"G:\My Drive\Databases"
db_file = os.path.join(db_folder, "strategic_partners.db")

# Ensure the directory exists
os.makedirs(db_folder, exist_ok=True)

# Export classification data
export_data = [
    (
        1, # tech_id for 20KW Drone Motor
        "ITAR",
        "USML Cat VIII or Cat XII",
        "in_review",
        "UAV systems/components and sensors can be USML VIII/XII"
    ),
    (
        2, # tech_id for Monochromatic Hard X-ray Laser
        "ITAR",
        "USML Cat XII",
        "in_review",
        "High-energy laser systems often Cat XII"
    ),
    (
        2, # tech_id for Monochromatic Hard X-ray Laser
        "EAR",
        "ECCN 6A005/6A205",
        "in_review",
        "Ultrafast lasers may be dual-use under 6A"
    )
]

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the export_classifications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS export_classifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tech_id INTEGER,
        regime TEXT,
        category_code TEXT,
        status TEXT,
        notes TEXT,
        FOREIGN KEY (tech_id) REFERENCES technologies (id)
    )
    """)

    # Insert data into the export_classifications table
    for item in export_data:
        cursor.execute("SELECT 1 FROM export_classifications WHERE tech_id = ? AND regime = ? AND category_code = ?", (item[0], item[1], item[2]))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO export_classifications (tech_id, regime, category_code, status, notes)
            VALUES (?, ?, ?, ?, ?)
            """, item)

    # Commit the changes and close the connection
    conn.commit()
    print(f"Database '{db_file}' updated with export classification information successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if conn:
        conn.close()
        print("Database connection closed.")
