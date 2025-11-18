#!/usr/bin/env python3
"""Test balanced mix: memory (50%) + web (50%)."""

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
    DB_PATH
)

async def test_balanced_mix():
    """Test that web is ALWAYS called, even when memory is full."""
    init_db()

    test_word = "darkness"

    print(f"\n=== Test: Balanced Mix (50% memory + 50% web) ===\n")

    # Clear any existing memory for this word
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM word_memory WHERE word = ?", (test_word,))
    conn.commit()

    # Add 10 words to memory (way more than width=3)
    fake_memory = ["shadow", "night", "void", "abyss", "black",
                   "gloom", "murk", "dimness", "obscurity", "shade"]
    for word in fake_memory:
        conn.execute(
            "INSERT INTO word_memory (word, related) VALUES (?, ?)",
            (test_word, word)
        )
    conn.commit()
    conn.close()

    # Check memory
    mem = recall_word_relations(test_word, 10)
    print(f"Memory has: {len(mem)} words")
    print(f"  Memory: {mem}")

    # Run lookup with width=4
    print(f"\nRunning lookup_branches_for_word('{test_word}', width=4)...")
    print("Expected: ~2 from memory (50%) + ~2 from web (50%)")
    print()

    branches = await lookup_branches_for_word(test_word, width=4, all_candidates=[])

    print(f"Result: {branches}")
    print(f"Total: {len(branches)} words")

    # Check which are from memory
    from_memory = [w for w in branches if w in mem]
    from_web = [w for w in branches if w not in mem]

    print(f"\nBreakdown:")
    print(f"  From memory: {len(from_memory)} - {from_memory}")
    print(f"  From web: {len(from_web)} - {from_web}")
    print(f"  Ratio: {len(from_memory)}/{len(branches)} memory, {len(from_web)}/{len(branches)} web")

    # Test with width=6
    print(f"\n=== Testing with width=6 ===\n")
    branches2 = await lookup_branches_for_word(test_word, width=6, all_candidates=[])

    from_memory2 = [w for w in branches2 if w in mem]
    from_web2 = [w for w in branches2 if w not in mem]

    print(f"Result: {branches2}")
    print(f"\nBreakdown:")
    print(f"  From memory: {len(from_memory2)} - {from_memory2}")
    print(f"  From web: {len(from_web2)} - {from_web2}")
    print(f"  Ratio: {len(from_memory2)}/{len(branches2)} memory, {len(from_web2)}/{len(branches2)} web")

    # Verify web was actually called
    if from_web or from_web2:
        print("\n✅ SUCCESS: Web scraping is working even with full memory cache!")
        print("   Fresh web data is being mixed with cached memory.")
    else:
        print("\n❌ FAILURE: No web words found. System still using only memory cache.")

if __name__ == "__main__":
    asyncio.run(test_balanced_mix())
