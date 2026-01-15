import requests

def fetch_by_doi(doi):
    url = f"https://api.openalex.org/works/https://doi.org/{doi}"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return {
            "title": data.get("title"),
            "citation_count": data.get("cited_by_count"),
            "authors": [a["author"]["display_name"] for a in data.get("authorships", [])]
        }
    else:
        return {"error": "Not found"}

if __name__ == "__main__":
    doi = "10.1021/acs.jctc.0c00121"
    print(fetch_by_doi(doi))