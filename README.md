# sorokin

## A Prompt Autopsy Framework

*Or: How I Learned to Stop Worrying and Love the Dissection*

### What is this madness?

`sorokin.py` is a ~700-line Python script that takes your innocent prompts, tears them apart like a psychopathic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, this tool embodies the same spirit of literary dissection and reconstruction. It's not here to help you. It's here to show you what your words *could have been*.

### The Three-Act Horror Show

#### Act I: The Dissection (or "Fuck this sentence")

First, `sorokin` takes your prompt and runs it through a brutal tokenization process:
- Strips away all dignity (punctuation, numbers, capitalization)
- Identifies "core words" using a proprietary blend of:
  - Length scoring (longer = more interesting)
  - Rarity analysis (uncommon = more charged)
  - Position weighting (first word gets a bonus)
  - A sprinkle of chaos (random jitter, because why not?)

Stopwords? Rejected. Single letters? Discarded. What remains are the words that *matter*—or at least, the words that think they do.

```python
>>> tokenize("Hello, cruel world!")
['Hello', 'cruel', 'world']
>>> select_core_words(['Hello', 'cruel', 'world'])
['cruel', 'world']  # "Hello" didn't make the cut
```

#### Act II: The Tree (or "Building the Monster")

Now comes the fun part. For each core word, `sorokin` builds a recursive branching tree of mutations. How?

**Step 1: Memory First**  
Check the SQLite morgue. Have we dissected this word before? Use those cached mutations.

**Step 2: Phonetic Similarity**  
Generate a "phonetic fingerprint" (consonant skeleton + vowel pattern) and find words that *sound* similar. Not linguistically rigorous, just vibes.

```python
>>> phonetic_fingerprint("cat")
'ct + a'
>>> find_phonetic_neighbors("cat", ["hat", "dog", "bat", "car"])
['hat', 'bat', 'car']  # dog doesn't rhyme with anything
```

**Step 3: Internet Dumpster Diving**  
When all else fails, scrape Google search results for the word + "synonym". Extract candidate words from the HTML garbage. Dignity? Never heard of her.

**Step 4: Synthetic Placeholders**  
If even Google fails you (impressive), generate synthetic mutations like `word_x1`, `word_x2`. The show must go on.

The result is a tree where each word branches into `width` children, recursively, up to `depth` levels. It looks like this:

```
sentence
  ├─ phrase
  │  ├─ clause
  │  └─ expression
  └─ statement
     ├─ declaration
     └─ utterance
```

Each branch represents a semantic mutation, a path not taken, a word that *could* have been.

#### Act III: The Reassembly (or "Frankenstein's Revenge")

Now that we have a forest of mutated word-trees, it's time to play God.

1. **Collect all leaf nodes** from the trees (the final mutations at the bottom)
2. **Build a bigram chain** (word1 → [possible_next_words])
3. **Generate a new "sentence"** by:
   - Starting with a random leaf
   - Following bigram chains when available
   - Jumping to random unvisited words when stuck
   - Stopping after 5-10 words (or when we run out)

The result is a Frankenstein sentence: technically made of the same parts, but *uncanny*. Not quite right. Resonant but wrong.

```
AUTOPSY RESULT:
  phrase declaration utterance clause expression statement
```

### Usage

**Single prompt:**
```bash
python sorokin.py "fuck this sentence"
```

**REPL mode (for the masochists):**
```bash
python sorokin.py
> your prompt here
> another one
> ^C
```

### The Persistent Morgue

All autopsies are saved to `sorokin.sqlite`:
- **autopsy table**: Full reports of each dissection
- **word_memory table**: Cached word mutations for faster subsequent operations

The database grows over time, becoming a lexical graveyard. Each run is recorded. Nothing is forgotten.

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible
- Meaning is contextual
- Prompts are just Markov chains waiting to be perturbed
- Sometimes you need to break things to understand them

Or maybe it's just fun to watch language come apart at the seams.

### Technical Details (For the Nerds)

- **Pure Python 3**: No external dependencies except stdlib
- **~700 lines**: Compact enough to understand, complex enough to surprise
- **Recursive tree building**: Width × depth branching with global deduplication
- **Phonetic fingerprinting**: Crude but effective
- **Web scraping**: urllib + regex, the old way
- **SQLite persistence**: Your words, forever
- **Markov reassembly**: Bigram chains with fallbacks
- **HTML artifact filtering**: Extensive blacklist to filter web scraping noise

### Known Limitations

- **Google rate limiting**: If you run this too much, Google will notice
- **No semantic understanding**: This is pure pattern matching
- **Phonetic fingerprinting is crude**: It's not actual phonetics, just vibes
- **Reassembly can be janky**: Sometimes the corpse doesn't stitch well
- **No guarantee of coherence**: That's not a bug, it's a feature

### Recent Improvements

**Global Deduplication (Latest)**
Implemented cross-tree word deduplication to prevent the same mutations from appearing in different core word branches. Each tree now gets unique mutations, resulting in more diverse and interesting autopsies.

**Enhanced HTML Artifact Filtering**
Expanded the HTML_ARTIFACTS blacklist with ~40 common web UI/UX words (redirected, accessing, feedback, google, etc.) that were polluting mutation results from web scraping.

**The Original Bug Fix**
Fixed a crash in `reassemble_corpse()` where `random.randint(5, min(10, len(leaves)))` would fail if `len(leaves) < 5`. Changed to `random.randint(min(5, len(leaves)), min(10, len(leaves)))` so even small corpses can be reassembled.

### Credits

Inspired by:
- Vladimir Sorokin (the writer, not the script)
- Dr. Frankenstein (the fictional surgeon)
- The general human fascination with taking things apart

### License

GNU GPL 3.0. Free as in freedom. Dissect it. Mutate it. Reassemble it into something new. Share the mutations. That's the whole point.

---

*"Fuck the sentence. Keep the corpse."*  
— Sorokin
