#!/usr/bin/env python3
"""Debug README bigrams for specific words."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sorokin import _build_readme_bigrams, init_db

def check_readme_bigrams():
    """Check README bigrams for test words."""
    init_db()

    bigrams = _build_readme_bigrams()

    print(f"Total README bigram keys: {len(bigrams)}")
    print()

    test_words = ["fat", "ass", "kim", "kardashyan", "machine", "language"]

    for word in test_words:
        if word in bigrams:
            print(f"'{word}' → {bigrams[word][:10]}")  # First 10
        else:
            print(f"'{word}' → NOT IN README")

    # Show sample of what IS in README
    print(f"\nSample bigrams (first 10 keys):")
    for i, (k, v) in enumerate(list(bigrams.items())[:10]):
        print(f"  '{k}' → {v[:3]}")
        if i >= 9:
            break

if __name__ == "__main__":
    check_readme_bigrams()
