#!/usr/bin/env python3
"""Debug script to check memory vs web priority."""

import asyncio
import sys
import os
import sqlite3

# Add current dir to path
sys.path.insert(0, os.path.dirname(__file__))

from sorokin import (
    lookup_branches_for_word,
    recall_word_relations,
    init_db,
    DB_PATH,
    _fetch_web_synonyms,
    _extract_candidate_words
)

async def test_memory_priority():
    """Test if memory blocks web scraping."""
    init_db()

    test_word = "darkness"

    print(f"\n=== Round 1: Fresh word (no memory) ===\n")

    # Clear any existing memory for this word
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM word_memory WHERE word = ?", (test_word,))
    conn.commit()
    conn.close()

    # Check memory
    mem = recall_word_relations(test_word, 3)
    print(f"Memory has: {len(mem)} words - {mem}")

    # Run lookup
    print("\nRunning lookup_branches_for_word (width=3)...")
    branches = await lookup_branches_for_word(test_word, width=3, all_candidates=[])
    print(f"Result: {branches}")

    # Now add to memory manually
    print(f"\n=== Round 2: After adding to memory ===\n")
    conn = sqlite3.connect(DB_PATH)
    # Add some fake memory entries
    for word in ["shadow", "night", "void"]:
        conn.execute(
            "INSERT INTO word_memory (word, related) VALUES (?, ?)",
            (test_word, word)
        )
    conn.commit()
    conn.close()

    # Check memory again
    mem = recall_word_relations(test_word, 3)
    print(f"Memory now has: {len(mem)} words - {mem}")

    # Run lookup again - will it go to web?
    print("\nRunning lookup_branches_for_word (width=3) again...")
    branches = await lookup_branches_for_word(test_word, width=3, all_candidates=[])
    print(f"Result: {branches}")

    # Try web directly to see what it would have returned
    print("\n=== What web would have returned: ===\n")
    html = await _fetch_web_synonyms(f"{test_word} synonym")
    candidates = _extract_candidate_words(html)
    print(f"Web has {len(candidates)} candidates")
    print(f"First 10: {candidates[:10]}")

if __name__ == "__main__":
    asyncio.run(test_memory_priority())
