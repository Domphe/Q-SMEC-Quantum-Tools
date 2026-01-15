import os, datetime, hashlib
from pdfminer.high_level import extract_text
from .db import get_conn
from .sourcing_policy import extract_host, domain_is_trusted, is_fresh
from .config import DEFAULT_MIN_RECENCY_DAYS

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()

def ingest_pdf(file_path: str, project_id: int = None, source_url: str = None, last_modified: str = None, min_recency_days: int = DEFAULT_MIN_RECENCY_DAYS):
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    text = extract_text(file_path) or ""
    title = os.path.basename(file_path)
    trusted = False
    fresh = False
    host = None
    lm = None
    if source_url:
        host = extract_host(source_url)
        trusted = domain_is_trusted(host)
    if last_modified:
        try:
            lm = datetime.datetime.fromisoformat(last_modified)
        except Exception:
            lm = None
    if lm:
        cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=min_recency_days)
        fresh = is_fresh(cutoff, lm)
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""INSERT INTO document(project_id,title,doc_type,link,created_on,notes)
                   VALUES(?,?,?,?,?,?)""",
                (project_id, title, "pdf", file_path, datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 f"trusted={trusted}; fresh={fresh}; src={source_url}; last_mod={lm}"))
    doc_id = cur.lastrowid
    cur.execute("""INSERT INTO interaction(project_id,date,mode,participants,summary,action_items)
                   VALUES(?,?,?,?,?,?)""",
                (project_id, datetime.datetime.now(datetime.timezone.utc).isoformat(), "pdf", host or "local",
                 f"Ingested PDF; trust={trusted}; fresh={fresh}", f"hash={sha256(text[:10000])}"))
    conn.commit()
    conn.close()
    return {"doc_id": doc_id, "trusted": trusted, "fresh": fresh, "last_modified": str(lm), "source_host": host}
