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

import asyncio
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

import httpx

DB_PATH = Path("sorokin.sqlite")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
MAX_INPUT_CHARS = 100
MAX_WORDS = 6          # max core words to dissect
MAX_DEPTH = 4          # recursion safety cap
TREE_WIDTH = 4         # constant fan-out (4 branches per node)
MAX_HTML_CACHE = 50    # max cached HTML responses to prevent unbounded memory growth
MAX_CONCURRENT_REQUESTS = 3   # max simultaneous web requests (lowered from 10 to avoid DDG rate limiting)
WEB_REQUEST_TIMEOUT = 3.0     # timeout in seconds
MIN_REQUEST_DELAY = 0.5       # minimum delay between web requests (anti-spam)

# Latin + extended + Cyrillic
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿА-Яа-яЁё]+")

STOPWORDS = {
    "the", "and", "to", "a", "in", "it", "of", "for", "on", "with", "as", "is", "at",
    "by", "from", "or", "an", "be", "this", "that", "are", "was", "but", "not",
    "i", "you", "he", "she", "they", "we",
    # Common interjections/greetings (don't dissect these)
    "hello", "hi", "hey", "yo", "sup", "bye", "ok", "okay", "yes", "no", "yeah",
    "привет", "пока", "да", "нет",
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

# PATCH: Sentence templates for paragraph generation (Sorokin-style syntax)
SOROKIN_SENTENCE_TEMPLATES = [
    "{noun1} {verb} {noun2}, where {noun3} becomes {adj}.",
    "The {adj} {noun1} {verb} through {noun2}.",
    "When {noun1} {verb}, {noun2} forgets {noun3}.",
    "{noun1} is {adj}. {noun2} {verb}. Nothing remains.",
    "{noun1} {verb} {noun2} until {adj} {noun3} consumes.",
    "Where {noun1} {verb}, {noun2} becomes {adj}, and {noun3} persists.",
    "{noun1} {verb}. {noun2} {verb}. The {adj} {noun3} collapses.",
    "Through {noun1}, {noun2} {verb} {noun3}, but {adj} darkness remains.",
]

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
    "wordreference", "wordhippo", "wordpanda", "wordthesauri", "snappywords",
    "opensynonym", "sinonimkata", "vocabdictionary", "webdictionary", "collins",
    "relatedwords", "bighugelabs", "thefrenchfocus", "writingbeginner", "grammartipshub",
    "grammarpen", "lalanguefrancaise", "namediscoveries", "pronounceonline",
    "differentsynonym", "overcrowdednycschools", "pronunciation", "pronunciations",
    "pronouncement", "definitions", "collocations", "international", "reference",
    "translations", "meanings", "dictionary", "thesaurus", "synonyms", "antonyms",
    "examples", "dictionaries", "categories", "quotations", "alphabetically",
    "yourdictionary", "thefreedictionary", "urbanthesaurus", "urbandictionary",

    # Geographic names that pollute DDG results (countries, cities, etc.)
    "singapore", "philippines", "colombia", "argentina", "australia", "austria",
    "netherlands", "switzerland", "denmark", "iceland", "sweden", "norway",
    "finland", "poland", "portugal", "spain", "france", "germany", "italy",
    "greece", "turkey", "brazil", "mexico", "canada", "russia", "china",
    "japan", "korea", "india", "thailand", "vietnam", "indonesia", "malaysia",
    "africa", "asia", "europe", "america", "oceania",
    "lithuania", "latvia", "estonia", "bulgaria", "romania", "croatia",
    "montenegro", "macedonia", "slovenia", "slovakia", "czech",
    "ireland", "scotland", "wales", "england", "britain",

    # Language/dictionary metadata
    "spanish", "french", "german", "italian", "portuguese", "russian",
    "chinese", "japanese", "korean", "arabic", "hindi", "turkish",
    "tellmeinspanish", "frenchdictionary", "spanishdict", "reversedict",
    "reversethesaurus", "lawlessfrench", "frenchtogether",
    "singaporean", "singaporeans", "singlish", "singlishdict",
    "colombian", "argentinian", "brazilian", "mexican", "canadian",

    # DuckDuckGo-specific artifacts (common in DDG search results)
    "duckduckgo", "unfortunately", "containing", "error", "confirm",
    "challenge", "following", "email", "made", "squares", "lite",
    "related", "example", "associated", "comparable", "correlated",

    # DDG error/rate-limit page artifacts
    "persists", "anonymized", "understand", "context", "getting",
    "helps", "support", "address", "includes",

    # DDG HTML/CSS artifacts (IDs, classes, common UI elements)
    "dabcf", "bots", "duck", "code", "complete", "human",

    # Reddit/forum/social media artifacts
    "subredditstats", "subreddit", "generationiron", "assoass",
    "redditors", "upvote", "downvote", "karma",
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
        # README cache tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readme_cache (
                id INTEGER PRIMARY KEY DEFAULT 1,
                mtime REAL NOT NULL,
                CHECK (id = 1)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readme_bigrams (
                word1 TEXT NOT NULL,
                word2 TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_readme_bigrams_word1
            ON readme_bigrams(word1)
        """)
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_readme_bigrams_unique
            ON readme_bigrams(word1, word2)
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


# ───────────────────────────
# README self-cannibalism — The morgue eats its own documentation
# ───────────────────────────

def _build_readme_bigrams() -> Dict[str, List[str]]:
    """
    Extract structural bigrams from README.md with SQLite caching.

    This makes the README part of Sorokin's structural DNA.
    Self-cannibalism as corpus-building strategy.

    The README is both tombstone and weather report:
    - It documents what Sorokin does
    - It becomes part of what Sorokin does
    - Changes to README automatically update the corpus
    - The system eats its own documentation and hallucinates it back
    """
    readme_path = Path("README.md")
    if not readme_path.exists():
        return {}

    # Get README mtime before opening DB
    readme_mtime = readme_path.stat().st_mtime

    # Check cache validity
    conn = sqlite3.connect(DB_PATH)
    try:
        # Check cached version (may fail on first run before init_db)
        try:
            cached = conn.execute(
                "SELECT mtime FROM readme_cache WHERE id = 1"
            ).fetchone()

            # Use 1.0 second tolerance for coarse filesystem timestamp granularity (FAT32, network FS)
            if cached and abs(cached[0] - readme_mtime) < 1.0:
                # Load from cache
                rows = conn.execute(
                    "SELECT word1, word2 FROM readme_bigrams"
                ).fetchall()
                bigrams = defaultdict(list)
                for w1, w2 in rows:
                    bigrams[w1].append(w2)
                return dict(bigrams)
        except sqlite3.OperationalError:
            # Tables don't exist yet (first run before init_db)
            pass
    finally:
        conn.close()

    # Parse README (cache miss or stale)
    bigrams = defaultdict(list)
    try:
        text = readme_path.read_text(encoding='utf-8')
        # Remove code blocks (just examples)
        text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
        # Remove markdown headers/formatting
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*|\*|`', '', text)  # Remove bold/italic/code

        sentences = text.split('\n')
        for sentence in sentences:
            if not sentence.strip():
                continue
            words = tokenize(sentence)
            for i in range(len(words) - 1):
                bigrams[words[i].lower()].append(words[i+1].lower())
    except Exception:
        pass  # If README parsing fails, just skip it

    # Save to cache (may fail on first run before init_db)
    conn = sqlite3.connect(DB_PATH)
    try:
        # Clear old bigrams cache
        conn.execute("DELETE FROM readme_bigrams")

        # Store new mtime (replace or insert)
        conn.execute(
            "REPLACE INTO readme_cache (id, mtime) VALUES (1, ?)",
            (readme_mtime,)
        )

        # Store bigrams
        bigram_rows = []
        for word1, nexts in bigrams.items():
            for word2 in nexts:
                bigram_rows.append((word1, word2))

        if bigram_rows:
            conn.executemany(
                "INSERT OR IGNORE INTO readme_bigrams (word1, word2) VALUES (?, ?)",
                bigram_rows
            )

        conn.commit()
    except sqlite3.OperationalError:
        # Tables don't exist yet (first run before init_db), skip caching
        conn.rollback()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

    return dict(bigrams)

README_BIGRAMS = _build_readme_bigrams()  # Loaded once at startup


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
# PATCH: POS tagging and syllable counting for paragraph generation
# ───────────────────────────

def guess_pos(word: str) -> str:
    """
    Heuristic POS tagger. Returns: noun, verb, adj, adv, unknown.
    Based on suffix patterns + common word whitelist for better accuracy on short words.
    """
    lw = word.lower()

    # PATCH: Common verb whitelist (short words that are always verbs)
    # Fixes misclassification of "to", "come", "look", etc. in autopsy results
    common_verbs = {
        'is', 'are', 'was', 'were', 'be', 'being', 'been',
        'becomes', 'become', 'do', 'does', 'did', 'done',
        'have', 'has', 'had', 'come', 'came', 'go', 'goes', 'went',
        'make', 'makes', 'made', 'take', 'takes', 'took',
        'see', 'sees', 'saw', 'look', 'looks', 'find', 'finds', 'found',
        'give', 'gives', 'get', 'gets', 'got', 'say', 'says', 'said',
        'know', 'knows', 'knew', 'think', 'thinks', 'thought',
        'use', 'uses', 'used', 'work', 'works', 'worked',
        'feel', 'feels', 'felt', 'tell', 'tells', 'told',
        'ask', 'asks', 'asked', 'try', 'tries', 'tried',
        'call', 'calls', 'called', 'need', 'needs', 'needed',
        'want', 'wants', 'wanted', 'seem', 'seems', 'seemed',
        'help', 'helps', 'helped', 'show', 'shows', 'showed',
        'leave', 'leaves', 'left', 'keep', 'keeps', 'kept',
        'hold', 'holds', 'held', 'turn', 'turns', 'turned',
        'start', 'starts', 'started', 'run', 'runs', 'ran',
        'move', 'moves', 'moved', 'play', 'plays', 'played',
        'live', 'lives', 'lived', 'bring', 'brings', 'brought',
        'write', 'writes', 'wrote', 'sit', 'sits', 'sat',
        'stand', 'stands', 'stood', 'lose', 'loses', 'lost',
        'pay', 'pays', 'paid', 'meet', 'meets', 'met',
        'include', 'includes', 'led', 'understand', 'understood',
        'watch', 'watches', 'watched', 'follow', 'follows', 'followed',
        'stop', 'stops', 'stopped', 'create', 'creates', 'created',
        'speak', 'speaks', 'spoke', 'read', 'reads', 'allow', 'allows',
        'add', 'adds', 'added', 'spend', 'spends', 'spent',
        'grow', 'grows', 'grew', 'open', 'opens', 'opened',
        'walk', 'walks', 'walked', 'win', 'wins', 'won',
        'offer', 'offers', 'offered', 'remember', 'remembers', 'remembered',
        'love', 'loves', 'loved', 'consider', 'considers', 'considered',
        'appear', 'appears', 'appeared', 'buy', 'buys', 'bought',
        'wait', 'waits', 'waited', 'serve', 'serves', 'served',
        'die', 'dies', 'died', 'send', 'sends', 'sent',
        'expect', 'expects', 'expected', 'build', 'builds', 'built',
        'stay', 'stays', 'stayed', 'fall', 'falls', 'fell',
        'cut', 'cuts', 'reach', 'reaches', 'reached',
        'kill', 'kills', 'killed', 'remain', 'remains', 'remained',
        'suggest', 'suggests', 'suggested', 'raise', 'raises', 'raised',
        'pass', 'passes', 'passed', 'sell', 'sells', 'sold',
        'require', 'requires', 'required', 'report', 'reports', 'reported',
        'decide', 'decides', 'decided', 'pull', 'pulls', 'pulled',
    }

    # PATCH: Common noun whitelist
    common_nouns = {
        'time', 'times', 'year', 'years', 'day', 'days',
        'thing', 'things', 'man', 'men', 'woman', 'women',
        'life', 'lives', 'child', 'children', 'world',
        'school', 'state', 'family', 'student', 'group',
        'country', 'problem', 'hand', 'part', 'place',
        'case', 'week', 'company', 'system', 'program',
        'question', 'work', 'government', 'number', 'night',
        'point', 'home', 'water', 'room', 'mother',
        'area', 'money', 'story', 'fact', 'month',
        'lot', 'right', 'study', 'book', 'eye',
        'job', 'word', 'business', 'issue', 'side',
        'kind', 'head', 'house', 'service', 'friend',
        'father', 'power', 'hour', 'game', 'line',
        'end', 'member', 'law', 'car', 'city',
        'community', 'name', 'president', 'team', 'minute',
        'idea', 'kid', 'body', 'information', 'back',
        'parent', 'face', 'level', 'office', 'door',
        'health', 'person', 'art', 'war', 'history',
        'party', 'result', 'change', 'morning', 'reason',
        'research', 'girl', 'guy', 'moment', 'air',
        'teacher', 'force', 'education',
    }

    # Check whitelists first (before suffix patterns)
    if lw in common_verbs:
        return 'verb'
    if lw in common_nouns:
        return 'noun'

    # Nouns (most common suffixes)
    if lw.endswith(('tion', 'ness', 'ity', 'ment', 'ance', 'ence', 'ship', 'hood', 'dom', 'ism')):
        return 'noun'

    # Verbs
    if lw.endswith(('ed', 'ing', 'ize', 'ise', 'ate', 'ify', 'en')):
        return 'verb'

    # Adverbs
    if lw.endswith('ly'):
        return 'adv'

    # Adjectives
    if lw.endswith(('ful', 'less', 'ous', 'ive', 'able', 'ible', 'al', 'ic', 'ant', 'ent')):
        return 'adj'
    if len(lw) <= 5 and lw.endswith(('y', 'er', 'est')):
        return 'adj'

    return 'unknown'


def count_syllables(word: str) -> int:
    """
    Crude syllable counter based on vowel clusters.
    Not linguistically perfect, but good enough for rhythm analysis.
    """
    vowels = 'aeiouyаеёиоуыэюя'
    word = word.lower()
    count = 0
    prev_was_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            count += 1
        prev_was_vowel = is_vowel

    return max(1, count)


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
_request_semaphore: Optional[asyncio.Semaphore] = None  # Initialized on first use
_httpx_client: Optional[httpx.AsyncClient] = None  # Shared async client
_last_request_time: float = 0.0  # Track last web request for rate limiting


async def _cleanup_httpx() -> None:
    """Cleanup httpx client gracefully."""
    global _httpx_client
    if _httpx_client is not None:
        try:
            await _httpx_client.aclose()
        except Exception:
            pass  # Ignore errors during cleanup
        finally:
            _httpx_client = None


async def _fetch_web_synonyms(query: str) -> str:
    """
    Scrapes DuckDuckGo like a raccoon in a trash can (async edition).
    DDG blocks bots less aggressively than Google.
    Meaning is irrelevant. Resonance is king.

    Now with:
    - Async HTTP requests (httpx - works everywhere including Termux)
    - Rate limiting with MIN_REQUEST_DELAY to avoid DDG ban
    - Semaphore limiting concurrent requests to 3
    - Realistic User-Agent to blend in
    - Error page detection
    """
    global _request_semaphore, _httpx_client, _last_request_time
    import time

    # Lazy init semaphore
    if _request_semaphore is None:
        _request_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    # Check cache first (synchronous, fast)
    if query in _html_cache:
        return _html_cache[query]

    # Create async client if needed
    if _httpx_client is None:
        _httpx_client = httpx.AsyncClient(
            timeout=WEB_REQUEST_TIMEOUT,
            follow_redirects=True  # CRITICAL: Follow DDG redirects!
        )

    html_text = ""

    # Acquire semaphore to limit concurrent requests
    async with _request_semaphore:
        # Rate limiting: wait if last request was too recent
        current_time = time.time()
        time_since_last = current_time - _last_request_time
        if time_since_last < MIN_REQUEST_DELAY:
            await asyncio.sleep(MIN_REQUEST_DELAY - time_since_last)

        try:
            url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            headers = {"User-Agent": USER_AGENT}

            resp = await _httpx_client.get(url, headers=headers)
            html_text = resp.text

            # Update last request time
            _last_request_time = time.time()

            # Detect DDG error/rate-limit pages
            if len(html_text) < 1000 and "error" in html_text.lower():
                # Likely an error page, treat as empty
                html_text = ""
            elif "If this persists" in html_text or "email us" in html_text:
                # DDG rate limit / ban page
                html_text = ""

        except Exception:
            # Silently fail - we'll return empty string
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


async def lookup_branches_for_word(
    word: str,
    width: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> List[str]:
    """
    Return EXACTLY `width` branches for a word (async edition with SOURCE MIXING).

    Strategy: Mix memory cache (50%) + fresh web data (50%) to maintain both
    performance and novelty. No early returns - always fetch web data!

    Order of sources:
      1) SQLite memory (limited to ~50% of width)
      2) Fresh web scraping from DuckDuckGo (PARALLEL requests!)
      3) Phonetic neighbors from candidate pool
      4) Fallback to all_candidates if needed

    global_used: set of already-used words across all trees (for deduplication)
    """
    width = max(1, width)
    if global_used is None:
        global_used = set()

    filtered = []
    seen: Set[str] = set(global_used)
    lw = word.lower()

    # 1) Memory first - but LIMITED to ~50% of width (balanced mix!)
    # This ensures we always fetch fresh web data even if cache is full
    memory_limit = max(1, width // 2)  # At least 1, at most 50% of width
    mem = recall_word_relations(word, memory_limit * 2)  # Get more candidates
    # Filter out globally used words AND HTML artifacts
    mem = [m for m in mem if m.lower() not in seen and m.lower() not in HTML_ARTIFACTS]
    mem = mem[:memory_limit]  # Take at most memory_limit
    filtered.extend(mem)
    seen.update(w.lower() for w in mem)

    # 2) Web synonyms from DuckDuckGo - ALWAYS fetch (even if memory was full!)
    # This is the KEY change: no early returns, always get fresh data
    search_queries = [
        f"{word} synonym",
        f"{word} similar",
        word,
        f"{word} meaning",
    ]

    # Fire all requests in parallel
    html_results = await asyncio.gather(
        *[_fetch_web_synonyms(q) for q in search_queries],
        return_exceptions=True
    )

    # Take first non-empty result
    candidates = []
    for html_text in html_results:
        if isinstance(html_text, str) and html_text:
            candidates = _extract_candidate_words(html_text)
            if candidates:
                break

    # Add web candidates - prefer phonetic matches first, then any valid candidates
    if candidates:
        # First try phonetic neighbors from web results
        web_phonetic = find_phonetic_neighbors(word, candidates, width - len(filtered))
        for wp in web_phonetic:
            if wp.lower() not in seen and wp.lower() not in HTML_ARTIFACTS:
                filtered.append(wp)
                seen.add(wp.lower())
                if len(filtered) >= width:
                    break

    # If still not enough, add other non-phonetic web candidates
    if len(filtered) < width and candidates:
        for c in candidates:
            lc = c.lower()
            if lc == lw:
                continue
            if lc in seen:
                continue
            if lc in HTML_ARTIFACTS:
                continue
            seen.add(lc)
            filtered.append(c)
            if len(filtered) >= width:
                break

    # 3) Smart fallback to MORE memory if web failed
    # If web returned nothing (DDG ban/error) and we still need more candidates,
    # go back to memory and get the rest (up to full width)
    if len(filtered) < width and not candidates:
        # Web failed! Try to get more from memory (beyond the 50% limit)
        additional_needed = width - len(filtered)
        # Fetch extra words from memory
        additional_mem = recall_word_relations(word, memory_limit * 2 + additional_needed)
        # IMPORTANT: Slice BEFORE filtering (Copilot bug fix!)
        # Skip the ones we already took (first memory_limit items)
        additional_mem = additional_mem[memory_limit:]
        # THEN filter for unseen/non-artifact words
        additional_mem = [m for m in additional_mem
                         if m.lower() not in seen and m.lower() not in HTML_ARTIFACTS]

        for m in additional_mem[:additional_needed]:
            filtered.append(m)
            seen.add(m.lower())
            if len(filtered) >= width:
                break

    # 4) EMERGENCY FALLBACK: README words (phonetic matching)!
    # If still don't have enough (DDG banned + empty memory), use README vocabulary
    # Use PHONETIC MATCHING to find related words (not just direct bigrams)
    if len(filtered) < width:
        readme_bigrams = _build_readme_bigrams()

        # Try direct bigrams first
        if lw in readme_bigrams:
            readme_words = [w for w in readme_bigrams[lw]
                           if w.lower() not in seen and w.lower() not in HTML_ARTIFACTS]
            for rw in readme_words[:width - len(filtered)]:
                filtered.append(rw)
                seen.add(rw.lower())

        # If still need more, do phonetic matching against ALL README words
        if len(filtered) < width:
            # Get all unique words from README bigrams (keys + values)
            readme_vocab = set(readme_bigrams.keys())
            for vals in readme_bigrams.values():
                readme_vocab.update(vals)
            readme_vocab = list(readme_vocab)

            # Phonetic matching
            phonetic_matches = find_phonetic_neighbors(word, readme_vocab, width - len(filtered))
            for pm in phonetic_matches:
                if pm.lower() not in seen and pm.lower() not in HTML_ARTIFACTS:
                    filtered.append(pm)
                    seen.add(pm.lower())
                    if len(filtered) >= width:
                        break

    # 5) NO FALLBACK TO all_candidates!
    # Previously: used prompt words as fallback, but this creates garbage.
    # Better to use memory → web → README → partial trees.
    # Never breed prompt words recursively.
    #
    # Fallback chain:
    # 1. Memory (50% baseline)
    # 2. Web (DDG parallel queries)
    # 3. More memory (if web failed)
    # 4. README bigrams (emergency)
    # 5. Partial tree (honest failure)
    #
    # Result: Smart cascading fallback, no garbage.

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


async def build_tree_for_word(
    word: str,
    width: int,
    depth: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None,
    is_core_word: bool = False
) -> Node:
    """
    Recursively mutate a word into a branching freak (async edition).
    width = fan-out, depth = how far down we keep mutating.
    global_used: set of already-used words across all trees (for deduplication)
    is_core_word: True for top-level core words (allows synthetic words to be dissected)
    """
    if global_used is None:
        global_used = set()

    node = Node(word=word)
    if depth <= 1:
        return node

    # Synthetic words don't breed further, EXCEPT core words (user-provided prompts must dissect)
    if _is_synthetic_word(word) and not is_core_word:
        return node

    first_level = await lookup_branches_for_word(word, width, all_candidates, global_used)

    # Build ALL children in PARALLEL (async recursion!)
    next_depth = depth - 1
    child_tasks = [
        build_tree_for_word(b, width=width, depth=next_depth, all_candidates=all_candidates, global_used=global_used, is_core_word=False)
        for b in first_level
    ]
    node.children = await asyncio.gather(*child_tasks)

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

    # Only render trees that have children (skip empty trees)
    skipped = []
    for w, t in zip(words, trees):
        if t.children:
            out.append(w)
            for i, ch in enumerate(t.children):
                last = (i == len(t.children) - 1)
                out.extend(render_node(ch, "  ", last))
            out.append("")
        else:
            skipped.append(w)

    # Optionally mention skipped words
    if skipped:
        out.append(f"(Skipped {len(skipped)} words with no synonyms: {', '.join(skipped)})")
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

async def sorokin_autopsy(prompt: str) -> str:
    """Main entry: take a prompt, return its dissection (async edition)."""
    short = prompt.strip()[:MAX_INPUT_CHARS]
    tokens = tokenize(short)
    if not tokens:
        return "Nothing to dissect.\n\n— Sorokin"

    core = select_core_words(tokens)

    # Width is CONSTANT (4×4 trees), depth varies with number of core words
    width = TREE_WIDTH
    depth = max(1, min(len(core), MAX_DEPTH))

    all_candidates = tokens.copy()

    # Global deduplication: prevent same mutations across different core words
    global_used: Set[str] = {w.lower() for w in core}  # Start with core words themselves

    # Build ALL trees in PARALLEL!
    tree_tasks = [build_tree_for_word(w, width, depth, all_candidates, global_used, is_core_word=True) for w in core]
    trees = await asyncio.gather(*tree_tasks)

    report = render_autopsy(short, core, trees)
    store_autopsy(short, report)
    return report


# ═══════════════════════════════════════════════════════════════
# PATCH: Paragraph generation with syntax templates
# ═══════════════════════════════════════════════════════════════

def fill_template(template: str, leaves: List[str]) -> str:
    """
    Fill template slots with words from leaves based on POS.
    Example: "{noun1} {verb} {noun2}" -> "darkness consumes reality"
    """
    # Build POS buckets
    pos_buckets = defaultdict(list)
    for w in leaves:
        pos = guess_pos(w)
        pos_buckets[pos].append(w)

    # Also add 'unknown' words to all buckets as fallback
    for w in leaves:
        if guess_pos(w) == 'unknown':
            for bucket in pos_buckets.values():
                if w not in bucket:
                    bucket.append(w)

    # Extract slots from template
    slots = re.findall(r'\{(\w+)\}', template)
    filled = template

    for slot in slots:
        # Extract POS type (e.g., "noun1" -> "noun")
        pos_type = re.sub(r'\d+', '', slot)

        if pos_buckets[pos_type]:
            word = random.choice(pos_buckets[pos_type])
            filled = filled.replace(f'{{{slot}}}', word, 1)
        elif pos_buckets['unknown']:
            # Fallback to unknown words
            word = random.choice(pos_buckets['unknown'])
            filled = filled.replace(f'{{{slot}}}', word, 1)
        else:
            # Last resort: any leaf
            word = random.choice(leaves)
            filled = filled.replace(f'{{{slot}}}', word, 1)

    return filled


def score_paragraph_resonance(paragraph: str) -> float:
    """
    Score paragraph quality based on:
    - Phonetic diversity
    - Rhythmic variance (syllable distribution)
    - Chaos factor (unpredictability bonus)

    Returns float 0.0-1.0
    """
    words = paragraph.strip().split()
    if not words:
        return 0.0

    # 1. Phonetic diversity
    fingerprints = {phonetic_fingerprint(w) for w in words}
    phon_div = len(fingerprints) / len(words)

    # 2. Rhythmic variance (syllable count variance)
    syllables = [count_syllables(w) for w in words]
    if len(syllables) > 1:
        mean_syl = sum(syllables) / len(syllables)
        variance = sum((s - mean_syl) ** 2 for s in syllables) / len(syllables)
        rhythm = min(variance / 2.0, 1.0)  # Cap at 1.0
    else:
        rhythm = 0.0

    # 3. Chaos factor (random, adds unpredictability)
    chaos = random.uniform(0.3, 0.7)

    return phon_div * 0.4 + rhythm * 0.4 + chaos * 0.2


def generate_sorokin_paragraph(leaves: List[str], n_sentences: int = 3) -> str:
    """
    Generate a multi-sentence paragraph with:
    - Syntactic templates (Sorokin-style)
    - POS-based slot filling
    - Punctuation (commas, periods)
    - Proper capitalization (first letter of each sentence)
    - Maximum resonance selection (generate 20 candidates, pick best)

    Returns a grammatically valid but semantically absurd paragraph.
    """
    if not leaves:
        return ""

    # Generate multiple candidates
    candidates = []
    for _ in range(20):
        sentences = []
        for _ in range(n_sentences):
            template = random.choice(SOROKIN_SENTENCE_TEMPLATES)
            sentence = fill_template(template, leaves)
            # Capitalize first letter of ALL sentences (templates may contain multiple sentences)
            if sentence:
                # Split by '. ' to handle multi-sentence templates, capitalize each
                parts = sentence.split('. ')
                capitalized_parts = []
                for part in parts:
                    if part:  # Skip empty parts
                        capitalized_parts.append(part[0].upper() + part[1:] if len(part) > 1 else part.upper())
                sentence = '. '.join(capitalized_parts)
            sentences.append(sentence)

        paragraph = ' '.join(sentences)

        # PATCH: Remove consecutive duplicate words (fixes "to to", "come, come")
        words = paragraph.split()
        deduped = []
        prev = None
        for w in words:
            if w.lower() != (prev or '').lower():  # Case-insensitive comparison
                deduped.append(w)
            prev = w
        paragraph = ' '.join(deduped)

        score = score_paragraph_resonance(paragraph)
        candidates.append((score, paragraph))

    # Return best scoring paragraph
    candidates.sort(reverse=True, key=lambda x: x[0])
    return candidates[0][1]


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


async def lookup_branches_bootstrap(
    word: str,
    width: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None
) -> List[str]:
    """
    Enhanced lookup using learned mutation templates (async edition).
    Priority order:
    1. mutation_templates (highest success_count)
    2. Original lookup (memory + phonetic + web - async!)
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

    # Otherwise, fill remaining with original lookup (async!)
    remaining = width - len(template_results)
    original_results = await lookup_branches_for_word(word, remaining, all_candidates, global_used)

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

    # PATCH: Add README bigrams (medium-low weight)
    for word1, nexts in README_BIGRAMS.items():
        for word2 in nexts:
            weighted_bigrams[word1].append((word2, int(1.5)))

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


