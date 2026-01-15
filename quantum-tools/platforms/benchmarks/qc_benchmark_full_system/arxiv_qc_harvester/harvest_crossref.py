import requests
import json
from pathlib import Path
from datetime import datetime

HEADERS = {
    "User-Agent": "QCBD/1.0 (mailto:you@example.com)"
}
BASE_URL = "https://api.crossref.org/works"

# Supported Crossref types to look for (not just journal-article)
ACCEPTED_TYPES = [
    "journal-article", "proceedings-article", "dataset", "report", "posted-content"
]

RETRY_FILE = Path("data/retry_crossref.txt")
LOG_FILE = Path("data/crossref_harvest.log")
OUT_FILE = Path("data/raw/journals/crossref_qcqp.jsonl")
OUT_FILE.parent.mkdir(parents=True, exist_ok=True)

def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {msg}\n")

def save_retry(container_title):
    with open(RETRY_FILE, "a") as f:
        f.write(container_title + "\n")

def fetch_crossref_metadata(container_title, from_year=1990, to_year=2025, rows=200):
    cursor = "*"
    all_items = []
    while True:
        params = {
            "query": "quantum superconduct DFT THz",
            "filter": f"from-pub-date:{from_year}-01-01,until-pub-date:{to_year}-12-31,container-title:{container_title}",
            "rows": rows,
            "cursor": cursor,
            "mailto": "you@example.com",
            "cursor": cursor
        }
        try:
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            items = data.get("message", {}).get("items", [])
            items = [item for item in items if item.get("type") in ACCEPTED_TYPES]
            all_items.extend(items)

            next_cursor = data["message"].get("next-cursor")
            if not next_cursor or not items:
                break
            cursor = next_cursor
        except Exception as e:
            log(f"[ERROR] Failed for '{container_title}': {e}")
            save_retry(container_title)
            break
    return all_items
def run_crossref_harvest():
    sources = [
        "The Journal of Chemical Physics",
        "Journal of Chemical Theory and Computation",
        "Nature Communications",
        "Science Advances",
        "Physical Review Letters",
        "arXiv",
        "bioRxiv",
        "Zenodo",
        "OSF Preprints",
        "Figshare"
    ]

    all_records = []
    for source in sources:
        log(f"[INFO] Fetching from {source}")
        results = fetch_crossref_metadata(source)
        all_records.extend(results)

    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for record in all_records:
            f.write(json.dumps(record) + "\n")

    log(f"[SUCCESS] Harvested {len(all_records)} records to {OUT_FILE}")
        recovered = retry_failed_sources()
    all_records.extend(recovered)
    print(f"Harvested {len(all_records)} records to {OUT_FILE}")

if __name__ == "__main__":
    run_crossref_harvest()
