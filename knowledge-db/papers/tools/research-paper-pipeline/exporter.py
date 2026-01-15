import csv
import json
from pathlib import Path
from datetime import datetime
import zipfile

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def timestamped(name):
    return f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def to_csv(entries, session_name):
    path = EXPORT_DIR / f"{timestamped(session_name)}.csv"
    keys = ["title", "authors", "published", "url", "abstract", "doi"]
    with open(path, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for entry in entries:
            row = {k: entry.get(k, "") for k in keys}
            row["authors"] = ", ".join(entry.get("authors", []))
            writer.writerow(row)
    return path

def to_markdown(entries, session_name):
    path = EXPORT_DIR / f"{timestamped(session_name)}.md"
    with open(path, "w", encoding="utf-8") as f:
        for e in entries:
            f.write(f"## [{e['title']}]({e['url']})\n")
            f.write(f"**Authors:** {', '.join(e['authors'])}\n\n")
            f.write(f"**Abstract:** {e['abstract']}\n\n---\n")
    return path

def to_bibtex(entries, session_name):
    path = EXPORT_DIR / f"{timestamped(session_name)}.bib"
    with open(path, "w", encoding="utf-8") as f:
        for i, e in enumerate(entries):
            f.write(f"@article{{entry{i},\n")
            f.write(f"  title={{ {e['title']} }},\n")
            f.write(f"  author={{ {' and '.join(e['authors'])} }},\n")
            f.write(f"  journal={{arXiv}},\n")
            f.write(f"  year={{ {e['published'][:4]} }},\n")
            f.write(f"  url={{ {e['url']} }},\n")
            if e.get("doi"):
                f.write(f"  doi={{ {e['doi']} }},\n")
            f.write("}\n\n")
    return path

def create_export_zip(file_paths, session_name):
    zip_path = EXPORT_DIR / f"{timestamped(session_name)}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for fpath in file_paths:
            zipf.write(fpath, arcname=fpath.name)
    return zip_path
