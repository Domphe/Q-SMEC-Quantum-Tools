"""Harvest quantum physics/chemistry preprints from arXiv API.
Scope: categories quant-ph, cond-mat.mtrl-sci, physics.atom-ph, physics.optics, physics.chem-ph.
Filters: title/abstract contains quantum, superconduct, DFT, THz.
"""
import sys
import time
import json
from datetime import date, datetime
from typing import List, Dict, Optional
from urllib.parse import urlencode
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from utils import write_jsonl, DATA_RAW

ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "QCBD/1.0 (mailto:qcbd@example.com)"

CATEGORIES = [
    "quant-ph",
    "cond-mat.mtrl-sci",
    "physics.atom-ph",
    "physics.optics",
    "physics.chem-ph",
]

TITLE_ABS_QUERY = "(quantum OR superconduct OR DFT OR THz)"


def _session_with_retries() -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def fetch_arxiv(cat: str, max_results: int = 200, start: int = 0, since: Optional[datetime] = None, session: Optional[requests.Session] = None) -> List[Dict]:
    # Build arXiv API search query: category AND title/abstract terms
    search_query = f"cat:{cat} AND all:{TITLE_ABS_QUERY}"
    params = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    headers = {"User-Agent": USER_AGENT}
    sess = session or _session_with_retries()
    resp = sess.get(ARXIV_API, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    # arXiv returns Atom XML; parse minimally for essentials
    from xml.etree import ElementTree as ET
    root = ET.fromstring(resp.text)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    items: List[Dict] = []
    for entry in root.findall("atom:entry", ns):
        # canonical id (e.g., https://arxiv.org/abs/YYMM.NNNNN or older formats)
        raw_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
        arxiv_id = None
        if raw_id:
            # Prefer the last path segment as ID
            try:
                arxiv_id = raw_id.split("/")[-1]
            except Exception:
                arxiv_id = raw_id
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        abstract = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
        authors = [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)]
        link = entry.find("atom:link[@rel='alternate']", ns)
        url = link.get("href") if link is not None else None
        published = entry.findtext("atom:published", default="", namespaces=ns)
        updated = entry.findtext("atom:updated", default="", namespaces=ns)
        doi = None
        doi_el = entry.find("arxiv:doi", ns)
        if doi_el is not None and doi_el.text:
            doi = doi_el.text
        # since-date cutoff: skip entries older than cutoff
        if since and published:
            try:
                pub_dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
                if pub_dt < since:
                    continue
            except Exception:
                pass
        items.append({
            "id": f"src.arxiv.{arxiv_id or abs(hash(title))}",
            "type": "preprint",
            "title": title,
            "authors": authors,
            "year": int(published[:4]) if published else None,
            "doi": doi,
            "publisher": "arXiv",
            "provenance": "arxiv_api",
            "url": url,
            "domains": ["quantum_physics", "quantum_chemistry"],
            "trust_tier": "A",
            "allowed_content": "metadata_and_abstracts",
            "open_access": True,
            "keywords": [cat],
            "notes": "arXiv preprint harvested via API",
            "last_verified": str(date.today()),
            "abstract": abstract,
            "container_title": "arXiv",
            "subject": [cat],
        })
    return items

def main():
    # optional --since YYYY-MM-DD for incremental harvesting
    since_arg: Optional[datetime] = None
    if len(sys.argv) > 1 and sys.argv[1] == "--since" and len(sys.argv) > 2:
        try:
            since_arg = datetime.strptime(sys.argv[2], "%Y-%m-%d")
        except Exception:
            print("[WARN] --since value is invalid; expected YYYY-MM-DD. Ignoring.")
            since_arg = None

    outputs: List[Dict] = []
    sess = _session_with_retries()
    # Optional environment controls
    import os
    max_pages_env = os.environ.get("ARXIV_MAX_PAGES")
    max_pages = int(max_pages_env) if (max_pages_env and max_pages_env.isdigit() and int(max_pages_env) > 0) else None
    delay_env = os.environ.get("ARXIV_DELAY")
    delay_s = float(delay_env) if delay_env else 0.5
    max_results_env = os.environ.get("ARXIV_MAX_RESULTS")
    max_results_default = int(max_results_env) if (max_results_env and max_results_env.isdigit()) else 200
    for cat in CATEGORIES:
        try:
            start = 0
            max_results = max_results_default
            page_count = 0
            while True:
                try:
                    batch = fetch_arxiv(cat, max_results=max_results, start=start, since=since_arg, session=sess)
                except requests.exceptions.HTTPError as e:
                    status = e.response.status_code if e.response is not None else None
                    if status in (500, 503):
                        # Backoff and retry this page once
                        time.sleep(delay_s * 2)
                        try:
                            batch = fetch_arxiv(cat, max_results=max_results, start=start, since=since_arg, session=sess)
                        except Exception as e2:
                            print(f"[ERROR] arXiv repeated server error for {cat} start={start}: {e2}")
                            break
                    else:
                        raise
                if not batch:
                    break
                outputs.extend(batch)
                # If fewer than max_results, we've reached the end
                if len(batch) < max_results:
                    break
                start += max_results
                page_count += 1
                # Optional per-category page cap
                if max_pages is not None and page_count >= max_pages:
                    break
                time.sleep(delay_s)
        except Exception as e:
            print(f"[ERROR] arXiv fetch for {cat}: {e}")
    out_path = DATA_RAW / "preprints" / "arxiv_qcqp.jsonl"
    write_jsonl(out_path, outputs)
    print(f"Harvested {len(outputs)} arXiv preprints to {out_path}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
