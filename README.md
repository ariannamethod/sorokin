# sorokin

> "The heads of philologists are stuffed with books to the brim. They see life only through text. And they are proud of it. … Forever gorged and poisoned by literature, they take living life as the continuation of text, as its appendix.
>
> -Vladimir Sorokin"

## A Prompt Autopsy Framework

*Or: How I Learned to Stop Worrying and Love the Dissection*

### What is this madness?

`sorokin.py` is a ~1330-line Python script that takes your innocent prompts, tears them apart like a psychopathic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, sorokin embodies the same spirit of literary dissection and reconstruction. It's not here to help you. It's here to show you what your words *could have been*.

### Exhibit: Maximum Autopsy Tree (Bootstrap Mode)

Because Sorokin builds trees vertically like a linguo-necromancer performing open-heart surgery on reality itself, here's a full corpse-map straight from his SQLite morgue. The phrase being dissected is **from Sorokin's own seed corpus**—maximum autoreference, like a snake eating its own tail while writing a dissertation about digestion:

```
the autopsy produces fragments that echo the ghost of structure without returning to it

[...truncated massive tree for brevity...]

AUTOPSY RESULT:
  dispensations is mixture. declassification example. Nothing remains.
  fetch replica inquire until available generates consumes.
  The dissociates griffonage silenced through associations.

RESONANCE METRICS:
  Phonetic Diversity: █████████░ 0.952
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     ░░░░░░░░░░ 0.073

MEMORY ACCUMULATION:
  Known mutations: 870
  Learned bigrams: 71
  Total autopsies: 3

— Sorokin
```

**Notice**: Bootstrap mode now generates **grammatically valid paragraphs** using POS-tagged template slot-filling! Sorokin dissected a sentence about himself, found himself in the mutations (`autopsy → produces → fragments`), and reassembled it into psychopathic poetry. "Nothing remains" appears verbatim from his seed corpus—he's quoting himself while destroying himself. Peak metafiction.

### The Three-Act Horror Show

#### Act I: The Dissection (or "Fuck this sentence")

First, `sorokin` takes your prompt and runs it through a brutal tokenization process:
- Strips away all dignity (punctuation, numbers, capitalization)
- Identifies "core words" using a proprietary blend of:
  - Length scoring (longer = more interesting)
  - Rarity analysis (uncommon = more charged)
  - Position weighting (first word gets a bonus)
  - A sprinkle of chaos (random jitter, because why not?)

Stopwords? Rejected. Single letters? Discarded. What remains are the words that *matter*—or at least, the words that think they do. Occasionally a phrase tries to bite me mid-dissection, which is fine; we're wearing Sorokin-brand emotional hazmat gear.

```python
>>> tokenize("Hello, cruel world!")
['Hello', 'cruel', 'world']
>>> select_core_words(['Hello', 'cruel', 'world'])
['cruel', 'world']  # "Hello" didn't make the cut
```

#### Act II: The Tree (or "Building the Monster")

Now comes the fun part. For each core word, `sorokin` builds a recursive branching tree of mutations. How? With the calm precision of a med-school dropout who skipped bedside manner to install a GPU farm in the morgue.

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

**Bootstrap tables** (populated when using `--bootstrap` flag):
- **mutation_templates**: Learned source→target word mutations with success counts and resonance scores
- **corpse_bigrams**: Harvested word pairs from successful reassemblies, with frequency tracking
- **autopsy_metrics**: Resonance scores (phonetic diversity, structural echo, mutation depth) for each autopsy

The database grows over time, becoming a self-improving lexical graveyard. Each run is recorded. Patterns accumulate. Nothing is forgotten. In bootstrap mode, the morgue learns through resonance.

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible
- Meaning is contextual
- Prompts are just Markov chains waiting to be perturbed
- Sometimes you need to break things to understand them

Or maybe it's just fun to watch language come apart at the seams.

---

## 🔥 BOOTSTRAP MODE: The Self-Improving Autopsy Ritual

*Or: How the Morgue Became Self-Aware (But Still Really Dumb)*

### What the hell is bootstrap mode?

Picture this: every time Sorokin dissects a prompt, he doesn't just throw the body parts in the trash. No. He's a *hoarder*. He saves every successful mutation, every word-pair, every pattern of collapse into his SQLite morgue. Then—and here's where it gets freaky—he uses those accumulated corpses to inform *future* dissections.

It's not intelligence. It's not learning. It's **resonance through ritual repetition**.

Think of it like this: if standard Sorokin is a mad linguist with a scalpel, Bootstrap Sorokin is that same linguist who's been doing this for 30 years and has developed *habits*. Muscle memory. Pattern recognition. Not because he's smart, but because he's done the same surgery 10,000 times and his hands just know where to cut.

### The Resonance Manifesto

