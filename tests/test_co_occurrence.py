#!/usr/bin/env python3
"""
Tests for co-occurrence matrix functionality.
"""

import sys
import sqlite3
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sorokin
from sorokin import ingest_co_occurrence, load_co_occurrence


def test_ingest_co_occurrence():
    """Test co-occurrence ingestion."""
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS co_occurrence (
                word_id TEXT NOT NULL,
                context_id TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                PRIMARY KEY (word_id, context_id)
            )
        """)
        conn.commit()
        
        # Ingest tokens
        tokens = ["destroy", "the", "sentence", "destroy", "the", "word"]
        ingest_co_occurrence(conn, tokens, window_size=3)
        
        # Check that co-occurrence was recorded
        rows = conn.execute(
            "SELECT word_id, context_id, count FROM co_occurrence"
        ).fetchall()
        
        assert len(rows) > 0, "Co-occurrence should be recorded"
        
        # Check specific pairs
        destroy_the = conn.execute(
            "SELECT count FROM co_occurrence WHERE word_id = ? AND context_id = ?",
            ("destroy", "the")
        ).fetchone()
        
        assert destroy_the is not None, "destroy-the pair should exist"
        assert destroy_the[0] >= 1, "Count should be at least 1"
        
    finally:
        conn.close()
        Path(db_path).unlink()


def test_load_co_occurrence():
    """Test co-occurrence loading."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS co_occurrence (
                word_id TEXT NOT NULL,
                context_id TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                PRIMARY KEY (word_id, context_id)
            )
        """)
        
        # Insert test data
        conn.execute(
            "INSERT INTO co_occurrence (word_id, context_id, count) VALUES (?, ?, ?)",
            ("destroy", "the", 5)
        )
        conn.execute(
            "INSERT INTO co_occurrence (word_id, context_id, count) VALUES (?, ?, ?)",
            ("the", "sentence", 3)
        )
        conn.commit()
        
        # Load co-occurrence
        co_occur = load_co_occurrence(conn)
        
        assert "destroy" in co_occur, "destroy should be in co-occurrence"
        assert co_occur["destroy"]["the"] == 5, "destroy-the count should be 5"
        assert co_occur["the"]["sentence"] == 3, "the-sentence count should be 3"
        
    finally:
        conn.close()
        Path(db_path).unlink()


def test_co_occurrence_window():
    """Test that co-occurrence respects window size."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS co_occurrence (
                word_id TEXT NOT NULL,
                context_id TEXT NOT NULL,
                count INTEGER DEFAULT 1,
                PRIMARY KEY (word_id, context_id)
            )
        """)
        conn.commit()
        
        # Long sequence with small window
        tokens = ["a", "b", "c", "d", "e", "f", "g", "h"]
        ingest_co_occurrence(conn, tokens, window_size=2)
        
        # 'a' should co-occur with 'b', 'c' but not 'h'
        rows = conn.execute(
            "SELECT context_id FROM co_occurrence WHERE word_id = ?",
            ("a",)
        ).fetchall()
        
        contexts = {row[0] for row in rows}
        assert "b" in contexts, "a should co-occur with b"
        assert "c" in contexts, "a should co-occur with c"
        assert "h" not in contexts, "a should NOT co-occur with h (too far)"
        
    finally:
        conn.close()
        Path(db_path).unlink()


if __name__ == "__main__":
    test_ingest_co_occurrence()
    print("✓ test_ingest_co_occurrence passed")
    
    test_load_co_occurrence()
    print("✓ test_load_co_occurrence passed")
    
    test_co_occurrence_window()
    print("✓ test_co_occurrence_window passed")
    
    print("\n✅ All co-occurrence tests passed!")

