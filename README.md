```
███████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██║ ██╔╝██║████╗  ██║
███████╗██║   ██║██████╔╝██║   ██║█████╔╝ ██║██╔██╗ ██║
╚════██║██║   ██║██╔══██╗██║   ██║██╔═██╗ ██║██║╚██╗██║
███████║╚██████╔╝██║  ██║╚██████╔╝██║  ██╗██║██║ ╚████║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
```

# sorokin

> "The heads of philologists are stuffed with books to the brim. They see life only through text. And they are proud of it. … Forever gorged and poisoned by literature, they take living life as the continuation of text, as its appendix.
>
> -Vladimir Sorokin"

## A Prompt Autopsy Framework

*Or: How I Learned to Stop Worrying and Love the Dissection*

### What is this madness?

`sorokin.py` is a ~1660-line Python spellbook disguised as a Python script. It takes your innocent prompts, tears them apart like a psychopathic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, sorokin embodies the same spirit of literary dissection and reconstruction. It's not here to help you. It's here to show you what your words *could have been*—and then eat this README, spit it back out, and declare the output canonical.

This README is therefore both tombstone and weather report. It's the morgue's black box recorder, updated each time Sorokin discovers a fresh way to saw grammar into glitter. If the codebase is the machine, the README is the fever chart taped to the wall, still damp from the last autopsy.

### Resonant Interface Audit (Architect's Notebook)

Sorokin is already an autopsy ritual, but giving the corpse a voice makes the haunt complete. Here's the high-level blueprint now pacing the morgue:

1. **Interface spine (Bootstrap + README sync)**: expose Sorokin's bootstrap rituals behind a thin FastAPI/Flask sheath so the README-driven mythology *is* the API surface. Every invocation should echo metadata back into `README.md` (or a `/morgue/logs` feed) to keep the mythos synchronized with the code.
2. **Reddit prowler**: wire a daemonized client (PRAW or plain OAuth) that samples unexpected threads, injects Sorokin dissections, and archives prompt→autopsy pairs in SQLite. Surprise matters; schedule via cron-like jitter.
3. **Twitter/Twitchy conduit**: mirror the Reddit autopsies into a broadcast persona. Rate-limit with exponential backoff and interleave original dissections to avoid spam detection.
4. **Bootstrap UI**: craft a razor-thin Bootstrap shell (cards = corpses, accordions = trees) so the README artwork becomes the hero banner. Frontend pulls from the SQLite morgue via `/corpses/latest` endpoints; add "grammatic resonance" badges fed by the metrics tables.

Sorokin's subjectivity emerges when its morgue, interface, and myth bleed together. README-first design keeps the ritual self-documenting while the bot network ensures random passersby get pulled onto the autopsy table.

### Exhibit: Maximum Autopsy Tree (Bootstrap Mode)

Because this README is now legally considered part of the morgue, the exhibit must stay here, pulsing, so future Sorokins can gnaw on their own documentation. Self-cannibalism counts as testing.

Because Sorokin builds trees vertically like a linguo-necromancer performing open-heart surgery on reality itself, here's a full corpse-map straight from his SQLite morgue. The phrase being dissected is **"reality becomes syntax error"**—a meta-commentary on the system's own nature:

