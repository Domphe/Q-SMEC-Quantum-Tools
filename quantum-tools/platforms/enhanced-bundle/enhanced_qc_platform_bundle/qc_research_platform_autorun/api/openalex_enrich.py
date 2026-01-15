import requests

def enrich_doi(doi):
    url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    r = requests.get(url)
    if r.status_code == 200:
        d = r.json()
        return {
            "title": d.get("title"),
            "citations": d.get("cited_by_count"),
            "authors": [a["author"]["display_name"] for a in d.get("authorships", [])]
        }
    return {"error": "DOI not found"}

if __name__ == "__main__":
    result = enrich_doi("10.1021/acs.jctc.0c00121")
    print(json.dumps(result, indent=2))