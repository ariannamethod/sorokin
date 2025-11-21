#!/usr/bin/env python3
"""
gowiththeflow.py — mutation patterns flowing through time

"Go with the flow" — evolutionary tracking of mutation constellations.

Core idea:
- Mutation patterns aren't static — they flow, grow, fade, merge
- Record theme state after each autopsy → build archaeological record
- Detect emerging mutations (↗), fading mutations (↘), persistent mutations (→)
- Track autopsy phases as mutations flow through time

This is memory archaeology: watching mutation currents shift and eddy.
Not training data — just temporal awareness of the flow.
"""

from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional

# DB_PATH defined here to avoid circular import
DB_PATH = Path("sorokin.sqlite")


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class ThemeSnapshot:
    """
    Snapshot of a theme at a specific moment in the flow.
    
    Captures:
    - When the theme was active
    - How strongly it flowed
    - Which words belonged to it at that moment
    - How many times it appeared in autopsies
    """
    timestamp: float
    theme_id: int
    strength: float  # activation score
    active_words: Set[str]
    activation_count: int  # cumulative count across autopsies


@dataclass
class ThemeTrajectory:
    """
    Evolution of a single theme as it flows through time.
    
    Contains:
    - Full history of snapshots
    - Computed slope (growing/fading)
    - Current state
    """
    theme_id: int
    snapshots: List[ThemeSnapshot]
    
    def slope(self, hours: float = 6.0) -> float:
        """
        Compute flow trajectory over last N hours.
        
        Positive slope → emerging theme (↗ growing)
        Negative slope → fading theme (↘ dying)
        Zero slope → stable theme (→ persistent)
        
        Uses simple linear regression over strength values.
        
        Args:
            hours: Time window to compute slope (default: 6 hours)
        
        Returns:
            Slope value: positive = growing, negative = fading, ~0 = stable
        """
        if len(self.snapshots) < 2:
            return 0.0
        
        now = time.time()
        cutoff = now - (hours * 3600)
        
        # Filter recent snapshots
        recent = [s for s in self.snapshots if s.timestamp >= cutoff]
        
        if len(recent) < 2:
            return 0.0
        
        # Simple linear regression: slope = cov(x,y) / var(x)
        # x = time offset from first snapshot
        # y = strength
        times = [s.timestamp - recent[0].timestamp for s in recent]
        strengths = [s.strength for s in recent]
        
        n = len(times)
        mean_t = sum(times) / n
        mean_s = sum(strengths) / n
        
        # Covariance and variance
        cov = sum((t - mean_t) * (s - mean_s) for t, s in zip(times, strengths))
        var = sum((t - mean_t) ** 2 for t in times)
        
        if var == 0.0:
            return 0.0
        
        return cov / var
    
    def current_strength(self) -> float:
        """Get most recent strength value."""
        if not self.snapshots:
            return 0.0
        return self.snapshots[-1].strength


# ============================================================================
# FLOW TRACKING
# ============================================================================


def snapshot_theme(
    conn: sqlite3.Connection,
    theme_id: int,
    active_words: Set[str],
    strength: float,
    timestamp: Optional[float] = None
) -> None:
    """
    Record a theme snapshot at current moment.
    
    Args:
        conn: Database connection
        theme_id: Unique theme identifier
        active_words: Words active in this theme
        strength: Activation strength (0-1)
        timestamp: Optional timestamp (defaults to now)
    """
    if timestamp is None:
        timestamp = time.time()
    
    # Get current activation count
    last_snapshot = conn.execute(
        "SELECT activation_count FROM theme_snapshots "
        "WHERE theme_id = ? ORDER BY timestamp DESC LIMIT 1",
        (theme_id,)
    ).fetchone()
    
    activation_count = (last_snapshot[0] + 1) if last_snapshot else 1
    
    # Insert snapshot
    words_str = ",".join(sorted(active_words))
    conn.execute(
        """
        INSERT INTO theme_snapshots 
        (timestamp, theme_id, strength, activation_count, words)
        VALUES (?, ?, ?, ?, ?)
        """,
        (timestamp, theme_id, strength, activation_count, words_str)
    )
    conn.commit()


