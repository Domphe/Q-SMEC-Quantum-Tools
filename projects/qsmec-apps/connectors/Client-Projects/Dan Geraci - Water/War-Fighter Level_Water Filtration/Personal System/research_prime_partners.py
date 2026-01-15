#!/usr/bin/env python3
"""
Research script to find prime partner POCs in Arizona for soldier systems/defense partnerships.
Targets: RTX (Raytheon) Tucson, L3Harris Phoenix/Tucson, Collins Aerospace Phoenix,
General Dynamics Scottsdale, and local AZ manufacturing partners.
"""

import json
import re
import sys
import time
from urllib.parse import quote
from urllib.request import Request, urlopen

DDG_HTML = "https://duckduckgo.com/html/?q={query}&kl=us-en"
USER_AGENT = "Mozilla/5.0 (research-script/2.0)"

TARGETS = [
    {
        "company": "RTX (Raytheon)",
        "location": "Tucson, Arizona",
        "query": "RTX Raytheon Tucson Arizona business development partnerships contact soldier systems",
    },
    {
        "company": "L3Harris",
        "location": "Phoenix/Tucson, Arizona",
        "query": "L3Harris Phoenix Tucson Arizona business development soldier communications contact",
    },
    {
        "company": "Collins Aerospace (RTX)",
        "location": "Phoenix, Arizona",
        "query": "Collins Aerospace Phoenix Arizona capture manager avionics contact",
    },
    {
        "company": "General Dynamics Mission Systems",
        "location": "Scottsdale, Arizona",
        "query": "General Dynamics Mission Systems Scottsdale Arizona partnerships contact",
    },
    {
        "company": "Arizona Manufacturing (Berry Compliant)",
        "location": "Tucson, Arizona",
        "query": "Arizona Tucson manufacturing Berry compliant defense harness enclosure contact",
    },
]


def search_html(query: str):
    """Scrape DuckDuckGo HTML results."""
    html_url = DDG_HTML.format(query=quote(query))
    req = Request(html_url, headers={"User-Agent": USER_AGENT})
    try:
        with urlopen(req, timeout=15) as resp:  # noqa: S310
            html = resp.read().decode("utf-8", errors="ignore")
        # Regex to grab result links and snippets
        anchor_re = re.compile(
            r'<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
            re.IGNORECASE,
        )
        snippet_re = re.compile(
            r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>', re.IGNORECASE
        )
        results = []
        for href, text in anchor_re.findall(html):
            clean_text = re.sub(r"<[^>]+>", "", text)
            results.append({"url": href, "title": clean_text})
        for snippet_match in snippet_re.findall(html):
            clean_snippet = re.sub(r"<[^>]+>", "", snippet_match)
            if results:
                # Attach snippet to last result (simple heuristic)
                results[-1]["snippet"] = clean_snippet
        return results[:5]  # Top 5 results
    except Exception as exc:  # noqa: BLE001
        return [{"error": str(exc)}]


def main():
    output = []
    for target in TARGETS:
        print(
            f"Searching: {target['company']} ({target['location']})...", file=sys.stderr
        )
        results = search_html(target["query"])
        output.append(
            {
                "company": target["company"],
                "location": target["location"],
                "query": target["query"],
                "results": results,
            }
        )
        time.sleep(2)  # Be polite
    json.dump(output, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
