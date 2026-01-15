import json
import argparse
from pathlib import Path
from typing import Dict, Any, Iterable

ROOT = Path(__file__).resolve().parents[2] if '__file__' in globals() else Path.cwd().parents[0]
DATA_PROCESSED = ROOT / 'data' / 'processed'
OUT_DIR = ROOT / 'expert' / 'sources' / 'processed'

# Example field mapping; adjust to your QCDB export structure
FIELD_MAP = {
    "source": {
        "id": "id",
        "title": "title",
        "authors": "authors",
        "year": "year",
        "publisher": "publisher",
        "provenance": "provenance",
        "url": "url",
        "domains": "domains"
    },
    "dataset": {
        "id": "id",
        "name": "name",
        "domain": "domain",
        "category": "category",
        "description": "description",
        "source_id": "source_id",
        "url": "url"
    }
}


def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def map_source(obj: Dict[str, Any]) -> Dict[str, Any]:
    src = {
        "id": obj.get(FIELD_MAP['source']['id'], 'src.qcdb.unknown'),
        "type": obj.get('type', 'other'),
        "title": obj.get(FIELD_MAP['source']['title'], ''),
        "authors": obj.get(FIELD_MAP['source']['authors'], []),
        "year": obj.get(FIELD_MAP['source']['year'], 0),
        "publisher": obj.get(FIELD_MAP['source']['publisher'], ''),
        "provenance": obj.get(FIELD_MAP['source']['provenance'], 'QCDB'),
        "url": obj.get(FIELD_MAP['source']['url'], ''),
        "domains": obj.get(FIELD_MAP['source']['domains'], ['quantum_chemistry']),
        "trust_tier": obj.get('trust_tier', 'B'),
        "open_access": obj.get('open_access', True),
        "notes": obj.get('notes', 'Imported from QCDB'),
        "last_verified": obj.get('last_verified', '2025-12-01')
    }
    if not src['id'].startswith('src.'):
        src['id'] = 'src.qcdb.' + src['id'][:180]
    return src


def map_dataset(obj: Dict[str, Any]) -> Dict[str, Any]:
    ds = {
        "id": obj.get(FIELD_MAP['dataset']['id'], 'ds.qcdb.unknown'),
        "name": obj.get(FIELD_MAP['dataset']['name'], ''),
        "domain": obj.get(FIELD_MAP['dataset']['domain'], 'quantum_chemistry'),
        "category": obj.get(FIELD_MAP['dataset']['category'], 'qcdb'),
        "description": obj.get(FIELD_MAP['dataset']['description'], ''),
        "source_id": obj.get(FIELD_MAP['dataset']['source_id'], ''),
        "url": obj.get(FIELD_MAP['dataset']['url'], ''),
        "last_reviewed": obj.get('last_reviewed', '2025-12-01')
    }
    if not ds['id'].startswith('ds.'):
        ds['id'] = 'ds.qcdb.' + ds['id'][:180]
    return ds


def persist_document(meta: Dict[str, Any], fname_prefix: str) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / (fname_prefix + '.json')
    doc = {
        "raw_text": "",
        "facts": [],
        "equations": [],
        "citations": [],
        "quality": {"score": 0},
        "meta": meta
    }
    out_path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=str, help='Path to QCDB sources.jsonl')
    parser.add_argument('--datasets', type=str, help='Path to QCDB datasets.jsonl')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # In absence of explicit paths, try default locations under Databases
    base = Path('G:/My Drive/Databases')
    sources_path = Path(args.sources) if args.sources else next(base.rglob('sources.jsonl'), None)
    datasets_path = Path(args.datasets) if args.datasets else next(base.rglob('datasets.jsonl'), None)

    print('[QCDB] sources:', sources_path)
    print('[QCDB] datasets:', datasets_path)

    if sources_path and sources_path.exists():
        for obj in read_jsonl(sources_path):
            meta = map_source(obj)
            if args.dry_run:
                print(json.dumps(meta, indent=2))
            else:
                persist_document(meta, meta['id'].replace('src.', '').replace('.', '_'))
    else:
        print('[WARN] No sources.jsonl found')

    if datasets_path and datasets_path.exists():
        for obj in read_jsonl(datasets_path):
            meta = map_dataset(obj)
            if args.dry_run:
                print(json.dumps(meta, indent=2))
            else:
                persist_document(meta, meta['id'].replace('ds.', '').replace('.', '_'))
    else:
        print('[WARN] No datasets.jsonl found')

    print('[OK] QCDB ingest complete')


if __name__ == '__main__':
    main()
