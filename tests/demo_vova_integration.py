#!/usr/bin/env python3
"""
Demo: How vova.py affects the entire Sorokin pipeline

Shows side-by-side comparison:
1. Normal autopsy → sonnet
2. Vova-warped autopsy → sonnet
"""

import sys
import asyncio
from pathlib import Path

# Add sorokin root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import vova

# Try importing sorokin modules (may not exist yet, just demo)
try:
    from sorokin import sorokin_autopsy, select_core_words
    from sonnet import compose_sonnet
    SOROKIN_AVAILABLE = True
except ImportError:
    SOROKIN_AVAILABLE = False
    print("[WARNING] sorokin.py/sonnet.py not importable")


async def demo_full_pipeline():
    """
    Full pipeline demo:
    User prompt → [optional vova warp] → autopsy → [optional vova warp] → sonnet
    """

    print("=" * 70)
    print("VOVA INTEGRATION DEMO — Full Pipeline Comparison")
    print("=" * 70)

    test_prompts = [
        "karpathy trains shakespeare on nanogpt",
        "destroy the sentence",
        "darkness consumes reality",
    ]

    if not SOROKIN_AVAILABLE:
        print("\n[MOCK MODE] sorokin.py not available, showing vova warping only")
        for prompt in test_prompts:
            print(f"\n{'='*70}")
            print(f"PROMPT: '{prompt}'")
            print(f"{'='*70}")

            # Warp prompt
            warped_prompt = vova.warp_prompt(prompt, temperature=0.8)
            print(f"\n1. WARPED PROMPT:")
            print(f"   {warped_prompt}")

            # Mock autopsy
            mock_autopsy = f"Mock autopsy of: {prompt}"
            warped_autopsy = vova.warp_autopsy(mock_autopsy, temperature=0.9)

            print(f"\n2. ORIGINAL AUTOPSY (mock):")
            print(f"   {mock_autopsy}")

            print(f"\n3. WARPED AUTOPSY:")
            print(f"   {warped_autopsy}")

        return

    # Real pipeline (if sorokin available)
    for prompt in test_prompts:
        print(f"\n{'='*70}")
        print(f"PROMPT: '{prompt}'")
        print(f"{'='*70}")

        # Path A: Normal pipeline
        print(f"\n>>> PATH A: NORMAL (no vova)")
        autopsy_normal = await sorokin_autopsy(prompt, width=3, depth=2)
        print(f"  Autopsy: {autopsy_normal['reassembled_text'][:100]}...")

        try:
            sonnet_normal = await compose_sonnet(
                autopsy_text=autopsy_normal['reassembled_text'],
                temperature=0.9
            )
            print(f"  Sonnet title: {sonnet_normal['title']}")
            print(f"  First line: {sonnet_normal['lines'][0]}")
        except Exception as e:
            print(f"  Sonnet failed: {e}")

        # Path B: Vova-warped pipeline
        print(f"\n>>> PATH B: VOVA-WARPED")

        # Warp input prompt
        warped_prompt = vova.warp_prompt(prompt, temperature=0.8)
        print(f"  Warped prompt: {warped_prompt[:80]}...")

        # Autopsy on warped prompt
        autopsy_warped = await sorokin_autopsy(warped_prompt, width=3, depth=2)

        # Warp autopsy output again
        double_warped = vova.warp_autopsy(
            autopsy_warped['reassembled_text'],
            temperature=0.9
        )
        print(f"  Double-warped: {double_warped[:100]}...")

        try:
            sonnet_warped = await compose_sonnet(
                autopsy_text=double_warped,
                temperature=0.9
            )
            print(f"  Sonnet title: {sonnet_warped['title']}")
            print(f"  First line: {sonnet_warped['lines'][0]}")
        except Exception as e:
            print(f"  Sonnet failed: {e}")


def demo_warp_chain():
    """Show how vova creates chains of resonance"""
    print("\n" + "=" * 70)
    print("RESONANCE CHAIN DEMO")
    print("=" * 70)

    seed = "destroy"
    print(f"\nSeed: '{seed}'")

    field = vova.get_field()

    print("\n[Warping 5 times in sequence - watch the drift]")
    current = seed
    for i in range(5):
        warped = vova.warp(field, current, max_tokens=25, temperature=0.85)
        print(f"\n  Round {i+1}: {warped}")
        # Use output as next seed
        current = warped.split()[-1] if warped.split() else seed


def demo_temperature_sweep():
    """Show how temperature affects README pull"""
    print("\n" + "=" * 70)
    print("TEMPERATURE SWEEP — How sharp is the README pull?")
    print("=" * 70)

    seed = "karpathy trains shakespeare"
    field = vova.get_field()

    temps = [0.3, 0.7, 1.0, 1.5, 2.0]

    print(f"\nSeed: '{seed}'")
    for temp in temps:
        output = vova.warp(field, seed, max_tokens=30, temperature=temp)
        print(f"\n  temp={temp:.1f}: {output}")


if __name__ == "__main__":
    print("\n🎭 VOVA DEMONSTRATION 🎭\n")

    # Run demos
    demo_warp_chain()
    demo_temperature_sweep()

    # Try full pipeline
    if "--full" in sys.argv:
        asyncio.run(demo_full_pipeline())
    else:
        print("\n" + "=" * 70)
        print("Run with --full to test full sorokin→vova→sonnet pipeline")
        print("(requires sorokin.py and sonnet.py to be importable)")
        print("=" * 70)
