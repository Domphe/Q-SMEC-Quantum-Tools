#!/usr/bin/env python3
"""
Quick research helper to find candidate labs/POCs for Tucson-first P248 testing and AZ secondaries.
Uses DuckDuckGo's JSON API (no key required) to collect URLs and snippets for manual follow-up.
"""

import json
import re
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

QUERIES = [
    "Tucson water testing laboratory NSF P248",
    "Tucson environmental testing lab drinking water contact",
    "Arizona water quality lab certification contact",
    "Phoenix shock vibration testing MIL-STD-810H lab",
    "Yuma Proving Ground sand dust test facility contact",
]

DDG_API = "https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
DDG_HTML = "https://duckduckgo.com/html/?q={query}&kl=us-en"
USER_AGENT = "Mozilla/5.0 (research-script/1.0)"


def search(query: str):
    url = DDG_API.format(query=quote(query))
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=15) as resp:  # noqa: S310
        raw = resp.read()
    data = json.loads(raw)
    results = []
    # DuckDuckGo returns related topics; each may have FirstURL and Text
    related = data.get("RelatedTopics", [])
    for item in related:
        if isinstance(item, dict) and item.get("FirstURL"):
            results.append(
                {
                    "url": item.get("FirstURL"),
                    "text": item.get("Text"),
                }
            )
        # Some entries are nested under "Topics"
        if isinstance(item, dict) and item.get("Topics"):
            for sub in item.get("Topics", []):
                if isinstance(sub, dict) and sub.get("FirstURL"):
                    results.append(
                        {
                            "url": sub.get("FirstURL"),
                            "text": sub.get("Text"),
                        }
                    )
    if results:
        return results

    # Fallback: scrape HTML SERP for result links
    html_url = DDG_HTML.format(query=quote(query))
    html_req = Request(html_url, headers={"User-Agent": USER_AGENT})
    with urlopen(html_req, timeout=15) as resp:  # noqa: S310
        html = resp.read().decode("utf-8", errors="ignore")
    # Simple regex to grab anchors with result__a class
    anchor_re = re.compile(
        r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE
    )
    for href, text in anchor_re.findall(html):
        # Clean HTML tags from text
        clean_text = re.sub(r"<[^>]+>", "", text)
        results.append({"url": href, "text": clean_text})
    return results


def main():
    output = []
    for q in QUERIES:
        try:
            results = search(q)
            output.append({"query": q, "results": results})
            time.sleep(1)  # be gentle
        except Exception as exc:  # noqa: BLE001
            output.append({"query": q, "error": str(exc)})
    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
