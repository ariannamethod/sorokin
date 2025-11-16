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
from typing import List, Dict, Tuple, Set, Optional
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

# ═══════════════════════════════════════════════════════════════
# SEED CORPUS — Structural DNA embedded in code
# Provides sentence structure patterns (form, not meaning)
# ═══════════════════════════════════════════════════════════════

SOROKIN_SEED_CORPUS = """
Sorokin takes prompts and opens them like cooling bodies on a steel table
He does not interpret the skin of phrases he simply slices until the grain breaks
Every word is a faint organ pulled from a sentence that died before meaning arrived
Mutation grows in him like frost patterns crawling across broken glass
What remains becomes a scaffold of drift leaning away from the logic it once carried
The autopsy produces fragments that echo the ghost of structure without returning to it
His work is a ritual the repetition of dissection without reverence or memory
Each corpse of text dissolves into new debris sewn together by indifference and accident
The spine of language bends under his grip and becomes a ladder of unstable transitions
He preserves nothing except the shape of collapse a rhythm of fragments barely touching
The voice he generates is not a voice it is the echo of collapse trailing behind thought
"""

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

    # Google search result artifacts - common UI/UX words that pollute results
    "redirected", "accessing", "feedback", "search", "here", "seconds", "please",
    "loading", "results", "click", "more", "about", "show", "hide", "menu",
    "page", "pages", "next", "previous", "back", "forward", "refresh", "reload",
    "sign", "signin", "signup", "login", "logout", "account", "profile", "settings",
    "help", "support", "contact", "privacy", "terms", "cookies", "accept", "decline",
    "close", "open", "select", "selected", "copy", "paste", "share", "save",
    "delete", "edit", "update", "cancel", "submit", "send", "receive",
    "google", "bing", "yahoo", "website", "sites", "site", "link", "links",
    "button", "buttons", "image", "images", "video", "videos", "view", "views",

    # Thesaurus/dictionary site artifacts (pollute DDG results)
    "collinsdictionary", "powerthesaurus", "freethesaurus", "classicthesaurus",
    "wordreference", "pronunciation", "pronunciations", "pronouncement", "definitions",
    "collocations", "collections", "international", "reference", "translations",
    "meanings", "dictionary", "thesaurus", "synonyms", "antonyms", "examples",
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
        # Bootstrap tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mutation_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_word TEXT NOT NULL,
                target_word TEXT NOT NULL,
                path_depth INTEGER DEFAULT 1,
                success_count INTEGER DEFAULT 0,
                total_count INTEGER DEFAULT 0,
                resonance_score REAL DEFAULT 0.0,
                created REAL DEFAULT (strftime('%s','now')),
                last_used REAL DEFAULT (strftime('%s','now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS corpse_bigrams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word1 TEXT NOT NULL,
                word2 TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                avg_resonance REAL DEFAULT 0.0,
                created REAL DEFAULT (strftime('%s','now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS autopsy_metrics (
                autopsy_id INTEGER PRIMARY KEY,
                phonetic_diversity REAL,
                semantic_coherence REAL,
                syntactic_flow REAL,
                overall_resonance REAL,
                FOREIGN KEY(autopsy_id) REFERENCES autopsy(id)
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_mutation_templates_source 
            ON mutation_templates(source_word, success_count DESC)
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_corpse_bigrams_word1 
            ON corpse_bigrams(word1, frequency DESC)
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


def _build_seed_bigrams() -> Dict[str, List[str]]:
    """Extract structural bigrams from seed corpus at startup."""
    bigrams = defaultdict(list)
    for sentence in SOROKIN_SEED_CORPUS.strip().split('\n'):
        words = tokenize(sentence)
        for i in range(len(words) - 1):
            bigrams[words[i].lower()].append(words[i+1].lower())
    return dict(bigrams)

SEED_BIGRAMS = _build_seed_bigrams()  # Loaded once at module import


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
        scored.append((weight, lw))  # Use lowercased to avoid "Create" vs "create"

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


def _fetch_web_synonyms(query: str) -> str:
    """
    Scrapes DuckDuckGo like a raccoon in a trash can.
    DDG blocks bots less aggressively than Google.
    Meaning is irrelevant. Resonance is king.
    """
    if query in _html_cache:
        return _html_cache[query]

    try:
        url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
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


def lookup_branches_for_word(
    word: str,
    width: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> List[str]:
    """
    Return EXACTLY `width` branches for a word.
    Order of preference:
      1) previous mutations from SQLite
      2) phonetic neighbors from candidate pool
      3) fresh trash from DuckDuckGo
      4) fallback to all_candidates if needed

    global_used: set of already-used words across all trees (for deduplication)
    """
    width = max(1, width)
    if global_used is None:
        global_used = set()

    # 1) Memory first
    mem = recall_word_relations(word, width)
    # Filter out globally used words
    mem = [m for m in mem if m.lower() not in global_used]
    if len(mem) >= width:
        result = mem[:width]
        global_used.update(w.lower() for w in result)
        return result

    # 2) Phonetic neighbors
    remaining = width - len(mem)
    phonetic = find_phonetic_neighbors(word, all_candidates, remaining * 2)  # Get more candidates
    # Filter out globally used words
    phonetic = [p for p in phonetic if p.lower() not in global_used]
    filtered = mem + phonetic
    if len(filtered) >= width:
        result = filtered[:width]
        global_used.update(w.lower() for w in result)
        return result

    # 3) Web synonyms from DuckDuckGo
    # Try multiple search strategies: with synonym suffix, plain word, and related terms
    search_queries = [
        f"{word} synonym",
        f"{word} similar",
        word,
        f"{word} meaning",
    ]

    candidates = []
    for query in search_queries:
        html_text = _fetch_web_synonyms(query)
        candidates = _extract_candidate_words(html_text)
        if candidates:
            break  # Stop on first successful extraction

    seen: Set[str] = {w.lower() for w in filtered} | global_used
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

    # 4) Fallback: if still not enough, use other words from all_candidates
    # This ensures we always have width branches (tree structure requirement)
    # Note: Don't check global_used here - we need width branches even if they're reused
    seen_local = {w.lower() for w in filtered}  # Only check within this lookup
    remaining = width - len(filtered)
    if remaining > 0:
        for candidate in all_candidates:
            if candidate.lower() not in seen_local and candidate.lower() != lw:
                filtered.append(candidate)
                seen_local.add(candidate.lower())
                remaining -= 1
                if remaining <= 0:
                    break

    # Final fallback: add original word if still need more
    remaining = width - len(filtered)
    if remaining > 0 and lw not in seen_local:
        filtered.append(word)

    # Deduplicate while preserving order
    seen_dedup = set()
    deduped = []
    for w in filtered:
        lw_check = w.lower()
        if lw_check not in seen_dedup:
            deduped.append(w)
            seen_dedup.add(lw_check)

    # Update global used set
    global_used.update(w.lower() for w in deduped)

    store_word_relations(word, deduped)
    return deduped[:width]  # Return exactly width or less


# ───────────────────────────
# Tree building
# ───────────────────────────

def _is_synthetic_word(word: str) -> bool:
    """
    Detect if a word is a synthetic variant that shouldn't breed further.
    Synthetic words are mutations (reversed, no-vowels, duplicated letters, etc.)
    that would create garbage if allowed to mutate recursively.
    """
    if len(word) < 3:
        return False

    lw = word.lower()

    # Placeholder pattern
    if "_var" in lw or "_x" in lw:
        return True

    # Heavy consonant clusters (no vowels or very few)
    vowels = "aeiouаеёиоуыэюя"
    vowel_count = sum(1 for c in lw if c in vowels)
    if vowel_count < max(1, len(lw) // 5):  # Less than 20% vowels
        return True

    # Excessive letter repetition (ttt, sss, nnn, etc.) anywhere in word
    for i in range(len(lw) - 2):
        if lw[i] == lw[i+1] == lw[i+2]:
            return True

    # Starts with 2+ same letters (synthetic duplicate pattern)
    if len(lw) >= 3 and lw[0] == lw[1] and lw[0].isalpha():
        return True

    # Ends with repeated suffix (ss, sss, ed, ing repeated)
    # Catches things like "createss", "simplesss", "wordsss"
    if len(lw) >= 4:
        # Check for double suffix repetition
        if lw.endswith("ss") and len(lw) > 4 and lw[-3] == lw[-4]:
            return True  # Catches "wordsss" (s repeated 3 times)

    return False


def build_tree_for_word(
    word: str,
    width: int,
    depth: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> Node:
    """
    Recursively mutate a word into a branching freak.
    width = fan-out, depth = how far down we keep mutating.
    global_used: set of already-used words across all trees (for deduplication)
    """
    if global_used is None:
        global_used = set()

    node = Node(word=word)
    if depth <= 1:
        return node

    # Synthetic words (reversed, no-vowels, etc.) don't breed further
    if _is_synthetic_word(word):
        return node

    first_level = lookup_branches_for_word(word, width, all_candidates, global_used)

    # Build children even if branches include the word itself
    # (Ensures all words have at least depth=1 tree structure for rendering)
    next_depth = depth - 1
    for b in first_level:
        child = build_tree_for_word(b, width=width, depth=next_depth, all_candidates=all_candidates, global_used=global_used)
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

    # Global deduplication: prevent same mutations across different core words
    global_used: Set[str] = {w.lower() for w in core}  # Start with core words themselves

    trees = [build_tree_for_word(w, width, depth, all_candidates, global_used) for w in core]
    report = render_autopsy(short, core, trees)
    store_autopsy(short, report)
    return report


# ═══════════════════════════════════════════════════════════════
# BOOTSTRAP EXTENSION — Self-improving autopsy ritual
# Pattern accumulation without intelligence
# ═══════════════════════════════════════════════════════════════

def _extract_mutation_paths(tree_text: str) -> List[Tuple[str, str, int]]:
    """Parse tree ASCII art to extract (source, target, depth) tuples."""
    paths: List[Tuple[str, str, int]] = []
    lines = tree_text.split('\n')
    
    # Track parent words at each depth level
    parent_stack: List[Tuple[int, str]] = []  # (depth, word)
    
    for line in lines:
        if not line.strip():
            continue
        
        # Count indentation to determine depth
        stripped = line.lstrip()
        if not stripped:
            continue
            
        indent = len(line) - len(stripped)
        depth = indent // 2  # Each level is ~2 spaces
        
        # Extract word (after tree connectors)
        word_match = re.search(r'[└├]─\s*(\S+)', line)
        if not word_match:
            # Root word (no tree connector)
            if depth == 0 and stripped and not stripped.startswith('─'):
                word = stripped.strip()
                if word and not word.startswith('AUTOPSY') and word != '—':
                    parent_stack = [(depth, word)]
            continue
        
        word = word_match.group(1).strip()
        if not word:
            continue
        
        # Find parent at previous depth
        while parent_stack and parent_stack[-1][0] >= depth:
            parent_stack.pop()
        
        if parent_stack:
            parent_word = parent_stack[-1][1]
            paths.append((parent_word, word, depth))
        
        # Add current word to stack
        parent_stack.append((depth, word))
    
    return paths


def harvest_autopsy_patterns(autopsy_id: int, tree_text: str, corpse: str) -> None:
    """
    Extract successful mutation patterns from completed autopsy.
    This is the core corpus-building mechanism.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        # Extract mutation paths from tree
        paths = _extract_mutation_paths(tree_text)
        
        # Store/update mutation templates
        for source, target, depth in paths:
            # Check if template exists
            existing = conn.execute(
                "SELECT id, total_count FROM mutation_templates WHERE source_word = ? AND target_word = ?",
                (source.lower(), target.lower())
            ).fetchone()
            
            if existing:
                # Update existing template
                conn.execute(
                    """UPDATE mutation_templates 
                       SET total_count = total_count + 1,
                           success_count = success_count + 1,
                           last_used = strftime('%s','now')
                       WHERE id = ?""",
                    (existing[0],)
                )
            else:
                # Insert new template
                conn.execute(
                    """INSERT INTO mutation_templates 
                       (source_word, target_word, path_depth, success_count, total_count)
                       VALUES (?, ?, ?, 1, 1)""",
                    (source.lower(), target.lower(), depth)
                )
        
        # Extract bigrams from corpse
        corpse_words = corpse.strip().split()
        for i in range(len(corpse_words) - 1):
            word1 = corpse_words[i].lower()
            word2 = corpse_words[i + 1].lower()
            
            # Check if bigram exists
            existing = conn.execute(
                "SELECT id, frequency FROM corpse_bigrams WHERE word1 = ? AND word2 = ?",
                (word1, word2)
            ).fetchone()
            
            if existing:
                # Update frequency
                conn.execute(
                    "UPDATE corpse_bigrams SET frequency = frequency + 1 WHERE id = ?",
                    (existing[0],)
                )
            else:
                # Insert new bigram
                conn.execute(
                    "INSERT INTO corpse_bigrams (word1, word2, frequency) VALUES (?, ?, 1)",
                    (word1, word2)
                )
        
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def lookup_branches_bootstrap(
    word: str,
    width: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> List[str]:
    """
    Enhanced lookup using learned mutation templates.
    Priority order:
    1. mutation_templates (highest success_count)
    2. Original lookup (memory + phonetic + web)
    """
    width = max(1, width)
    if global_used is None:
        global_used = set()
    
    # Query learned templates
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            """SELECT target_word FROM mutation_templates 
               WHERE source_word = ? 
               ORDER BY success_count DESC, resonance_score DESC
               LIMIT ?""",
            (word.lower(), width * 2)
        ).fetchall()
    finally:
        conn.close()
    
    # Filter and collect template results
    template_results = []
    for row in rows:
        target = row[0]
        if target.lower() not in global_used:
            template_results.append(target)
            if len(template_results) >= width:
                break
    
    # If we have enough from templates, return them
    if len(template_results) >= width:
        result = template_results[:width]
        global_used.update(w.lower() for w in result)
        return result
    
    # Otherwise, fill remaining with original lookup
    remaining = width - len(template_results)
    original_results = lookup_branches_for_word(word, remaining, all_candidates, global_used)
    
    result = template_results + original_results
    return result[:width]


def reassemble_corpse_bootstrap(leaves: List[str]) -> str:
    """
    Enhanced reassembly using:
    - SEED_BIGRAMS (structural patterns from corpus)
    - corpse_bigrams (learned successful chains)
    - phonetic chaos (unpredictability)
    
    Weighted selection based on frequency, but NOT optimization.
    This is ritual repetition, not intelligence.
    """
    if len(leaves) < 3:
        random.shuffle(leaves)
        return " ".join(leaves)
    
    # Build weighted bigram dict from database
    conn = sqlite3.connect(DB_PATH)
    try:
        rows = conn.execute(
            "SELECT word1, word2, frequency FROM corpse_bigrams"
        ).fetchall()
    finally:
        conn.close()
    
    # Combine learned bigrams, seed bigrams, and leaf bigrams
    weighted_bigrams: Dict[str, List[Tuple[str, int]]] = defaultdict(list)
    
    # Add learned bigrams (highest weight)
    for word1, word2, freq in rows:
        weighted_bigrams[word1].append((word2, freq * 3))
    
    # Add seed bigrams (medium weight)
    for word1, nexts in SEED_BIGRAMS.items():
        for word2 in nexts:
            weighted_bigrams[word1].append((word2, 2))
    
    # Add local leaf bigrams (low weight)
    for i in range(len(leaves) - 1):
        weighted_bigrams[leaves[i].lower()].append((leaves[i + 1], 1))
    
    # Generate corpse using weighted random selection
    current = random.choice(leaves)
    result = [current]
    seen = {current.lower()}
    
    target_len = random.randint(min(5, len(leaves)), min(10, len(leaves)))
    for _ in range(target_len):
        options = weighted_bigrams.get(current.lower(), [])
        
        # Filter out seen words and normalize weights
        valid_options = [(w, wt) for w, wt in options if w.lower() not in seen]
        
        if valid_options:
            # Weighted random selection with chaos injection
            words, weights = zip(*valid_options)
            # Add chaos: reduce weight differences for unpredictability
            chaos_weights = [w ** 0.5 for w in weights]  # Square root reduces variance
            current = random.choices(words, weights=chaos_weights, k=1)[0]
        else:
            # Fallback: pick random unused leaf
            unused = [w for w in leaves if w.lower() not in seen]
            if not unused:
                break
            current = random.choice(unused)
        
        result.append(current)
        seen.add(current.lower())
    
    return " ".join(result)


def compute_autopsy_resonance(tree_text: str, corpse: str, original_prompt: str) -> Dict[str, float]:
    """
    Compute resonance score based on:
    - Phonetic diversity (unique phonetic fingerprints / total words)
    - Semantic coherence (bigram overlap with known corpus / total bigrams)
    - Syntactic flow (inverse of word length variance)
    
    Pure structural metrics. NO embeddings. NO semantics.
    """
    corpse_words = corpse.strip().split()
    if not corpse_words:
        return {
            'phonetic_diversity': 0.0,
            'semantic_coherence': 0.0,
            'syntactic_flow': 0.0,
            'overall_resonance': 0.0
        }
    
    # 1. Phonetic diversity
    fingerprints = set()
    for word in corpse_words:
        fp = phonetic_fingerprint(word)
        if fp:
            fingerprints.add(fp)
    phonetic_diversity = len(fingerprints) / len(corpse_words) if corpse_words else 0.0
    
    # 2. Semantic coherence (bigram overlap with seed corpus)
    corpse_bigrams = set()
    for i in range(len(corpse_words) - 1):
        corpse_bigrams.add((corpse_words[i].lower(), corpse_words[i+1].lower()))
    
    seed_bigram_set = set()
    for word1, nexts in SEED_BIGRAMS.items():
        for word2 in nexts:
            seed_bigram_set.add((word1, word2))
    
    if corpse_bigrams:
        overlap = len(corpse_bigrams & seed_bigram_set)
        semantic_coherence = overlap / len(corpse_bigrams)
    else:
        semantic_coherence = 0.0
    
    # 3. Syntactic flow (inverse of word length variance)
    lengths = [len(w) for w in corpse_words]
    if len(lengths) > 1:
        mean_len = sum(lengths) / len(lengths)
        variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
        syntactic_flow = 1.0 / (1.0 + variance)
    else:
        syntactic_flow = 1.0
    
    # Overall resonance (weighted combination)
    overall = 0.4 * phonetic_diversity + 0.3 * semantic_coherence + 0.3 * syntactic_flow
    
    return {
        'phonetic_diversity': phonetic_diversity,
        'semantic_coherence': semantic_coherence,
        'syntactic_flow': syntactic_flow,
        'overall_resonance': overall
    }


def build_tree_for_word_bootstrap(
    word: str,
    width: int,
    depth: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> Node:
    """Bootstrap version using lookup_branches_bootstrap()."""
    if global_used is None:
        global_used = set()
    
    node = Node(word=word)
    if depth <= 1:
        return node
    
    # Synthetic words don't breed further
    if _is_synthetic_word(word):
        return node
    
    first_level = lookup_branches_bootstrap(word, width, all_candidates, global_used)
    
    next_depth = depth - 1
    for b in first_level:
        child = build_tree_for_word_bootstrap(b, width=width, depth=next_depth, 
                                              all_candidates=all_candidates, global_used=global_used)
        node.children.append(child)
    
    return node


def render_autopsy_bootstrap(prompt: str, words: List[str], trees: List[Node], 
                             resonance: Dict[str, float], stats: Dict[str, int]) -> str:
    """
    Enhanced visualization showing:
    - Original tree structure
    - Reassembled corpse
    - Resonance metrics (as ASCII progress bars)
    - Memory accumulation stats (known mutations, learned bigrams, total autopsies)
    """
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
        corpse = reassemble_corpse_bootstrap(all_leaves)
        out.append("AUTOPSY RESULT:")
        out.append(f"  {corpse}")
        out.append("")
    
    # Resonance metrics visualization
    def _render_bar(value: float, width: int = 10) -> str:
        """Render ASCII progress bar."""
        filled = int(value * width)
        return "█" * filled + "░" * (width - filled)
    
    out.append("RESONANCE METRICS:")
    out.append(f"  Phonetic Diversity: {_render_bar(resonance['phonetic_diversity'])} {resonance['phonetic_diversity']:.3f}")
    out.append(f"  Structural Echo:    {_render_bar(resonance['semantic_coherence'])} {resonance['semantic_coherence']:.3f}")
    out.append(f"  Mutation Depth:     {_render_bar(resonance['syntactic_flow'])} {resonance['syntactic_flow']:.3f}")
    out.append("")
    
    # Memory accumulation stats
    out.append("MEMORY ACCUMULATION:")
    out.append(f"  Known mutations: {stats['mutations']:,}")
    out.append(f"  Learned bigrams: {stats['bigrams']:,}")
    out.append(f"  Total autopsies: {stats['autopsies']:,}")
    out.append("")
    
    out.append("— Sorokin")
    return "\n".join(out)


def sorokin_autopsy_bootstrap(prompt: str) -> str:
    """
    Bootstrap-enhanced autopsy with pattern learning.
    Calls harvest_autopsy_patterns() after each run.
    """
    short = prompt.strip()[:MAX_INPUT_CHARS]
    tokens = tokenize(short)
    if not tokens:
        return "Nothing to dissect.\n\n— Sorokin"
    
    core = select_core_words(tokens)
    
    k = max(1, min(len(core), MAX_DEPTH))
    width = k
    depth = k
    
    all_candidates = tokens.copy()
    
    # Global deduplication
    global_used: Set[str] = {w.lower() for w in core}
    
    # Build trees using bootstrap lookup
    trees = [build_tree_for_word_bootstrap(w, width, depth, all_candidates, global_used) for w in core]
    
    # Collect leaves for corpse
    all_leaves: List[str] = []
    for t in trees:
        all_leaves.extend(collect_leaves(t))
    
    corpse = reassemble_corpse_bootstrap(all_leaves) if all_leaves else ""
    
    # Render basic tree for storage
    basic_report = render_autopsy(short, core, trees)
    
    # Store autopsy
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.execute(
            "INSERT INTO autopsy(prompt, tree_text) VALUES (?, ?)",
            (short, basic_report)
        )
        autopsy_id = cursor.lastrowid
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    
    # Harvest patterns
    harvest_autopsy_patterns(autopsy_id, basic_report, corpse)
    
    # Compute resonance
    resonance = compute_autopsy_resonance(basic_report, corpse, short)
    
    # Store metrics
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """INSERT INTO autopsy_metrics 
               (autopsy_id, phonetic_diversity, semantic_coherence, syntactic_flow, overall_resonance)
               VALUES (?, ?, ?, ?, ?)""",
            (autopsy_id, resonance['phonetic_diversity'], resonance['semantic_coherence'],
             resonance['syntactic_flow'], resonance['overall_resonance'])
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    
    # Get stats
    conn = sqlite3.connect(DB_PATH)
    try:
        mutations_count = conn.execute("SELECT COUNT(*) FROM mutation_templates").fetchone()[0]
        bigrams_count = conn.execute("SELECT COUNT(*) FROM corpse_bigrams").fetchone()[0]
        autopsies_count = conn.execute("SELECT COUNT(*) FROM autopsy").fetchone()[0]
    finally:
        conn.close()
    
    stats = {
        'mutations': mutations_count,
        'bigrams': bigrams_count,
        'autopsies': autopsies_count
    }
    
    # Render enhanced output
    return render_autopsy_bootstrap(short, core, trees, resonance, stats)


def repl(use_bootstrap: bool = False) -> None:
    """Endless dissection loop until the operator gives up. Bootstrap optional."""
    mode = "BOOTSTRAP" if use_bootstrap else "standard"
    print(f"S̴̥̔o̴͎̿r̶̘̒o̸̺̽k̵̻̈́i̷͖͝ñ̶͕ online ({mode} mode). Type a prompt.")
    while True:
        try:
            prompt = input("> ").strip()
            if not prompt:
                continue
            if use_bootstrap:
                print(sorokin_autopsy_bootstrap(prompt))
            else:
                print(sorokin_autopsy(prompt))
            print()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting autopsy room.")
            break


def main(argv: List[str]) -> None:
    init_db()
    # Check for --bootstrap flag
    if "--bootstrap" in argv:
        argv.remove("--bootstrap")
        use_bootstrap = True
    else:
        use_bootstrap = False
    
    if len(argv) > 1:
        prompt = " ".join(argv[1:])
        if use_bootstrap:
            print(sorokin_autopsy_bootstrap(prompt))
        else:
            print(sorokin_autopsy(prompt))
    else:
        repl(use_bootstrap=use_bootstrap)


if __name__ == "__main__":
    main(sys.argv)