def load_theme_trajectories(
    conn: sqlite3.Connection,
    hours: float = 24.0
) -> Dict[int, ThemeTrajectory]:
    """
    Load theme trajectories from database.
    
    Args:
        conn: Database connection
        hours: Time window to load (default: 24 hours)
    
    Returns:
        Dict mapping theme_id -> ThemeTrajectory
    """
    cutoff = time.time() - (hours * 3600)
    
    rows = conn.execute(
        """
        SELECT timestamp, theme_id, strength, activation_count, words
        FROM theme_snapshots
        WHERE timestamp >= ?
        ORDER BY theme_id, timestamp
        """,
        (cutoff,)
    ).fetchall()
    
    trajectories: Dict[int, ThemeTrajectory] = {}
    
    for timestamp, theme_id, strength, activation_count, words_str in rows:
        active_words = set(words_str.split(",")) if words_str else set()
        
        snapshot = ThemeSnapshot(
            timestamp=timestamp,
            theme_id=theme_id,
            strength=strength,
            active_words=active_words,
            activation_count=activation_count
        )
        
        if theme_id not in trajectories:
            trajectories[theme_id] = ThemeTrajectory(
                theme_id=theme_id,
                snapshots=[]
            )
        
        trajectories[theme_id].snapshots.append(snapshot)
    
    return trajectories


def analyze_flow(
    conn: sqlite3.Connection,
    hours: float = 6.0
) -> Dict[str, List[ThemeTrajectory]]:
    """
    Analyze theme flow: which themes are emerging, fading, stable?
    
    Args:
        conn: Database connection
        hours: Time window for slope computation
    
    Returns:
        Dict with keys: 'emerging', 'fading', 'stable'
        Each value is list of ThemeTrajectory objects
    """
    trajectories = load_theme_trajectories(conn, hours=hours * 2)
    
    emerging: List[ThemeTrajectory] = []
    fading: List[ThemeTrajectory] = []
    stable: List[ThemeTrajectory] = []
    
    slope_threshold = 0.01  # Minimum slope to be considered growing/fading
    
    for traj in trajectories.values():
        slope = traj.slope(hours=hours)
        
        if slope > slope_threshold:
            emerging.append(traj)
        elif slope < -slope_threshold:
            fading.append(traj)
        else:
            stable.append(traj)
    
    # Sort by current strength (strongest first)
    emerging.sort(key=lambda t: t.current_strength(), reverse=True)
    fading.sort(key=lambda t: t.current_strength(), reverse=True)
    stable.sort(key=lambda t: t.current_strength(), reverse=True)
    
    return {
        'emerging': emerging,
        'fading': fading,
        'stable': stable
    }


def get_active_themes(
    words: List[str],
    themes: List[Set[str]]
) -> List[Set[str]]:
    """
    Find which themes are activated by given words.
    
    Returns: List of active theme sets
    """
    word_set = {w.lower() for w in words}
    active = []
    
    for theme in themes:
        if word_set & theme:  # Intersection exists
            active.append(theme)
    
    return active


def track_autopsy_themes(
    conn: sqlite3.Connection,
    words: List[str],
    themes: List[Set[str]],
    co_occur: Dict[str, Dict[str, int]]
) -> None:
    """
    Track which themes were active during an autopsy.
    
    Args:
        conn: Database connection
        words: Words from autopsy (leaves)
        themes: List of theme sets (from cluster_themes)
        co_occur: Co-occurrence matrix (for computing theme strength)
    """
    active_themes = get_active_themes(words, themes)
    
    for theme in active_themes:
        # Compute theme strength: average co-occurrence density
        theme_words = list(theme)
        if not theme_words:
            continue
        
        # Strength = average co-occurrence count within theme
        total_co_occur = 0.0
        pairs = 0
        
        for word1 in theme_words:
            for word2 in theme_words:
                if word1 == word2:
                    continue
                ctx = co_occur.get(word1, {})
                count = ctx.get(word2, 0)
                total_co_occur += count
                pairs += 1
        
        strength = total_co_occur / pairs if pairs > 0 else 0.0
        # Normalize to [0, 1] range (assuming max co-occurrence ~100)
        strength = min(1.0, strength / 100.0)
        
        # Use hash of theme words as theme_id
        theme_id = hash(frozenset(theme)) % (2 ** 31)  # Positive int
        
        snapshot_theme(
            conn,
            theme_id=theme_id,
            active_words=theme,
            strength=strength
        )