async def build_tree_for_word_bootstrap(
    word: str,
    width: int,
    depth: int,
    all_candidates: List[str],
    global_used: Optional[Set[str]] = None,
    is_core_word: bool = False
) -> Node:
    """Bootstrap version using lookup_branches_bootstrap() - async recursive edition!"""
    if global_used is None:
        global_used = set()

    node = Node(word=word)
    if depth <= 1:
        return node

    # Synthetic words don't breed further, EXCEPT core words (user-provided prompts must dissect)
    if _is_synthetic_word(word) and not is_core_word:
        return node

    first_level = await lookup_branches_bootstrap(word, width, all_candidates, global_used)

    next_depth = depth - 1

    # Build all children in PARALLEL (async recursion!)
    child_tasks = [
        build_tree_for_word_bootstrap(b, width=width, depth=next_depth,
                                      all_candidates=all_candidates, global_used=global_used, is_core_word=False)
        for b in first_level
    ]

    node.children = await asyncio.gather(*child_tasks)

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

    # Only render trees that have children (skip empty trees)
    skipped = []
    for w, t in zip(words, trees):
        if t.children:
            out.append(w)
            for i, ch in enumerate(t.children):
                last = (i == len(t.children) - 1)
                out.extend(render_node(ch, "  ", last))
            out.append("")
        else:
            skipped.append(w)

    # Optionally mention skipped words
    if skipped:
        out.append(f"(Skipped {len(skipped)} words with no synonyms: {', '.join(skipped)})")
        out.append("")

    all_leaves: List[str] = []
    for t in trees:
        all_leaves.extend(collect_leaves(t))

    # PATCH: Use paragraph generator instead of simple reassembly
    if all_leaves:
        paragraph = generate_sorokin_paragraph(all_leaves, n_sentences=random.randint(2, 4))
        out.append("AUTOPSY RESULT:")
        out.append(f"  {paragraph}")
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
    out.append(f"  README bigrams: {stats.get('readme_bigrams', 0):,}")
    out.append(f"  Total autopsies: {stats['autopsies']:,}")
    out.append("")
    
    out.append("— Sorokin")
    return "\n".join(out)


