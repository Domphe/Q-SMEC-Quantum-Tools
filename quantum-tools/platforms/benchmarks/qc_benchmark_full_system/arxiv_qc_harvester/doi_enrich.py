import requests

def enrich_with_crossref(entries):
    headers = {"User-Agent": "QCBD/1.0 (mailto:qcbd@example.com)"}
    for entry in entries:
        if not entry.get("doi"):
            continue
        doi = entry["doi"]
        url = f"https://api.crossref.org/works/{doi}"
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json().get("message", {})
            entry["publisher_full"] = data.get("publisher")
            entry["journal"] = data.get("container-title", [None])[0]
            entry["doi_url"] = data.get("URL")
        except Exception as e:
            entry["crossref_error"] = str(e)
    return entries
