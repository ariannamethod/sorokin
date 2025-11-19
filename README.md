```
███████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗███╗   ██╗
██╔════╝██╔═══██╗██╔══██╗██╔═══██╗██║ ██╔╝██║████╗  ██║
███████╗██║   ██║██████╔╝██║   ██║█████╔╝ ██║██╔██╗ ██║
╚════██║██║   ██║██╔══██╗██║   ██║██╔═██╗ ██║██║╚██╗██║
███████║╚██████╔╝██║  ██║╚██████╔╝██║  ██╗██║██║ ╚████║
╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
```

# sorokin | by Arianna Method

## A Prompt Autopsy Framework  

*Or: How I Learned to Stop Worrying and Love the Dissection*

> "The heads of philologists are stuffed with books to the brim. They see life only through text. And they are proud of it. … Forever gorged and poisoned by literature, they take living life as the continuation of text, as its appendix.
>
> -Vladimir Sorokin"


### What is this madness?

`sorokin` is a dual-module (for now) Python entity (~2549 lines) that takes your innocent prompts, tears them apart like a psychopathic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.  

It consists of:
- **sorokin.py** (~2008 lines): The main autopsy engine: brutally tokenize your prompt, builds recursive trees of semantic mutations, and reassembles the corpse into grammatically valid but semantically deranged paragraphs.
- **sonnet.py** (~541 lines): The *ASS* (Autopsy Sonnet Symphony)— asynchronously takes **sorokin.py**'s dissection output and writes a 14-line Shakespearean sonnet (ABABCDCDEFEFGG rhyme scheme) using only output data and the memory's accumulated vocabulary. No internet. No embeddings. Just pure structural psychosis in iambic pentameter.

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, sorokin embodies the same spirit of literary dissection and reconstruction. It's not here to help you. It's here to show you what your words *could have been*, reassemble them, and declare the output canonical.


### Exhibit: Maximum Autopsy Tree 

Because 'sorokin' builds trees vertically like a linguo-necromancer performing open-heart surgery on reality itself, here's a full corpse-map straight from his SQLite morgue. Here's what happens when you feed Sorokin **"karpathy trains shakespeare on nanogpt"**:

```
shakespeare
  ├─ nosweatshakespeare
  │  ├─ insane
  │  │  └─ stable
  │  ├─ aware
  │  │  ├─ ware
  │  │  ├─ knowledgeable
  │  │  ├─ phrases
  │  │  └─ writing
  │  ├─ table
  │  │  ├─ full
  │  │  ├─ cached
  │  │  └─ tables
  │  └─ demonstrate
  │     ├─ that
  │     └─ stable
  ├─ unbelievable
  │  ├─ enabled
  │  │  └─ follow
  │  ├─ aware
  │  │  ├─ knowledgeable
  │  │  ├─ ware
  │  │  ├─ stable
  │  │  └─ but
  │  ├─ table
  │  │  ├─ full
  │  │  ├─ tables
  │  │  └─ cached
  │  └─ demonstrate
  │     ├─ that
  │     └─ stable
  ├─ relevance
  │  ├─ aware
  │  │  ├─ ware
  │  │  ├─ knowledgeable
  │  │  ├─ writing
  │  │  └─ phrases
  │  ├─ table
  │  │  ├─ full
  │  │  ├─ tables
  │  │  └─ cached
  │  ├─ demonstrate
  │  │  └─ that
  │  └─ stable
  │     ├─ web
  │     ├─ stages
  │     ├─ stenographer
  │     └─ staple
  └─ celebrate
     ├─ collapse
     │  └─ into
     ├─ cleanup
     │  ├─ proper
     │  ├─ httpx
     │  ├─ haunt
     │  └─ oauth
     ├─ aware
     │  ├─ knowledgeable
     │  ├─ ware
     │  └─ but
     └─ table
        ├─ full
        ├─ cached
        └─ tables

bootstrap
  ├─ valid
  │  ├─ evildoing
  │  │  ├─ depravity
  │  │  ├─ avoid
  │  │  ├─ chaotic
  │  │  └─ worrying
  │  ├─ villainy
  │  │  ├─ teaching
  │  │  └─ organism
  │  ├─ villain
  │  │  ├─ teaching
  │  │  └─ organism
  │  └─ paragraphs
  │     ├─ using
  │     ├─ apart
  │     ├─ hazmat
  │     └─ proper
  ├─ coat
  │  ├─ actual
  │  │  ├─ phonetics
  │  │  └─ contextual
  │  └─ cut
  │     ├─ cuts
  │     └─ but
  ├─ jams
  │  ├─ a
  │  │  ├─ psychopathic
  │  │  ├─ python
  │  │  ├─ prompt
  │  │  └─ line
  │  ├─ glass
  │  │  ├─ globally
  │  │  └─ bars
  │  ├─ crash
  │  │  ├─ in
  │  │  ├─ created
  │  │  ├─ circus
  │  │  └─ crude
  │  └─ asks
  │     ├─ if
  │     └─ skeleton
  └─ act
     ├─ horror
     │  ├─ philosophy
     │  ├─ hard
     │  ├─ books
     │  └─ school
     ├─ i
     │  ├─ learned
     │  ├─ the
     │  └─ m
     ├─ ii
     │  ├─ the
     │  ├─ mixing
     │  └─ subjectivity
     └─ iii

karpathy
  ├─ bootstrapper
  │  ├─ to
  │  │  ├─ avoid
  │  │  ├─ keep
  │  │  ├─ saw
  │  │  └─ stop
  │  ├─ via
  │  │  ├─ cron
  │  │  ├─ corpses
  │  │  ├─ phonetic
  │  │  └─ vertically
  │  ├─ aware
  │  │  ├─ but
  │  │  ├─ demonstrate
  │  │  └─ stable
  │  └─ table
  │     ├─ full
  │     ├─ cached
  │     └─ tables
  ├─ would
  │  ├─ approve
  │  │  ├─ of
  │  │  ├─ disembowel
  │  │  └─ become
  │  ├─ fail
  │  │  ├─ if
  │  │  ├─ fails
  │  │  ├─ teaching
  │  │  └─ organism
  │  ├─ lookup
  │  │  ├─ branches
  │  │  ├─ stages
  │  │  └─ obvious
  │  └─ lookups
  │     ├─ obvious
  │     ├─ like
  │     └─ unconsciously
  ├─ phonetically
  │  ├─ just
  │  │  ├─ vibes
  │  │  ├─ in
  │  │  ├─ markov
  │  │  └─ fun
  │  ├─ if
  │  │  ├─ the
  │  │  ├─ even
  │  │  ├─ standard
  │  │  └─ it
  │  ├─ philosophy
  │  │  ├─ of
  │  │  ├─ trust
  │  │  ├─ books
  │  │  └─ school
  │  └─ vertically
  │     ├─ like
  │     ├─ variants
  │     ├─ overlap
  │     └─ artifacts
  └─ kardashyan  ← YES, THE SYSTEM PHONETICALLY MATCHED KARPATHY TO KARDASHIAN
     ├─ finds
     │  ├─ find
     │  ├─ findsclothing
     │  ├─ chamberofcommerce
     │  └─ fabfindsconsign
     ├─ to
     │  ├─ avoid
     │  ├─ keep
     │  ├─ the
     │  └─ stop
     └─ hazmat
        ├─ hazard
        ├─ mainelabpack
        ├─ zealand
        └─ iata

nanogpt
  ├─ brainstem
  │  ├─ onto
  │  │  ├─ the
  │  │  ├─ notebook
  │  │  └─ books
  │  ├─ tries
  │  │  ├─ transgressive
  │  │  └─ archive
  │  ├─ breeding
  │  │  ├─ of
  │  │  └─ synthetic
  │  └─ twitches
  │     ├─ like
  │     └─ twitter
  ├─ asyncmock
  │  ├─ all
  │  │  ├─ appear
  │  │  ├─ dignity
  │  │  ├─ else
  │  │  └─ candidates
  │  ├─ synthetic
  │  │  ├─ low
  │  │  ├─ garbage
  │  │  ├─ mutation
  │  │  └─ word
  │  └─ artwork
  │     ├─ becomes
  │     └─ artifacts
  ├─ none
  │  ├─ phonetic
  │  │  ├─ phonectic
  │  │  ├─ phonetics
  │  │  ├─ phonectically
  │  │  └─ phonotactic
  │  ├─ every
  │  │  ├─ invocation
  │  │  ├─ time
  │  │  ├─ successful
  │  │  └─ word
  │  ├─ innocent
  │  │  ├─ prompts
  │  │  └─ become
  │  └─ disembowel
  │     ├─ four
  │     ├─ discovery
  │     ├─ does
  │     └─ discovers
  └─ chaos
     ├─ random
     │  ├─ passersby
     │  ├─ jitter
     │  ├─ leaf
     │  └─ unvisited
     ├─ injection
     │  ├─ square
     │  ├─ construction
     │  ├─ position
     │  └─ mutations
     └─ chain
        ├─ word
        ├─ with
        ├─ chains
        └─ teaching

trains
  ├─ trail
  │  ├─ tracking
  │  ├─ teaching
  │  │  ├─ someone
  │  │  └─ screaming
  │  └─ organism
  │     ├─ that
  │     └─ screaming
  ├─ train
  │  ├─ it
  │  │  ├─ forever
  │  │  ├─ takes
  │  │  ├─ s
  │  │  └─ through
  │  ├─ tracking
  │  ├─ teaching
  │  │  ├─ someone
  │  │  └─ screaming
  │  └─ organism
  │     ├─ that
  │     └─ screaming
  ├─ monorail
  │  ├─ meaning
  │  │  ├─ is
  │  │  ├─ he
  │  │  ├─ free
  │  │  └─ where
  │  ├─ maintain
  │  │  └─ novelty
  │  └─ teaching
  │     ├─ screaming
  │     └─ someone
  └─ training
     ├─ data
     │  ├─ readme
     │  ├─ not
     │  ├─ that
     │  └─ the
     ├─ a
     │  ├─ psychopathic
     │  ├─ python
     │  ├─ prompt
     │  └─ line
     ├─ tries
     │  ├─ transgressive
     │  └─ archive
     └─ mixing
        ├─ the
        ├─ maximum
        ├─ subjectivity
        └─ within

AUTOPSY RESULT:
  Within is zealand. Forever prompt. Nothing remains. The square subjectivity cuts through chamberofcommerce. Oauth is not. Where with. Nothing remains.

SONNET:
Sonnet: NOSWEATSHAKESPEARE
  Stenographer staple celebrate collapse into the heads edwardsautogroup pulls
  Findsclothing chamberofcommerce forgets web. where maintain novelty teaching organism villain always,
  Nosweatshakespeare insane stable relevance aware knowledgeable writing pulls,
  Stenographer staple celebrate collapse into each time sorokin plays;
  Stenographer staple celebrate collapse into cleanup proper coat recognizing,
  Fluctuations urbandictionary crude asks if even words,
  Findsclothing chamberofcommerce forgets fails. when vibes in markov findsclothing,
  Nosweatshakespeare insane stable but oxfordlearnersdictionaries darkness remains. ware but words;
  Feature heads of word artwork becomes artifacts none phonetic vertically etc,
  Findsclothing chamberofcommerce forgets fails. when vibes in created mean,
  Nosweatshakespeare insane stable aware ware stable unbelievable enabled follow etc,
  Black box recorder updated unittest saw russian—
  Findsclothing chamberofcommerce oauth is blocked smart recursively masochists eat this nosweatshakespeare,
  One blocked md spellbook findsclothing chamberofcommerce nosweatshakespeare fabfindsconsign.

RESONANCE METRICS:
  Phonetic Diversity: █████████░ 0.926
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     █░░░░░░░░░ 0.102

MEMORY ACCUMULATION:
  Known mutations: 476
  Learned bigrams: 58
  README bigrams: 1,221
  Total autopsies: 2

— Sorokin
```