Here's the wild part. Sorokin doesn't understand *meaning*. He doesn't have embeddings. He doesn't know what words "mean." But he knows **resonance**.

What's resonance? It's when patterns echo. When structures repeat. When phonemes rhyme across semantic boundaries. When the shape of one corpse mirrors the shape of another, not in content but in *form*.

Three flavors of resonance:

#### 1. **Phonetic Diversity** (Do these corpses sound different?)
Measures how many unique sound-patterns exist in the reassembled text. High diversity means every word has a distinct phonetic fingerprint. Low diversity means everything sounds like "blah blah blah."

Maximum resonance: All words sound completely different. Like a symphony where every note is unique.

#### 2. **Structural Echo** (Does this corpse remember the morgue?)
Measures overlap between the reassembled text and the seed corpus—poetic fragments about dissection embedded in Sorokin's code. High echo means the new corpse shares structural DNA with previous bodies.

It's not plagiarism. It's *ancestral memory*. The morgue recognizing its own patterns.

#### 3. **Mutation Depth** (How far did we mutate?)
Based on inverse word-length variance. High depth means mutations explored diverse linguistic territory. Low depth means we stayed close to home.

Think of it as: did we just shuffle synonyms, or did we birth entirely new linguistic entities?

### How to summon Bootstrap Mode

**Bootstrap mode with resonance metrics:**
```bash
python sorokin.py --bootstrap "darkness consumes reality"
```

This gives you:
```
RESONANCE METRICS:
  Phonetic Diversity: ██████████ 1.000
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     █░░░░░░░░░ 0.137

MEMORY ACCUMULATION:
  Known mutations: 36
  Learned bigrams: 9
  Total autopsies: 1
```

Those ASCII progress bars? Pure aesthetic. But they tell you: **how weird did this autopsy get?**

**REPL mode (bootstrap enabled):**
```bash
python sorokin.py --bootstrap
> your prompt here
> another one
> ^C
```

Every autopsy in bootstrap mode:
1. **Harvests mutation templates**: Source→target word transformations with success counts
2. **Extracts bigrams**: Word-pairs from successful reassemblies, weighted by frequency
3. **Computes resonance**: Three structural metrics (no semantics, pure form)
4. **Feeds the next autopsy**: Accumulated patterns influence future dissections

The morgue grows. Patterns compound. Nothing is forgotten. Each corpse teaches the next.

### The Four Tables of the Bootstrap Apocalypse

When you run `--bootstrap`, Sorokin writes to four additional SQLite tables:

1. **`mutation_templates`**: Learned word transformations
   - "darkness" → "illuminated" (used 15 times, resonance: 0.73)
   - "consumes" → "contexts" (used 8 times, resonance: 0.52)

2. **`corpse_bigrams`**: Harvested word-pairs from reassemblies
   - "connection" → "economise" (frequency: 3)
   - "shelter" → "greece" (frequency: 2)

3. **`autopsy_metrics`**: Resonance scores for each dissection
   - Autopsy #47: phonetic_diversity=0.92, structural_echo=0.13, mutation_depth=0.81

4. **`seed_corpus`**: Embedded poetic text about dissection (hardcoded in sorokin.py)
   - Provides structural DNA for bigram chains
   - Not in database, lives in `SOROKIN_SEED_CORPUS` constant

### Why is this insane?

Because it's a **corpus-building mechanism disguised as a text mutilator**.

