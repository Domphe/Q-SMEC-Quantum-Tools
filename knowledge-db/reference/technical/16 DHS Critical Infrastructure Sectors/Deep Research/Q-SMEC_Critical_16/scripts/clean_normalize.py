import json, pandas as pd
from pathlib import Path
from datetime import datetime, timezone
from ruamel.yaml import YAML

ROOT = Path(__file__).resolve().parents[1]
yaml = YAML(typ="safe")
cfg = yaml.load((ROOT/"config"/"config.yaml").read_text())

RAW = ROOT/"data"/"raw"
INT = ROOT/"data"/"interim"
CUR = ROOT/"data"/"curated"
INT.mkdir(parents=True, exist_ok=True)
CUR.mkdir(parents=True, exist_ok=True)

def stamp(): return datetime.now(timezone.utc).isoformat()

def normalize_example():
    rows = []
    for p in RAW.glob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            obj = json.loads(line)
            rows.append({
                "sector": "Energy",                # assign sector downstream in real mappings
                "source": obj.get("source"),
                "retrieved_at": obj.get("retrieved_at"),
                "variable": "payload_len",
                "value": len(json.dumps(obj.get("payload"))),
                "unit": "bytes",
                "geo": "US",
                "timespan": "2018-2025",
                "license": "public",
                "source_url": ""
            })
    df = pd.DataFrame(rows)
    df.to_parquet(CUR/"normalized_example.parquet", index=False)
    df.to_csv(CUR/"normalized_example.csv", index=False)

if __name__ == "__main__":
    normalize_example()
    print("Normalized sample written to curated/")
