
from typing import List, Dict
from difflib import SequenceMatcher
from utils import fuzzy_score

def link_software(preprint: Dict, tools: List[Dict]) -> List[str]:
    title = preprint.get("title", "").lower()
    abstract = preprint.get("abstract", "").lower()
    candidates = []
    for tool in tools:
        if tool["name"].lower() in title or tool["name"].lower() in abstract:
            candidates.append(tool["id"])
    return candidates

def link_patents(preprint: Dict, patents: List[Dict]) -> List[str]:
    preprint_title = preprint.get("title", "").lower()
    linked = []
    for pat in patents:
        score = SequenceMatcher(None, preprint_title, pat["title"].lower()).ratio()
        if score > 0.75:
            linked.append(pat["id"])
    return linked

def link_datasets(preprint: Dict, datasets: List[Dict]) -> List[str]:
    abstract = preprint.get("abstract", "").lower()
    linked = []
    for ds in datasets:
        if ds["name"].lower() in abstract:
            linked.append(ds["id"])
    return linked
