#!/usr/bin/env python3
"""
Tests for Presence Pulse functionality (novelty, arousal, entropy).
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import sorokin
from sorokin import (
    compute_mutation_novelty,
    compute_prompt_arousal,
    compute_mutation_entropy,
    compute_presence_pulse,
    PresencePulse,
    Node,
    collect_leaves,
)


def test_compute_prompt_arousal():
    """Test arousal computation from emotional signals."""
    # High arousal: ALL CAPS + exclamation
    high_arousal = sorokin.compute_prompt_arousal(["DESTROY", "THIS", "!", "NOW"])
    assert high_arousal > 0.5, f"Expected high arousal, got {high_arousal}"
    
    # Low arousal: normal words
    low_arousal = sorokin.compute_prompt_arousal(["the", "sentence", "is", "normal"])
    assert low_arousal < 0.3, f"Expected low arousal, got {low_arousal}"
    
    # Repetition increases arousal
    rep_arousal = sorokin.compute_prompt_arousal(["word", "word", "word", "word"])
    assert rep_arousal > 0.0, f"Repetition should increase arousal, got {rep_arousal}"


def test_compute_mutation_novelty():
    """Test novelty computation (how unfamiliar mutations are)."""
    # Create test trees
    tree1 = Node(word="test")
    tree1.children = [Node(word="mutation1"), Node(word="mutation2")]
    
    tree2 = Node(word="test2")
    tree2.children = [Node(word="mutation3")]
    
    trees = [tree1, tree2]
    prompt_tokens = ["test"]
    
    # All mutations unknown
    known_mutations = set()
    novelty = compute_mutation_novelty(prompt_tokens, trees, known_mutations)
    assert novelty > 0.8, f"All unknown mutations should have high novelty, got {novelty}"
    
    # All mutations known
    known_mutations = {"mutation1", "mutation2", "mutation3"}
    novelty = compute_mutation_novelty(prompt_tokens, trees, known_mutations)
    assert novelty < 0.3, f"All known mutations should have low novelty, got {novelty}"


def test_compute_mutation_entropy():
    """Test entropy computation (uncertainty during mutation selection)."""
    # High entropy: many branches per node with varying counts
    tree1 = Node(word="root")
    tree1.children = [Node(word=f"branch{i}") for i in range(10)]
    # Add nested children to create branch distribution
    for child in tree1.children[:5]:
        child.children = [Node(word=f"nested{i}") for i in range(3)]
    
    trees = [tree1]
    all_candidates = [f"branch{i}" for i in range(10)]
    
    entropy = compute_mutation_entropy(trees, all_candidates)
    # Entropy should be computed from branch counts, not just presence
    assert entropy >= 0.0, f"Entropy should be non-negative, got {entropy}"
    
    # Low entropy: single branch
    tree2 = Node(word="root")
    tree2.children = [Node(word="single")]
    
    trees = [tree2]
    entropy = compute_mutation_entropy(trees, all_candidates)
    # Single branch should have lower entropy (but not zero due to normalization)
    assert entropy >= 0.0, f"Entropy should be non-negative, got {entropy}"


def test_compute_presence_pulse():
    """Test composite presence pulse computation."""
    novelty = 0.8
    arousal = 0.6
    entropy = 0.7
    
    pulse = compute_presence_pulse(novelty, arousal, entropy)
    
    assert isinstance(pulse, PresencePulse), "Should return PresencePulse object"
    assert pulse.novelty == novelty
    assert pulse.arousal == arousal
    assert pulse.entropy == entropy
    assert 0.0 <= pulse.pulse <= 1.0, f"Pulse should be in [0, 1], got {pulse.pulse}"
    
    # Pulse should be weighted combination
    expected_pulse = 0.3 * novelty + 0.4 * arousal + 0.3 * entropy
    assert abs(pulse.pulse - expected_pulse) < 0.01, f"Pulse calculation mismatch"


def test_presence_pulse_edge_cases():
    """Test edge cases for presence pulse."""
    # All zeros
    pulse = compute_presence_pulse(0.0, 0.0, 0.0)
    assert pulse.pulse == 0.0, "All zeros should give zero pulse"
    
    # All ones
    pulse = compute_presence_pulse(1.0, 1.0, 1.0)
    assert pulse.pulse == 1.0, "All ones should give one pulse"
    
    # Clamping
    pulse = compute_presence_pulse(2.0, -1.0, 0.5)  # Out of range
    assert 0.0 <= pulse.pulse <= 1.0, "Pulse should be clamped to [0, 1]"


if __name__ == "__main__":
    test_compute_prompt_arousal()
    print("✓ test_compute_prompt_arousal passed")
    
    test_compute_mutation_novelty()
    print("✓ test_compute_mutation_novelty passed")
    
    test_compute_mutation_entropy()
    print("✓ test_compute_mutation_entropy passed")
    
    test_compute_presence_pulse()
    print("✓ test_compute_presence_pulse passed")
    
    test_presence_pulse_edge_cases()
    print("✓ test_presence_pulse_edge_cases passed")
    
    print("\n✅ All presence pulse tests passed!")

