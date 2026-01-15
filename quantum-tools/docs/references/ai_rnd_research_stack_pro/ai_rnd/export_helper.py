import datetime
from .db import get_conn

HEURISTICS = [
    ("uav", "ITAR", "USML Cat VIII or Cat XII", "UAV systems/components and sensors can be USML VIII/XII"),
    ("drone", "ITAR", "USML Cat VIII or Cat XII", "UAV systems/components and sensors can be USML VIII/XII"),
    ("laser", "ITAR", "USML Cat XII", "High-energy laser systems often Cat XII"),
    ("femtosecond", "EAR", "ECCN 6A005/6A205", "Ultrafast lasers may be dual-use under 6A"),
    ("x-ray", "EAR", "ECCN 6A001/6A005", "Detectors/sources under Cat 6"),
    ("rf amplifier", "EAR", "ECCN 3A001/5A991", "RF amplifiers may be dual-use"),
]

def draft_export_classification(tech_id: int, regime_name: str, hints: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT regime_id FROM compliance_regime WHERE name=?", (regime_name,))
    r = cur.fetchone()
    if not r:
        cur.execute("INSERT INTO compliance_regime(name,authority,notes) VALUES(?,?,?)",
                    (regime_name, "auto", "created by export_helper"))
        regime_id = cur.lastrowid
    else:
        regime_id = r[0]
    code = "unspecified"
    note = "heuristic"
    h_lower = (hints or "").lower()
    for kw, reg, code_hint, why in HEURISTICS:
        if kw in h_lower and reg.lower() == regime_name.lower():
            code = code_hint
            note = why
            break
    cur.execute("""INSERT INTO export_classification(tech_id, regime_id, category_code, status, date_classified)
                   VALUES(?,?,?,?,?)""",
                (tech_id, regime_id, code, "in_review", datetime.datetime.now(datetime.timezone.utc).isoformat()))
    class_id = cur.lastrowid
    cur.execute("""INSERT INTO approval_gate(project_id,name,criteria,approved_by,approved_on,status)
                   SELECT project_id, 'Export Control Review', 'Human export officer review required', NULL, NULL, 'pending'
                   FROM project_technology WHERE tech_id=?""", (tech_id,))
    conn.commit()
    conn.close()
    return {"class_id": class_id, "category_code": code, "status": "in_review", "note": note}
