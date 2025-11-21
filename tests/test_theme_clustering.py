#!/usr/bin/env python3
"""
Tests for theme clustering functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sorokin
from sorokin import cluster_themes, get_active_themes, jaccard_similarity


def test_jaccard_similarity():
    """Test Jaccard similarity computation."""
    set1 = {"a", "b", "c"}
    set2 = {"b", "c", "d"}
    
    sim = jaccard_similarity(set1, set2)
    # Intersection: {b, c} = 2, Union: {a, b, c, d} = 4
    expected = 2.0 / 4.0
    assert abs(sim - expected) < 0.001, f"Expected {expected}, got {sim}"
    
    # Identical sets
    sim = jaccard_similarity(set1, set1)
    assert sim == 1.0, "Identical sets should have similarity 1.0"
    
    # Disjoint sets
    set3 = {"x", "y", "z"}
    sim = jaccard_similarity(set1, set3)
    assert sim == 0.0, "Disjoint sets should have similarity 0.0"
    
    # Empty sets
    sim = jaccard_similarity(set(), set())
    assert sim == 0.0, "Empty sets should have similarity 0.0"


def test_cluster_themes():
    """Test theme clustering."""
    # Create co-occurrence matrix with two clear clusters
    co_occur = {
        "destroy": {"the": 10, "sentence": 8, "word": 5},
        "the": {"destroy": 10, "sentence": 12, "word": 7},
        "sentence": {"destroy": 8, "the": 12, "word": 9},
        "word": {"destroy": 5, "the": 7, "sentence": 9},
        # Second cluster
        "love": {"poetry": 10, "sonnet": 8},
        "poetry": {"love": 10, "sonnet": 9},
        "sonnet": {"love": 8, "poetry": 9},
    }
    
    themes = cluster_themes(co_occur, threshold=0.3, min_theme_size=2)
    
    assert len(themes) > 0, "Should find at least one theme"
    
    # Check that words from same cluster are grouped
    theme_words = set()
    for theme in themes:
        theme_words.update(theme)
    
    # Both clusters should be represented
    assert "destroy" in theme_words or "the" in theme_words, "First cluster should be found"
    assert "love" in theme_words or "poetry" in theme_words, "Second cluster should be found"


def test_get_active_themes():
    """Test active theme detection."""
    themes = [
        {"destroy", "the", "sentence"},
        {"love", "poetry", "sonnet"},
        {"test", "check", "verify"},
    ]
    
    # Words from first theme
    words = ["destroy", "sentence"]
    active = get_active_themes(words, themes)
    
    assert len(active) >= 1, "Should find at least one active theme"
    assert any("destroy" in theme for theme in active), "First theme should be active"
    
    # Words from multiple themes
    words = ["destroy", "love"]
    active = get_active_themes(words, themes)
    
    assert len(active) >= 2, "Should find multiple active themes"
    
    # No matching words
    words = ["nonexistent", "words"]
    active = get_active_themes(words, themes)
    
    assert len(active) == 0, "Should find no active themes"


def test_cluster_themes_empty():
    """Test clustering with empty co-occurrence."""
    themes = cluster_themes({}, threshold=0.3, min_theme_size=3)
    assert themes == [], "Empty co-occurrence should return empty themes"


def test_cluster_themes_min_size():
    """Test that min_theme_size filter works."""
    co_occur = {
        "a": {"b": 5},
        "b": {"a": 5},
        "c": {"d": 3},
        "d": {"c": 3},
    }
    
    # min_theme_size=3 should filter out small themes
    themes = cluster_themes(co_occur, threshold=0.3, min_theme_size=3)
    
    # All themes should have at least 3 words (or be filtered out)
    for theme in themes:
        assert len(theme) >= 3, f"Theme {theme} should have at least 3 words"


if __name__ == "__main__":
    test_jaccard_similarity()
    print("✓ test_jaccard_similarity passed")
    
    test_cluster_themes()
    print("✓ test_cluster_themes passed")
    
    test_get_active_themes()
    print("✓ test_get_active_themes passed")
    
    test_cluster_themes_empty()
    print("✓ test_cluster_themes_empty passed")
    
    test_cluster_themes_min_size()
    print("✓ test_cluster_themes_min_size passed")
    
    print("\n✅ All theme clustering tests passed!")

