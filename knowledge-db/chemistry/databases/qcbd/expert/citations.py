"""Citation normalization utilities.

Provides deterministic citation key generation while avoiding any verbatim large text ingestion.
Future extension points: CrossRef / DOI resolution, author disambiguation.
"""
from __future__ import annotations
from typing import List, Dict, Optional
import re, hashlib

DOI_RE = re.compile(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', re.IGNORECASE)

def parse_doi(text: str) -> Optional[str]:
    if not text: return None
    m = DOI_RE.search(text)
    if m: return m.group(0).lower()
    return None

def canonical_author(author: str) -> str:
    parts = [p for p in re.split(r'\s+', author.strip()) if p]
    if not parts: return ''
    last = parts[-1].lower()
    initials = ''.join(p[0].lower() for p in parts[:-1])
    return f"{last}_{initials}" if initials else last

def citation_key(authors: List[str], year: Optional[int], title: str, doi: Optional[str]) -> str:
    a_part = (authors[0].split()[-1].lower() if authors else 'anon')
    y_part = str(year) if year else 'noyear'
    base = f"{a_part}_{y_part}"[:20]
    # Hash to ensure uniqueness without exposing full title content
    tail = hashlib.sha256(title.encode()).hexdigest()[:8]
    if doi:
        doi_hash = hashlib.sha256(doi.encode()).hexdigest()[:6]
        return f"{base}_{tail}_{doi_hash}"
    return f"{base}_{tail}"

def normalize_record(raw: Dict[str, str]) -> Dict[str, str]:
    title = raw.get('title','')
    authors_raw = raw.get('authors','')
    authors = [a for a in re.split(r';|,', authors_raw) if a.strip()]
    authors_can = [canonical_author(a) for a in authors][:5]  # limit author list length
    year = None
    try:
        year = int(raw.get('year'))
    except Exception:
        year = None
    doi = parse_doi(title) or parse_doi(raw.get('doi',''))
    key = citation_key(authors_can, year, title, doi)
    return {
        'key': key,
        'title': title[:200],  # truncate to avoid large ingestion
        'year': year,
        'authors': authors_can,
        'doi': doi
    }
