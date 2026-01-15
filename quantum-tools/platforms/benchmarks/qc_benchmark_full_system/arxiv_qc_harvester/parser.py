import xml.etree.ElementTree as ET
from .filters import abstract_matches

def parse_arxiv_entries(xml_text: str, category: str) -> list:
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", ns):
        title = entry.findtext("atom:title", "").strip()
        abstract = entry.findtext("atom:summary", "").strip()
        if not abstract_matches(abstract):
            continue
        authors = [a.findtext("atom:name", "") for a in entry.findall("atom:author", ns)]
        url_el = entry.find("atom:link[@rel='alternate']", ns)
        url = url_el.get("href", None) if url_el is not None else None
        published = entry.findtext("atom:published", "")
        doi_el = entry.find("arxiv:doi", ns)
        doi = doi_el.text if doi_el is not None else None
        entries.append({
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "url": url,
            "doi": doi,
            "published": published,
            "subject": [category],
        })
    return entries
