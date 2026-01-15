import sqlite3
import os
from datetime import datetime

def generate_report():
    db_path = r"G:\My Drive\.0 Q-SMEC Clients\Nikolay - Drone - Laser\ai_rnd_research_stack_pro\database.db"
    report_path = r"G:\My Drive\.0 Q-SMEC Clients\Nikolay - Drone - Laser\reports\Strategic_Analysis_Report.md"

    # Create the directory for the report if it doesn't exist
    report_dir = os.path.dirname(report_path)
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    if not os.path.exists(db_path):
        return "Error: Database file not found."

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    report_content = f"# Strategic Analysis Report\n\n"
    report_content += f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    # --- Project Info ---
    project = cur.execute("SELECT * FROM project WHERE project_id=1").fetchone()
    if project:
        report_content += "## 1. Project Overview\n"
        report_content += f"- **Project:** {project['name']}\n"
        report_content += f"- **Description:** {project['description']}\n"
        report_content += f"- **Status:** {project['status']}\n\n"

    # --- Technologies ---
    report_content += "## 2. Core Technologies Under Review\n"
    technologies = cur.execute("SELECT * FROM technology").fetchall()
    for tech in technologies:
        report_content += f"### 2.1. {tech['name']} (Tech ID: {tech['tech_id']})\n"
        
        # Export Classifications
        classifications = cur.execute("""
            SELECT ec.category_code, ec.status, cr.name as regime_name
            FROM export_classification ec
            JOIN compliance_regime cr ON ec.regime_id = cr.regime_id
            WHERE ec.tech_id = ?
        """, (tech['tech_id'],)).fetchall()
        
        if classifications:
            report_content += "**Export Control Classification:**\n"
            for c in classifications:
                report_content += f"- **{c['regime_name']}:** {c['category_code']} (Status: {c['status']})\n"
        report_content += "\n"

    # --- Grant Opportunities ---
    report_content += "## 3. Harvested Grant Opportunities\n"
    grants = cur.execute("""
        SELECT gc.title, gc.url, fp.name as program_name, c.name as country
        FROM grant_call gc
        JOIN funding_program fp ON gc.program_id = fp.program_id
        JOIN country c ON fp.country_id = c.country_id
    """).fetchall()
    if grants:
        for grant in grants:
            report_content += f"- **Program:** {grant['program_name']} ({grant['country']})\n"
            report_content += f"  - **Title/Query:** {grant['title']}\n"
            report_content += f"  - **URL:** {grant['url']}\n"
    report_content += "\n"

    # --- Source Documents & Risks ---
    report_content += "## 4. Data Sources and Associated Risks\n"
    documents = cur.execute("SELECT * FROM document WHERE project_id=1").fetchall()
    risks = cur.execute("SELECT * FROM risk WHERE project_id=1").fetchall()
    
    if documents:
        report_content += "### 4.1. Ingested Source Documents\n"
        for doc in documents:
            report_content += f"- **{doc['title']}**\n"
            report_content += f"  - **URL:** {doc['link']}\n"
            report_content += f"  - **Notes:** {doc['notes']}\n"
    
    if risks:
        report_content += "\n### 4.2. Identified Risks\n"
        for risk in risks:
            report_content += f"- **Risk:** {risk['description']}\n"
            report_content += f"  - **Category:** {risk['category']}\n"
            report_content += f"  - **Mitigation:** {risk['mitigation']}\n"
            report_content += f"  - **Status:** {risk['status']}\n"

    # --- Interactions ---
    report_content += "\n## 5. Project Log\n"
    interactions = cur.execute("SELECT * FROM interaction WHERE project_id=1 ORDER BY date DESC").fetchall()
    if interactions:
        for i in interactions:
            summary = i['summary'].replace('\n', ' ')
            report_content += f"- **{i['date']}:** {summary}\n"

    conn.close()

    try:
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        return f"Report successfully generated at {report_path}"
    except Exception as e:
        return f"Error writing report file: {e}"

if __name__ == "__main__":
    print(generate_report())
