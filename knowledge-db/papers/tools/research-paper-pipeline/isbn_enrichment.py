
import requests
import logging

logger = logging.getLogger("isbn_enrichment")

OPENLIBRARY_API = "https://openlibrary.org/api/books"

def enrich_with_openlibrary(isbn: str) -> dict:
    """Enrich textbook metadata using OpenLibrary ISBN API."""
    try:
        resp = requests.get(
            OPENLIBRARY_API,
            params={"bibkeys": f"ISBN:{isbn}", "format": "json", "jscmd": "data"},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        entry = data.get(f"ISBN:{isbn}")
        if not entry:
            logger.warning(f"No metadata found for ISBN {isbn}")
            return {}

        enriched = {
            "title": entry.get("title"),
            "subtitle": entry.get("subtitle"),
            "subjects": [s["name"] for s in entry.get("subjects", [])],
            "number_of_pages": entry.get("number_of_pages"),
            "publish_date": entry.get("publish_date"),
            "cover_url": entry.get("cover", {}).get("large") or entry.get("cover", {}).get("medium")
        }
        return enriched
    except Exception as e:
        logger.error(f"[OpenLibrary ISBN Error] {isbn} → {e}")
        return {}
