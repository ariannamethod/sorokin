#!/usr/bin/env python3
# sorokin.py — ruthless prompt autopsy
#
# Dedicated to the great russian writer Vladimir Sorokin.
#
# Usage:
#   python sorokin.py "fuck this sentence"
#   python sorokin.py              # REPL mode
#
# Motto:
#   "Fuck the sentence. Keep the corpse."

from __future__ import annotations

import html
import random
import re
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Tuple, Set
import urllib.parse
import urllib.request

DB_PATH = Path("sorokin.sqlite")
USER_AGENT = "Mozilla/5.0 (compatible; SorokinAutopsy/1.0)"
MAX_INPUT_CHARS = 100
MAX_WORDS = 6          # max core words to dissect
MAX_DEPTH = 4          # recursion safety cap
MAX_HTML_CACHE = 50    # max cached HTML responses to prevent unbounded memory growth

# Latin + extended + Cyrillic
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿА-Яа-яЁё]+")

STOPWORDS = {
    "the", "and", "to", "a", "in", "it", "of", "for", "on", "with", "as", "is", "at",
    "by", "from", "or", "an", "be", "this", "that", "are", "was", "but", "not",
    "i", "you", "he", "she", "they", "we",
    "и", "в", "на", "но", "не", "это", "как", "что", "тот", "той", "то", "за",
}

# HTML/JS artifact blacklist - garbage from poorly parsed web content
# Keep this list minimal to preserve interesting words from web results
HTML_ARTIFACTS = {
    # Obvious JS artifacts
    "multiselectable", "canhavechildren", "sourcemappingurl", "encodeuricomponent",
    "removelistener", "removeattribute", "stoppropagation", "textcontent",
    "getboundingclientrect", "addeventlistener", "preventdefault", "appendchild",
    "createelement", "setattribute", "tostring", "valueof", "prototype",

    # HTML structure tags (very common in parsing)
    "thead", "tbody", "tfoot", "colgroup", "doctype", "charset", "viewport",
    "blockquote", "figcaption", "noscript", "marquee", "plaintext",

    # Very common JS framework names
    "uricomponent", "javascript", "chrome", "webkit",
}


@dataclass
class Node:
    """One word on the slab, plus its branching mutations."""
    word: str
    children: List["Node"] = field(default_factory=list)


# ───────────────────────────
# SQLite morgue
# ───────────────────────────