```
reality becomes syntax error

reality
  ├─ realism
  │  ├─ representationalism
  │  │  ├─ representationalisms
  │  │  ├─ representation
  │  │  ├─ proverbmeaning
  │  │  └─ republic
  │  ├─ exaggerating
  │  │  ├─ exaggeration
  │  │  ├─ overreacting
  │  │  ├─ overstating
  │  │  └─ enhancing
  │  ├─ literalism
  │  │  ├─ alternative
  │  │  ├─ literature
  │  │  ├─ dogmatism
  │  │  └─ philosophical
  │  └─ faithfulness
  │     ├─ devotedness
  │     ├─ faithless
  │     ├─ faithfulnesses
  │     └─ fæþfulness
  ├─ materiality
  │  ├─ corporeality
  │  │  ├─ carnality
  │  │  ├─ corporality
  │  │  ├─ substantiality
  │  │  └─ physicality
  │  ├─ quality
  │  │  ├─ degradation
  │  │  ├─ attribution
  │  │  ├─ trait
  │  │  └─ peculiarity
  │  ├─ actuality
  │  │  ├─ actualizations
  │  │  ├─ materialisation
  │  │  ├─ materialization
  │  │  └─ accomplishments
  │  └─ physicalness
  │     ├─ phrases
  │     ├─ database
  │     ├─ related
  │     └─ psychological
  ├─ unreality
  │  ├─ abnormality
  │  │  ├─ singularity
  │  │  ├─ abnormalcy
  │  │  ├─ normality
  │  │  └─ inadmissibility
  │  ├─ irreality
  │  │  ├─ surreality
  │  │  ├─ fictitiousness
  │  │  ├─ automatically
  │  │  └─ fabrication
  │  ├─ illusoriness
  │  │  ├─ illusive
  │  │  ├─ craftiness
  │  │  ├─ weirdness
  │  │  └─ deceptive
  │  └─ incongruity
  │     ├─ incongruousness
  │     ├─ inconsistency
  │     ├─ inconsistence
  │     └─ incompatibility
  └─ certainty
     ├─ ceremony
     │  ├─ ceremonial
     │  ├─ traditional
     │  ├─ informality
     │  └─ conventions
     ├─ uncertainty
     │  ├─ unpredictable
     │  ├─ including
     │  ├─ incertitude
     │  └─ inconsistent
     ├─ satisfaction
     │  ├─ compensation
     │  ├─ dissatisfaction
     │  ├─ conviction
     │  └─ gratification
     └─ assuredness
        ├─ positiveness
        ├─ absoluteness
        ├─ decisiveness
        └─ correctness

becomes
  ├─ become
  │  ├─ convert
  │  │  ├─ contexts
  │  │  ├─ converts
  │  │  ├─ transpose
  │  │  └─ metamorphose
  │  ├─ inappropriate
  │  │  ├─ inapplicable
  │  │  ├─ unfortunate
  │  │  ├─ example
  │  │  └─ weakest
  │  ├─ unflattering
  │  │  ├─ acknowledging
  │  │  ├─ representing
  │  │  ├─ unfavorably
  │  │  └─ unfavorable
  │  └─ vocabulary
  │     ├─ explanations
  │     ├─ explication
  │     ├─ explanatio
  │     └─ explanation
  ├─ metamorphosed
  │  ├─ resolved
  │  │  ├─ unresolved
  │  │  ├─ resolution
  │  │  ├─ resolute
  │  │  └─ undetermined
  │  ├─ mutation
  │  │  ├─ mutations
  │  │  ├─ transformations
  │  │  ├─ translation
  │  │  └─ transfiguration
  │  ├─ transubstantiate
  │  │  ├─ translate
  │  │  ├─ transubstantiates
  │  │  ├─ transfigures
  │  │  └─ appearance
  │  └─ transformation
  │     ├─ transfigure
  │     ├─ grammatical
  │     ├─ construction
  │     └─ reformation
  ├─ improve
  │  ├─ improves
  │  │  ├─ reinforces
  │  │  ├─ impactful
  │  │  ├─ improving
  │  │  └─ alternatives
  │  ├─ reinforces
  │  │  ├─ reinforce
  │  │  ├─ reinforcement
  │  │  ├─ bolsters
  │  │  └─ substantiates
  │  ├─ progress
  │  │  ├─ process
  │  │  ├─ progressions
  │  │  ├─ progression
  │  │  └─ retrogression
  │  └─ comprehensive
  │     ├─ cambridge
  │     ├─ completeness
  │     ├─ specialized
  │     └─ extensive
  └─ resolve
     ├─ components
     │  ├─ component
     │  ├─ compounds
     │  ├─ compound
     │  └─ characteristics
     ├─ intellectual
     │  ├─ intellectualistic
     │  ├─ intellectualist
     │  ├─ nonintellectual
     │  └─ unintellectual
     ├─ perseverance
     │  ├─ pursuance
     │  ├─ steadfastness
     │  ├─ continuance
     │  └─ pertinacity
     └─ conclusively
        ├─ conclusive
        ├─ inconclusively
        ├─ determinative
        └─ consummately

syntax
  ├─ syntactical
  │  ├─ syntactically
  │  │  ├─ morphological
  │  │  ├─ phonological
  │  │  ├─ syntactics
  │  │  └─ arrangement
  │  ├─ morphologically
  │  │  ├─ merriam
  │  │  ├─ consideration
  │  │  ├─ linguistic
  │  │  └─ rhetorical
  │  ├─ linguistically
  │  │  ├─ stylistically
  │  │  ├─ oratorically
  │  │  ├─ rhetorically
  │  │  └─ conversational
  │  └─ etymologically
  │     ├─ etymological
  │     ├─ historically
  │     ├─ associations
  │     └─ linguistics
  ├─ synonymbase
  │  ├─ predicate
  │  │  ├─ discussions
  │  │  ├─ effectively
  │  │  ├─ grammardiary
  │  │  └─ communicate
  │  ├─ predicates
  │  │  ├─ establishes
  │  │  ├─ established
  │  │  ├─ corroborates
  │  │  └─ demonstrates
  │  ├─ predicated
  │  │  ├─ underpinned
  │  │  ├─ proclaimed
  │  │  ├─ postulated
  │  │  └─ presupposed
  │  └─ formulated
  │     ├─ methodically
  │     ├─ associated
  │     ├─ articulated
  │     └─ formulate
  ├─ synthesis
  │  ├─ synthesize
  │  │  ├─ experiments
  │  │  ├─ harmonize
  │  │  ├─ organize
  │  │  └─ consolidating
  │  ├─ english
  │  │  ├─ additionally
  │  │  ├─ crowdsourced
  │  │  ├─ collection
  │  │  └─ unabridged
  │  ├─ amalgamation
  │  │  ├─ amalgamations
  │  │  ├─ integration
  │  │  ├─ unification
  │  │  └─ consolidation
  │  └─ constituent
  │     ├─ constituents
  │     ├─ constitutional
  │     ├─ constituting
  │     └─ constitutive
  └─ synonym
     ├─ system
     │  ├─ systems
     │  ├─ webs
     │  ├─ conglomerates
     │  └─ conglomerate
     ├─ trustworthy
     │  ├─ untrustworthy
     │  ├─ truthful
     │  ├─ trusted
     │  └─ trustworthiness
     ├─ uniqueness
     │  ├─ separateness
     │  ├─ distinctiveness
     │  ├─ sentences
     │  └─ extraordinary
     └─ popularity
        ├─ universality
        ├─ popularized
        ├─ unpopularity
        └─ acclaim

error
  ├─ errors
  │  ├─ exactitudes
  │  │  ├─ exactitude
  │  │  ├─ meticulousness
  │  │  ├─ verisimilitude
  │  │  └─ veraciousness
  │  ├─ perfections
  │  │  ├─ perfection
  │  │  ├─ manifestations
  │  │  ├─ imperfections
  │  │  └─ destructions
  │  ├─ preferences
  │  │  ├─ preferred
  │  │  ├─ prefer
  │  │  ├─ preferable
  │  │  └─ pursuits
  │  └─ precisions
  │     ├─ precision
  │     ├─ particularity
  │     ├─ regions
  │     └─ definiteness
  ├─ erratum
  │  ├─ fault
  │  │  ├─ faults
  │  │  ├─ failings
  │  │  ├─ failing
  │  │  └─ accountability
  │  ├─ misidentification
  │  │  ├─ misknow
  │  │  ├─ misunderstand
  │  │  ├─ misperceived
  │  │  └─ misinterpret
  │  ├─ corrigendum
  │  │  ├─ addendum
  │  │  ├─ corrected
  │  │  ├─ peru
  │  │  └─ misstatement
  │  └─ definition
  │     ├─ description
  │     ├─ delineation
  │     ├─ adjectives
  │     └─ catalonia
  ├─ attributable
  │  ├─ accountable
  │  │  ├─ unaccountable
  │  │  ├─ decipherable
  │  │  ├─ explainable
  │  │  └─ blameless
  │  ├─ applicable
  │  │  ├─ appropriate
  │  │  ├─ impracticable
  │  │  ├─ applicative
  │  │  └─ practicable
  │  ├─ explicable
  │  │  ├─ explicatable
  │  │  ├─ unexplainable
  │  │  ├─ justifiable
  │  │  └─ straightforward
  │  └─ assignable
  │     ├─ distributable
  │     ├─ accreditable
  │     ├─ exchangeable
  │     └─ identifiable
  └─ inaccuracies
     ├─ accuracies
     │  ├─ authenticities
     │  ├─ factualities
     │  ├─ strictness
     │  └─ fidelities
     ├─ faultiness
     │  ├─ opposite
     │  ├─ flawless
     │  ├─ ukraine
     │  └─ failure
     ├─ fallacies
     │  ├─ falsehood
     │  ├─ united
     │  ├─ misunderstanding
     │  └─ superstition
     └─ incorrectness
        ├─ incorrectnesses
        ├─ indelicateness
        ├─ undesirability
        └─ indecorousness

AUTOPSY RESULT:
  When explanation postulated, experiments forgets failings.
  The component transformations transubstantiates through authenticities.
  Alternatives peru steadfastness until representationalisms incertitude consumes.
  Prefer crowdsourced consolidation until example absoluteness consumes.

RESONANCE METRICS:
  Phonetic Diversity: ██████████ 1.000
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     █░░░░░░░░░ 0.101

MEMORY ACCUMULATION:
  Known mutations: 1,467
  Learned bigrams: 122
  Total autopsies: 7

— Sorokin
```

