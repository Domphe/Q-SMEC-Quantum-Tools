
import logging
from schema import BenchmarkRecord
from resolver import resolve_structure
from doi_resolver import enrich_doi

logging.basicConfig(
    filename="logs/benchmark_enrichment.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

RETRY_FILE = "data/retry_records.jsonl"

def validate_and_enrich(entry: dict) -> dict:
    enriched = dict(entry)

    # Enrich structure (SMILES, InChI)
    if "smiles" not in enriched or not enriched.get("smiles"):
        structure = resolve_structure(enriched.get("system_name") or enriched.get("molecular_formula"))
        if structure:
            enriched.update(structure)
        else:
            logging.warning(f"[STRUCTURE MISSING] {enriched.get('system_name')}")
            mark_for_retry(enriched)

    # Enrich DOI (journal, published)
    if enriched.get("doi") and ("journal" not in enriched or not enriched.get("journal")):
        meta = enrich_doi(enriched["doi"])
        if meta:
            enriched.update(meta)
        else:
            logging.warning(f"[DOI UNRESOLVED] {enriched['doi']}")
            mark_for_retry(enriched)

    # Validate the enriched object
    try:
        BenchmarkRecord(**enriched)
    except Exception as e:
        logging.error(f"[VALIDATION ERROR] {enriched.get('id')} - {e}")
        mark_for_retry(enriched)

    return enriched

def mark_for_retry(entry):
    import json
    with open(RETRY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
