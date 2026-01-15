from __future__ import annotations
import argparse, json, os, datetime
from tqdm import tqdm

from .config import cfg
from .sources import SOURCES
from .db import connect, init
from .fetch import fetch_url, extract_text_html, sha256_bytes, url_to_path, polite_sleep
from .schema import Evidence, ResearchRecord
from .extract import extract_entities, extract_events

def now_iso() -> str:
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"

def save_text(data_dir: str, url: str, text: str) -> str:
    os.makedirs(os.path.join(data_dir,"texts"), exist_ok=True)
    import hashlib
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    path = os.path.join(data_dir,"texts", f"{h}.txt")
    with open(path,"w",encoding="utf-8") as f:
        f.write(text)
    return path

def upsert_sources(conn):
    for s in SOURCES:
        conn.execute(
            "INSERT OR REPLACE INTO sources(source_id,url,type,tags) VALUES (?,?,?,?)",
            (s["id"], s["url"], s["type"], ",".join(s.get("tags",[])))
        )
    conn.commit()

def store_entities(conn, entities):
    import json as _json
    for e in entities:
        conn.execute(
            "INSERT OR REPLACE INTO entities(entity_id,entity_type,name,aliases,attributes_json) VALUES (?,?,?,?,?)",
            (e.entity_id, e.entity_type, e.name, ",".join(e.aliases), _json.dumps(e.attributes, ensure_ascii=False))
        )
        for ev in e.evidence:
            conn.execute(
                "INSERT OR REPLACE INTO entity_evidence(entity_id,url,sha256,retrieved_at) VALUES (?,?,?,?)",
                (e.entity_id, ev.url, ev.sha256, ev.retrieved_at)
            )
    conn.commit()

def store_events(conn, events, entity_ids_by_name):
    import json as _json
    for ev in events:
        conn.execute(
            "INSERT OR REPLACE INTO events(event_id,event_type,occurred_on,location_json,outcomes_json,constraints) VALUES (?,?,?,?,?,?)",
            (ev.event_id, ev.event_type, ev.occurred_on, _json.dumps(ev.location, ensure_ascii=False),
             _json.dumps(ev.outcomes, ensure_ascii=False), "\n".join(ev.constraints))
        )
        # participants are optional in v1; add later with entity linking
    conn.commit()

def ingest_once():
    conn = connect(cfg.db_url)
    init(conn)
    upsert_sources(conn)

    os.makedirs(cfg.data_dir, exist_ok=True)
    os.makedirs(os.path.join(cfg.data_dir,"normalized"), exist_ok=True)

    for s in tqdm(SOURCES, desc="Ingesting sources"):
        url = s["url"]
        polite_sleep(cfg.rate_limit_rps)
        content, ctype = fetch_url(url, cfg.user_agent, cfg.timeout_secs)
        sha = sha256_bytes(content)

        # store raw
        suffix = ".pdf" if "pdf" in ctype else ".html"
        raw_path = url_to_path(cfg.data_dir, url, suffix)
        with open(raw_path,"wb") as f:
            f.write(content)

        text = extract_text_html(content) if "html" in ctype else ""
        text_path = save_text(cfg.data_dir, url, text)

        fetched_at = now_iso()
        conn.execute(
            "INSERT OR REPLACE INTO fetches(url,fetched_at,sha256,content_type,title,publisher,raw_path) VALUES (?,?,?,?,?,?,?)",
            (url, fetched_at, sha, ctype, None, None, raw_path)
        )

        record_id = f"rec.{sha[:16]}"
        conn.execute(
            "INSERT OR REPLACE INTO records(record_id,source_id,url,title,fetched_at,text_path) VALUES (?,?,?,?,?,?)",
            (record_id, s["id"], url, None, fetched_at, text_path)
        )
        conn.commit()

        ev = Evidence(evidence_type="webpage", url=url, retrieved_at=fetched_at, sha256=sha)
        ents = extract_entities(text, ev)
        events = extract_events(text, ev)

        store_entities(conn, ents)
        store_events(conn, events, {})

        # Write normalized JSONL
        rr = ResearchRecord(
            record_id=record_id,
            source_id=s["id"],
            url=url,
            title=None,
            fetched_at=fetched_at,
            extracted_text=text,
            entities=ents,
            events=events
        )
        out_path = os.path.join(cfg.data_dir,"normalized", f"{record_id}.json")
        with open(out_path,"w",encoding="utf-8") as f:
            f.write(rr.model_dump_json(indent=2))

    print("Done. DB:", cfg.db_url)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true", help="run once and exit")
    ap.add_argument("--loop", action="store_true", help="poll forever")
    ap.add_argument("--minutes", type=int, default=180, help="poll interval minutes")
    args = ap.parse_args()

    if args.once or not args.loop:
        ingest_once()
        return

    import time
    while True:
        ingest_once()
        time.sleep(args.minutes * 60)

if __name__ == "__main__":
    main()