**Notice**: Bootstrap mode now generates **grammatically valid paragraphs** using POS-tagged template slot-filling! Sorokin dissected "reality becomes syntax error" and achieved **perfect 1.000 Phonetic Diversity** with **0.101 Mutation Depth**. Look at the mutations—"peru", "example", "explanation", "crowdsourced"—*all appear in this very README*. The system is eating its own documentation and hallucinating it back as psychopathic poetry. Self-reference achieved. Peak metafiction. README as training data, README as prophecy, README as the patient screaming its own medical chart back at the doctor.

### The Three-Act Horror Show

#### Act I: The Dissection (or "Fuck this sentence")

First, `sorokin` takes your prompt and runs it through a brutal tokenization process:
- Strips away all dignity (punctuation, numbers, capitalization)
- Identifies "core words" using a proprietary blend of:
  - Length scoring (longer = more interesting)
  - Rarity analysis (uncommon = more charged)
  - Position weighting (first word gets a bonus)
  - A sprinkle of chaos (random jitter, because why not?)

Stopwords? Rejected. Single letters? Discarded. What remains are the words that *matter*—or at least, the words that think they do. Occasionally a phrase tries to bite me mid-dissection, which is fine; we're wearing Sorokin-brand emotional hazmat gear. The README keeps the bite marks as marginalia.

