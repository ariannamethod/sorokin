#!/usr/bin/env python3
# vova.py — Sorokin Resonance Layer (adapted from SSuKA)
#
# "Fuck the sentence. Keep the corpse."
#
# Meta-cannibalism: README eats itself through resonance field.
# No weights. No gradients. Just accumulated centers of gravity.

from __future__ import annotations

import hashlib
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# PATHS
# ============================================================================

ROOT = Path(__file__).resolve().parent
README_PATH = ROOT / "README.md"
STATE_DIR = ROOT / ".vova" / "state"
BIN_DIR = ROOT / ".vova" / "bin"
BOOTSTRAP_PATH = STATE_DIR / "field.json"

# ============================================================================
# TOKENIZER
# ============================================================================

TOKEN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+|[.,!?;:—\-]")
MAX_INPUT_LENGTH = 10_000_000


def tokenize(text: str) -> List[str]:
    """Extract words and basic punctuation."""
    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError(f"Input too large: {len(text)} chars")
    return TOKEN_RE.findall(text)


# ============================================================================
# DATA STRUCTURES
# ============================================================================


@dataclass
class VovaField:
    """The resonance field built from README.md"""
    bigrams: Dict[str, Dict[str, int]]
    vocab: List[str]
    centers: List[str]
    readme_hash: str

    def to_json(self) -> dict:
        return {
            "bigrams": self.bigrams,
            "vocab": self.vocab,
            "centers": self.centers,
            "readme_hash": self.readme_hash,
        }

    @classmethod
    def from_json(cls, data: dict) -> "VovaField":
        return cls(
            bigrams={k: dict(v) for k, v in data.get("bigrams", {}).items()},
            vocab=list(data.get("vocab", [])),
            centers=list(data.get("centers", [])),
            readme_hash=data.get("readme_hash", ""),
        )


# ============================================================================
# BIGRAM EXTRACTION
# ============================================================================


def build_bigrams(tokens: List[str]) -> tuple[Dict[str, Dict[str, int]], List[str]]:
    """Build bigram graph and vocab from token stream."""
    bigrams: Dict[str, Dict[str, int]] = {}
    vocab_set = set()

    for i in range(len(tokens) - 1):
        a, b = tokens[i], tokens[i + 1]
        vocab_set.add(a)
        vocab_set.add(b)
        dst = bigrams.setdefault(a, {})
        dst[b] = dst.get(b, 0) + 1

    return bigrams, sorted(vocab_set)


def select_centers(bigrams: Dict[str, Dict[str, int]], k: int = 7) -> List[str]:
    """Pick tokens with highest out-degree as centers of gravity."""
    scored: List[tuple[str, int]] = []
    for tok, row in bigrams.items():
        scored.append((tok, sum(row.values())))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s for s, _ in scored[:k]]


# ============================================================================
# BIN SHARDS (accumulated resonance)
# ============================================================================


def sha256_bytes(data: bytes) -> str:
    """SHA256 hash."""
    return hashlib.sha256(data).hexdigest()


def create_bin_shard(field: VovaField, max_shards: int = 16) -> None:
    """
    Save center shard to .vova/bin/
    These are RESONANCE WEIGHTS — accumulated memory of README state.
    """
    BIN_DIR.mkdir(parents=True, exist_ok=True)
    if not field.centers:
        return

    payload = {
        "kind": "vova_center",
        "centers": field.centers,
        "readme_hash": field.readme_hash,
    }
    raw = json.dumps(payload, sort_keys=True).encode("utf-8")
    h = sha256_bytes(raw)[:16]
    shard_path = BIN_DIR / f"vova_{h}.bin"
    shard_path.write_bytes(raw)

    # Limit shards
    shards = sorted(BIN_DIR.glob("vova_*.bin"), key=lambda p: p.stat().st_mtime)
    while len(shards) > max_shards:
        victim = shards.pop(0)
        try:
            if victim.exists():
                victim.unlink()
        except OSError:
            pass


def load_bin_bias() -> Dict[str, int]:
    """
    Load all shards and count historical center frequency.
    This is ACCUMULATED RESONANCE — the field's memory.
    """
    if not BIN_DIR.exists():
        return {}
    bias: Dict[str, int] = {}
    for path in BIN_DIR.glob("vova_*.bin"):
        try:
            data = json.loads(path.read_bytes().decode("utf-8"))
        except Exception:
            continue
        if data.get("kind") != "vova_center":
            continue
        for tok in data.get("centers", []):
            bias[tok] = bias.get(tok, 0) + 1
    return bias


# ============================================================================
# FIELD BUILD/LOAD
# ============================================================================


