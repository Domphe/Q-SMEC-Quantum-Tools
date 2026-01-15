import re
from .config import FILTER_TERMS

def abstract_matches(abstract: str) -> bool:
    return any(re.search(term, abstract, re.IGNORECASE) for term in FILTER_TERMS)
