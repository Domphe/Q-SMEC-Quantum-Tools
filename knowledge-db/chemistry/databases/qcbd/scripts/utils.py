"""Core utilities for QCBD expert database."""
import json
from pathlib import Path
from typing import Iterator, Any, Dict

# Path constants
ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
SCHEMAS = ROOT / "schemas"
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DB_DIR = ROOT / "db"
SCRIPTS = ROOT / "scripts"

def read_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    """Read JSONL file line by line."""
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)

def write_jsonl(path: Path, records: list[Dict[str, Any]]) -> None:
    """Write records to JSONL file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

def read_json(path: Path) -> Dict[str, Any]:
    """Read JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """Write data to JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path
