
from .sourcing_policy import extract_host, domain_is_trusted
import re

BLOCK_PATTERNS = [r"forum\.", r"reddit\.com", r"quora\.com", r"facebook\.com", r"tiktok\.com", r"instagram\.com"]

def basic_trust(url: str) -> bool:
    host = extract_host(url)
    if not domain_is_trusted(host):
        return False
    for pat in BLOCK_PATTERNS:
        if re.search(pat, host):
            return False
    return True
