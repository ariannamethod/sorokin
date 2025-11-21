#!/usr/bin/env python3
"""
Tests for flow tracking functionality (gowiththeflow.py).
"""

import sys
import sqlite3
import tempfile
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import gowiththeflow
from gowiththeflow import (
    ThemeSnapshot,
    ThemeTrajectory,
    snapshot_theme,
    load_theme_trajectories,
    analyze_flow,
    get_active_themes,
    track_autopsy_themes,
)


def test_theme_snapshot():
    """Test ThemeSnapshot creation."""
    snapshot = ThemeSnapshot(
        timestamp=time.time(),
        theme_id=1,
        strength=0.7,
        active_words={"destroy", "the", "sentence"},
        activation_count=5
    )
    
    assert snapshot.strength == 0.7
    assert len(snapshot.active_words) == 3
    assert snapshot.activation_count == 5


def test_theme_trajectory_slope():
    """Test trajectory slope computation."""
    now = time.time()
    snapshots = [
        ThemeSnapshot(now - 3600, 1, 0.3, set(), 1),
        ThemeSnapshot(now - 1800, 1, 0.5, set(), 2),
        ThemeSnapshot(now, 1, 0.7, set(), 3),
    ]
    
    traj = ThemeTrajectory(theme_id=1, snapshots=snapshots)
    slope = traj.slope(hours=2.0)
    
    assert slope > 0, "Growing theme should have positive slope"
    
    # Fading theme
    snapshots_fading = [
        ThemeSnapshot(now - 3600, 2, 0.7, set(), 1),
        ThemeSnapshot(now - 1800, 2, 0.5, set(), 2),
        ThemeSnapshot(now, 2, 0.3, set(), 3),
    ]
    
    traj_fading = ThemeTrajectory(theme_id=2, snapshots=snapshots_fading)
    slope_fading = traj_fading.slope(hours=2.0)
    
    assert slope_fading < 0, "Fading theme should have negative slope"


def test_snapshot_theme():
    """Test theme snapshot recording."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS theme_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                theme_id INTEGER NOT NULL,
                strength REAL NOT NULL,
                activation_count INTEGER NOT NULL,
                words TEXT NOT NULL
            )
        """)
        conn.commit()
        
        # Record snapshot
        active_words = {"destroy", "the", "sentence"}
        snapshot_theme(conn, theme_id=1, active_words=active_words, strength=0.7)
        
        # Check it was recorded
        rows = conn.execute(
            "SELECT theme_id, strength, words FROM theme_snapshots"
        ).fetchall()
        
        assert len(rows) == 1, "Should have one snapshot"
        assert rows[0][0] == 1, "Theme ID should match"
        assert rows[0][1] == 0.7, "Strength should match"
        
        # Check activation count increments
        snapshot_theme(conn, theme_id=1, active_words=active_words, strength=0.8)
        rows = conn.execute(
            "SELECT activation_count FROM theme_snapshots WHERE theme_id = 1 ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        
        assert rows[0] == 2, "Activation count should increment"
        
    finally:
        conn.close()
        Path(db_path).unlink()


def test_analyze_flow():
    """Test flow analysis (emerging/fading/stable)."""
    with tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False) as f:
        db_path = f.name
    
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS theme_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                theme_id INTEGER NOT NULL,
                strength REAL NOT NULL,
                activation_count INTEGER NOT NULL,
                words TEXT NOT NULL
            )
        """)
        conn.commit()
        
        now = time.time()
        
        # Emerging theme (growing strength)
        for i, strength in enumerate([0.2, 0.4, 0.6, 0.8]):
            snapshot_theme(
                conn,
                theme_id=1,
                active_words={"emerging"},
                strength=strength,
                timestamp=now - (3 - i) * 1800
            )
        
        # Fading theme (decreasing strength)
        for i, strength in enumerate([0.8, 0.6, 0.4, 0.2]):
            snapshot_theme(
                conn,
                theme_id=2,
                active_words={"fading"},
                strength=strength,
                timestamp=now - (3 - i) * 1800
            )
        
        # Analyze flow
        flow = analyze_flow(conn, hours=6.0)
        
        assert len(flow['emerging']) > 0, "Should find emerging themes"
        assert len(flow['fading']) > 0, "Should find fading themes"
        
        # Check that themes are correctly classified
        emerging_ids = {t.theme_id for t in flow['emerging']}
        fading_ids = {t.theme_id for t in flow['fading']}
        
        assert 1 in emerging_ids, "Theme 1 should be emerging"
        assert 2 in fading_ids, "Theme 2 should be fading"
        
    finally:
        conn.close()
        Path(db_path).unlink()


def test_get_active_themes():
    """Test get_active_themes function."""
    themes = [
        {"destroy", "the", "sentence"},
        {"love", "poetry", "sonnet"},
    ]
    
    words = ["destroy", "sentence"]
    active = get_active_themes(words, themes)
    
    assert len(active) >= 1, "Should find active themes"
    assert any("destroy" in theme for theme in active), "First theme should be active"


if __name__ == "__main__":
    test_theme_snapshot()
    print("✓ test_theme_snapshot passed")
    
    test_theme_trajectory_slope()
    print("✓ test_theme_trajectory_slope passed")
    
    test_snapshot_theme()
    print("✓ test_snapshot_theme passed")
    
    test_analyze_flow()
    print("✓ test_analyze_flow passed")
    
    test_get_active_themes()
    print("✓ test_get_active_themes passed")
    
    print("\n✅ All flow tracking tests passed!")