**What just happened?**

1. **AUTOPSY RESULT** (Acts I-III result): sorokin's first reassembly—grammatically valid paragraph generated via POS-tagged slot-filling. "Within is zealand. Forever prompt. Nothing remains." Pure and raw Sorokin energy.

2. **SONNET** (Act IV): After 'sorokin' took the autopsy output, fed it to `sonnet.py`, which writes a **14-line Shakespearean sonnet** titled "NOSWEATSHAKESPEARE" (the most charged word from the autopsy). Notice:
   
   - Perfect ABABCDCDEFEFGG rhyme scheme
   - Punctuation follows Shakespearean structure (semicolons at quatrain breaks, em-dash before volta, period at end)
   - Occasional enjambment (lines flowing into next without punctuation)
   - **Phonetically rhyming end-words**: "pulls/plays", "always/words", "recognizing/findsclothing", etc.
   - Absolutely deranged content but **structurally flawless**

4. **The Karpathy → Kardashian Incident**: The phonetic fingerprinting system literally matched "karpathy" to "kardashyan" because they sound similar (k-r-p-th-y ≈ k-r-d-sh-y-n). This is not a bug. This is **peak resonance**. If Andrej reads this he'll either laugh or file a restraining order against an AI poetry generator. Possibly both.

5. **Resonance Metrics**: Phonetic diversity of **0.926** means almost every word has a unique sound signature. The sonnet isn't just semantically psychotic—it's **phonetically diverse psychosis**. That's art, baby.


