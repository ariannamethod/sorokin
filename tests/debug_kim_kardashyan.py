#!/usr/bin/env python3
"""Debug why Kim Kardashyan test produces garbage."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sorokin import _fetch_web_synonyms, _extract_candidate_words, init_db

async def test_problematic_words():
    """Test web scraping for 'fat', 'ass', 'kim'."""
    init_db()

    problem_words = ["fat", "ass", "kim", "kardashyan"]

    for word in problem_words:
        print(f"\n{'='*60}")
        print(f"Testing: '{word}'")
        print('='*60)

        query = f"{word} synonym"
        html = await _fetch_web_synonyms(query)

        print(f"HTML length: {len(html)} bytes")

        if len(html) < 1000:
            print(f"HTML content:\n{html[:500]}")

        candidates = _extract_candidate_words(html)
        print(f"\nFound {len(candidates)} candidates")

        if candidates:
            print(f"First 15: {candidates[:15]}")
        else:
            print("NO CANDIDATES FOUND!")

if __name__ == "__main__":
    asyncio.run(test_problematic_words())
