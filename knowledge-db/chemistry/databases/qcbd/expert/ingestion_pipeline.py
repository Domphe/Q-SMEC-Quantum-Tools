"""Modular ingestion pipeline for trusted quantum chemistry & physics sources.

Pipeline stages:
 1. Select sources (registry filtering)
 2. Fetch raw content (HTTP / local)
 3. Parse (HTML -> text blocks, PDF stub, JSON direct)
 4. Extract structured facts (rules + light NLP placeholders)
 5. Normalize citations & metadata
 6. Score quality & provenance
 7. Store as JSON documents (expert/sources/processed/*.json)

NOTE: Avoid storing copyrighted verbatim content. Only metadata, derived facts, equations encoded symbolically, and short factual summaries.
"""

from __future__ import annotations
import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
import re
import datetime
import hashlib
import requests

QCBD_ROOT = Path(os.environ.get('QCBD_ROOT', r'G:\My Drive\Databases\QCBD'))
REGISTRY_PATH = QCBD_ROOT / 'expert' / 'source_registry.json'
PROCESSED_DIR = QCBD_ROOT / 'expert' / 'sources' / 'processed'
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Fallback registry embedded (metadata only) if file reads empty due to environment anomaly.
SOURCE_REGISTRY_FALLBACK = {
    "sources": [
        {
            "id": "gov_nist_constants_2025",
            "category": "government",
            "title": "NIST Fundamental Physical Constants",
            "year": 2025,
            "url": "https://physics.nist.gov/constants",
            "topics": ["fundamental constants", "precision", "metrology"],
            "access": {"license": "public_domain", "extraction_allowed": True}
        },
        {
            "id": "std_iupac_atomic_weights_2025",
            "category": "standards",
            "title": "IUPAC Standard Atomic Weights (2025 revision)",
            "year": 2025,
            "url": "https://iupac.org/what-we-do/periodic-table-of-elements/",
            "topics": ["atomic weights", "chemistry"],
            "access": {"license": "fair_use_metadata", "extraction_allowed": True}
        },
        {
            "id": "journal_jcp_coupled_cluster_review",
            "category": "journals",
            "title": "Coupled-Cluster Theory Overview",
            "year": 2025,
            "url": "https://example.org/cc_review",
            "topics": ["CCSD(T)", "many-body"],
            "access": {"license": "copyrighted", "extraction_allowed": False}
        },
        {
            "id": "preprint_arxiv_td_magnetism_2025",
            "category": "preprints",
            "title": "Time-Dependent Magnetism in Correlated 2D Materials",
            "year": 2025,
            "url": "https://arxiv.org/abs/2501.01234",
            "topics": ["2D materials", "spin dynamics"],
            "access": {"license": "arxiv_license", "extraction_allowed": True}
        }
    ]
}

# ---- Data Classes ----
@dataclass
class SourceMeta:
    id: str
    category: str
    title: str
    year: Optional[int] = None
    url: Optional[str] = None
    access: Dict[str, Any] = field(default_factory=dict)
    topics: List[str] = field(default_factory=list)

@dataclass
class IngestedDocument:
    source_id: str
    title: str
    category: str
    fetched_at: str
    hash: str
    facts: List[Dict[str, Any]]
    equations: List[Dict[str, str]]
    citations: List[Dict[str, Any]]
    quality: Dict[str, Any]
    warnings: List[str] = field(default_factory=list)

# ---- Load Registry ----
def load_registry() -> Dict[str, Any]:
    if not REGISTRY_PATH.exists():
        print("Info: registry file missing, using fallback.")
        return SOURCE_REGISTRY_FALLBACK
    raw = REGISTRY_PATH.read_text(encoding='utf-8')
    if not raw.strip():
        print(f"Warning: source registry empty: {REGISTRY_PATH} -> using fallback")
        return SOURCE_REGISTRY_FALLBACK
    try:
        data = json.loads(raw)
        if not data.get('sources'):
            print("Warning: registry has no sources -> using fallback")
            return SOURCE_REGISTRY_FALLBACK
        return data
    except json.JSONDecodeError as e:
        print(f"Registry JSON decode error: {e} -> using fallback")
        return SOURCE_REGISTRY_FALLBACK

# ---- Fetch Stage ----
def fetch_content(meta: SourceMeta) -> str:
    if not meta.url:
        return ''
    try:
        resp = requests.get(meta.url, timeout=10)
        ct = resp.headers.get('Content-Type', '')
        if 'text' in ct or 'json' in ct or ct == '':
            return resp.text
        return ''
    except Exception as e:
        return f"FETCH_ERROR:{e}"  # Recorded as warning downstream

# ---- Parse Stage (simplified) ----
HTML_TAG_RE = re.compile(r'<[^>]+>')

