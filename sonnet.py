#!/usr/bin/env python3
# sonnet.py — or ASS: Autopsy Sonnet SymphonY
#
# Async-friendly helper that turns Sorokin's autopsy output
# + SQLite morgue into a Shakespeare-style nonsense sonnet.
#
# Public API:
#   async compose_sonnet(autopsy_text: str, db_path: Union[str, Path]) -> str
#   compose_sonnet_sync(...) -> str
#
# Design goals:
#   - never talk to the web
#   - use only autopsy text + SQLite + seed corpus
#   - keep shape strict, content deranged
#
# Dedicated to Vladimir Sorokin, William Shakespeare, and Andrej Karpathy.

from __future__ import annotations

import asyncio
import random
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ']+")

# 14-line Shakespearean sonnet rhyme scheme
RHYME_SCHEME: Sequence[str] = list("ABABCDCDEFEFGG")

# Reasonable defaults for line length (in words)
MIN_LINE_WORDS = 7
MAX_LINE_WORDS = 11

# Max items we ever pull from SQLite to keep things light
MAX_VOCAB_FROM_DB = 256
MAX_BIGRAMS_FROM_DB = 1024


# ---------- Public async API ----------


async def compose_sonnet(
    autopsy_text: str,
    db_path: Optional[Path | str] = None,
    seed_corpus: Optional[str] = None,
    *,
    safe: bool = True,
    rng: Optional[random.Random] = None,
) -> str:
    """
    High-level async entrypoint.

    - Runs sync implementation in a thread so it doesn't block Sorokin's event loop.
    - Returns "" on any error if safe=True (recommended for main sorokin.py).
    """
    if rng is None:
        # tiny bit of entropy from hash of text, so same prompt is roughly stable
        rng = random.Random(hash(autopsy_text) & 0xFFFFFFFF)

    try:
        return await asyncio.to_thread(
            _compose_sonnet_impl, autopsy_text, db_path, seed_corpus, rng
        )
    except Exception:
        if safe:
            return ""
        raise


def compose_sonnet_sync(
    autopsy_text: str,
    db_path: Optional[Path | str] = None,
    seed_corpus: Optional[str] = None,
    *,
    rng: Optional[random.Random] = None,
) -> str:
    """
    Synchronous helper for debugging / REPL.
    """
    if rng is None:
        rng = random.Random(hash(autopsy_text) & 0xFFFFFFFF)
    return _compose_sonnet_impl(autopsy_text, db_path, seed_corpus, rng)


# ---------- Core implementation ----------


def _compose_sonnet_impl(
    autopsy_text: str,
    db_path: Optional[Path | str],
    seed_corpus: Optional[str],
    rng: random.Random,
) -> str:
    # 1. Tokenize autopsy text
    autopsy_tokens = _tokenize(autopsy_text)
    if not autopsy_tokens:
        return ""

    # 2. Build vocabulary pool (autopsy + sqlite + seed corpus)
    vocab: List[str] = []
    vocab.extend(autopsy_tokens)

    bigrams: Dict[str, List[str]] = defaultdict(list)

    if db_path is not None:
        db_path = Path(db_path)
        if db_path.exists():
            db_vocab, db_bigrams = _load_from_sqlite(db_path)
            vocab.extend(db_vocab)
            _merge_bigrams(bigrams, db_bigrams)

    if seed_corpus:
        seed_tokens = _tokenize(seed_corpus)
        vocab.extend(seed_tokens)
        _merge_bigrams(bigrams, _bigrams_from_tokens(seed_tokens))

    # Always include local autopsy bigrams
    _merge_bigrams(bigrams, _bigrams_from_tokens(autopsy_tokens))

    # Deduplicate and keep only alphabetic-ish tokens
    vocab = _normalise_vocab(vocab)
    
    # PATCH 5: Fallback for small vocab
    if len(vocab) < 4:
        if not vocab:
            return ""  # Truly nothing to work with
        # Pad vocab with repetitions to have at least 14 words (one per line)
        while len(vocab) < 14:
            vocab.extend(vocab[:min(len(vocab), 14 - len(vocab))])

    # 3. Pick "charged" words (for final couplet etc.)
    charged = _select_charged_words(autopsy_tokens, vocab, rng, max_words=8)

    # 4. Build rhyme classes and assign end-words for each line
    end_words = _assign_rhyme_words(vocab, charged, rng)

    # 5. Generate 14 lines according to the scheme
    lines: List[str] = []
    for line_idx, rhyme_letter in enumerate(RHYME_SCHEME):
        end_word = end_words[(rhyme_letter, line_idx)]
        line = _generate_line(end_word, vocab, bigrams, charged, rng, line_idx)
        lines.append(line)

    # PATCH 6: Optional title from most charged word
    title = None
    if charged:
        # Pick most charged word (first in list), split CamelCase, and title-case it
        # Splits "OxfordLearnersDictionaries" -> "Oxford Learners Dictionaries"
        raw_word = charged[0]
        split_word = _split_camel_case(raw_word)
        title = f"Sonnet: {split_word.title()}"
    
    # 6. Return formatted sonnet (with optional title)
    if title:
        return title + "\n" + "\n".join(lines)
    else:
        return "\n".join(lines)


