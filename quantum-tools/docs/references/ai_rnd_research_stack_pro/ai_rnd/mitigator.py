import re, datetime
from .db import get_conn

def mitigate_sources(project_id: int = None):
    conn = get_conn()
    cur = conn.cursor()
    q = "SELECT doc_id, project_id, notes FROM document"
    params = []
    if project_id:
        q += " WHERE project_id=?"
        params.append(project_id)
    rows = cur.execute(q, params).fetchall()
    opened = 0
    for doc_id, pid, notes in rows:
        notes = notes or ""
        trusted = re.search(r"trusted=(True|False)", notes)
        fresh = re.search(r"fresh=(True|False)", notes)
        t_val = (trusted.group(1).lower()=="true") if trusted else False
        f_val = (fresh.group(1).lower()=="true") if fresh else False
        if (not t_val) or (not f_val):
            cur.execute("""INSERT INTO risk(project_id, category, description, likelihood, impact, mitigation, owner_person_id, status)
                           VALUES(?,?,?,?,?,?,?,?)""",
                        (pid, "data_quality", f"Source doc_id={doc_id} has trusted={t_val}, fresh={f_val}",
                         3, 3, "Replace with trusted/fresh source or obtain verification", None, "open"))
            opened += 1
    conn.commit()
    conn.close()
    return {"opened_risks": opened}
