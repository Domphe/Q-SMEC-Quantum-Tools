
import requests
from tqdm import tqdm

def enrich_with_openalex(methods):
    for m in tqdm(methods):
        try:
            title = m["name"]
            url = f"https://api.openalex.org/works?search={title}"
            resp = requests.get(url, timeout=10)
            if resp.ok:
                data = resp.json()
                if data["results"]:
                    m["citation_count"] = data["results"][0].get("cited_by_count", None)
        except Exception as e:
            print("OpenAlex fetch failed for", m.get("id"), ":", str(e))
    return methods