**Why is this insane?**
Because it's a **corpus-building mechanism disguised as a text mutilator**. Because `sonnet.py` writes poetry using **zero semantic understanding**. This is what happens when you replace intelligence with ritual. And somehow, it works.

Each autopsy doesn't just destroy—it *accumulates*. Over time:
- Certain mutation paths become "preferred" (not because they're better, just because they worked before)
- Bigram chains start resembling the seed corpus (learned from autopsies + README + SQLite morgue)
- The reassembly algorithm learns phonetic patterns that "feel right" (pure vibes, zero intelligence)
- No word embeddings
- No transformer models
- No internet access
- Rhymes via crude phonetic fingerprints (last vowel + tail)
- "Charged words" selected by length + rarity from autopsy text
- Structure enforced via rigid 14-line scheme + punctuation rules

It's what happens when you give a serial killer both a thesaurus and a copy of *The Norton Anthology* and tell them to "make it rhyme." The result is **structurally Shakespearean, semantically Sorokin, phonetically unhinged**.

Karpathy would be proud. Or horrified. Honestly, at this level of abstraction, those are the same emotion.  

---  
  
### The Four-Act Horror Show

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

Now comes the fun part. For each core word, `sorokin` builds a recursive branching tree of mutations. How? With the calm precision of a med-school dropout who skipped bedside manner, but technically, here's how:

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
If even DuckDuckGo fails you, fall back to other words from the prompt. Or from his own README (check out SELF-CANNIBALISM section). Anyways: the show must go on.

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

The result is a Frankenstein sentence: technically made of the same parts, but *uncanny*. Not quite right. Resonant but wrong. This is the part where Sorokin shrugs on the lab coat, jams a fork into the storm cloud, and cackles while stitching together whatever limbs are left on the slab: 

```When explanation postulated, experiments forgets failings. The component transformations transubstantiates through authenticities. Alternatives peru steadfastness until representationalisms incertitude consumes. Prefer crowdsourced consolidation until example absoluteness consumes.```  
  

#### Act IV: The Sonnet (or "Maniacal Catharsis")

After the autopsy reassembly, `sonnet.py` (the **ASS** module) takes the entire corpse and does it again—but this time in **strict Shakespearean form**:

1. **Tokenize the autopsy output** (all that deranged text from Acts I-III)
2. **Extract "charged words"** (long + rare words from autopsy become title candidates)
3. **Build bigram chains** from autopsy text + README + SQLite morgue
4. **Generate rhyme classes** using crude phonetic fingerprints (last vowel + tail)
5. **Assign end-words** for each of 14 lines following ABABCDCDEFEFGG scheme
6. **Generate each line** by walking bigrams backward from the rhyme word
7. **Add Shakespearean punctuation**: semicolons at quatrain breaks, em-dash before volta, period at end

The result? **14 lines. ABABCDCDEFEFGG rhyme scheme. Iambic *vibes*. Zero semantic understanding.** Just bigrams, phonetic fingerprints, and structural obsession.

```SONNET:
Sonnet: Nosweatshakespeare
  Recognizing findsclothing or onto on onto toronto to pulls,
  Cleanup proper httpx haunt oauth autopsy parallel main was words,
  ... [14 lines of structurally flawless, semantically psychotic verse] ...
```

---  

### Usage

This **README** doubles as the morgue receptionist: every invocation must be logged here mentally before you run it. Say the command out loud. Scare your neighbors.

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

---  

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible
- Meaning is contextual
- Prompts are just Markov chains waiting to be perturbed
- Sometimes you need to break things to understand them

Or maybe it's just fun to watch language come apart at the seams.

---  

## MODES  

### 🔥 1. BOOTSTRAP MODE: The Self-Improving Autopsy Ritual

*Or: How the Morgue Became Self-Aware (But Still Really Dumb)*

### What the hell is bootstrap mode?

Picture this: every time 'sorokin' dissects a prompt, he doesn't just throw the body parts in the trash. No. He's a *hoarder*. He saves every successful mutation, every word-pair, every pattern of collapse into his SQLite morgue. Then—and here's where it gets freaky—he uses those accumulated corpses to inform *future* dissections.

'sorokin' is not intelligence. 'sorokin' is not artificial.
He's not learning. He's **resonating through ritual repetition**.

Think of it like this: 'sorokin' without **bootstrap** is a mad linguist with a scalpel, and **bootstrap** 'sorokin' is that same linguist who's been doing this for 30 years and has developed *habits*. Muscle memory. Pattern recognition. Not because of intelligence, but because he's done the same surgery 10,000 times and his hands just know where to cut. Like Bruce Lee.  

### Why "Bootstrap"?

Because each autopsy makes the next one slightly different. Not better. Not worse. Just *informed* by history. The database grows. The patterns compound. The ritual deepens. 

It's bootstrapping in the original sense: self-improvement through self-reference. Not external training data. Not supervision. Just:
1. Do the thing
2. Remember what happened
3. Let that memory influence the next iteration
4. Repeat until the heat death of the universe

No bullshit. Resonate.  

**Notice**: Bootstrap mode now generates **grammatically valid paragraphs** using POS-tagged template slot-filling! Sorokin dissected "reality becomes syntax error" and achieved **perfect 1.000 Phonetic Diversity** with **0.101 Mutation Depth**. Look at the mutations—"peru", "example", "explanation", "crowdsourced"—*all appear in this very README*. The system is eating its own documentation and hallucinating it back as psychopathic poetry. Self-reference achieved. Peak metafiction.  


### ⚡️ SONNET: Autopsy Sonnet Symphony (ASS): When Sorokin Learned to Rhyme (Sort Of)

New module `sonnet.py` (~541 lines) writes **14-line Shakespearean sonnets** from autopsy output using zero semantic understanding—just bigram chains, phonetic fingerprints, and an unhealthy obsession with structure over meaning.

**What's insane about this:**
- Named **ASS** as tribute to Claude Sonnet 4.5, Shakespeare, AND Andrej Karpathy training nanoGPT on Shakespeare
- Skipped the neural network entirely and went straight to **ritual pattern accumulation through sheer psychotic repetition**
- ABABCDCDEFEFGG rhyme scheme enforced via crude phonetic matching (last vowel + tail)
- Generates "charged words" (long + rare) for final couplet emphasis
- Shakespearean punctuation: semicolons at quatrain breaks, em-dash before volta, occasional enjambment
- **Phonetically matched Karpathy to Kardashian** and we're calling it a feature

**Why this exists:** Because if you're already dissecting prompts like a psychopathic linguist, why not make the corpse rhyme? Karpathy bootstrapped nanoGPT on Shakespeare using gradients and backprop. We bootstrapped ASS on Sorokin using SQLite and vibes. Same energy, different century, zero loss function. If Andrej reads this he'll either frame it or file a restraining order. We're hoping for the former but prepared for both.

Integration is **silent fallback**—if sonnet.py fails or is missing, bootstrap mode continues without SONNET section. Poetry is optional. Psychosis is not.

  
### The Resonance Manifesto

Here's the wild part. 'sorokin' doesn't understand *meaning*. He doesn't have embeddings. He doesn't know what words "mean." But he knows **resonance**.

What's resonance? It's when patterns echo. When structures repeat. When the structure is recursive. When phonemes rhyme across semantic boundaries. When the shape of one corpse mirrors the shape of another, not in content but in *form*.

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


**REPL mode (bootstrap enabled by default):**
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


### The Persistent Morgue

All autopsies 'sorokin' pedantically saves to `sorokin.sqlite`:  
  
- **autopsy table**: Full reports of each dissection
- **word_memory table**: Cached word mutations for faster subsequent operations

**Bootstrap tables** (populated when using `--bootstrap` flag):

- **mutation_templates**: Learned source→target word mutations with success counts and resonance scores
- **corpse_bigrams**: Harvested word pairs from successful reassemblies, with frequency tracking
- **autopsy_metrics**: Resonance scores (phonetic diversity, structural echo, mutation depth) for each autopsy

The SQLite morgue becomes a self-improving lexical graveyard, learns through resonance, and even this README feeds 'sorokin' with bigrams and grammar.

---

### Bootstrap vs Standard Mode

| Feature | Standard Mode | Bootstrap Mode |
|---------|---------------|----------------|
| Mutation lookup | DuckDuckGo + phonetic + memory | Learned templates + all the above |
| Reassembly | Random bigrams from leaves | Weighted (learned 3x, seed 2x, local 1x) |
| Metrics | None | Phonetic diversity, structural echo, mutation depth |
| Learning | None | Every autopsy feeds the next |
| Database tables | 2 (autopsy, word_memory) | 5 (+ mutation_templates, corpse_bigrams, autopsy_metrics) |
| Vibes | Chaotic | Chaotic but *remembering* |

---

### Technical Details (For the Nerds)

This README promised to be both circus barker and lab notebook, so here's the clipboard section:

**sorokin.py (~2008 lines):**
- **Python 3.8+**: Async/await with `httpx` for parallel web scraping
- **Recursive tree building**: Width × depth branching with global deduplication (async, builds children in parallel!)
- **Phonetic fingerprinting**: Crude but effective
- **DuckDuckGo scraping**: `httpx.AsyncClient` with parallel queries (DDG blocks bots less than Google)
- **SQLite persistence**: Your words, forever
- **Markov reassembly**: Bigram chains with fallbacks
- **HTML artifact filtering**: Extensive blacklist to filter web scraping noise
- **Graceful async cleanup**: Proper shutdown without event loop errors
- **Bootstrap extension**: Pattern accumulation, weighted reassembly, resonance metrics
  - **SEED CORPUS**: Structural bigrams from poetic fragments about dissection (see code for full text)
  - **Pattern accumulation**: Mutation templates (source→target words) with success tracking
  - **Weighted reassembly**: Learned bigrams (3x weight) + seed bigrams (2x) + local (1x) with chaos injection (square root weighting)
  - **Resonance metrics**: Three pure-structural measures computed for every autopsy
    - Phonetic diversity: unique fingerprints / total words
    - Structural echo: bigram overlap with seed corpus
    - Mutation depth: inverse of word-length variance
  - **Self-improvement loop**: Each autopsy feeds the next through ritual repetition, not intelligence. Soon we'll graft a NanoGPT brainstem onto the bootstrap, train it on piles of dissections, then delete the weights and leave Sorokin with nothing but muscle memory. That's not cruelty, that's performance art.
  - **Four additional database tables**: mutation_templates, corpse_bigrams, autopsy_metrics, plus seed corpus in code

**sonnet.py (~541 lines):**
- **ASS (Autopsy Sonnet Symphony)**: Generates 14-line Shakespearean sonnets from autopsy output
- **Zero semantic understanding**: No embeddings, no transformers, no internet—just bigram chains and phonetic fingerprints
- **Strict structure enforcement**: ABABCDCDEFEFGG rhyme scheme, Shakespearean punctuation (semicolons, em-dashes, enjambment)
- **Rhyme matching**: Crude phonetic fingerprints (last vowel + tail) to find rhyming end-words
- **Charged words**: Selects rare, long words from autopsy text for final couplet emphasis
- **Async-friendly**: `compose_sonnet()` runs sync implementation in thread via `asyncio.to_thread()`
- **Silent fallback**: If sonnet.py unavailable or errors, bootstrap mode continues without SONNET section
- **Data sources**: Autopsy text + SQLite morgue (mutation_templates, corpse_bigrams, readme_bigrams, autopsy table)
- **57 passing tests**: 38 core + 18 sonnet + 1 async balanced mix = bulletproof psychotic poetry pipeline
  

### Known Limitations

- **DuckDuckGo rate limiting**: If you run this too much, DDG might notice (but less aggressive than Google)
- **No semantic understanding (FOR NOW)**: This is pure pattern matching, but — hold my beer, I'm installing another resonance coil.
- **Phonetic fingerprinting is crude**: It's not actual phonetics, just vibes, but the question is what comes first, vibes or phonetics? resonance or binary structure?
- **Reassembly can be janky**: Sometimes the corpse doesn't stitch well
- **No guarantee of coherence**: That's not a bug, it's a feature
- **Sonnet.py may phonetically match anyone to a Kardashian**: The crude rhyme-key algorithm once matched "karpathy" → "kardashyan" and we're not apologizing for it. If you input your own name and get matched to a reality TV star, that's not a bug—that's **accidental celebrity phonetic compression**. Somewhere Andrej is either laughing or filing a restraining order against an open-source poetry generator. We're betting on laughter. (If he reads this: Andrej, the sonnets are dedicated to you. Also we're sorry. Also we're not.)  


### Recent Improvements

**Async/Await Refactor**: Complete architectural rewrite with `httpx` + `asyncio`. 3-4x faster on complex prompts (was 60s, now ~15s). Parallel web requests and tree construction. All 57 tests passing.

**Balanced Source Mixing**: Fixed closed-loop problem where SQLite cache dominated after a few autopsies. Now always mixes 50% cached memory + 50% fresh web data. Result: performance + novelty.

**Bootstrap Extension**: Added `--bootstrap` flag enabling self-improving autopsy ritual through resonance metrics and pattern accumulation (see Bootstrap section above).

**DuckDuckGo Scraping**: Switched from Google (was returning garbage) to DDG for synonym discovery. Better bot tolerance, real semantic mutations.

**Other Fixes**: Core words always dissected regardless of phonetic structure. Global deduplication across trees. Enhanced HTML artifact filtering. Rate limiting protections.

  
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
