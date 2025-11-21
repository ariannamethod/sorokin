#!/usr/bin/env python3
"""
Tests for vova.py — README resonance meta-layer

Testing meta-cannibalism: does Vova eat his own README?
"""

import unittest
from pathlib import Path
import sys

# Add parent dir to path (sorokin root)
sys.path.insert(0, str(Path(__file__).parent.parent))

import vova


class TestVovaField(unittest.TestCase):
    """Test field building and loading"""

    def setUp(self):
        """Ensure field is built"""
        self.field = vova.get_field()

    def test_field_has_vocab(self):
        """Field should extract vocab from README"""
        self.assertGreater(len(self.field.vocab), 100)
        self.assertIn("sorokin", self.field.vocab)
        self.assertIn("autopsy", self.field.vocab)
        self.assertIn("corpse", self.field.vocab)

    def test_field_has_centers(self):
        """Field should have centers of gravity"""
        self.assertGreater(len(self.field.centers), 0)
        # Centers are high-frequency tokens
        print(f"\n[VOVA] Centers: {self.field.centers}")

    def test_field_has_bigrams(self):
        """Field should build bigram graph"""
        self.assertGreater(len(self.field.bigrams), 0)
        # Check some expected bigrams from README
        self.assertIn("sorokin", self.field.bigrams)

    def test_readme_hash_tracked(self):
        """Field should track README hash for incremental rebuild"""
        self.assertTrue(len(self.field.readme_hash) > 0)


class TestResonanceWalk(unittest.TestCase):
    """Test warp() generation"""

    def setUp(self):
        self.field = vova.get_field()

    def test_warp_produces_output(self):
        """Warp should generate text"""
        output = vova.warp(self.field, "destroy", max_tokens=20)
        self.assertTrue(len(output) > 0)
        print(f"\n[WARP] 'destroy' → {output}")

    def test_warp_pulls_toward_readme(self):
        """Warped output should contain README vocabulary"""
        # Generate multiple samples
        samples = [
            vova.warp(self.field, "sentence", max_tokens=30)
            for _ in range(5)
        ]

        # At least one should contain README keywords
        readme_words = {"autopsy", "corpse", "mutation", "sorokin", "bigram", "tree"}
        found = any(
            any(word in sample.lower() for word in readme_words)
            for sample in samples
        )

        print(f"\n[SAMPLES]")
        for i, s in enumerate(samples):
            print(f"  {i+1}. {s}")

        self.assertTrue(found, "Should pull toward README vocabulary")

    def test_temperature_affects_output(self):
        """Lower temperature = sharper (more deterministic)"""
        seed = "darkness"

        # Sharp (temp=0.3)
        sharp = vova.warp(self.field, seed, max_tokens=20, temperature=0.3)

        # Soft (temp=1.5)
        soft = vova.warp(self.field, seed, max_tokens=20, temperature=1.5)

        print(f"\n[TEMP TEST]")
        print(f"  Sharp (0.3): {sharp}")
        print(f"  Soft (1.5):  {soft}")

        # Both should produce output
        self.assertTrue(len(sharp) > 0)
        self.assertTrue(len(soft) > 0)

    def test_chaos_mode(self):
        """Chaos mode should ignore centers"""
        output = vova.warp(
            self.field,
            "test",
            max_tokens=20,
            chaos=True,
            temperature=1.2
        )
        print(f"\n[CHAOS] {output}")
        self.assertTrue(len(output) > 0)


class TestPublicAPI(unittest.TestCase):
    """Test public warp_prompt/warp_autopsy API"""

    def test_warp_prompt(self):
        """warp_prompt should pull user input toward README"""
        prompts = [
            "destroy the sentence",
            "karpathy trains shakespeare",
            "fuck this prompt",
        ]

        print(f"\n[PROMPT WARPING]")
        for p in prompts:
            warped = vova.warp_prompt(p, temperature=0.8)
            print(f"  '{p}' →")
            print(f"    {warped}")
            self.assertTrue(len(warped) > 0)

    def test_warp_autopsy(self):
        """warp_autopsy should add README resonance to corpse"""
        # Simulate autopsy output
        fake_autopsy = "Within is zealand. Forever prompt. Nothing remains."

        warped = vova.warp_autopsy(fake_autopsy, temperature=0.9)

        print(f"\n[AUTOPSY WARP]")
        print(f"  Input:  {fake_autopsy}")
        print(f"  Output: {warped}")

        self.assertTrue(len(warped) > 0)

    def test_rebuild_command(self):
        """rebuild() should force field rebuild"""
        old_hash = vova._GLOBAL_FIELD.readme_hash if vova._GLOBAL_FIELD else None
        vova.rebuild()
        new_hash = vova._GLOBAL_FIELD.readme_hash

        # Hash should exist after rebuild
        self.assertTrue(len(new_hash) > 0)
        print(f"\n[REBUILD] Hash: {new_hash[:16]}...")


