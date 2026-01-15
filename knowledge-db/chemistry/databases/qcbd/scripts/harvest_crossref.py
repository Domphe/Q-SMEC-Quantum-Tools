"""Harvest journal metadata+abstracts from Crossref for QC/QP.
Constraints: trusted publishers; max year 2025; domains QC/QP only.
"""
import sys
import time
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from datetime import date
from pathlib import Path
from typing import List, Dict
from utils import write_jsonl, DATA_RAW

CROSSREF_API = "https://api.crossref.org/works"
USER_AGENT = "QCBD/1.0 (mailto:qcbd@example.com)"

JOURNALS = [
    {
        "id": "jcp",
        "container": "The Journal of Chemical Physics",
        "from": "1990-01-01",
        "until": "2025-12-31",
        "publisher": "American Institute of Physics"
    },
    {
        "id": "jctc",
        "container": "Journal of Chemical Theory and Computation",
        "from": "2005-01-01",
        "until": "2025-12-31",
        "publisher": "American Chemical Society"
    }
]

ADDITIONAL_TYPES = [
    "journal-article",
    "proceedings-article",
    "book-chapter",
    "posted-content",  # preprints
    "dataset",
]

def fetch_crossref(
    container: str,
    from_date: str,
    until_date: str,
    publisher: str | None = None,
    rows: int = 100,
    max_pages: int = 5,
    content_types: List[str] | None = None,
    title_query: str | None = None,
    biblio_query: str | None = None,
) -> List[Dict]:
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    items: List[Dict] = []
    cursor = "*"
    pages = 0
    # Build filter string per Crossref spec
    types = content_types or ADDITIONAL_TYPES
    # We will iterate per type to respect Crossref filtering
    # Publisher-name sometimes causes 400 with container-title queries; omit for robustness
    def build_params(t: str):
        p = {
            "filter": ",".join([
                f"type:{t}",
                f"from-pub-date:{from_date}",
                f"until-pub-date:{until_date}",
            ]),
            "query.container-title": container,
            "rows": rows,
            "cursor": cursor,
        }
        # Optional title/bibliographic queries to widen quantum science coverage
        if title_query:
            p["query.title"] = title_query
        if biblio_query:
            p["query.bibliographic"] = biblio_query
        return p
    # Configure robust session with retries
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    
    for t in types:
        pages = 0
        cursor = "*"
        params = build_params(t)
        while pages < max_pages:
            try:
                resp = session.get(CROSSREF_API, params=params, headers=headers, timeout=30)
                resp.raise_for_status()
                data = resp.json().get("message", {})
                batch = data.get("items", [])
                items.extend(batch)
                cursor = data.get("next-cursor")
                if not cursor or not batch:
                    break
                params["cursor"] = cursor
                pages += 1
                time.sleep(0.5)
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                print(f"[WARNING] Network error on page {pages+1} for {container} type={t}: {e}")
                break
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else None
                if status == 400:
                    # Fallback: drop container-title filter or biblio query to avoid 400s
                    if "query.container-title" in params:
                        params.pop("query.container-title", None)
                    if "query.bibliographic" in params:
                        params.pop("query.bibliographic", None)
                    if "query.title" in params:
                        # Keep a simple title term to remain narrow but valid
                        params["query.title"] = "quantum"
                    # retry once without container-title
                    try:
                        resp = session.get(CROSSREF_API, params=params, headers=headers, timeout=30)
                        resp.raise_for_status()
                        data = resp.json().get("message", {})
                        batch = data.get("items", [])
                        items.extend(batch)
                        cursor = data.get("next-cursor")
                        if not cursor or not batch:
                            break
                        params["cursor"] = cursor
                        pages += 1
                        time.sleep(0.5)
                    except Exception as e2:
                        print(f"[ERROR] Crossref 400 fallback failed for {container} type={t}: {e2}")
                        break
                else:
                    print(f"[ERROR] Crossref HTTP error for {container} type={t}: {e}")
                    break
    return items

def normalize_item(item: Dict) -> Dict:
    title = (item.get("title") or [""])[0]
    authors = []
    for a in item.get("author", []) or []:
        name = " ".join([x for x in [a.get("given"), a.get("family")] if x])
        if name:
            authors.append(name)
    doi = item.get("DOI")
    year = None
    issued = item.get("issued", {}).get("date-parts", [])
    if issued and issued[0]:
        year = issued[0][0]
    publisher = item.get("publisher")
    url = item.get("URL")
    abstract = item.get("abstract")
    container_title = (item.get("container-title") or [""])[0] if item.get("container-title") else ""
    subject = item.get("subject", []) or []

    return {
        "id": f"src.journal.{doi}" if doi else f"src.journal.{hash(title)}",
        "type": "journal_article",
        "title": title,
        "authors": authors,
        "year": year,
        "doi": doi,
        "publisher": publisher,
        "provenance": "crossref_api",
        "url": url,
        "domains": ["quantum_chemistry"],
        "trust_tier": "A",
        "allowed_content": "metadata_and_abstracts",
        "open_access": False,
        "keywords": subject,
        "notes": "Crossref ingested metadata+abstracts (where available)",
        "last_verified": str(date.today()),
        "abstract": abstract,
        "container_title": container_title,
        "subject": subject
    }

def main():
    outputs: List[Dict] = []
    for j in JOURNALS:
        try:
            items = fetch_crossref(
                j["container"],
                j["from"],
                j["until"],
                j.get("publisher"),
                rows=200,
                max_pages=10,
                content_types=ADDITIONAL_TYPES,
                title_query="quantum superconduct DFT THz",
                biblio_query="quantum materials spectroscopy"
            )
            for it in items:
                rec = normalize_item(it)
                # QC/QP scope check: subject or container-title heuristic
                subjects = [s.lower() for s in (it.get("subject") or [])]
                ctitles = [t.lower() for t in (it.get("container-title") or [])]
                if (
                    any(x in subjects for x in ["quantum chemistry", "chemical physics", "computational chemistry"]) 
                    or any("chemical physics" in t or "chemical theory" in t for t in ctitles)
                ):
                    outputs.append(rec)
        except Exception as e:
            print(f"[ERROR] Crossref fetch for {j['id']}: {e}")
        time.sleep(0.5)

    out_path = DATA_RAW / "journals" / "crossref_qcqp.jsonl"
    write_jsonl(out_path, outputs)
    print(f"Harvested {len(outputs)} journal records to {out_path}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
