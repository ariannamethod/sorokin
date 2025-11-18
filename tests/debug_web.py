#!/usr/bin/env python3
"""Debug script to check if web scraping actually happens."""

import asyncio
import sys
import os

# Add current dir to path
sys.path.insert(0, os.path.dirname(__file__))

from sorokin import _fetch_web_synonyms, _extract_candidate_words, recall_word_relations, init_db

async def test_web_scraping():
    """Test if web scraping returns real data."""
    init_db()

    test_word = "destroy"

    print(f"\n=== Testing web scraping for '{test_word}' ===\n")

    # Check memory first
    print("1) Checking SQLite memory...")
    mem_words = recall_word_relations(test_word, 10)
    print(f"   Memory has: {len(mem_words)} words")
    if mem_words:
        print(f"   Words: {mem_words[:5]}")

    # Try web scraping
    print("\n2) Fetching from DuckDuckGo...")
    query = f"{test_word} synonym"
    html = await _fetch_web_synonyms(query)

    print(f"   HTML length: {len(html)} bytes")
    if len(html) < 1000:
        print(f"   HTML content: {html[:500]}")
    else:
        print(f"   HTML starts with: {html[:200]}...")

    # Extract candidates
    print("\n3) Extracting candidate words...")
    candidates = _extract_candidate_words(html)
    print(f"   Found {len(candidates)} candidates")
    if candidates:
        print(f"   First 10: {candidates[:10]}")

    # Test another word
    test_word2 = "machine"
    print(f"\n=== Testing web scraping for '{test_word2}' ===\n")

    query2 = f"{test_word2} synonym"
    html2 = await _fetch_web_synonyms(query2)
    print(f"   HTML length: {len(html2)} bytes")

    candidates2 = _extract_candidate_words(html2)
    print(f"   Found {len(candidates2)} candidates")
    if candidates2:
        print(f"   First 10: {candidates2[:10]}")

if __name__ == "__main__":
    asyncio.run(test_web_scraping())