async def sorokin_autopsy_bootstrap(prompt: str) -> str:
    """
    Bootstrap-enhanced autopsy with pattern learning (async edition).
    Calls harvest_autopsy_patterns() after each run.
    Now builds ALL trees in PARALLEL!
    """
    short = prompt.strip()[:MAX_INPUT_CHARS]
    tokens = tokenize(short)
    if not tokens:
        return "Nothing to dissect.\n\n— Sorokin"

    core = select_core_words(tokens)

    # Width is CONSTANT (4×4 trees), depth varies with number of core words
    width = TREE_WIDTH
    depth = max(1, min(len(core), MAX_DEPTH))

    all_candidates = tokens.copy()

    # Global deduplication
    global_used: Set[str] = {w.lower() for w in core}

    # Build ALL trees in PARALLEL (async!)
    tree_tasks = [
        build_tree_for_word_bootstrap(w, width, depth, all_candidates, global_used, is_core_word=True)
        for w in core
    ]
    trees = await asyncio.gather(*tree_tasks)
    
    # Collect leaves for corpse
    all_leaves: List[str] = []
    for t in trees:
        all_leaves.extend(collect_leaves(t))

    # PATCH: Generate paragraph instead of simple corpse
    corpse = generate_sorokin_paragraph(all_leaves, n_sentences=random.randint(2, 4)) if all_leaves else ""
    
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
        'readme_bigrams': len(README_BIGRAMS),  # PATCH: show README self-cannibalism
        'autopsies': autopsies_count
    }
    
    # Render enhanced output
    return render_autopsy_bootstrap(short, core, trees, resonance, stats)


