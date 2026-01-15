"""Deduplicate arxiv_qcqp.jsonl by record ID.
Reads all records, keeps unique entries by id field, writes back to same file.
"""
import json
from pathlib import Path
from typing import Dict, List

def deduplicate_jsonl(file_path: Path) -> None:
    """Read JSONL, deduplicate by id, overwrite file with unique records."""
    if not file_path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return
    
    records: List[Dict] = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"[WARN] Skipping invalid JSON line: {e}")
    
    print(f"Read {len(records)} total records from {file_path.name}")
    
    # Deduplicate by id field, keeping first occurrence
    seen_ids = set()
    unique_records: List[Dict] = []
    for record in records:
        record_id = record.get('id')
        if record_id and record_id not in seen_ids:
            seen_ids.add(record_id)
            unique_records.append(record)
        elif not record_id:
            print(f"[WARN] Record missing 'id' field, skipping: {record.get('title', 'unknown')[:50]}")
    
    duplicates_removed = len(records) - len(unique_records)
    print(f"Removed {duplicates_removed} duplicate records")
    print(f"Writing {len(unique_records)} unique records back to {file_path.name}")
    
    # Write back to same file
    with open(file_path, 'w', encoding='utf-8') as f:
        for record in unique_records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"✓ Deduplication complete: {file_path}")

def main():
    from utils import DATA_RAW
    arxiv_file = DATA_RAW / "preprints" / "arxiv_qcqp.jsonl"
    deduplicate_jsonl(arxiv_file)

if __name__ == '__main__':
    main()
