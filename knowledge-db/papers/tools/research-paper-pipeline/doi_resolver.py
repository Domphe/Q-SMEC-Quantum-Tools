import requests

def enrich_doi(doi: str):
    if not doi:
        return {}
    try:
        url = f"https://api.crossref.org/works/{doi}"
        headers = {"User-Agent": "QCBD/1.0 (mailto:you@example.com)"}
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()["message"]
        return {
            "journal": data.get("container-title", [""])[0],
            "published": data.get("issued", {}).get("date-parts", [[None]])[0][0]
        }
    except Exception as e:
        return {}
