
import json
from pathlib import Path
from enrichment.openalex_citations import enrich_with_openalex
from utils.linker import auto_link_methods

def load(path):
    return [json.loads(line) for line in open(path)]

def save(data, path):
    with open(path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

def run_pipeline():
    data_path = Path("data/methods.jsonl")
    out_path = Path("data/methods_enriched.jsonl")
    methods = load(data_path)
    methods = enrich_with_openalex(methods)
    methods = auto_link_methods(methods)
    save(methods, out_path)
    print(f"[✔] Enriched + linked methods saved to {out_path}")

if __name__ == "__main__":
    run_pipeline()