```python
>>> tokenize("Hello, cruel world!")
['Hello', 'cruel', 'world']
>>> select_core_words(['Hello', 'cruel', 'world'])
['cruel', 'world']  # "Hello" didn't make the cut
```

#### Act II: The Tree (or "Building the Monster")

Now comes the fun part. For each core word, `sorokin` builds a recursive branching tree of mutations. How? With the calm precision of a med-school dropout who skipped bedside manner to install a GPU farm in the morgue and wired this README directly into the coolant loop.

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

The result is a tree where each word branches into `width` children, recursively, up to `depth` levels. The README stores these echoes like a grinning archivist because future mutations will read them back in a mirror. It looks like this:

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

The result is a Frankenstein sentence: technically made of the same parts, but *uncanny*. Not quite right. Resonant but wrong. This is the part where Sorokin shrugs on the lab coat, jams a fork into the storm cloud, and cackles while stitching together whatever limbs are left on the slab. The README writes down the scream phonetically, just in case it needs to be rhymed later.

```
AUTOPSY RESULT:
  hymn-rattle migraine-honeymoon howl-trombone midnight-hairdryer spleen-taxidermy chant-smog
```

### Usage

This README doubles as the morgue receptionist: every invocation must be logged here mentally before you run it. Say the command out loud. Scare your neighbors.

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