def parse_raw(raw: str) -> Dict[str, Any]:
    if raw.startswith('FETCH_ERROR:'):
        return {'text': '', 'warnings': [raw]}
    # Strip HTML tags
    text = HTML_TAG_RE.sub(' ', raw)
    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return {'text': text, 'warnings': []}

# ---- Extraction Stage (placeholder heuristics) ----
def extract_facts(parsed: Dict[str, Any], meta: SourceMeta) -> List[Dict[str, Any]]:
    text = parsed['text']
    facts: List[Dict[str, Any]] = []
    # Simple heuristic: sentences containing keywords
    KEYWORDS = ['correlation', 'Hamiltonian', 'basis set', 'exchange', 'spin', 'density', 'coupled cluster']
    for kw in KEYWORDS:
        if kw in text.lower():
            facts.append({'type': 'keyword_presence', 'keyword': kw, 'context_excerpt': '...'})
    # Placeholder domain pattern examples (expand with NLP later)
    if 'CCSD' in text:
        facts.append({'type': 'method_reference', 'method': 'CCSD'})
    if 'DFT' in text:
        facts.append({'type': 'method_reference', 'method': 'DFT'})
    return facts

# ---- Equation Extraction (stub) ----
EQUATION_PATTERNS = [r'H =', r'E =', r'\nabla^2', r'\int', r'\sum']

def extract_equations(text: str) -> List[Dict[str, str]]:
    equations = []
    for pat in EQUATION_PATTERNS:
        if pat in text:
            equations.append({'pattern': pat, 'representation': pat})
    return equations

# ---- Citation Normalization (stub) ----
def normalize_citations(meta: SourceMeta) -> List[Dict[str, Any]]:
    # Only self-citation placeholder; expand with crossref/doi lookups later
    citation_key = hashlib.sha256(meta.id.encode()).hexdigest()[:10]
    return [{'source_id': meta.id, 'key': citation_key, 'title': meta.title, 'year': meta.year}]

# ---- Quality Scoring ----

def score_quality(meta: SourceMeta, facts: List[Dict[str, Any]]) -> Dict[str, Any]:
    score = 0
    if meta.category in {'government', 'standards'}:
        score += 40
    if meta.category == 'journals':
        score += 30
    if meta.category == 'preprints':
        score += 10
    topical_bonus = min(len(facts) * 2, 20)
    score += topical_bonus
    return {
        'confidence_score': score,
        'category': meta.category,
        'fact_count': len(facts)
    }

# ---- Document Assembly ----

def build_document(meta: SourceMeta, parsed: Dict[str, Any]) -> IngestedDocument:
    raw_text = parsed['text']
    facts = extract_facts(parsed, meta)
    equations = extract_equations(raw_text)
    citations = normalize_citations(meta)
    quality = score_quality(meta, facts)
    warnings = parsed.get('warnings', [])
    doc_hash = hashlib.sha256((meta.id + raw_text[:200]).encode()).hexdigest()
    return IngestedDocument(
        source_id=meta.id,
        title=meta.title,
        category=meta.category,
        fetched_at=datetime.datetime.utcnow().isoformat(),
        hash=doc_hash,
        facts=facts,
        equations=equations,
        citations=citations,
        quality=quality,
        warnings=warnings
    )

# ---- Persistence ----

def persist_document(doc: IngestedDocument):
    out_path = PROCESSED_DIR / f"{doc.source_id}.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({
            'source_id': doc.source_id,
            'title': doc.title,
            'category': doc.category,
            'fetched_at': doc.fetched_at,
            'hash': doc.hash,
            'facts': doc.facts,
            'equations': doc.equations,
            'citations': doc.citations,
            'quality': doc.quality,
            'warnings': doc.warnings
        }, f, indent=2)
    return out_path

# ---- Orchestrator ----

def ingest_all(limit: Optional[int] = None, categories: Optional[List[str]] = None):
    registry = load_registry()
    sources = registry.get('sources', [])
    count = 0
    results = []
    for s in sources:
        if categories and s['category'] not in categories:
            continue
        meta = SourceMeta(id=s['id'], category=s['category'], title=s['title'], year=s.get('year'), url=s.get('url'), access=s.get('access', {}), topics=s.get('topics', []))
        raw = fetch_content(meta)
        parsed = parse_raw(raw)
        doc = build_document(meta, parsed)
        path = persist_document(doc)
        results.append({'id': meta.id, 'path': str(path), 'facts': len(doc.facts), 'warnings': doc.warnings})
        count += 1
        if limit and count >= limit:
            break
    return results


def main():
    print("=== Ingestion Start ===")
    results = ingest_all(limit=None)
    for r in results:
        print(f"{r['id']}: facts={r['facts']} warnings={len(r['warnings'])} -> {r['path']}")
    print("=== Ingestion Complete ===")

if __name__ == '__main__':
    main()
