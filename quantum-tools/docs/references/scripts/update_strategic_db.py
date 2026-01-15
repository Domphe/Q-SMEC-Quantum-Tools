import sqlite3
import os

# Define the path for the database
db_folder = r"G:\My Drive\Databases"
db_file = os.path.join(db_folder, "strategic_partners.db")

# Ensure the directory exists
os.makedirs(db_folder, exist_ok=True)

# Data to be inserted
companies_data = [
    (
        "ACOM",
        "https://www.acom-bg.com/",
        "Bulgaria",
        "Specializes in high-power radio frequency (RF) amplifiers, antenna tuners, and related electronics for the amateur radio and commercial markets. Deep experience in power electronics and manufacturing for export.",
        "Potential partner for developing and producing the electronic components (controllers, power systems) for a high-power drone motor. Their experience with military-grade electronics is a significant asset."
    ),
    (
        "NSK Group",
        "https://nskgroup.com.tr/en",
        "Turkey",
        "Large-scale manufacturer of steering, suspension, hydraulic, and forged metal parts for commercial, agricultural, and construction vehicles.",
        "Key supplier for the mechanical parts of the drone motor, such as casings, shafts, and other structural elements, leveraging Turkey's competitive pricing on metals."
    ),
    (
        "Volacom",
        "https://www.volacom.com/",
        "Bulgaria",
        "Develops and deploys advanced bird and wildlife detection and deterrence systems for airports and wind farms. Utilizes specialized drones as part of their solutions.",
        "Demonstrates existing group experience with drone technology and its application in industrial settings (airport security). Provides a potential initial use case and integration partner for the new motor."
    )
]

# Technology data
technology_data = [
    (
        "20KW Drone Motor",
        "A 20KW (20,000 Watt) motor is a high-power system for heavy-lift and high-endurance drones. It is typically a brushless DC (BLDC) outrunner motor operating at high voltages (400-800V DC).",
        "Key applications include heavy-lift logistics, large-scale agricultural drones, long-endurance tethered drones, and the emerging Urban Air Mobility (UAM) / eVTOL market.",
        "Requires advanced power electronics (ESCs), robust cooling systems (air or liquid), and high-voltage battery systems. The market is a specialized, low-volume, high-value niche with motors and ESCs costing $5,000-$20,000+.",
        "The proposed partnership (ACOM for electronics, NSK for mechanicals) is well-aligned with the technical challenges. Key players include T-Motor, KDE Direct, and Plettenberg."
    ),
    (
        "Monochromatic Hard X-ray Laser",
        "A cutting-edge research instrument, not a commercial product. It is generated via High Harmonic Generation (HHG), where an intense (10^16 - 10^18 W/cm^2) femtosecond laser pulse interacts with a gas target.",
        "Primary application is advanced materials characterization. The technology is crucial for fundamental research in physics, chemistry, and material science.",
        "Extremely high technical barriers, including the need for a multi-million dollar driving laser, high-vacuum systems, and specialized X-ray optics. Subject to strict ITAR export controls.",
        "The 'Build, Don't Buy' strategy proposed by Alex is the most viable path, bypassing export issues and fostering local R&D. Q-SMEC can be integrated as a core material for enhancing the HHG process or for the optics. Key driving laser suppliers include Amplitude Laser, Class 5 Photonics."
    )
]

try:
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create the table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        website TEXT,
        location TEXT,
        expertise TEXT,
        relevance TEXT
    )
    """)

    # Create the technologies table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS technologies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        applications TEXT,
        challenges_and_market TEXT,
        synergy_and_players TEXT
    )
    """)

    # Insert data into the companies table
    # Using a loop and checking for existence to prevent duplicates on re-runs
    for company in companies_data:
        cursor.execute("SELECT 1 FROM companies WHERE name = ?", (company[0],))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO companies (name, website, location, expertise, relevance)
            VALUES (?, ?, ?, ?, ?)
            """, company)

    # Insert data into the technologies table
    for tech in technology_data:
        cursor.execute("SELECT 1 FROM technologies WHERE name = ?", (tech[0],))
        if cursor.fetchone() is None:
            cursor.execute("""
            INSERT INTO technologies (name, description, applications, challenges_and_market, synergy_and_players)
            VALUES (?, ?, ?, ?, ?)
            """, tech)

    # Commit the changes and close the connection
    conn.commit()
    print(f"Database '{db_file}' created and populated successfully.")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if conn:
        conn.close()
        print("Database connection closed.")

