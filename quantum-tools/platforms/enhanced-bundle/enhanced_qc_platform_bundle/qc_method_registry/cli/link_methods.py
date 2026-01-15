
import json
from pathlib import Path
from schemas.qc_method import QuantumChemistryMethod
from utils.linker import auto_link_methods

def load_methods(path: Path):
    return [json.loads(line) for line in open(path)]

def save_methods(methods, path: Path):
    with open(path, "w") as f:
        for item in methods:
            f.write(json.dumps(item) + "\n")

def enrich_and_link(input_path, output_path):
    methods = load_methods(Path(input_path))
    linked = auto_link_methods(methods)
    save_methods(linked, Path(output_path))
    print(f"[✔] Enriched {len(linked)} methods and saved to {output_path}")

if __name__ == "__main__":
    enrich_and_link("data/methods.jsonl", "data/methods_linked.jsonl")
