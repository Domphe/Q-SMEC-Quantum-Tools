from __future__ import annotations
import hashlib, os, time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def url_to_path(data_dir: str, url: str, suffix: str) -> str:
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]
    os.makedirs(os.path.join(data_dir,"raw"), exist_ok=True)
    return os.path.join(data_dir,"raw", f"{h}{suffix}")

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def fetch_url(url: str, user_agent: str, timeout_secs: int) -> tuple[bytes, str]:
    r = requests.get(url, headers={"User-Agent":user_agent}, timeout=timeout_secs)
    r.raise_for_status()
    content_type = r.headers.get("Content-Type","").split(";")[0].strip()
    return r.content, content_type

def extract_text_html(content: bytes) -> str:
    soup = BeautifulSoup(content, "lxml")
    # Remove noisy tags
    for tag in soup(["script","style","noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    # Light normalization
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n".join(lines)

def polite_sleep(rate_limit_rps: float) -> None:
    if rate_limit_rps <= 0:
        return
    time.sleep(1.0 / rate_limit_rps)