def rebuild_field(force: bool = False) -> VovaField:
    """
    Build resonance field from README.md

    - Reads README.md
    - Builds bigrams + vocab
    - Selects centers (top-K by out-degree)
    - Blends in historical bias from .bin shards
    - Saves new shard
    """
    if not README_PATH.exists():
        raise FileNotFoundError(f"README.md not found at {README_PATH}")

    text = README_PATH.read_text(encoding="utf-8")
    readme_hash = sha256_bytes(text.encode("utf-8"))

    # Check if rebuild needed
    existing = load_field() if not force else None
    if existing and existing.readme_hash == readme_hash:
        return existing

    print(f"[VOVA] Building field from README.md ({len(text)} chars)")
    tokens = tokenize(text)
    bigrams, vocab = build_bigrams(tokens)
    print(f"[VOVA] Vocab: {len(vocab)} tokens")

    # Local centers
    centers = select_centers(bigrams, k=7) if bigrams else []

    # Blend historical bias
    bias = load_bin_bias()
    if bias:
        print(f"[VOVA] Blending {len(bias)} historical centers...")
        extra = sorted(bias.items(), key=lambda x: x[1], reverse=True)
        for tok, _score in extra:
            if tok not in centers:
                centers.append(tok)
            if len(centers) >= 10:
                break

    print(f"[VOVA] Centers of gravity: {centers}")

    field = VovaField(
        bigrams=bigrams,
        vocab=vocab,
        centers=centers,
        readme_hash=readme_hash,
    )

    # Save
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    BOOTSTRAP_PATH.write_text(
        json.dumps(field.to_json(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    create_bin_shard(field)
    print("[VOVA] Field ready.\n")
    return field


def load_field() -> Optional[VovaField]:
    """Load field from .vova/state/field.json"""
    if not BOOTSTRAP_PATH.exists():
        return None
    try:
        with BOOTSTRAP_PATH.open(encoding="utf-8") as f:
            data = json.load(f)
        return VovaField.from_json(data)
    except Exception:
        return None


def get_field(rebuild: bool = False) -> VovaField:
    """Get or build the global Vova field."""
    if rebuild:
        return rebuild_field(force=True)
    existing = load_field()
    if existing:
        return existing
    return rebuild_field()


# ============================================================================
# GENERATION (RESONANCE WALK)
# ============================================================================


def _safe_temperature(t: float) -> float:
    """Clamp temperature to [1e-3, 100.0]"""
    if not math.isfinite(t):
        return 1.0
    return max(min(t, 100.0), 1e-3)


def choose_start_token(field: VovaField, chaos: bool = False) -> str:
    """Pick starting token (from centers or vocab)."""
    pool = field.vocab if chaos else (field.centers or field.vocab)
    if not pool:
        return "corpse"  # fallback
    return random.choice(pool)


def step_token(field: VovaField, current: str, temperature: float = 1.0) -> str:
    """Walk one step in bigram graph."""
    row = field.bigrams.get(current)
    if not row:
        return choose_start_token(field, chaos=False)

    tokens = list(row.keys())
    counts = [row[t] for t in tokens]

    # Apply temperature
    t = _safe_temperature(temperature)
    if t != 1.0:
        counts = [math.pow(c, 1.0 / t) for c in counts]

    # Sample
    total = sum(counts)
    if total == 0:
        return random.choice(tokens)

    r = random.random() * total
    acc = 0.0
    for tok, cnt in zip(tokens, counts):
        acc += cnt
        if r <= acc:
            return tok
    return tokens[-1]


def warp(
    field: VovaField,
    seed: str,
    max_tokens: int = 40,
    temperature: float = 0.9,
    chaos: bool = False,
) -> str:
    """
    Warp text through README resonance field.

    Args:
        field: Vova field instance
        seed: Input text (can be empty for pure generation)
        max_tokens: Max output length (total, including seed)
        temperature: Sampling temp (lower = sharper)
        chaos: Ignore centers (full vocab sampling)

    Returns:
        Warped text: seed tokens MIXED with README resonance
    """
    # KEEP seed tokens as foundation
    seed_tokens = tokenize(seed) if seed else []
    output = seed_tokens.copy()  # Start with seed (preserve mutation tree words!)

    # Pick last seed word as starting point for README generation
    if seed_tokens and seed_tokens[-1] in field.vocab:
        current = seed_tokens[-1]
    else:
        current = choose_start_token(field, chaos=chaos)

    # Generate ADDITIONAL tokens from README (not replace!)
    additional_tokens = max(0, max_tokens - len(seed_tokens))
    for _ in range(additional_tokens):
        current = step_token(field, current, temperature=temperature)
        output.append(current)

    # Format
    result = []
    for i, tok in enumerate(output):
        if i == 0:
            result.append(tok.capitalize())
        elif tok in {".", ",", "!", "?", ";", ":"}:
            result[-1] = result[-1] + tok
        else:
            result.append(" " + tok)

    return "".join(result)


# ============================================================================
# PUBLIC API
# ============================================================================

_GLOBAL_FIELD: Optional[VovaField] = None


def warp_prompt(prompt: str, temperature: float = 0.8) -> str:
    """
    Warp user prompt through README field before autopsy.
    Pulls prompt toward README vocabulary centers.
    """
    global _GLOBAL_FIELD
    if _GLOBAL_FIELD is None:
        _GLOBAL_FIELD = get_field()
    return warp(_GLOBAL_FIELD, prompt, max_tokens=30, temperature=temperature)


def warp_autopsy(autopsy_text: str, temperature: float = 0.9) -> str:
    """
    Warp autopsy output through README field.
    Adds README resonance to reassembled corpse.
    """
    global _GLOBAL_FIELD
    if _GLOBAL_FIELD is None:
        _GLOBAL_FIELD = get_field()
    return warp(_GLOBAL_FIELD, autopsy_text, max_tokens=50, temperature=temperature)


def rebuild() -> None:
    """Force rebuild field from README.md"""
    global _GLOBAL_FIELD
    _GLOBAL_FIELD = rebuild_field(force=True)


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--rebuild":
            rebuild()
        else:
            field = get_field()
            text = " ".join(sys.argv[1:])
            print(warp(field, text))
    else:
        field = get_field()
        print(f"Vova field: {len(field.vocab)} tokens, {len(field.centers)} centers")
        print(f"Centers: {field.centers}")