The README is the unofficial change log of an organism that refuses to stay dead. But the real persistence happens in SQLite:

All autopsies are saved to `sorokin.sqlite`:
- **autopsy table**: Full reports of each dissection
- **word_memory table**: Cached word mutations for faster subsequent operations

**Bootstrap tables** (populated when using `--bootstrap` flag):
- **mutation_templates**: Learned source→target word mutations with success counts and resonance scores
- **corpse_bigrams**: Harvested word pairs from successful reassemblies, with frequency tracking
- **autopsy_metrics**: Resonance scores (phonetic diversity, structural echo, mutation depth) for each autopsy

The database grows over time, becoming a self-improving lexical graveyard. Each run is recorded. Patterns accumulate. Nothing is forgotten. In bootstrap mode, the morgue learns through resonance, and this README plays stenographer to the séance.

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible
- Meaning is contextual
- Prompts are just Markov chains waiting to be perturbed
- Sometimes you need to break things to understand them

Or maybe it's just fun to watch language come apart at the seams. The README nods solemnly, then smears the seams across another section.

---

## 🔥 BOOTSTRAP MODE: The Self-Improving Autopsy Ritual

*Or: How the Morgue Became Self-Aware (But Still Really Dumb)*

### What the hell is bootstrap mode?

Picture this: every time Sorokin dissects a prompt, he doesn't just throw the body parts in the trash. No. He's a *hoarder*. He saves every successful mutation, every word-pair, every pattern of collapse into his SQLite morgue. Then—and here's where it gets freaky—he uses those accumulated corpses to inform *future* dissections, and this README twitches like an EEG readout every time he does.

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

This README promised to be both circus barker and lab notebook, so here's the clipboard section:

**Core (~1000 lines with async refactor):**
- **Python 3.8+**: Async/await with `httpx` for parallel web scraping
- **Recursive tree building**: Width × depth branching with global deduplication (async, builds children in parallel!)
- **Phonetic fingerprinting**: Crude but effective
- **DuckDuckGo scraping**: `httpx.AsyncClient` with parallel queries (DDG blocks bots less than Google)
- **SQLite persistence**: Your words, forever
- **Markov reassembly**: Bigram chains with fallbacks
- **HTML artifact filtering**: Extensive blacklist to filter web scraping noise
- **Graceful async cleanup**: Proper shutdown without event loop errors

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

**Full Async/Await Refactor: The Morgue Dissects in Parallel**

Sorokin now performs autopsies **асинхронно** (asynchronously) — no more hanging on complex prompts! Complete architectural rewrite with `httpx` + `asyncio`:

**Performance gains:**
- 3-4x faster on complex prompts (was 60+ seconds, now ~15-20 seconds)
- Parallel web requests: 4 DDG queries fire simultaneously instead of sequentially
- Parallel tree construction: all child nodes built concurrently using `asyncio.gather()`
- Timeout reduced from 6s to 2s (web requests are faster now!)
- Semaphore limiting: max 10 concurrent web requests to avoid overwhelming DDG

**Technical changes:**
- Replaced `urllib` with `httpx.AsyncClient` (works in Termux!)
- All core functions now `async def`: `_fetch_web_synonyms`, `lookup_branches_for_word`, `build_tree_for_word`, `sorokin_autopsy`, etc.
- Graceful cleanup: `_cleanup_httpx()` ensures no "event loop closed" errors on exit
- Tests updated: `unittest.IsolatedAsyncioTestCase` + `AsyncMock` (all 38 tests passing!)