async def repl(use_bootstrap: bool = False) -> None:
    """Endless dissection loop until the operator gives up (async edition). Bootstrap optional."""
    mode = "BOOTSTRAP" if use_bootstrap else "standard"
    print(f"S̴̥̔o̴͎̿r̶̘̒o̸̺̽k̵̻̈́i̷͖͝ñ̶͕ online ({mode} mode). Type a prompt.")
    try:
        while True:
            try:
                # Use asyncio to handle input without blocking event loop
                prompt = await asyncio.to_thread(input, "> ")
                prompt = prompt.strip()
                if not prompt:
                    continue
                if use_bootstrap:
                    result = await sorokin_autopsy_bootstrap(prompt)
                    print(result)
                else:
                    result = await sorokin_autopsy(prompt)
                    print(result)
                print()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting autopsy room.")
                break
    finally:
        # Ensure cleanup happens even if interrupted
        await _cleanup_httpx()


async def async_main(argv: List[str]) -> None:
    """Async entry point for Sorokin."""
    init_db()
    # Bootstrap mode is DEFAULT (best quality output with paragraph generation)
    # Use --simple flag to disable bootstrap and get basic reassembly
    if "--simple" in argv:
        argv.remove("--simple")
        use_bootstrap = False
    else:
        use_bootstrap = True

    try:
        if len(argv) > 1:
            prompt = " ".join(argv[1:])
            if use_bootstrap:
                result = await sorokin_autopsy_bootstrap(prompt)
                print(result)
            else:
                result = await sorokin_autopsy(prompt)
                print(result)
        else:
            await repl(use_bootstrap=use_bootstrap)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\nInterrupted. Cleaning up...")
    finally:
        # Always cleanup httpx client
        await _cleanup_httpx()


def main(argv: List[str]) -> None:
    """Synchronous entry point - launches async event loop."""
    try:
        asyncio.run(async_main(argv))
    except KeyboardInterrupt:
        # Already handled in async_main, just exit cleanly
        pass
    except Exception as e:
        print(f"\nFatal error: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    main(sys.argv)