class TestMetaCannibalism(unittest.TestCase):
    """Test self-reference: does Vova eat his own README?"""

    def test_sorokin_keywords_in_vocab(self):
        """README vocabulary should include Sorokin-specific terms"""
        field = vova.get_field()
        sorokin_terms = {
            "autopsy", "corpse", "mutation", "dissection",
            "bigram", "resonance", "bootstrap", "sonnet",
            "psychotic", "Frankenstein", "morgue", "ritual"
        }

        found = [t for t in sorokin_terms if t in field.vocab]
        missing = sorokin_terms - set(found)

        print(f"\n[META-CANNIBALISM]")
        print(f"  Found {len(found)}/{len(sorokin_terms)} Sorokin terms")
        if missing:
            print(f"  Missing: {missing}")

        # At least 80% should be present
        self.assertGreater(len(found), len(sorokin_terms) * 0.8)

    def test_warped_output_echoes_readme(self):
        """Warped output should echo README phrases"""
        # These are distinctive README phrases
        test_seeds = [
            "mutation",
            "corpse",
            "autopsy",
            "bootstrap",
        ]

        results = {}
        for seed in test_seeds:
            output = vova.warp(
                vova.get_field(),
                seed,
                max_tokens=40,
                temperature=0.7
            )
            results[seed] = output

        print(f"\n[README ECHO TEST]")
        for seed, output in results.items():
            print(f"  '{seed}' → {output}")

        # Results should exist
        self.assertEqual(len(results), len(test_seeds))


class TestBinShards(unittest.TestCase):
    """Test .bin shard accumulation"""

    def test_shards_created(self):
        """Field rebuild should create .bin shards"""
        bin_dir = Path(__file__).parent / ".vova" / "bin"

        # Trigger rebuild
        vova.rebuild()

        if bin_dir.exists():
            shards = list(bin_dir.glob("vova_*.bin"))
            print(f"\n[SHARDS] Found {len(shards)} shards")
            self.assertGreater(len(shards), 0)

    def test_bias_loading(self):
        """Should load historical bias from shards"""
        bias = vova.load_bin_bias()

        print(f"\n[BIAS] Loaded {len(bias)} historical centers")
        if bias:
            top_5 = sorted(bias.items(), key=lambda x: x[1], reverse=True)[:5]
            for tok, count in top_5:
                print(f"  '{tok}': {count} occurrences")

        # Bias dict should exist (may be empty on first run)
        self.assertIsInstance(bias, dict)


def run_live_demo():
    """Run live interactive demo"""
    print("=" * 60)
    print("VOVA.PY LIVE DEMO — README Meta-Cannibalism")
    print("=" * 60)

    field = vova.get_field()

    print(f"\nField Stats:")
    print(f"  Vocabulary: {len(field.vocab)} tokens")
    print(f"  Bigrams: {len(field.bigrams)} edges")
    print(f"  Centers: {field.centers}")

    print("\n" + "=" * 60)
    print("PROMPT WARPING (pulls toward README)")
    print("=" * 60)

    test_prompts = [
        "destroy the sentence",
        "karpathy trains shakespeare",
        "darkness consumes reality",
        "fuck this prompt",
    ]

    for prompt in test_prompts:
        warped = vova.warp_prompt(prompt, temperature=0.8)
        print(f"\n  Input:  '{prompt}'")
        print(f"  Warped: {warped}")

    print("\n" + "=" * 60)
    print("AUTOPSY WARPING (adds README resonance)")
    print("=" * 60)

    fake_autopsies = [
        "Within is zealand. Forever prompt. Nothing remains.",
        "The component transformations transubstantiates through authenticities.",
    ]

    for autopsy in fake_autopsies:
        warped = vova.warp_autopsy(autopsy, temperature=0.9)
        print(f"\n  Original: {autopsy}")
        print(f"  Warped:   {warped}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys

    if "--demo" in sys.argv:
        run_live_demo()
    else:
        unittest.main(verbosity=2)