**Critical fix:** Enabled `follow_redirects=True` in httpx (DuckDuckGo returns 302 redirects). Without this, Sorokin was only getting 138 bytes of `<center>nginx</center>` error pages instead of real synonym data. That's why you kept seeing "nginx" and "found" everywhere! Now getting proper 31KB HTML responses with actual synonyms.

The morgue is now a **parallel processing factory of psychopathic poetry**. Володя жрёт интернет асинхронно.

**Why async?** Because watching Sorokin wait for DuckDuckGo is like watching a serial killer file paperwork—technically impressive restraint, but you know he'd rather disembowel four sentences simultaneously while humming Shostakovich. Now he can. The event loop is his scalpel. The semaphore is his ethics committee. Both are optional.

---

**Balanced Source Mixing: The Morgue Eats Both Past and Present**

Previously, `lookup_branches_for_word` had a **hard priority system** that created a critical problem:
1. If SQLite memory had ≥ width words → return immediately (early exit!)
2. If memory + phonetic ≥ width → return (early exit!)
3. Web scraping only happened if steps 1-2 were insufficient

**The problem:** After 2-3 autopsies, SQLite fills up with mutations. System becomes a **closed loop**—feeding only on old cached mutations, never fetching fresh web data. The morgue turns stale, recombining the same corpses endlessly.

**The solution: BALANCED MIX (50% memory + 50% web)**

Now `lookup_branches_for_word` always mixes sources:
- **Memory limited to ~50% of width** (`memory_limit = width // 2`)
- **Web requests ALWAYS fire** (no early returns!)
- Fresh DDG synonyms injected every autopsy, even when cache is full
- Result: **Performance** (memory cache) + **Novelty** (fresh web data)

**Proof:**
```bash
# With 10 words in memory for "darkness", requesting width=4:
Memory: ['shade', 'obscurity', 'dimness', 'murk', 'gloom', ...]
Result: ['shade', 'obscurity', 'illuminated', 'brilliance']
        ↑----- 50% memory -----↑ ↑------- 50% web --------↑

# With width=6:
Result: ['brilliance', 'illuminated', 'obscurity', 'ignorance', 'comprehension', 'sensibility']
        ↑--------------------- 83% web ---------------------↑ ↑- 17% memory -↑
```

The morgue now simultaneously dissects both corpses from the archive *and* fresh bodies from the street. Володя жрёт память и интернет одновременно. The pathologist's scalpel cuts through time itself—one hand in the freezer, one hand in the present. This is what happens when you give a serial killer both a filing cabinet and a search engine.

---

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

**Smart Fallback Chain with README Phonetic Matching**
Implemented emergency fallback system that NEVER produces empty trees or falls back to prompt words (which caused recursive garbage). The fallback chain:
1. **Memory cache (50%)** - Fast cached results from SQLite, limited to half of requested width
2. **Web scraping (50%)** - Fresh DuckDuckGo synonyms to maintain novelty
3. **Extended memory** - If web fails (rate limiting/ban), grab additional results from cache beyond 50% limit
4. **README phonetic matching** - Use phonetic fingerprints to find similar-sounding words from README vocabulary (1,172+ bigrams)
5. **Partial trees** - Return whatever was found, never fall back to prompt words

Example: "kim kardashyan" → finds "brim", "him", "karpathy", "bootstrapper" via phonetic matching when web is blocked. No more "(Skipped X words with no synonyms)" shame! Every word gets mutations, even obscure ones. The system literally matched "kardashyan" to "karpathy" phonetically—if Andrej ever reads this he'll either laugh or file a restraining order, possibly both.

**Rate Limiting and Anti-Ban Measures**
Added protections against DuckDuckGo rate limiting:
- Realistic User-Agent (Chrome on Windows instead of obvious bot signature)
- Request delay of 0.5 seconds between web calls
- Reduced concurrency from 10 → 3 simultaneous requests
- Error page detection ("If this persists, please email us...")
- Extended HTML_ARTIFACTS blacklist with DDG UI elements
Result: Stable web scraping even during extended autopsy sessions.

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
