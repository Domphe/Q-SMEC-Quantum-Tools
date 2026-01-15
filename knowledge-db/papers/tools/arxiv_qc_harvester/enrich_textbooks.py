
import json
import os
import argparse
from pathlib import Path
from utils import write_jsonl, read_jsonl
from isbn_enrichment import enrich_with_openlibrary
from nlp_tagging import extract_topics

CACHE_DIR = Path("cache/isbn")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def load_cache(isbn):
    cache_file = CACHE_DIR / f"{isbn.replace('-', '')}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    return None

def save_cache(isbn, data):
    cache_file = CACHE_DIR / f"{isbn.replace('-', '')}.json"
    cache_file.write_text(json.dumps(data, indent=2))

def enrich_textbook(record):
    isbn = record.get("isbn")
    if not isbn:
        record["enrichment_notes"] = "Missing ISBN"
        return record

    cached = load_cache(isbn)
    if cached:
        record.update(cached)
    else:
        enrich_data = enrich_with_openlibrary(isbn)
        if enrich_data:
            record.update(enrich_data)
            save_cache(isbn, enrich_data)
        else:
            record["enrichment_notes"] = "Enrichment failed or not found"

    # NLP topic extraction
    record["extracted_topics"] = extract_topics(record)
    return record

def main():
    parser = argparse.ArgumentParser(description="Auto-enrich textbook metadata.")
    parser.add_argument("--input", required=True, help="Path to textbook metadata .jsonl")
    parser.add_argument("--output", required=True, help="Path to enriched .jsonl output")

    args = parser.parse_args()
    records = read_jsonl(args.input)
    enriched = []

    for record in records:
        enriched_record = enrich_textbook(record)
        enriched.append(enriched_record)

    write_jsonl(args.output, enriched)
    print(f"Enriched {len(enriched)} textbooks to {args.output}")
    print("Cached ISBN lookups stored in /cache/isbn/")

if __name__ == "__main__":
    main()