def init_db() -> None:
    """Create tiny morgue tables if they don't exist yet."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS autopsy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                tree_text TEXT NOT NULL,
                created REAL DEFAULT (strftime('%s','now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS word_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                related TEXT NOT NULL,
                created REAL DEFAULT (strftime('%s','now'))
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_word_memory_word
            ON word_memory(word)
        """)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def store_autopsy(prompt: str, tree_text: str) -> None:
    """Save the full autopsy report for future horror."""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO autopsy(prompt, tree_text) VALUES (?, ?)",
            (prompt, tree_text),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def store_word_relations(word: str, related: List[str]) -> None:
    """Remember what we found around a word, like labeling jars in a basement."""
    if not related:
        return
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executemany(
            "INSERT INTO word_memory(word, related) VALUES (?, ?)",
            [(word.lower(), r.lower()) for r in related],
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def recall_word_relations(word: str, limit: int) -> List[str]:
    """Recall previous mutations of a word from the morgue."""
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            """
            SELECT related FROM word_memory
            WHERE word = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (word.lower(), limit),
        ).fetchall()
    finally:
        conn.close()
    return [r[0] for r in rows]


# ───────────────────────────
# Tokenization & core selection
# ───────────────────────────

def tokenize(text: str) -> List[str]:
    """Carve out tokens: only letters, no digits, no punctuation."""
    return WORD_RE.findall(text)


def select_core_words(tokens: List[str]) -> List[str]:
    """
    Pick the charged words to dissect.
    Longer, rarer, earlier words get more weight + a bit of chaos.
    """
    if not tokens:
        return []

    lowered = [t.lower() for t in tokens]
    scored: List[Tuple[float, str]] = []
    seen = set()

    for idx, t in enumerate(tokens):
        lw = t.lower()
        if len(lw) < 2:
            continue
        if lw in STOPWORDS:
            continue
        if lw in seen:
            continue
        seen.add(lw)

        freq = lowered.count(lw)
        length_score = len(lw) ** 1.2
        rarity_bonus = 1.0 / (1.0 + freq)
        position_bonus = 1.2 if idx == 0 else 1.0
        jitter = random.uniform(0.9, 1.1)

        weight = length_score * rarity_bonus * position_bonus * jitter
        scored.append((weight, t))

    if not scored:
        return tokens[:MAX_WORDS]

    scored.sort(reverse=True, key=lambda x: x[0])
    chosen = [w for _, w in scored[:MAX_WORDS]]
    return chosen


# ───────────────────────────
# Phonetic similarity — sound-based mutations
# ───────────────────────────

def phonetic_fingerprint(word: str) -> str:
    """
    Crude phonetic hash: reduce word to consonant skeleton + vowel pattern.
    Not linguistically rigorous — just enough to catch alliteration/rhyme.
    """
    lw = word.lower()
    consonants = re.sub(r'[aeiouаеёиоуыэюя]', '', lw)
    vowels = re.sub(r'[^aeiouаеёиоуыэюя]', '', lw)
    return consonants[:3] + vowels[-2:]


def _generate_phonetic_variants(word: str, count: int) -> List[str]:
    """Generate interesting phonetic variants for more creative mutations."""
    variants = []
    lw = word.lower()

    # Reverse the word (uncanny)
    if count > 0:
        reversed_word = lw[::-1]
        if reversed_word != lw:
            variants.append(reversed_word)
            count -= 1

    # Remove vowels (skeleton)
    if count > 0:
        no_vowels = "".join(c for c in lw if c not in "aeiouаеёиоуыэюя")
        if no_vowels and no_vowels != lw and len(no_vowels) > 1:
            variants.append(no_vowels)
            count -= 1

    # Duplicate first consonant
    if count > 0:
        vowels = "aeiouаеёиоуыэюя"
        first_consonant = next((c for c in lw if c not in vowels), None)
        if first_consonant:
            variants.append(first_consonant + lw)
            count -= 1

    # Add suffix to original
    if count > 0:
        suffixes = ["s", "ed", "ing", "er", "est", "ly"]
        for suffix in suffixes:
            if count > 0:
                candidate = lw + suffix
                if candidate not in variants:
                    variants.append(candidate)
                    count -= 1

    # Keep original word itself if needed
    if count > 0 and lw not in variants:
        variants.append(lw)
        count -= 1

    # Pad with placeholders
    while count > 0:
        variants.append(f"{lw}_var{count}")
        count -= 1

    return variants[:len(set(variants))]


def find_phonetic_neighbors(word: str, candidate_pool: List[str], limit: int) -> List[str]:
    """
    Return words from candidate_pool that sound similar to word.
    Similarity = shared phonetic fingerprint prefix or suffix.
    """
    if limit <= 0:
        return []

    fp = phonetic_fingerprint(word)
    if len(fp) < 2:
        return []

    scored: List[Tuple[int, str]] = []
    lw = word.lower()

    for cand in candidate_pool:
        lc = cand.lower()
        if lc == lw:
            continue
        cfp = phonetic_fingerprint(cand)
        if len(cfp) < 2:
            continue

        score = 0
        if fp[:2] == cfp[:2]:
            score += 2
        if fp[-2:] == cfp[-2:]:
            score += 2
        if score == 0:
            continue

        scored.append((score, cand))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [w for _, w in scored[:limit]]


# ───────────────────────────
# Internet scraping: dirty synonyms
# ───────────────────────────

_html_cache: Dict[str, str] = {}


def _fetch_google_snippets(query: str) -> str:
    """
    Scrapes the web like a raccoon in a trash can.
    Meaning is irrelevant. Resonance is king.
    """
    if query in _html_cache:
        return _html_cache[query]

    try:
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&num=3"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=6) as resp:
            html_text = resp.read().decode("utf-8", "ignore")
    except Exception:
        html_text = ""

    # Prevent unbounded memory growth of cache
    if len(_html_cache) >= MAX_HTML_CACHE:
        _html_cache.clear()

    _html_cache[query] = html_text
    return html_text


def _split_camelcase(text: str) -> str:
    """Split camelCase words into separate words."""
    # Insert spaces before uppercase letters
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', text)


def _extract_candidate_words(html_text: str) -> List[str]:
    """Strip tags, keep charged co-occurrences, discard dignity."""
    if not html_text:
        return []

    # Remove script and style blocks completely (they add noise)
    stripped = re.sub(r'<script[^>]*>.*?</script>', ' ', html_text, flags=re.DOTALL | re.IGNORECASE)
    stripped = re.sub(r'<style[^>]*>.*?</style>', ' ', stripped, flags=re.DOTALL | re.IGNORECASE)

    # First unescape HTML entities
    stripped = html.unescape(stripped)

    # Remove non-semantic tags (noscript, meta, etc)
    stripped = re.sub(r'<(?:noscript|meta|link|base|title)[^>]*>', ' ', stripped, flags=re.IGNORECASE)

    # Add spaces around tags to prevent word concatenation
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    # Split camelCase words
    stripped = _split_camelcase(stripped)
    # Also replace common separators with spaces
    stripped = re.sub(r"[&\-_=/\\:;,.\(\)\[\]\{\}]", " ", stripped)
    # Collapse multiple spaces
    stripped = re.sub(r"\s+", " ", stripped)
    words = WORD_RE.findall(stripped)

    def _looks_like_real_word(word: str) -> bool:
        """Filter out gibberish - real words have some vowels and not all same consonants."""
        vowels = "aeiouаеёиоуыэюя"
        vowel_count = sum(1 for c in word if c in vowels)
        consonant_count = len(word) - vowel_count

        # Must have at least some vowels
        if vowel_count < max(1, len(word) // 4):
            return False

        # Check for repeating patterns (gibberish detector)
        # e.g., "xyzxyzxyz" or "tttttt" are probably garbage
        if len(word) >= 6:
            # Check if it's mostly repeating 1-2 char patterns
            for pattern_len in [1, 2, 3]:
                pattern = word[:pattern_len]
                if all(word[i:i+pattern_len] == pattern for i in range(0, len(word), pattern_len)):
                    return False

        return True

    counts: Dict[str, int] = {}
    for w in words:
        lw = w.lower()
        if len(lw) < 4:  # Increased from 3
            continue
        if lw in STOPWORDS:
            continue
        if lw in HTML_ARTIFACTS:
            continue
        if not _looks_like_real_word(lw):
            continue
        counts[lw] = counts.get(lw, 0) + 1

    scored: List[Tuple[float, str]] = []
    for w, freq in counts.items():
        # Prefer less frequent words (they're more interesting)
        # and reasonably sized words
        score = (min(len(w) / 10.0, 1.5)) * (1.0 / (1.0 + freq))
        scored.append((score, w))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [w for _, w in scored]


def lookup_branches_for_word(word: str, width: int, all_candidates: List[str]) -> List[str]:
    """
    Return EXACTLY `width` branches for a word.
    Order of preference:
      1) previous mutations from SQLite
      2) phonetic neighbors from candidate pool
      3) fresh trash from Google
      4) synthetic placeholders if all else fails
    """
    width = max(1, width)

    # 1) Memory first
    mem = recall_word_relations(word, width)
    if len(mem) >= width:
        return mem[:width]

    # 2) Phonetic neighbors
    remaining = width - len(mem)
    phonetic = find_phonetic_neighbors(word, all_candidates, remaining)
    filtered = mem + phonetic
    if len(filtered) >= width:
        return filtered[:width]

    # 3) Google synonyms
    # Try multiple search strategies: with synonym suffix, plain word, and related terms
    search_queries = [
        f"{word} synonym",
        f"{word} similar",
        word,
        f"{word} meaning",
    ]

    candidates = []
    for query in search_queries:
        html_text = _fetch_google_snippets(query)
        candidates = _extract_candidate_words(html_text)
        if candidates:
            break  # Stop on first successful extraction

    seen: Set[str] = {w.lower() for w in filtered}
    lw = word.lower()

    # Try to find more phonetic neighbors in Google results
    if candidates:
        google_phonetic = find_phonetic_neighbors(word, candidates, width - len(filtered))
        for gp in google_phonetic:
            if gp.lower() not in seen:
                filtered.append(gp)
                seen.add(gp.lower())
                if len(filtered) >= width:
                    break

    # If still not enough, add other non-phonetic candidates
    for c in candidates:
        lc = c.lower()
        if lc == lw:
            continue
        if lc in seen:
            continue
        seen.add(lc)
        filtered.append(c)
        if len(filtered) >= width:
            break

    # 4) Pad with phonetic variants if the web was boring
    remaining = width - len(filtered)
    if remaining > 0:
        variants = _generate_phonetic_variants(word, remaining)
        filtered.extend(variants)

    store_word_relations(word, filtered)
    return filtered


# ───────────────────────────
# Tree building
# ───────────────────────────

def build_tree_for_word(word: str, width: int, depth: int, all_candidates: List[str]) -> Node:
    """
    Recursively mutate a word into a branching freak.
    width = fan-out, depth = how far down we keep mutating.
    """
    node = Node(word=word)
    if depth <= 1:
        return node

    first_level = lookup_branches_for_word(word, width, all_candidates)

    next_depth = depth - 1
    for b in first_level:
        child = build_tree_for_word(b, width=width, depth=next_depth, all_candidates=all_candidates)
        node.children.append(child)

    return node


def collect_leaves(node: Node) -> List[str]:
    """Gather all leaf words from the tree — the final mutated fragments."""
    if not node.children:
        return [node.word]
    leaves: List[str] = []
    for ch in node.children:
        leaves.extend(collect_leaves(ch))
    return leaves


# ───────────────────────────
# Frankenstein reassembly — markov-style corpse
# ───────────────────────────

def reassemble_corpse(leaves: List[str]) -> str:
    """
    Build a new "sentence" from leaf words using a simple bigram chain.
    If leaves < 3, just shuffle and return.
    """
    if len(leaves) < 3:
        random.shuffle(leaves)
        return " ".join(leaves)

    bigrams: Dict[str, List[str]] = defaultdict(list)
    for i in range(len(leaves) - 1):
        bigrams[leaves[i].lower()].append(leaves[i + 1])

    current = random.choice(leaves)
    result = [current]
    seen = {current.lower()}

    target_len = random.randint(min(5, len(leaves)), min(10, len(leaves)))
    for _ in range(target_len):
        options = bigrams.get(current.lower(), [])
        options = [w for w in options if w.lower() not in seen]

        if not options:
            unused = [w for w in leaves if w.lower() not in seen]
            if not unused:
                break
            current = random.choice(unused)
        else:
            current = random.choice(options)

        result.append(current)
        seen.add(current.lower())

    return " ".join(result)


# ───────────────────────────
# ASCII rendering — vertical scalpel
# ───────────────────────────

def render_node(node: Node, prefix: str, is_last: bool) -> List[str]:
    """Render one node and its descendants as a clean morgue diagram."""
    connector = "└─ " if is_last else "├─ "
    lines = [f"{prefix}{connector}{node.word}"]

    if node.children:
        new_prefix = prefix + ("   " if is_last else "│  ")
        for i, ch in enumerate(node.children):
            last = (i == len(node.children) - 1)
            lines.extend(render_node(ch, new_prefix, last))

    return lines


def render_autopsy(prompt: str, words: List[str], trees: List[Node]) -> str:
    """Stitch together the full autopsy report as a single text block."""
    out: List[str] = []
    out.append(prompt.strip())
    out.append("")

    for w, t in zip(words, trees):
        out.append(w)
        for i, ch in enumerate(t.children):
            last = (i == len(t.children) - 1)
            out.extend(render_node(ch, "  ", last))
        out.append("")

    all_leaves: List[str] = []
    for t in trees:
        all_leaves.extend(collect_leaves(t))

    if all_leaves:
        corpse = reassemble_corpse(all_leaves)
        out.append("AUTOPSY RESULT:")
        out.append(f"  {corpse}")
        out.append("")

    out.append("— Sorokin")
    return "\n".join(out)


# ───────────────────────────
# Main pipeline
# ───────────────────────────

def sorokin_autopsy(prompt: str) -> str:
    """Main entry: take a prompt, return its dissection."""
    short = prompt.strip()[:MAX_INPUT_CHARS]
    tokens = tokenize(short)
    if not tokens:
        return "Nothing to dissect.\n\n— Sorokin"

    core = select_core_words(tokens)

    k = max(1, min(len(core), MAX_DEPTH))
    width = k
    depth = k

    all_candidates = tokens.copy()

    trees = [build_tree_for_word(w, width, depth, all_candidates) for w in core]
    report = render_autopsy(short, core, trees)
    store_autopsy(short, report)
    return report


def repl() -> None:
    """Endless dissection loop until the operator gives up."""
    print("S̴̥̔o̴͎̿r̶̘̒o̸̺̽k̵̻̈́i̷͖͝ñ̶͕ online. Type a prompt.")
    while True:
        try:
            prompt = input("> ").strip()
            if not prompt:
                continue
            print(sorokin_autopsy(prompt))
            print()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting autopsy room.")
            break


def main(argv: List[str]) -> None:
    init_db()
    if len(argv) > 1:
        prompt = " ".join(argv[1:])
        print(sorokin_autopsy(prompt))
    else:
        repl()


if __name__ == "__main__":
    main(sys.argv)
