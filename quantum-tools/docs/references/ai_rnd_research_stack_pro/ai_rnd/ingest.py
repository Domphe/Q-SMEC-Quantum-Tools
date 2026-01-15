
import hashlib, requests, datetime
from bs4 import BeautifulSoup
from readability.readability import Document as ReadabilityDoc
from .config import USER_AGENT, TIMEOUT, DEFAULT_MIN_RECENCY_DAYS
from .sourcing_policy import extract_host, domain_is_trusted, get_last_modified, is_fresh
from .db import get_conn

HEADERS = {"User-Agent": USER_AGENT}

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()

def fetch_url(url: str) -> dict:
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
    r.raise_for_status()
    html = r.text
    doc = ReadabilityDoc(html)
    content_html = doc.summary()
    soup = BeautifulSoup(content_html, "lxml")
    text = soup.get_text("\n", strip=True)
    title = doc.short_title() or "Web Document"
    return {"html": html, "text": text, "url": r.url, "title": title}

def ingest_url(url: str, project_id: int = None, doc_type: str = "web", min_recency_days: int = DEFAULT_MIN_RECENCY_DAYS):
    host = extract_host(url)
    trusted = domain_is_trusted(host)
    fetched = fetch_url(url)
    last_mod = get_last_modified(fetched["url"], headers=HEADERS, timeout=TIMEOUT)
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=min_recency_days)
    fresh = is_fresh(cutoff, last_mod)
    trust_score = (1 if trusted else 0) + (1 if fresh else 0)

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO document(project_id,title,doc_type,link,created_on,notes) VALUES(?,?,?,?,?,?)",
        (project_id, fetched["title"], doc_type, fetched["url"], datetime.datetime.now(datetime.timezone.utc).isoformat(),
         f"trusted={trusted}; fresh={fresh}; last_mod={last_mod}")
    )
    doc_id = cur.lastrowid

    cur.execute(
        "INSERT INTO interaction(project_id,date,mode,participants,summary,action_items) VALUES(?,?,?,?,?,?)",
        (project_id, datetime.datetime.now(datetime.timezone.utc).isoformat(), "web", host,
         f"Ingested URL; trust={trusted}; fresh={fresh}; trust_score={trust_score}",
         f"hash={sha256(fetched['text'][:10000])}")
    )
    conn.commit()
    conn.close()
    return {"doc_id": doc_id, "trusted": trusted, "fresh": fresh, "last_modified": str(last_mod), "url": fetched["url"], "title": fetched["title"]}
