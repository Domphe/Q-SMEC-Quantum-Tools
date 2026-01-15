"""Quality scoring heuristics for ingested documents.

Factors:
 - Source category base weight
 - Recency (year proximity to current year)
 - Fact density (facts per 1k chars proxy)
 - Citation count (normalized)
"""
from __future__ import annotations
from typing import Dict, Any, List
import datetime, math

CATEGORY_WEIGHTS = {
    'government': 50,
    'standards': 45,
    'journals': 35,
    'textbooks': 30,
    'preprints': 15,
    'other': 10
}

def score(meta: Dict[str, Any], raw_text: str, facts: List[Dict[str, Any]], citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    base = CATEGORY_WEIGHTS.get(meta.get('category','other'), 10)
    year = meta.get('year')
    recency_bonus = 0
    if isinstance(year, int):
        current = datetime.datetime.utcnow().year
        delta = max(0, current - year)
        recency_bonus = max(0, 20 - delta)  # fade over ~20 years
    fact_density = len(facts)  # already heuristic small list
    citation_bonus = min(len(citations) * 2, 20)
    raw_len = len(raw_text)
    length_penalty = 0
    if raw_len and raw_len > 20000:  # discourage overly large dumps
        length_penalty = 10
    total = base + recency_bonus + fact_density + citation_bonus - length_penalty
    return {
        'total_score': total,
        'base': base,
        'recency_bonus': recency_bonus,
        'fact_count': len(facts),
        'citation_count': len(citations),
        'length_penalty': length_penalty
    }
