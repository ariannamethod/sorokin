# sorokin

## A Prompt Autopsy Framework

*Or: How I Learned to Stop Worrying and Love the Dissection*

### What is this madness?

`sorokin.py` is a ~1330-line Python script that takes your innocent prompts, tears them apart like a psychopathic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.

**NEW**: Bootstrap edition with pattern accumulation! Sorokin now learns from every autopsy, accumulating successful mutation templates and bigram patterns in his SQLite morgue. No intelligence, no embeddings—just structural resonance and ritual repetition.

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, sorokin embodies the same spirit of literary dissection and reconstruction. It's not here to help you. It's here to show you what your words *could have been*.

### Exhibit: Maximum Autopsy Tree (Bootstrap Edition)

Because Sorokin builds trees vertically like a linguo-necromancer performing open-heart surgery on reality itself, here's a full corpse-map straight from his SQLite morgue. The phrase being dissected is "darkness consumes reality," chosen because it sounds like a rejected Nietzsche tweet. Watch as DuckDuckGo synonyms breed with phonetic chaos and learned mutation patterns:

```
darkness consumes reality

darkness
  ├─ illuminated
  │  ├─ illustrated
  │  ├─ illustrate
  │  └─ illuminate
  ├─ brilliance
  │  ├─ brilliancy
  │  ├─ blackness
  │  └─ greatness
  └─ ignorance
     ├─ naïveté
     ├─ example
     └─ unenlightenment

consumes
  ├─ consume
  │  ├─ turkey
  │  ├─ philippines
  │  └─ vocabulary
  ├─ contexts
  │  ├─ context
  │  ├─ environment
  │  └─ connection
  └─ conserve
     ├─ economise
     ├─ shelter
     └─ greece

reality
  ├─ realism
  │  ├─ representationalism
  │  ├─ literalism
  │  └─ faithfulness
  ├─ materiality
  │  ├─ referentiality
  │  ├─ corporeality
  │  └─ temporality
  └─ certainty
     ├─ certain
     ├─ ceremony
     └─ uncertainty

AUTOPSY RESULT:
  connection economise shelter greece representationalism literalism faithfulness referentiality

RESONANCE METRICS:
  Phonetic Diversity: ██████████ 1.000
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     █░░░░░░░░░ 0.137

MEMORY ACCUMULATION:
  Known mutations: 36
  Learned bigrams: 9
  Total autopsies: 1
```

Somewhere between "unenlightenment" and "corporeality," Nietzsche rolled over in his grave and asked his accountant to sue for trademark infringement. The accountant, being dead, declined. Reality remains unconsumed. Darkness persists. We've all learned nothing.

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
When all else fails, scrape DuckDuckGo search results for the word + "synonym". DDG blocks bots less aggressively than Google. Extract candidate words from the HTML garbage. Dignity? Never heard of her.

**Step 4: Fallback to All Candidates**
If even DuckDuckGo fails you, fall back to other words from the prompt. The show must go on.

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

The result is a Frankenstein sentence: technically made of the same parts, but *uncanny*. Not quite right. Resonant but wrong. This is the part where Sorokin shrugs on the lab coat, jams a fork into the storm cloud, and cackles while stitching together whatever limbs are left on the slab.

```
AUTOPSY RESULT:
  hymn-rattle migraine-honeymoon howl-trombone midnight-hairdryer spleen-taxidermy chant-smog
```

### Usage

**Standard mode (classic autopsy):**
```bash
python sorokin.py "fuck this sentence"
```

**Bootstrap mode (learning autopsy with metrics):**
```bash
python sorokin.py --bootstrap "darkness consumes reality"
```

Bootstrap mode adds:
- **RESONANCE METRICS**: ASCII progress bars showing phonetic diversity, structural echo, and mutation depth
- **MEMORY ACCUMULATION**: Stats on learned mutations, bigrams, and total autopsies
- **PATTERN LEARNING**: Every autopsy harvests successful mutation templates for future use
- **SEED CORPUS**: Structural bigrams extracted from poetic descriptions of Sorokin's process

**REPL mode (for the masochists):**
```bash
python sorokin.py --bootstrap  # or without --bootstrap for standard mode
> your prompt here
> another one
> ^C
```

### The Persistent Morgue

All autopsies are saved to `sorokin.sqlite`:
- **autopsy table**: Full reports of each dissection
- **word_memory table**: Cached word mutations for faster subsequent operations

