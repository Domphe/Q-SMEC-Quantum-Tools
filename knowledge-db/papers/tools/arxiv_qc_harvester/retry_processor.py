
import json
from enrich_pipeline import validate_and_enrich

RETRY_FILE = "data/retry_records.jsonl"
PROCESSED_FILE = "data/retry_resolved.jsonl"

def retry_failed_records():
    with open(RETRY_FILE, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    reprocessed = []
    for entry in lines:
        enriched = validate_and_enrich(entry)
        reprocessed.append(enriched)

    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
        for item in reprocessed:
            f.write(json.dumps(item) + "\n")

    print(f"[RETRY] Reprocessed {len(reprocessed)} entries → {PROCESSED_FILE}")
