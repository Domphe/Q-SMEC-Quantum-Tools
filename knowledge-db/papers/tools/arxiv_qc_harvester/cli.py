
import argparse
import json
from enrich_pipeline import validate_and_enrich


def run_pipeline(input_file: str, output_file: str, filter_key=None, filter_value=None):
    
    with open(input_file, "r", encoding="utf-8") as f:
        
        entries = [json.loads(line) for line in f if line.strip()]
        if filter_key and filter_value:
            entries = [e for e in entries if e.get(filter_key) == filter_value]
        

    enriched = [validate_and_enrich(e) for e in entries]

    with open(output_file, "w", encoding="utf-8") as f:
        for item in enriched:
            f.write(json.dumps(item) + "\n")

    print(f"[DONE] Enriched {len(enriched)} records to {output_file}")

def run_cli():
    parser = argparse.ArgumentParser(description="QC Benchmark Enrichment CLI")
    parser.add_argument("--input", type=str, required=True, help="Path to input JSONL file")
    parser.add_argument("--output", type=str, required=True, help="Path to output JSONL file")
    parser.add_argument("--retry", action="store_true", help="Re-run retry_records.jsonl")
    parser.add_argument("--filter-key", type=str, help="Key to filter records by")
    parser.add_argument("--filter-value", type=str, help="Value to match on the filter key")

    args = parser.parse_args()

    if args.retry:
        from retry_processor import retry_failed_records
        retry_failed_records()
    else:
        run_pipeline(args.input, args.output, args.filter_key, args.filter_value)

if __name__ == "__main__":
    run_cli()
