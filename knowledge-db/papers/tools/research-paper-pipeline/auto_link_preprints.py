
import json
from pathlib import Path
from utils import read_jsonl, write_jsonl
from semantic_linker import link_software, link_patents, link_datasets

def auto_enrich_links(
    preprints_path: Path,
    tools_path: Path,
    patents_path: Path,
    datasets_path: Path,
    output_path: Path
):
    preprints = read_jsonl(preprints_path)
    tools = read_jsonl(tools_path)
    patents = read_jsonl(patents_path)
    datasets = read_jsonl(datasets_path)

    enriched = []
    for p in preprints:
        p["related_software"] = link_software(p, tools)
        p["related_patents"] = link_patents(p, patents)
        p["related_datasets"] = link_datasets(p, datasets)
        enriched.append(p)

    write_jsonl(output_path, enriched)
    print(f"[✔] Linked {len(enriched)} preprints with related assets.")
    print(f"[→] Enriched output saved to: {output_path}")

if __name__ == "__main__":
    auto_enrich_links(
        preprints_path=Path("data/raw/preprints/arxiv_qcqp.jsonl"),
        tools_path=Path("data/raw/tools/open_source_tools.jsonl"),
        patents_path=Path("data/raw/patents/quantum_patents.jsonl"),
        datasets_path=Path("data/raw/gov/nist_cccbdb_molecules.jsonl"),
        output_path=Path("exports/enriched_preprints.jsonl")
    )
