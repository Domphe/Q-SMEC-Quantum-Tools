
import re, tldextract, requests, datetime
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

GOV_DOMAINS = [
    r"\.gov$", r"\.mil$", r"\.eu$", r"\.europa\.eu$", r"\.nato\.int$", r"\.nso\.nato\.int$",
    r"\.itu\.int$", r"\.oecd\.org$", r"\.who\.int$", r"\.un\.org$"
]
OFFICIAL_DOMAINS = [
    r"\.iso\.org$", r"\.iec\.ch$", r"\.sae\.org$", r"\.nist\.gov$", r"\.esa\.int$", r"\.faa\.gov$",
    r"\.bis\.doc\.gov$", r"\.state\.gov$"
]
OPEN_SOURCE_TRUSTED = [
    r"\.arxiv\.org$", r"\.spiedigitallibrary\.org$", r"\.osapublishing\.org$", r"\.nature\.com$",
    r"\.ieee\.org$", r"\.springer\.com$", r"\.aiaa\.org$"
]

ALLOW_PATTERNS = GOV_DOMAINS + OFFICIAL_DOMAINS + OPEN_SOURCE_TRUSTED

def domain_is_trusted(host):
    for pat in ALLOW_PATTERNS:
        if re.search(pat, host):
            return True
    return False

def extract_host(url):
    ext = tldextract.extract(url)
    host = ".".join([p for p in [ext.subdomain, ext.domain, ext.suffix] if p])
    return host.lower()

def get_last_modified(url, timeout=30, headers=None):
    try:
        r = requests.head(url, timeout=timeout, headers=headers, allow_redirects=True)
        if 'Last-Modified' in r.headers:
            return dateparser.parse(r.headers['Last-Modified'])
    except Exception:
        pass
    try:
        r = requests.get(url, timeout=timeout, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        for sel in [
            {"name":"last-modified"}, {"property":"article:modified_time"},
            {"property":"og:updated_time"}, {"name":"dc.date"}, {"itemprop":"dateModified"}
        ]:
            tag = soup.find("meta", attrs=sel)
            if tag and tag.get("content"):
                try:
                    return dateparser.parse(tag["content"])
                except Exception:
                    continue
        import re
        m = re.search(r"(20\d{2}-\d{2}-\d{2}|[A-Za-z]+ \d{1,2}, 20\d{2})", soup.get_text(" ", strip=True))
        if m:
            return dateparser.parse(m.group(0))
    except Exception:
        pass
    return None

def is_fresh(enforced_after: datetime.datetime, page_dt):
    if page_dt is None:
        return False
    return page_dt >= enforced_after
