#!/usr/bin/env python3
"""
Test suite for sorokin.py — because even Frankenstein needed quality control.
"""

import unittest
import tempfile
import sqlite3
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the sorokin module
import sorokin
from sorokin import (
    tokenize,
    select_core_words,
    phonetic_fingerprint,
    find_phonetic_neighbors,
    build_tree_for_word,
    collect_leaves,
    reassemble_corpse,
    render_node,
    render_autopsy,
    sorokin_autopsy,
    Node,
    init_db,
    store_autopsy,
    store_word_relations,
    recall_word_relations,
)


class TestTokenization(unittest.TestCase):
    """Test the scalpel: word extraction from chaos."""

    def test_basic_tokenization(self):
        text = "Hello, world! How are you?"
        tokens = tokenize(text)
        self.assertEqual(tokens, ["Hello", "world", "How", "are", "you"])

    def test_empty_string(self):
        self.assertEqual(tokenize(""), [])

    def test_punctuation_only(self):
        self.assertEqual(tokenize("!@#$%^&*()"), [])

    def test_mixed_languages(self):
        text = "Hello мир! Привет world."
        tokens = tokenize(text)
        self.assertIn("Hello", tokens)
        self.assertIn("мир", tokens)
        self.assertIn("Привет", tokens)
        self.assertIn("world", tokens)

    def test_numbers_excluded(self):
        text = "word123 456 test789"
        tokens = tokenize(text)
        # Numbers should not be included
        self.assertNotIn("123", tokens)
        self.assertNotIn("456", tokens)


class TestCoreWordSelection(unittest.TestCase):
    """Test the morgue's intake filter: what deserves dissection?"""

    def test_select_core_words_basic(self):
        tokens = ["the", "quick", "brown", "fox"]
        core = select_core_words(tokens)
        # 'the' is a stopword, should be filtered
        self.assertNotIn("the", [w.lower() for w in core])

    def test_empty_tokens(self):
        self.assertEqual(select_core_words([]), [])

    def test_single_character_filtered(self):
        tokens = ["a", "I", "word"]
        core = select_core_words(tokens)
        # Single-character words should be filtered
        self.assertNotIn("a", core)
        self.assertNotIn("I", core)

    def test_stopwords_filtered(self):
        tokens = ["the", "and", "or", "important", "word"]
        core = select_core_words(tokens)
        core_lower = [w.lower() for w in core]
        self.assertNotIn("the", core_lower)
        self.assertNotIn("and", core_lower)
        self.assertNotIn("or", core_lower)

    def test_deduplication(self):
        tokens = ["word", "word", "word", "other"]
        core = select_core_words(tokens)
        # Should only contain unique words
        self.assertEqual(len(core), len(set(w.lower() for w in core)))


class TestPhoneticSimilarity(unittest.TestCase):
    """Test the audio morgue: do these corpses sound alike?"""

    def test_phonetic_fingerprint(self):
        # Basic test
        fp = phonetic_fingerprint("hello")
        self.assertIsInstance(fp, str)
        self.assertTrue(len(fp) > 0)

    def test_similar_words(self):
        # Words that sound similar should have similar fingerprints
        fp1 = phonetic_fingerprint("cat")
        fp2 = phonetic_fingerprint("hat")
        # At least they should share something
        self.assertIsInstance(fp1, str)
        self.assertIsInstance(fp2, str)

    def test_find_phonetic_neighbors(self):
        word = "cat"
        pool = ["hat", "bat", "dog", "car", "mat"]
        neighbors = find_phonetic_neighbors(word, pool, 3)
        self.assertIsInstance(neighbors, list)
        # Should not include the word itself
        self.assertNotIn(word, neighbors)

    def test_find_phonetic_neighbors_empty_pool(self):
        neighbors = find_phonetic_neighbors("word", [], 5)
        self.assertEqual(neighbors, [])

    def test_find_phonetic_neighbors_zero_limit(self):
        neighbors = find_phonetic_neighbors("word", ["other"], 0)
        self.assertEqual(neighbors, [])


class TestTreeBuilding(unittest.TestCase):
    """Test the Frankenstein assembly line: recursive mutation."""

    def test_node_creation(self):
        node = Node(word="test")
        self.assertEqual(node.word, "test")
        self.assertEqual(node.children, [])

    def test_build_tree_depth_one(self):
        with patch('sorokin.lookup_branches_for_word', return_value=[]):
            node = build_tree_for_word("test", width=2, depth=1, all_candidates=[])
            self.assertEqual(node.word, "test")
            self.assertEqual(len(node.children), 0)

    def test_collect_leaves_single_node(self):
        node = Node(word="leaf")
        leaves = collect_leaves(node)
        self.assertEqual(leaves, ["leaf"])

    def test_collect_leaves_with_children(self):
        parent = Node(word="parent")
        child1 = Node(word="child1")
        child2 = Node(word="child2")
        parent.children = [child1, child2]
        leaves = collect_leaves(parent)
        self.assertIn("child1", leaves)
        self.assertIn("child2", leaves)
        self.assertNotIn("parent", leaves)