# ---------- Helpers: tokenisation & vocab ----------


def _tokenize(text: str) -> List[str]:
    return [m.group(0) for m in WORD_RE.finditer(text)]


def _normalise_vocab(words: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for w in words:
        lw = w.strip().lower()
        if not lw:
            continue
        if len(lw) < 2:
            continue
        if lw in seen:
            continue
        seen.add(lw)
        result.append(lw)
    return result


def _split_camel_case(word: str) -> str:
    """
    Split concatenated words by capital letters.

    Examples:
        "oxfordlearnersdictionaries" -> "oxford learners dictionaries"
        "OXFORDLEARNERSDICTIONARIES" -> "OXFORD LEARNERS DICTIONARIES"
        "OxfordLearnersDictionaries" -> "Oxford Learners Dictionaries"
        "HTTP" -> "HTTP"  (no split for all-caps acronyms)
    """
    if not word:
        return word

    # If word is all lowercase or all uppercase (acronym), return as-is
    if word.islower() or word.isupper():
        return word

    # Split on capital letters (but keep the capital with the new word)
    parts = []
    current = word[0]

    for i in range(1, len(word)):
        if word[i].isupper():
            parts.append(current)
            current = word[i]
        else:
            current += word[i]

    if current:
        parts.append(current)

    return " ".join(parts)


def _bigrams_from_tokens(tokens: Sequence[str]) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = defaultdict(list)
    for a, b in zip(tokens, tokens[1:]):
        out[a.lower()].append(b.lower())
    return out


def _merge_bigrams(
    target: Dict[str, List[str]],
    source: Mapping[str, Sequence[str]],
) -> None:
    for k, vs in source.items():
        target[k].extend(vs)


# ---------- Helpers: SQLite morgue ----------


def _load_from_sqlite(
    path: Path,
) -> Tuple[List[str], Dict[str, List[str]]]:
    """
    Very defensive reader:
    - if tables/columns are missing, just skips them
    - returns (vocab, bigrams)
    
    PATCHED: Uses correct column names from sorokin.py schema
    """
    vocab: List[str] = []
    bigrams: Dict[str, List[str]] = defaultdict(list)

    conn = sqlite3.connect(str(path))
    conn.row_factory = lambda cur, row: row  # bare tuples
    try:
        cur = conn.cursor()

        # 1) mutation_templates: assume columns (source_word, target_word)
        try:
            cur.execute(
                "SELECT source_word, target_word FROM mutation_templates "
                "LIMIT ?",
                (MAX_VOCAB_FROM_DB,),
            )
            for src, tgt in cur.fetchall():
                if src:
                    vocab.append(str(src))
                if tgt:
                    vocab.append(str(tgt))
        except Exception:
            pass

        # 2) corpse_bigrams: PATCH 1 - correct column names (word1, word2)
        try:
            cur.execute(
                "SELECT word1, word2 FROM corpse_bigrams "
                "LIMIT ?",
                (MAX_BIGRAMS_FROM_DB,),
            )
            for w1, w2 in cur.fetchall():
                if w1 and w2:
                    w1s = str(w1).lower()
                    w2s = str(w2).lower()
                    bigrams[w1s].append(w2s)
                    vocab.append(w1s)
                    vocab.append(w2s)
        except Exception:
            pass

        # 2.5) PATCH 2: readme_bigrams - structural patterns from README
        try:
            cur.execute(
                "SELECT word1, word2 FROM readme_bigrams "
                "LIMIT ?",
                (MAX_BIGRAMS_FROM_DB,),
            )
            for w1, w2 in cur.fetchall():
                if w1 and w2:
                    w1s = str(w1).lower()
                    w2s = str(w2).lower()
                    bigrams[w1s].append(w2s)
                    vocab.append(w1s)
                    vocab.append(w2s)
        except Exception:
            pass

        # 3) PATCH 3: autopsy table - correct column name (tree_text)
        try:
            cur.execute(
                "SELECT tree_text FROM autopsy "
                "ORDER BY id DESC LIMIT 16"
            )
            for (txt,) in cur.fetchall():
                if txt:
                    vocab.extend(_tokenize(str(txt)))
        except Exception:
            pass

    finally:
        conn.close()

    return vocab, bigrams


# ---------- Helpers: rhyme & charged words ----------


def _rhyme_key(word: str) -> str:
    """
    Extremely crude rhyme key: last vowel + tail,
    or last 3 letters if no vowel.
    """
    w = re.sub(r"[^a-zA-Z]", "", word.lower())
    if not w:
        return ""
    vowels = "aeiouy"
    last_vowel = max((i for i, ch in enumerate(w) if ch in vowels), default=-1)
    if last_vowel != -1:
        tail = w[last_vowel:]
        return tail[-4:]
    # no vowels? just last 3 chars
    return w[-3:]


def _select_charged_words(
    autopsy_tokens: Sequence[str],
    vocab: Sequence[str],
    rng: random.Random,
    max_words: int = 8,
) -> List[str]:
    """
    Pick "charged" words: long, rare, and present in autopsy text.
    Returns words with original casing preserved.
    """
    # Build lowercase -> original case mapping (prefer first occurrence)
    case_map: Dict[str, str] = {}
    for token in autopsy_tokens:
        low = token.lower()
        if low not in case_map:
            case_map[low] = token

    autopsy_low = [w.lower() for w in autopsy_tokens]
    counts = Counter(autopsy_low)

    scored: List[Tuple[float, str]] = []
    for w, c in counts.items():
        if len(w) < 4:
            continue
        # longer + rarer = higher score
        score = len(w) * (1.0 / (1.0 + c)) + rng.random() * 0.3
        scored.append((score, w))

    scored.sort(reverse=True)
    # Return words with original casing
    top = [case_map.get(w, w) for _, w in scored[:max_words]]

    # fallback: if autopsy is too small, sample from vocab
    if len(top) < max_words // 2:
        extra = [w for w in vocab if len(w) >= 5]
        rng.shuffle(extra)
        top.extend(extra[: max_words - len(top)])

    # keep unique
    seen = set()
    out = []
    for w in top:
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


def _assign_rhyme_words(
    vocab: Sequence[str],
    charged: Sequence[str],
    rng: random.Random,
) -> Dict[Tuple[str, int], str]:
    """
    For each line position, choose an end-word that matches the scheme.
    Returns mapping (scheme_letter, line_idx) -> word.
    """
    # 1. Build clusters by rhyme key
    clusters: Dict[str, List[str]] = defaultdict(list)
    for w in vocab:
        key = _rhyme_key(w)
        if not key:
            continue
        clusters[key].append(w)

    # To make charged words more likely to be used as rhyme ends
    charged_set = set(charged)
    for key, words in list(clusters.items()):
        boosted = [w for w in words if w in charged_set]
        if boosted:
            clusters[key] = boosted + words

    # 2. Map rhyme letters -> rhyme keys
    unique_keys = list(clusters.keys())
    rng.shuffle(unique_keys)
    if not unique_keys:
        # emergency: just pretend all words rhyme
        unique_keys = ["_default"]
        clusters["_default"] = list(vocab)

    letter_to_key: Dict[str, str] = {}
    used_keys = 0
    for letter in sorted(set(RHYME_SCHEME)):
        if used_keys < len(unique_keys):
            letter_to_key[letter] = unique_keys[used_keys]
            used_keys += 1
        else:
            # reuse some key if we don't have enough distinct rhyme classes
            letter_to_key[letter] = unique_keys[used_keys % len(unique_keys)]

    # 3. For each line index, pick a word for its letter
    result: Dict[Tuple[str, int], str] = {}
    per_letter_indices: Dict[str, int] = defaultdict(int)
    used_end_words: set[str] = set()  # Track used end-words to avoid duplicates

    for idx, letter in enumerate(RHYME_SCHEME):
        key = letter_to_key[letter]
        candidates = clusters.get(key) or list(vocab)
        rng.shuffle(candidates)

        # Try to find unused end-word from candidates
        chosen_word = None
        for attempt in range(len(candidates)):
            offset = (per_letter_indices[letter] + attempt) % len(candidates)
            candidate = candidates[offset]
            if candidate not in used_end_words:
                chosen_word = candidate
                break

        # If all candidates used, fall back to first candidate (rare with large vocab)
        if chosen_word is None:
            offset = per_letter_indices[letter] % len(candidates)
            chosen_word = candidates[offset]

        per_letter_indices[letter] += 1
        result[(letter, idx)] = chosen_word
        used_end_words.add(chosen_word)

    # 4. Force heavy words into the final couplet if possible (GG)
    if charged:
        g_indices = [i for i, l in enumerate(RHYME_SCHEME) if l == "G"]
        if len(g_indices) == 2:
            first_g, second_g = g_indices
            # choose two charged words (or duplicate if only one)
            first_word = charged[0]
            second_word = charged[1] if len(charged) > 1 else charged[0]
            result[("G", first_g)] = first_word
            result[("G", second_g)] = second_word

    return result


# ---------- Helpers: line generation ----------


def _generate_line(
    end_word: str,
    vocab: Sequence[str],
    bigrams: Mapping[str, Sequence[str]],
    charged: Sequence[str],
    rng: random.Random,
    line_idx: int,
) -> str:
    """
    Build a single line ending with end_word.

    Strategy:
    - choose target length in [MIN_LINE_WORDS, MAX_LINE_WORDS]
    - pick a starting word from charged/vocab (final couplet is "heavier")
    - follow bigrams when possible, occasionally jumping to charged words
      in the couplet
    - append end_word as final token
    - deduplicate consecutive words
    - add punctuation (Shakespearean-ish) with occasional enjambment
    """
    length = rng.randint(MIN_LINE_WORDS, MAX_LINE_WORDS)

    is_final_couplet = line_idx >= 12

    # prefer charged words as starting anchors, especially in later lines
    if charged and rng.random() < (0.9 if is_final_couplet else 0.6):
        start = rng.choice(charged)
    else:
        start = rng.choice(vocab)

    words = [start]
    current = start

    # generate inner words (excluding final end_word)
    for _ in range(length - 2):
        followers = bigrams.get(current.lower())
        if followers:
            if is_final_couplet and charged and rng.random() < 0.4:
                # occasionally snap to a charged word inside the couplet
                next_word = rng.choice(charged)
            else:
                next_word = rng.choice(followers)
        else:
            next_word = rng.choice(vocab)
        words.append(next_word)
        current = next_word

    # ensure we don't accidentally duplicate end_word too many times
    if len(words) >= 2 and words[-1].lower() == end_word.lower():
        words[-1] = rng.choice(vocab)

    words.append(end_word)

    # PATCH 8: Remove consecutive duplicates
    deduped_words = []
    prev = None
    for w in words:
        if w.lower() != (prev or '').lower():
            deduped_words.append(w)
        prev = w
    words = deduped_words

    # Clean punctuation from words before adding line-level punctuation
    words = [w.rstrip('.,;:!?—') for w in words]

    line = " ".join(words)
    
    # PATCH 7: Punctuation with enjambment support
    # Enjambment: sometimes no punctuation to flow into next line
    # Increased from 0.2 to 0.3 for better flow (Desktop Claude suggestion)
    use_enjambment = rng.random() < 0.3 and line_idx not in {3, 7, 11, 12, 13}
    
    # Punctuation pass (loose "Shakespearean" vibe):
    # - lines 3 and 7 (end of first two quatrains) → ';'
    # - line 11 (end of third quatrain) → '—' as hinge before volta
    # - line 12 (lead-in to couplet) → ','
    # - line 13 (final line) → '.'
    # - others → ',' (unless enjambment)
    if line_idx == 3 or line_idx == 7:
        line += ";"
    elif line_idx == 11:
        line += "—"
    elif line_idx == 13:
        line += "."
    elif line_idx == 12:
        line += ","
    elif not use_enjambment:
        line += ","
    # else: no punctuation (enjambment)
    
    # Capitalise first letter of line
    if line:
        line = line[0].upper() + line[1:]
    
    return line


# ---------- Main for standalone testing ----------


def main():
    """Quick test harness."""
    import sys
    
    if len(sys.argv) > 1:
        test_text = " ".join(sys.argv[1:])
    else:
        test_text = "xylophone pterodactyl quasar metadata karpathy"
    
    print("Input:", test_text)
    print()
    
    sonnet = compose_sonnet_sync(
        autopsy_text=test_text,
        db_path="sorokin.sqlite",
        seed_corpus=None
    )
    
    print("SONNET:")
    for line in sonnet.split('\n'):
        print(f"  {line}")


if __name__ == "__main__":
    main()