**Bootstrap tables** (when using `--bootstrap` flag):
- **mutation_templates**: Learned source→target word mutations with success counts and resonance scores
- **corpse_bigrams**: Harvested word pairs from successful reassemblies, with frequency tracking
- **autopsy_metrics**: Resonance scores (phonetic diversity, structural echo, mutation depth) for each autopsy

The database grows over time, becoming a self-improving lexical graveyard. Each run is recorded. Patterns accumulate. Nothing is forgotten. The morgue learns.

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible
- Meaning is contextual
- Prompts are just Markov chains waiting to be perturbed
- Sometimes you need to break things to understand them

Or maybe it's just fun to watch language come apart at the seams.

### Technical Details (For the Nerds)

**Core (~760 lines):**
- **Pure Python 3**: No external dependencies except stdlib
- **Recursive tree building**: Width × depth branching with global deduplication
- **Phonetic fingerprinting**: Crude but effective
- **DuckDuckGo scraping**: urllib + regex, the old way (DDG blocks bots less than Google)
- **SQLite persistence**: Your words, forever
- **Markov reassembly**: Bigram chains with fallbacks
- **HTML artifact filtering**: Extensive blacklist to filter web scraping noise

**Bootstrap extension (~570 lines):**
- **SEED CORPUS**: Structural bigrams extracted from poetic text about Sorokin's process
- **Pattern accumulation**: Mutation templates harvested from every successful autopsy
- **Weighted reassembly**: Combines learned bigrams, seed bigrams, and local leaf bigrams
- **Resonance metrics**: Phonetic diversity, structural echo, mutation depth (pure structure, no semantics!)
- **Self-improvement loop**: Each autopsy feeds the next, patterns accumulate without intelligence

### Known Limitations

- **DuckDuckGo rate limiting**: If you run this too much, DDG might notice (but less aggressive than Google)
- **No semantic understanding (FOR NOW)**: This is pure pattern matching, but — hold my beer.
- **Phonetic fingerprinting is crude**: It's not actual phonetics, just vibes, but the question is what comes first, vibes or phonetics? resonance or binary structure?
- **Reassembly can be janky**: Sometimes the corpse doesn't stitch well
- **No guarantee of coherence**: That's not a bug, it's a feature

### Recent Improvements

**Bootstrap Extension with Pattern Accumulation (Latest)**
Sorokin now learns from every autopsy in bootstrap mode (`--bootstrap` flag):
- **SEED CORPUS**: Embedded poetic text about dissection provides structural DNA
- **Mutation templates**: Successful source→target word mutations are stored with success counts
- **Corpse bigrams**: Word pairs from reassembled text are harvested and reused
- **Resonance metrics**: ASCII progress bars showing phonetic diversity (1.000 = perfect), structural echo (overlap with seed corpus), and mutation depth (inverse of word length variance)
- **Memory accumulation stats**: Real-time display of learned patterns, bigrams, and total autopsies
- **Weighted reassembly**: Bigram selection combines learned patterns (3x weight), seed patterns (2x), and local patterns (1x) with chaos injection (square root weights) for unpredictability
- **No intelligence, just accumulation**: Pure structural pattern matching without embeddings or semantic understanding

Result: Each autopsy improves the next through ritual repetition, not reasoning. The morgue becomes smarter through sheer accumulation of corpses.

**DuckDuckGo Web Scraping**
Switched from Google to DuckDuckGo for synonym discovery. Google was blocking bot requests and returning garbage results (always the same words: "trouble", "within", "having"). DuckDuckGo is less aggressive with bot blocking and returns actual synonyms:
- "destroy" → destruction, disintegrate, dismantle, obliteration, demolish
- "evil" → villainy, villain, evildoing, depravity, wickedness
- "machines" → automobile, equipment, mechanical, apparatus
Result: Real semantic resonance instead of random HTML artifacts.

**Synthetic Mutation Purge**
Removed `_generate_phonetic_variants` entirely because it was creating garbage that polluted the autopsy:
- Reversed words ("elpmis", "etaerc") bred recursively into unreadable noise
- Suffix mutations ("createded" → "creatededed" → "createedededed") were pure madness
- Now uses minimal fallback: only real web-scraped synonyms + phonetic neighbors
- Synthetic word detection prevents breeding of low-vowel/repeated-letter mutations
- Result: Clean autopsy output instead of synthetic garbage like "creatededed elpmisss tttrouble"

**Global Deduplication**
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