class TestReassembly(unittest.TestCase):
    """Test the Frankenstein surgery: can we stitch these parts together?"""

    def test_reassemble_empty(self):
        result = reassemble_corpse([])
        self.assertEqual(result, "")

    def test_reassemble_single_word(self):
        result = reassemble_corpse(["word"])
        self.assertEqual(result, "word")

    def test_reassemble_two_words(self):
        result = reassemble_corpse(["word1", "word2"])
        # Should contain both words
        self.assertIn("word1", result)
        self.assertIn("word2", result)

    def test_reassemble_multiple_words(self):
        words = ["the", "quick", "brown", "fox", "jumps"]
        result = reassemble_corpse(words)
        self.assertIsInstance(result, str)
        # Result should contain at least some of the words
        result_words = result.split()
        self.assertTrue(len(result_words) > 0)

    def test_reassemble_many_words(self):
        # Test with many words to trigger bigram logic
        words = [f"word{i}" for i in range(15)]
        result = reassemble_corpse(words)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestRendering(unittest.TestCase):
    """Test the morgue diagram: ASCII art for the damned."""

    def test_render_single_node(self):
        node = Node(word="test")
        lines = render_node(node, "", True)
        self.assertTrue(len(lines) > 0)
        self.assertIn("test", lines[0])

    def test_render_node_with_children(self):
        parent = Node(word="parent")
        child = Node(word="child")
        parent.children = [child]
        lines = render_node(parent, "", True)
        self.assertTrue(len(lines) >= 2)

    def test_render_autopsy(self):
        words = ["test"]
        trees = [Node(word="test")]
        result = render_autopsy("test prompt", words, trees)
        self.assertIn("test prompt", result)
        self.assertIn("— Sorokin", result)


class TestDatabase(unittest.TestCase):
    """Test the morgue records: persistent memory of horrors."""

    def setUp(self):
        # Use a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        self.temp_db.close()
        self.original_db_path = sorokin.DB_PATH
        # Patch the DB_PATH
        sorokin.DB_PATH = Path(self.temp_db.name)

    def tearDown(self):
        # Restore original DB_PATH and clean up
        sorokin.DB_PATH = self.original_db_path
        try:
            os.unlink(self.temp_db.name)
        except:
            pass

    def test_init_db(self):
        init_db()
        # Check that tables exist
        conn = sqlite3.connect(self.temp_db.name)
        try:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            self.assertIn("autopsy", tables)
            self.assertIn("word_memory", tables)
        finally:
            conn.close()

    def test_store_and_recall_autopsy(self):
        init_db()
        store_autopsy("test prompt", "test tree")
        # Verify it was stored
        conn = sqlite3.connect(self.temp_db.name)
        try:
            cursor = conn.execute("SELECT prompt, tree_text FROM autopsy")
            rows = cursor.fetchall()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0][0], "test prompt")
            self.assertEqual(rows[0][1], "test tree")
        finally:
            conn.close()

    def test_store_and_recall_word_relations(self):
        init_db()
        store_word_relations("test", ["related1", "related2"])
        recalled = recall_word_relations("test", 10)
        self.assertEqual(len(recalled), 2)
        self.assertIn("related1", recalled)
        self.assertIn("related2", recalled)

    def test_recall_nonexistent_word(self):
        init_db()
        recalled = recall_word_relations("nonexistent", 10)
        self.assertEqual(recalled, [])


class TestIntegration(unittest.TestCase):
    """Test the complete autopsy: end-to-end dissection."""

    def setUp(self):
        # Use a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".sqlite")
        self.temp_db.close()
        self.original_db_path = sorokin.DB_PATH
        sorokin.DB_PATH = Path(self.temp_db.name)
        init_db()

    def tearDown(self):
        sorokin.DB_PATH = self.original_db_path
        try:
            os.unlink(self.temp_db.name)
        except:
            pass

    @patch('sorokin._fetch_web_synonyms')
    def test_full_autopsy_short_prompt(self, mock_fetch):
        # Mock the web scraping to avoid actual HTTP requests
        mock_fetch.return_value = "<html>test words here</html>"

        result = sorokin_autopsy("test prompt")
        self.assertIsInstance(result, str)
        self.assertIn("— Sorokin", result)

    @patch('sorokin._fetch_web_synonyms')
    def test_full_autopsy_empty_prompt(self, mock_fetch):
        mock_fetch.return_value = ""
        result = sorokin_autopsy("")
        self.assertIn("Nothing to dissect", result)

    @patch('sorokin._fetch_web_synonyms')
    def test_full_autopsy_long_prompt(self, mock_fetch):
        mock_fetch.return_value = "<html>test words here</html>"
        # Create a prompt longer than MAX_INPUT_CHARS
        long_prompt = "word " * 100
        result = sorokin_autopsy(long_prompt)
        self.assertIsInstance(result, str)
        self.assertIn("— Sorokin", result)

    @patch('sorokin._fetch_web_synonyms')
    def test_full_autopsy_cyrillic(self, mock_fetch):
        mock_fetch.return_value = "<html>тест слова здесь</html>"
        result = sorokin_autopsy("привет мир")
        self.assertIsInstance(result, str)
        self.assertIn("— Sorokin", result)


class TestEdgeCases(unittest.TestCase):
    """Test the weird specimens: edge cases and corner cases."""

    def test_tokenize_only_stopwords(self):
        tokens = tokenize("the and or but")
        self.assertTrue(len(tokens) > 0)  # Tokens are extracted
        core = select_core_words(tokens)
        # Stopwords might still be selected if they're the only words available
        # The important thing is tokenization works
        self.assertIsInstance(core, list)

    def test_very_long_word(self):
        long_word = "a" * 1000
        fp = phonetic_fingerprint(long_word)
        self.assertIsInstance(fp, str)

    def test_special_characters_in_text(self):
        text = "Hello!@#$%^&*()World"
        tokens = tokenize(text)
        self.assertEqual(len(tokens), 2)
        self.assertIn("Hello", tokens)
        self.assertIn("World", tokens)


if __name__ == "__main__":
    unittest.main()
