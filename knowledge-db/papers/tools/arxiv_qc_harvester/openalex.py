import requests
import json
from pathlib import Path

CACHE_FILE = Path("data/openalex_citations.json")
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

# Load or initialize cache
if CACHE_FILE.exists():
    with open(CACHE_FILE, "r") as f:
        CITATION_CACHE = json.load(f)
else:
    CITATION_CACHE = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(CITATION_CACHE, f)

def fetch_openalex_citations(doi: str):
    if not doi:
        return None
    doi = doi.lower()
    if doi in CITATION_CACHE:
        return CITATION_CACHE[doi]

    try:
        url = f"https://api.openalex.org/works/doi:{doi}"
        headers = {"User-Agent": "QCBD/1.0 (mailto:you@example.com)"}
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        count = data.get("cited_by_count", 0)
        CITATION_CACHE[doi] = count
        save_cache()
        return count
    except Exception as e:
        CITATION_CACHE[doi] = None
        save_cache()
        return None