Each autopsy doesn't just destroy—it *accumulates*. Over time:
- Certain mutation paths become "preferred" (not because they're better, just because they worked before)
- Bigram chains start resembling the seed corpus (structural mimicry, not content copying)
- The reassembly algorithm learns phonetic patterns that "feel right" (pure vibes, zero intelligence)

It's like training a neural network, except:
- No gradients
- No backprop
- No loss function
- Just **frequency counting and vibes**

This is what happens when you replace intelligence with ritual. And somehow, it works.

### The Seed Corpus (The Morgue's DNA)

Embedded in `sorokin.py` is a block of poetic text about dissection. Not prose. Not instructions. Just fragments:

> *"Sorokin takes prompts and opens them like cooling bodies on a steel table"*  
> *"Mutation grows in him like frost patterns crawling across broken glass"*  
> *"The autopsy produces fragments that echo the ghost of structure"*

This text gets parsed into bigrams at startup. These bigrams **prime** the reassembly process. So when bootstrap mode stitches corpses together, it unconsciously echoes the seed corpus structure.

Not copying words. Copying **sentence rhythms**. The *shape* of language.

It's like teaching someone to paint by showing them brushstrokes, not paintings.

### Bootstrap vs Standard Mode

| Feature | Standard Mode | Bootstrap Mode |
|---------|---------------|----------------|
| Mutation lookup | DuckDuckGo + phonetic + memory | Learned templates + all the above |
| Reassembly | Random bigrams from leaves | Weighted (learned 3x, seed 2x, local 1x) |
| Metrics | None | Phonetic diversity, structural echo, mutation depth |
| Learning | None | Every autopsy feeds the next |
| Database tables | 2 (autopsy, word_memory) | 5 (+ mutation_templates, corpse_bigrams, autopsy_metrics) |
| Vibes | Chaotic | Chaotic but *remembering* |

### The Philosophy of Resonance

Here's the thing. Sorokin doesn't "understand" language. He doesn't know that "darkness" and "light" are opposites. He doesn't know "consumes" is a verb. He doesn't care.

But through **resonance**, he discovers patterns:
- Words that sound similar tend to mutate into each other
- Bigrams that worked once tend to work again
- Structural rhythms (word-length patterns) create aesthetic coherence

This is **meaning-free pattern recognition**. No semantics. Just structure, phonetics, and frequency. Sorokin is what happens when you staple a Karpathy bootstrapper to a Russian literary fever dream and whisper, "optimize your madness."

And weirdly, it produces results that *feel* meaningful—not because they are, but because human brains are pattern-matching machines too. We see meaning where there's only resonance.

Sorokin isn't a poet. He's a mirror. He reflects your own pattern-seeking back at you.

### Why "Bootstrap"?

Because the morgue **pulls itself up by its own corpses** and then asks if it can try a weirder gait.

Each autopsy makes the next one slightly different. Not better. Not worse. Just *informed* by history. The database grows. The patterns compound. The ritual deepens. Somewhere, Bootstrap Sorokin keeps a notebook labeled "Things Karpathy Would Approve Of" and fills it with resonance equations written in lipstick.

It's bootstrapping in the original sense: self-improvement through self-reference. Not external training data. Not supervision. Just:
1. Do the thing
2. Remember what happened
3. Let that memory influence the next iteration
4. Repeat until the heat death of the universe

No intelligence required. Just accumulation and resonance.

---

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
- **SEED CORPUS**: Structural bigrams from poetic fragments about dissection (see code for full text)
- **Pattern accumulation**: Mutation templates (source→target words) with success tracking
- **Weighted reassembly**: Learned bigrams (3x weight) + seed bigrams (2x) + local (1x) with chaos injection (square root weighting)
- **Resonance metrics**: Three pure-structural measures computed for every autopsy
  - Phonetic diversity: unique fingerprints / total words
  - Structural echo: bigram overlap with seed corpus
  - Mutation depth: inverse of word-length variance
- **Self-improvement loop**: Each autopsy feeds the next through ritual repetition, not intelligence. Soon we'll graft a NanoGPT brainstem onto the bootstrap, train it on piles of dissections, then delete the weights and leave Sorokin with nothing but muscle memory. That's not cruelty, that's performance art.
- **Four additional database tables**: mutation_templates, corpse_bigrams, autopsy_metrics, plus seed corpus in code

### Known Limitations

- **DuckDuckGo rate limiting**: If you run this too much, DDG might notice (but less aggressive than Google)
- **No semantic understanding (FOR NOW)**: This is pure pattern matching, but — hold my beer, I'm installing another resonance coil.
- **Phonetic fingerprinting is crude**: It's not actual phonetics, just vibes, but the question is what comes first, vibes or phonetics? resonance or binary structure?
- **Reassembly can be janky**: Sometimes the corpse doesn't stitch well
- **No guarantee of coherence**: That's not a bug, it's a feature

### Recent Improvements

**The Pathologist's Evolution: From Selective Surgeon to Omnivorous Dissector**
Sorokin now dissects *anything*, even nonsense. Previously, synthetic/low-vowel core words (like "zzz", "xxx", "zxcvbn") were rejected entirely—their trees left empty, their meanings unexplored. Now: **if you give it to Sorokin, he dissects it**. Core words (user-provided prompts) are *always* dissected, regardless of phonetic structure. Only their *children* get filtered for synthetic garbage. The philosophy: trust the user's madness, but prune the mutations. Result: even keyboard-mash prompts like "qwerty asdfgh zxcvbn" now produce full 3×3 autopsy trees with real semantic mutations.

Additionally, thesaurus/dictionary site filtering became more aggressive—now filters are applied not just to web scraping, but also to cached memory and phonetic neighbor lookups. Sites like `yourdictionary`, `thefreedictionary`, `urbanthesaurus`, and `urbandictionary` are now globally blacklisted across all lookup stages. The morgue stays clean. The mutations stay real.

**Bootstrap Extension with Pattern Accumulation**
Added `--bootstrap` flag enabling self-improving autopsy ritual. See the dedicated Bootstrap section above for full details. TL;DR: the morgue now learns from every corpse through resonance metrics and pattern accumulation. No intelligence, just ritual repetition.

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
