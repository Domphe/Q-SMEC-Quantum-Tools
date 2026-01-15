import requests
from .config import ARXIV_API, USER_AGENT, FILTER_TERMS

def fetch_arxiv_xml(cat: str, start: int = 0, max_results: int = 200) -> str:
    query = f"cat:{cat} AND all:({' OR '.join(FILTER_TERMS)})"
    params = {
        "search_query": query,
        "start": start,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(ARXIV_API, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text
