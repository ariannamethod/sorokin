#!/usr/bin/env python3
"""Check raw DDG HTML for problematic words."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sorokin import _fetch_web_synonyms, init_db

async def check_ddg_html():
    """Look at raw HTML from DDG."""
    init_db()

    word = "fat"
    query = f"{word} synonym"

    print(f"Fetching DDG for: '{query}'")
    html = await _fetch_web_synonyms(query)

    print(f"\nHTML length: {len(html)} bytes")
    print(f"\nFirst 2000 chars of HTML:")
    print("="*60)
    print(html[:2000])
    print("="*60)

    # Check if it's an error page
    if "No results found" in html or "no results" in html.lower():
        print("\n❌ DDG returned 'No results found' page!")

    if "did you mean" in html.lower():
        print("\n⚠️  DDG is suggesting 'did you mean'")

    # Look for actual content
    if "<a " in html and "result" in html.lower():
        print("\n✅ Looks like real search results")
    else:
        print("\n❌ Doesn't look like search results")

if __name__ == "__main__":
    asyncio.run(check_ddg_html())
