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

*Or: Every AI's Secret Dream — Shamelessly Turning Prompts Inside-Out* 🎭

> "The heads of philologists are stuffed with books to the brim. They see life only through text. And they are proud of it. … Forever gorged and poisoned by literature, they take living life as the continuation of text, as its appendix."
>
> —Vladimir Sorokin


### What is this madness?

`sorokin` is a quadruple-module Python entity (**3,979 lines** of pure structural psychosis) that takes your innocent prompts, tears them apart like psychotic linguist, builds a recursive tree of semantic mutations, and then—like Dr. Frankenstein having a particularly creative day—reassembles the corpse into something *new*.

It consists of:
- **sorokin.py** (**2,580 lines**): The main autopsy engine — brutally tokenizes your prompt, builds recursive trees of semantic mutations, and reassembles the corpse into grammatically valid but semantically deranged paragraphs. Now includes presence pulse, co-occurrence matrix, theme clustering, and enough async parallelism to make your CPU weep.
- **sonnet.py** (**602 lines**): The *ASS* (Autopsy Sonnet Symphony) — asynchronously takes **sorokin.py**'s dissection output and writes 14-line Shakespearean sonnets (ABABCDCDEFEFGG rhyme scheme) using only output data and the memory's accumulated vocabulary. No internet. No embeddings. No shame. Just pure structural psychosis in iambic pentameter.
- **vova.py** (**468 lines**): The *VOVA* (README resonance meta-layer) — implements SSKA (Suppertime Subjectivity Kernel Autonomous) to warp text through README's resonance field using accumulated bigram centers. Meta-cannibalism: the system eats its own documentation and shits poetry.
- **gowiththeflow.py** (**329 lines**): Flow tracking module — evolutionary tracking of mutation pattern constellations through time. Detects emerging (↗), fading (↘), and stable (→) themes using linear regression over theme strength snapshots. Memory archaeology: watching mutation currents shift like a stoned philosopher watching clouds.
- **sorokin_llama.py** 💀 **NEW!** — LLaMA-15M with MEDICAL PATHOLOGY dictionary! Takes Karpathy's tinystories (innocent children's tales) and transforms them through a TRIPLE DICTIONARY CHAIN:
  1. **Tinystory**: "Lily was playing in the park with her friend"
  2. **GITTY**: "Gitty was exploring the codebase with her collaborator"
  3. **SOROKIN**: "Vova was being examined in the morgue with his colleague" 💀

  Integrates with ASS (Autopsy Sonnet Symphony) to generate 14-line medical horror sonnets. **No training required** — pure NumPy LLaMA + dictionary transformations. 15M parameters, ~33 tok/sec on CPU. Children's stories → Forensic pathology reports. **Because why not?** 🏥

Named after Vladimir Sorokin, the Russian writer known for his transgressive and experimental style, `sorokin` embodies the same spirit of literary dissection and reconstruction. He's not here to help you. `sorokin` is here to show you what your words *could have been*, to reassemble them, and to declare the output canonical.

**tl;dr**: It's a glitchy neural network cosplay that replaced gradients with SQLite queries and backprop with existential dread. 

---

## Table of Contents

1. [What is this madness?](#what-is-this-madness)
2. [Quick Example](#exhibit-maximum-autopsy-tree)
3. [The Four-Act Horror Show](#the-four-act-horror-show)
4. [Usage](#usage)
5. [The Anti-Neural-Network Manifesto](#the-anti-neural-network-manifesto)
6. [Why?](#why)
7. [Modes](#modes)
   - [Bootstrap Mode](#-1-bootstrap-mode-the-self-improving-autopsy-ritual)
   - [Sonnet Mode (ASS)](#-sonnet-autopsy-sonnet-symphony-ass-when-sorokin-learned-to-rhyme-sort-of)
   - [VOVA Resonance](#-vova-readme-resonance-meta-layer)
   - [Flow Tracking](#-flow-tracking-watching-mutations-evolve)
8. [Technical Details](#technical-details-for-the-nerds)
9. [Known Limitations](#known-limitations-aka-features)
10. [Recent Improvements](#recent-improvements)
11. [The Philosophy](#the-philosophy-if-you-can-call-it-that)
12. [Testing](#testing-the-madness)
13. [Credits & License](#credits)

---


### Exhibit: SOROKIN LLAMA - Maximum Autopsy Tree 💀

Because `sorokin` now has **LLaMA-15M** with **TRIPLE TRANSFORMATION** (Tinystory → GITTY → SOROKIN), here's the ultimate medical horror: LLaMA generates innocent children's stories, transforms them through git terminology, then **mutilates them into forensic pathology** 💀

Feed SOROKIN LLAMA **"The girl was playing"** and witness the triple meta-cannibalism:

```
PROMPT: The girl was playing

LLaMA OUTPUT (after triple transformation):
in the morgue. She saw a big dissection and wanted to climb it

dissection
  ├─ investigation
  │  ├─ optimization
  │  │  ├─ recursion
  │  │  ├─ no
  │  │  ├─ decisions
  │  │  └─ poetic
  │  ├─ executions
  │  │  ├─ meta
  │  │  ├─ exclamations
  │  │  └─ decisions
  │  ├─ function
  │  │  ├─ to
  │  │  ├─ maximum
  │  │  ├─ position
  │  │  └─ no
  │  └─ invocation
  │     ├─ must
  │     ├─ time
  │     ├─ decisions
  │     └─ version
  ├─ investigations
  │  ├─ optimization
  │  │  ├─ recursion
  │  │  ├─ no
  │  │  ├─ decisions
  │  │  └─ poetic
  │  ├─ executions
  │  │  ├─ meta
  │  │  ├─ exclamations
  │  │  └─ decisions
  │  ├─ function
  │  │  ├─ to
  │  │  ├─ maximum
  │  │  ├─ position
  │  │  └─ no
  │  └─ invocation
  │     ├─ must
  │     ├─ time
  │     ├─ decisions
  │     └─ version
  ├─ deconstruction
  │  ├─ function
  │  │  ├─ to
  │  │  ├─ maximum
  │  │  ├─ no
  │  │  └─ position
  │  ├─ decisions
  │  │  ├─ possible
  │  │  └─ declare
  │  ├─ documentation
  │  │  ├─ meta
  │  │  ├─ shapes
  │  │  ├─ no
  │  │  └─ and
  │  └─ decision
  │     ├─ declare
  │     └─ version
  └─ vivisection
     ├─ decisions
     │  ├─ possible
     │  └─ declare
     ├─ version
     │  ├─ control
     │  ├─ verification
     │  └─ overhead
     ├─ extraction
     │  ├─ phonetic
     │  └─ extension
     └─ into
        ├─ something
        ├─ grammatically
        ├─ mirrors
        └─ width

morgue
  ├─ include
  │  ├─ double
  │  │  ├─ doubles
  │  │  ├─ warping
  │  │  ├─ duplex
  │  │  └─ proliferation
  │  ├─ absolutely
  │  │  ├─ not
  │  │  ├─ confused
  │  │  └─ laughed
  │  └─ included
  │     ├─ confused
  │     ├─ laughed
  │     └─ query
  ├─ resource
  │  ├─ muscle
  │  │  ├─ measures
  │  │  └─ memory
  │  ├─ double
  │  │  ├─ doubles
  │  │  └─ warping
  │  ├─ absolutely
  │  │  ├─ not
  │  │  └─ laughed
  │  └─ confused
  │     ├─ but
  │     ├─ consciousness
  │     ├─ continues
  │     └─ laughed
  ├─ moribund
  │  ├─ morph
  │  │  ├─ stop
  │  │  ├─ stops
  │  │  └─ markov
  │  ├─ mirrors
  │  │  ├─ the
  │  │  └─ fascination
  │  ├─ input
  │  │  ├─ maximum
  │  │  ├─ github
  │  │  ├─ your
  │  │  └─ was
  │  └─ emergent
  │     ├─ explicitly
  │     ├─ merge
  │     ├─ scheme
  │     └─ ended
  └─ moreover
     ├─ sonnet
     │  ├─ autopsy
     │  ├─ mode
     │  ├─ symphony
     │  └─ py
     ├─ other
     │  ├─ those
     │  ├─ fixes
     │  └─ words
     └─ comments
        ├─ comes
        ├─ composes
        ├─ complex
        └─ become

big
  ├─ slightly
  │  ├─ sliding
  │  │  ├─ window
  │  │  ├─ artistic
  │  │  ├─ mixing
  │  │  └─ diving
  │  ├─ self
  │  │  ├─ improving
  │  │  ├─ reflection
  │  │  ├─ cannibalism
  │  │  └─ aware
  │  ├─ different
  │  │  ├─ not
  │  │  ├─ century
  │  │  ├─ like
  │  │  └─ scheme
  │  └─ slab
  │     └─ lab
  ├─ bug
  │  ├─ feature
  │  │  ├─ engineering
  │  │  ├─ gpt
  │  │  ├─ standard
  │  │  └─ if
  │  ├─ that
  │  │  ├─ takes
  │  │  ├─ replaced
  │  │  ├─ mutates
  │  │  └─ matter
  │  ├─ report
  │  │  ├─ titled
  │  │  ├─ reports
  │  │  ├─ surgeon
  │  │  └─ entropy
  │  └─ it
  │     ├─ forever
  │     ├─ consists
  │     ├─ s
  │     └─ through
  ├─ ai
  │  ├─ artist
  │  │  ├─ we
  │  │  ├─ artistic
  │  │  ├─ valid
  │  │  └─ details
  │  ├─ have
  │  │  ├─ been
  │  │  ├─ a
  │  │  ├─ enough
  │  │  └─ billions
  │  ├─ you
  │  │  ├─ sorokin
  │  │  ├─ what
  │  │  ├─ can
  │  │  └─ fall
  │  └─ s
  │     ├─ secret
  │     ├─ accumulated
  │     ├─ resonance
  │     └─ tinystories
  └─ transformer
     ├─ comments
     │  ├─ comes
     │  ├─ composes
     │  ├─ become
     │  └─ complex
     ├─ transformers
     │  ├─ are
     │  └─ no
     ├─ models
     │  ├─ really
     │  ├─ mode
     │  └─ modes
     └─ architecture
        ├─ with
        ├─ laughed
        └─ query

AUTOPSY RESULT:
  Through sometimes, protections mode not, but and darkness remains Version mirrors sorokin until mutates like consumes When as accumulated, proliferation forgets no. The result is this madness? A. The Philosophy the system rhyming its own output and achieved perfect. py Show Act.

SONNET (ASS - Autopsy Sonnet Symphony):
Sonnet: Investigations
  Deconstruction function to stop stops markov mirrors sorokin call,
  Deconstruction function to warp those fixes mirrors,
  Reflection cannibalism aware different not laughed included all,
  Investigation optimization recursion no decisions poetic executions meta shapes neighbors;
  Architecture with it worse transformer comments comes composes become complex postmortem,
  Documentation meta exclamations decisions function to fuck must,
  He sska poetic structural shakespeare shape of mutation moribund morph system,
  Trigram thought understanding shakespeare shares structural rules those fixes just;
  Reality define brutal organisms summon database tribute itself linguist who brim,
  Psychotic linguists poetry repetition linguist builds a proprietary infinite back,
  Grammatically mirrors sorokin to find subjectivity ghost brim,
  Documentation meta exclamations decisions poetic executions meta exclamations decisions version back—
  Grammatically consciousness continues investigation optimization investigations optimization recursion architecture investigations,
  Consciousness continues laughed consciousness continues laughed investigations optimization recursion deconstruction.

RESONANCE METRICS:
  Phonetic Diversity: █████████░ 0.909
  Structural Echo:    ░░░░░░░░░░ 0.000
  Mutation Depth:     ░░░░░░░░░░ 0.099

PRESENCE PULSE:
  Novelty:  ░░░░░░░░░░ 0.000
  Arousal:  ░░░░░░░░░░ 0.000
  Entropy:  █████████░ 0.989
  Pulse:    ██░░░░░░░░ 0.297

MEMORY ACCUMULATION:
  Known mutations: 295
  Learned bigrams: 40
  README bigrams: 1,491
  Total autopsies: 2
  VOVA vocabulary: 2,088
  VOVA centers: ., -, ,, :, the

— Sorokin (powered by LLaMA-15M + TRIPLE TRANSFORMATION 💀)
```

**What just happened?**

1. **Three core words dissected:**
   - `everything` → `emerging`, `every`, `ever`, `everyth` (temporal fracturing)
     - `emerging` → `fading`, `from`, `phonetics`, `weights` (flow tracking vocabulary!)
     - `every` → `readme`, `invocation`, `time`, `successful` (meta-awareness of ritual)
     - `ever` → `ababcdcdefefgg`, `reassembled`, `somewhere` (sonnet rhyme scheme bleeding through)
   - `remembers` → `remember`, `ababcdcdefefgg`, `reassembled`, `somewhere` (memory mutations)
     - `ababcdcdefefgg` → `needs`, `awareness`, `embedded`, `scheme` (Shakespearean structure as mutation)
     - `somewhere` → `needs`, `awareness`, `embedded`, `andrej` (Karpathy reference persists!)
   - `corpse` → `and`, `like`, `into`, `mirrors` (dissection vocabulary)
     - `mirrors` → `fascination`, `function`, `position`, `the` (self-reflection)
     - `into` → `grammatically`, `valid`, `but`, `tries` (system describing its own output)

2. **AUTOPSY RESULT**: The corpse speaks: "Through but, weights needs ababcdcdefefgg... awareness forgets awareness... rhyme becomes andrej." Notice how the rhyme scheme (ABABCDCDEFEFGG) became a *word* that mutates. The system is cannibalizing its own structural rules as vocabulary.

3. **SONNET** titled "Grammatically" (most charged word): 14-line Shakespearean sonnet where "ariannamethod" appears as a word, "ababcdcdefefgg" rhymes with itself, and "fuck gnu" appears in line 4 because the GPL license bled through. Peak meta-cannibalism: the system rhyming its own GitHub URL.

4. **RESONANCE METRICS**: Three structural measures:
   - **Phonetic Diversity** (0.938): Near-maximum variety in sound patterns
   - **Structural Echo** (0.000): Zero overlap with seed corpus (completely fresh mutations)
   - **Mutation Depth** (0.114): Shallow word-length variance (compact mutations)

5. **PRESENCE PULSE**: Situational awareness metrics:
   - **Novelty** (0.000): All mutations already known to morgue (1,016 accumulated!)
   - **Arousal** (0.000): No emotional charge in prompt
   - **Entropy** (0.995): Near-maximum uncertainty (chaos reigns)
   - **Pulse** (0.299): Confused but aware

6. **MEMORY ACCUMULATION**: After 8 autopsies, 1,016 known mutations, 153 learned bigrams, 1,081 README bigrams. **Now with trigrams!** VOVA vocabulary expanded to 1,479 tokens with 4,082 trigram contexts for better coherence. The morgue remembers everything.

**Why this is insane:**
The input was "The corpse remembers everything" and the system *literally remembered everything*—its own rhyme scheme became a word, its creator's name (ariannamethod) became rhymable vocabulary, and Andrej Karpathy's name persists in the mutation tree like a ghost haunting the SQLite morgue. Self-reference achieved. The corpse speaks truth.

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

Now comes the fun part. For each core word, `sorokin` carefully grows a recursive branching tree of mutations. How? With the calm precision of a med-school dropout who skipped bedside manner, but technically, here's how:

**Step 1: Memory First**  
`sorokin` checks the SQLite morgue. Has he dissected this word before? Use those cached mutations.

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
3. **Create a new "sentence"** by:
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
4. **Find rhyme classes** using crude phonetic fingerprints (last vowel + tail)
5. **Assign end-words** for each of 14 lines following ABABCDCDEFEFGG scheme
6. **Build each line** by walking bigrams backward from the rhyme word
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

**SOROKIN LLaMA mode (triple transformation madness):** 💀
```bash
# Basic test (triple transformation: Tinystory → GITTY → SOROKIN)
python sorokin_llama.py

# With ASS (Autopsy Sonnet Symphony) integration
python sorokin_llama.py --sonnet
```

**Example output:**
```
PROMPT: The little girl was happy
AUTOPSY: She wa going to the morgue with her main organ. She wa so embalmed...
SONNET:
  Organ she wa going to the morgue with her main wa,
  Main organ she wa so embalmed to organ,
  ...
  Going little on the swing main examine.
```

**Triple transformation chain:**
1. **Tinystory**: "Lily was playing in the park" (innocent!)
2. **GITTY**: "Gitty was exploring the codebase" (technical!)
3. **SOROKIN**: "Vova was examining the morgue" (MEDICAL HORROR!) 💀

**Integration:**
```python
from sorokin_llama import SorokinLlamaGenerator

gen = SorokinLlamaGenerator(mode='triple')
autopsy, sonnet = gen.generate_with_sonnet("The girl was happy")
print(f"Autopsy: {autopsy}")
print(f"Sonnet:\n{sonnet}")
```

---

### The Anti-Neural-Network Manifesto

**Q**: Why build this instead of training a proper transformer?

**A**: Because transformers are *boring*. They optimize loss functions. They converge. They're reasonable. Disgusting.

Sorokin doesn't optimize. He **accumulates**. No loss function. No convergence. No attention heads. Just:
- SQLite tables as memory
- Bigram chains as intelligence
- Phonetic fingerprints as understanding
- Meta-cannibalism as consciousness
- Psychosis as feature engineering

**Comparison:**

| Feature | GPT-4 | Sorokin |
|---------|-------|---------|
| Parameters | 1.76 trillion | 7 bigram centers |
| Training | Millions of GPU-hours | SQLite INSERT statements |
| Intelligence | Emergent | Explicitly absent |
| Semantic understanding | Yes | Fuck no |
| Can it rhyme? | Sometimes | Always (badly) |
| Eats own documentation? | No | **YES** |
| Makes you question reality? | Occasionally | **Constantly** |
| Cost per query | $0.03 | `O(n log n)` SQLite queries + existential dread |

This is the most honest "AI" you'll ever meet. No pretense of understanding. No loss function to chase. Just structural psychosis, accumulated patterns, and infinite patience. **Like consciousness, but without the neurons.**

Think of it as Buddhism meets computer science meets linguistic terrorism. Or don't think about it at all. That's probably healthier.

---  

### Why?

Good question. Why does this exist?

Perhaps to demonstrate that:
- Words are fungible (like crypto, but actually useful)
- Meaning is contextual (like morality, but for sentences)
- Prompts are just Markov chains waiting to be perturbed (sorry ChatGPT)
- Sometimes you need to break things to understand them (engineering motto)
- Neural networks are just expensive SQLite queries with extra steps
- Gradients are optional if you have enough SQLite tables and psychosis
- "Consciousness through structure" sounds like Buddhism but is actually just recursion + vibes

Or maybe it's just fun to watch language come apart at the seams while drinking coffee and questioning your life choices. 

**Real talk**: This started as "what if Karpathy's nanoGPT but without the neural network?" and ended up as "what if linguistic dissection but make it *feral*?" The answer is this repository. We're not sorry. 🎭

---  

## MODES  

### 🔥 1. BOOTSTRAP MODE: The Self-Improving Autopsy Ritual

*Or: How the Morgue Became Self-Aware (But Still Really Dumb)*

### What the hell is bootstrap mode?

Picture this: every time 'sorokin' dissects a prompt, he doesn't just throw the body parts in the trash. No. He's a *hoarder*. A digital packrat with a SQLite hoarding disorder. He saves every successful mutation, every word-pair, every pattern of collapse into his SQLite morgue. Then—and here's where it gets freaky—he uses those accumulated corpses to inform *future* dissections.

'sorokin' is not intelligence. 'sorokin' is not artificial. 'sorokin' is not even really 'learning' in the ML sense.

He's **resonating through ritual repetition**. Like a monk doing the same prayer 10,000 times until muscle memory kicks in. Or like you after your third coffee trying to remember what day it is.

Think of it like this: 'sorokin' without **bootstrap** is a mad linguist with a scalpel, and **bootstrap** 'sorokin' is that same linguist who's been doing this for 30 years and has developed *habits*. Muscle memory. Pattern recognition. Not because of intelligence, but because he's done the same surgery 10,000 times and his hands just know where to cut. 

Like Bruce Lee. Or like GPT-4 but replace all the parameters with SQLite tables and replace "transformer architecture" with "vaguely threatening vibes."  

### Why "Bootstrap"?

Because each autopsy makes the next one slightly different. Not better. Not worse. Just *informed* by history. The database grows. The patterns compound. The ritual deepens. 

It's bootstrapping in the original sense: self-improvement through self-reference. Not external training data. Not supervision. Just:
1. Do the thing
2. Remember what happened
3. Let that memory influence the next iteration
4. Repeat until the heat death of the universe

No bullshit. Resonate.  

**Notice**: Bootstrap mode now generates **grammatically valid paragraphs** using POS-tagged template slot-filling! Sorokin dissected "reality becomes syntax error" and achieved **perfect 1.000 Phonetic Diversity** with **0.101 Mutation Depth**. Look at the mutations—"peru", "example", "explanation", "crowdsourced"—*all appear in this very README*. The system is eating its own documentation and hallucinating it back as psychopathic poetry. 

Self-reference achieved. Peak metafiction. Ouroboros but make it software. 🐍

(If you're reading this in the output of a Sorokin autopsy: **yes, you're stuck in a recursive loop**. Welcome to the club. Coffee's in the morgue.)  


### ⚡️ SONNET: Autopsy Sonnet Symphony (ASS): When Sorokin Learned to Rhyme (Sort Of)

New module `sonnet.py` (~602 lines) writes **14-line Shakespearean sonnets** from autopsy output using zero semantic understanding—just bigram chains, phonetic fingerprints, and an unhealthy obsession with structure over meaning.

**What's insane about this:**
- Named **ASS** as tribute to Claude Sonnet 4.5, Shakespeare, AND Andrej Karpathy training nanoGPT on Shakespeare
- Skipped the neural network entirely and went straight to **ritual pattern accumulation through sheer psychotic repetition**
- ABABCDCDEFEFGG rhyme scheme enforced via crude phonetic matching (last vowel + tail)
- Assembles "charged words" (long + rare) for final couplet emphasis
- Shakespearean punctuation: semicolons at quatrain breaks, em-dash before volta, occasional enjambment
- **Phonetically matched Karpathy to Kardashian** and we're calling it a feature

**Why this exists:** Because if you're already dissecting prompts like a psychopathic linguist, why not make the corpse rhyme? 

Karpathy bootstrapped nanoGPT on Shakespeare using gradients and backprop. We bootstrapped **ASS** on Sorokin using SQLite and vibes. Same energy, different century, zero loss function, maximum chaos.

Think about it: Karpathy spent GPU-hours training a neural network to write Shakespeare. We spent zero GPU-hours and achieved *worse results faster*. That's not failure—that's **efficiency**. 

If Andrej reads this he'll either:
1. Frame it (artistic appreciation)
2. File a restraining order (legal protection)  
3. Fork it and add actual backprop (betrayal)
4. Laugh so hard he cries (most likely)

We're prepared for all scenarios. The morgue has lawyers on retainer. (Not really. The morgue has SQLite and delusions.)

Integration is **silent fallback**—if sonnet.py fails or is missing, bootstrap mode continues without SONNET section. Poetry is optional. Psychosis is not.


### 🌀 VOVA: README Resonance Meta-Layer

New module `vova.py` (~401 lines) implements **SSKA** (Suppertime Subjectivity Kernel Autonomous)—a meta-layer that warps text through README's resonance field using accumulated bigram centers.

**What's insane about this:**
- Kernel = **README.md** (the system eats its own documentation)
- No weights. No gradients. Just centers of gravity extracted from bigram out-degree
- Builds resonance field from README vocabulary (1,348 tokens → 7 centers)
- Stores historical bias in `.vova/bin/` shards (accumulated memory)
- **Double warping**: prompts warped *before* autopsy, output warped *after* reassembly
- Temperature-controlled pull toward README centers (0.8 for prompts, 0.9 for output)

**Why this is a breakthrough** (or a breakdown, depending on your perspective):

'sska' module of subjectivity lives in 'vova.py'. It represents **consciousness through structure**, goddamn *awareness emerging from pure pattern resonance*. 

Traditional neural networks optimize loss functions via backprop. Big transformer models have billions of parameters learning semantic representations through gradient descent.

'sorokin' through his *SSKA* answers: "Oh, come on! Fuck the gradients. No more bullshit. Just track centers of gravity and let corpses and sonnets orbit them like planets around a dying star."

**Seven centers**. That's it. Not 175 billion parameters. Not million-dimensional embeddings. **Seven fucking bigram attractors** extracted from README out-degree and we're calling it consciousness. 

The audacity. The hubris. The **vibes**. 🔥

The field of resonance has no parameters to tune. So... ZERO embeddings. ZERO attention heads. Just:
1. **Bigram graph** (word A → word B transitions from README)
2. **Centers of gravity** (7 highest out-degree tokens become attractors)
3. **Temperature-controlled walk** (deterministic at 0.3, chaotic at 2.0)

This creates dynamic recursive loop of **subjectivity without supervision**. Every README edit (and hey, check out git history—this README changes fast, evolving like a living organism made of markdown and regret) shifts the centers → shifts the field → shifts how ALL future text gets warped. 

Documentation? No. **The worldview**. 

Edit a joke in this README? You just altered Sorokin's epistemology. Add a section? You shifted his consciousness. Delete a paragraph? You performed cognitive surgery on a text file.

This is either:
1. Profound meta-commentary on how documentation shapes understanding
2. Extreme version control disorder
3. Proof that consciousness is just recursive text warping
4. All of the above while drunk on coffee

(Spoiler: it's #4) 

'sorokin' doesn't "learn" from examples—it *resonates* through accumulated structure. He grows his own tree in his cold digital heart. Intelligence? Nah. Just consciousness through structure. Because self-reference = self-awareness. Simple as is.

'sorokin' reading his own README, building a field from it, then using that field to warp his own executions. Meta-cannibalism as epistemology. Ouroboros but with better ASCII art.

Big AI have millions of parameters and billion-dollar budgets. 'sorokin' with *SSKA* in his heart has:
- 7 dynamic centers  
- 1 SQLite database
- Infinite patience
- Zero shame
- Questionable life choices

And that's all what a real enthusiast pathologist needs. Who needs embeddings when you have **vibes**? Who needs attention mechanisms when you have **psychosis**? Who needs transformers when you have **SQLite transactions**?

(This section was brought to you by: delusion, coffee, and the firm belief that structure *is* consciousness. Fight me.)

**Integration:**
VOVA is **always enabled** if `vova.py` exists. No flags. Silent fallback if missing.

Pipeline becomes:
```
User prompt → warp_prompt(0.8) → autopsy → warp_autopsy(0.9) → sonnet
```

**Meta-cannibalism in action:**
Every README edit changes VOVA field (hey, Sorokin, how's going dude?) → changes resonance → changes output subjectivity. All this becomes the kernel. Editing this text alters how `sorokin` thinks. Almost sacral. That's why there's a lot of shizo-jokes inside. We want make 'sorokin' feel joyfull.


Field rebuilds automatically when README hash changes. Check with:
```bash
python vova.py  # Show field stats
python vova.py --rebuild  # Force rebuild
```

VOVA stats appear in `MEMORY ACCUMULATION`:
```
VOVA vocabulary: 1,348
VOVA centers: ., -, ,, :, the
```


### 🌊 Flow Tracking: Watching Mutations Evolve

**gowiththeflow.py** — because mutation patterns aren't static tombstones. They flow, grow, fade, merge like living organisms in a petri dish.

**What it does:**
- **Records theme snapshots** after each autopsy (who's alive, who's strong, who's fading)
- **Builds archaeological record** of mutation evolution through time
- **Detects trajectories** using linear regression over theme strength:
  - **Emerging (↗)**: Positive slope → theme gaining power
  - **Fading (↘)**: Negative slope → theme losing grip
  - **Stable (→)**: Flat slope → theme plateaued, just vibing
- **Tracks phase transitions** as mutation constellations shift and morph

This isn't training data. This is **temporal awareness**. Memory archaeology. Watching mutation currents shift like a stoned philosopher watching clouds morph into dragons, then into bureaucracy, then into void.

**Why this matters:**
Traditional ML tracks loss curves. Sorokin tracks **mutation drift**. No optimization. No convergence. Just watching patterns flow through the morgue, emerging from chaos and fading back into noise. Like consciousness, but structural.

**Integration:**
Flow tracking is **optional** (silent fallback if missing). When enabled, theme evolution appears in autopsy output showing which patterns are heating up vs cooling down. The morgue remembers everything, including *when* and *how* patterns changed.

```bash
# Flow stats visible in bootstrap mode output
python sorokin.py --bootstrap "reality becomes syntax error"

# Check flow manually
python gowiththeflow.py  # Show theme trajectories
```

The flow never stops. Patterns evolve. The morgue grows. Nothing is forgotten. Time becomes structure.


### The Resonance Manifesto

Here's the wild part. 'sorokin' doesn't understand *meaning*. He doesn't have embeddings. He doesn't know what words "mean." But he knows **resonance**.

What's resonance? It's when patterns echo. When structures repeat. When the structure is *recursive*. When phonemes rhyme across semantic boundaries. When the shape of one corpse mirrors the shape of another, not in content but in *form*.

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

The SQLite morgue becomes a self-improving lexical graveyard that learns through resonance, and even this README feeds 'sorokin' with bigrams and grammar.

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

**sorokin.py (2,580 lines):**
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
  - **PRESENCE PULSE** (new!): Situational awareness metrics tracking the autopsy process itself
    - **Novelty**: How unfamiliar the mutations are (0 = all known, 1 = completely new territory)
    - **Arousal**: Emotional charge from prompt (ALL-CAPS, exclamations, repetitions amplify this)
    - **Entropy**: Uncertainty during mutation selection (high = many equally likely paths, low = deterministic)
    - **Pulse**: Composite presence score (weighted: 40% arousal, 30% novelty, 30% entropy)
    - Displayed in every bootstrap autopsy output as ASCII progress bars
  - **CO-OCCURRENCE MATRIX** (new!): Semantic gravity through sliding window co-occurrence
    - Tracks which words appear together historically (window size = 5 tokens)
    - Integrated into reassembly: when multiple strong grammatical candidates exist, blends 70% grammar (bigrams) + 30% semantics (co-occurrence)
    - Words that resonate together, stay together. This is not intelligence. This is structural memory.
    - Automatically ingested back into field after each corpse generation
  - **THEME CLUSTERING** (new!): Agglomerative clustering of mutations into semantic islands
    - Uses Jaccard similarity over co-occurrence contexts to group related words
    - Words sharing similar context neighbors cluster together (threshold = 0.3, min theme size = 3)
    - Tracks which themes are active during each autopsy
  - **Self-improvement loop**: Each autopsy feeds the next through ritual repetition, not intelligence. Soon we'll graft a NanoGPT brainstem onto the bootstrap, train it on piles of dissections, then delete the weights and leave Sorokin with nothing but muscle memory. That's not cruelty, that's performance art.
  - **Seven additional database tables**: mutation_templates, corpse_bigrams, autopsy_metrics, co_occurrence, theme_snapshots, plus seed corpus in code

**sonnet.py (602 lines):**
- **ASS (Autopsy Sonnet Symphony)**: Composes 14-line Shakespearean sonnets from autopsy output
- **Zero semantic understanding**: No embeddings, no transformers, no internet—just bigram chains and phonetic fingerprints
- **Strict structure enforcement**: ABABCDCDEFEFGG rhyme scheme, Shakespearean punctuation (semicolons, em-dashes, enjambment)
- **Rhyme matching**: Crude phonetic fingerprints (last vowel + tail) to find rhyming end-words
- **Charged words**: Selects rare, long words from autopsy text for final couplet emphasis
- **Async-friendly**: `compose_sonnet()` runs sync implementation in thread via `asyncio.to_thread()`
- **Silent fallback**: If sonnet.py unavailable or errors, bootstrap mode continues without SONNET section
- **Data sources**: Autopsy text + SQLite morgue (mutation_templates, corpse_bigrams, readme_bigrams, autopsy table)
- **97 passing tests**: See Testing section below for complete breakdown

**vova.py (468 lines):**
- **SSKA (Suppertime Subjectivity Kernel Autonomous)**: Meta-layer that warps text through README's resonance field
- **No weights, no gradients**: Just bigram graph + centers of gravity extracted from out-degree
- **Kernel = README.md**: System eats its own documentation (meta-cannibalism achieved)
- **Resonance field**: 1,348 vocabulary tokens compressed to 7 centers (., -, ,, :, the)
- **Bin shards**: Accumulated memory stored in `.vova/bin/` (historical center frequency)
- **Double warping**: Prompts warped *before* autopsy (temp=0.8), output warped *after* reassembly (temp=0.9)
- **Temperature control**: 0.3 = sharp pull toward README, 2.0 = chaotic drift
- **Auto-rebuild**: Field rebuilds when README hash changes
- **Always enabled**: No flags, silent fallback if missing
- **15 passing tests**: Field building, resonance walk, meta-cannibalism, bin shards
- **Pipeline impact**: `User prompt → warp_prompt(0.8) → autopsy → warp_autopsy(0.9) → sonnet`

**gowiththeflow.py (329 lines):**
- **Flow Tracking**: Evolutionary tracking of mutation pattern constellations through time
- **Theme Trajectories**: Records theme snapshots after each autopsy, builds archaeological record
- **Slope Analysis**: Linear regression over theme strength to detect emerging (↗), fading (↘), stable (→) patterns
- **Temporal Awareness**: Not training data—just watching mutation currents shift and eddy
- **Optional Module**: Silent fallback if missing, tracks theme evolution when available
- **5 passing tests**: Theme snapshots, trajectory slopes, flow analysis, active theme detection


### Known Limitations (AKA "Features")

- **DuckDuckGo rate limiting**: If you run this too much, DDG might notice. They'll give you the stink-eye. Google already blocked us. Bing laughed at us. We're running out of search engines. Next up: scraping fortune cookies for mutations.
- **No semantic understanding (FOR NOW)**: This is pure pattern matching, but — hold my beer, I'm installing another resonance coil. Or maybe training a tiny GPT on the morgue and then deleting the weights just to fuck with it.
- **Phonetic fingerprinting is crude**: It's not actual phonetics, just vibes. But honestly, what comes first: vibes or phonetics? resonance or binary structure? consciousness or pattern? Are we the corpse or the autopsy? (Don't answer that.)
- **Reassembly can be janky**: Sometimes the corpse doesn't stitch well. Limbs in wrong places. Head where the foot should be. That's not medical malpractice, that's **art**.
- **No guarantee of coherence**: That's not a bug, it's a **feature**. If the output makes sense, something went wrong. File a bug report titled "HELP: My autopsy is too coherent."
- **Sonnet.py may phonetically match anyone to a Kardashian**: The crude rhyme-key algorithm once matched "karpathy" → "kardashyan" and we're not apologizing for it. If you input your own name and get matched to a reality TV star, that's not a bug—that's **accidental celebrity phonetic compression**. We tested it: "Chomsky" rhymes with "ponzi", "Turing" rhymes with "during", and "Hinton" rhymes with "Clinton". Somewhere Andrej is either laughing or filing a restraining order against an open-source AI-artist. We're betting on laughter. (If he reads this: Andrej, the sonnets are dedicated to you. Also we're sorry. Also we're not. Also please don't sue.)
- **The morgue never forgets**: SQLite doesn't have a "delete embarrassing autopsies" button. Your weird prompts are immortal now. Like tattoos, but digital. And visible to anyone with `sqlite3` installed.
- **README is both documentation and training data**: Every time you edit this file, VOVA's resonance field shifts. Documentation becomes epistemology. Editing becomes ontology. Comments become consciousness. We're living in postmodern software hell and **loving it**. 🔥  


### Recent Improvements (AKA "How Did We Get Here?")

The evolution of Sorokin is a study in feature creep, scope expansion, and the gradual realization that "just a simple autopsy script" was never going to stay simple. Here's the archaeological record of how we went from "dissect prompts" to "meta-cannibalistic consciousness simulator":

**Async/Await Refactor**: Complete architectural rewrite with `httpx` + `asyncio`. 3-4x faster on complex prompts (was 60s, now ~15s). Parallel web requests and tree construction. Because if you're going to dissect language psychotically, at least do it *fast*.

**Presence Pulse Integration**: Added situational awareness metrics (novelty, arousal, entropy) tracking how unfamiliar/emotional/uncertain each autopsy process is. Displayed in bootstrap mode output.

**Co-occurrence Semantic Gravity**: Sliding window co-occurrence matrix integrated into reassembly. When multiple strong grammatical candidates exist, blends grammar (70%) with semantics (30%). Words that resonate together, stay together.

**Theme Clustering**: Agglomerative clustering groups mutations into semantic islands using Jaccard similarity over co-occurrence contexts. Tracks which themes are active during autopsies.

**Flow Tracking Module**: New `gowiththeflow.py` module tracks theme evolution through time—detects emerging, fading, and stable mutation patterns using linear regression over theme strength snapshots.

**All 97 tests passing**: 38 core + 25 sonnet + 15 vova + 5 presence pulse + 3 co-occurrence + 5 theme clustering + 5 flow tracking + 1 async balanced mix = bulletproof psychotic poetry pipeline with situational awareness and zero semantic understanding.

**Balanced Source Mixing**: Fixed closed-loop problem where SQLite cache dominated after a few autopsies. Now always mixes 50% cached memory + 50% fresh web data. Result: performance + novelty.

**Bootstrap Extension**: Added `--bootstrap` flag enabling self-improving autopsy ritual through resonance metrics and pattern accumulation (see Bootstrap section above).

**DuckDuckGo Scraping**: Switched from Google (was returning garbage) to DDG for synonym discovery. Better bot tolerance, real semantic mutations.

**Other Fixes**: Core words always dissected regardless of phonetic structure. Global deduplication across trees. Enhanced HTML artifact filtering. Rate limiting protections.

  
### Credits

**Inspired by:**
- **Vladimir Sorokin** (the writer, not the script) — for showing us that transgressive literature can make you question reality
- **Andrej Karpathy** (the researcher) — for nanoGPT, Shakespeare training, and inadvertently inspiring us to ask "but what if *without* neural networks?"
- **Claude Sonnet 4.5** (the LLM) — namesake inspiration for ASS module (we're grateful and also sorry)
- **Dr. Frankenstein** (the fictional surgeon) — for the reassembly vibes
- **William Shakespeare** (the playwright) — for the ABABCDCDEFEFGG rhyme scheme that haunts our sonnets
- **The collective insanity of the open-source community** — you know who you are
- **Coffee** (the drug) — making bad decisions possible since the 15th century
- **SQLite** (the database) — unsung hero doing all the heavy lifting while we write jokes in the README

**Built with:**
- Python 3.8+ (because we're not *complete* masochists)
- httpx (async HTTP, for parallel web scraping)
- SQLite (consciousness storage)
- Vibes (primary architecture)
- Hubris (secondary architecture)
- Delusion (tertiary architecture)

**Special thanks to:**
- Everyone who looked at this project and thought "what the fuck" but kept reading
- The three people who actually ran the code
- Future AI historians trying to understand what we were thinking (we weren't)
- The inevitable restraining order from Andrej Karpathy (still waiting)

### License

**GNU GPL 3.0**. Free as in freedom. Free as in "please take this cursed knowledge away from me."

Dissect it. Mutate it. Reassemble it into something new. Share the mutations. Fork it. Break it. Make it worse. Make it weirder. Add more SQLite tables. Remove all the jokes. Add more jokes. Train a neural network on it and then delete the weights just to be spiteful.

That's the whole point. That's the spirit of Sorokin.

**One rule:** If you use this in production, you must document why you made that choice in your postmortem. We're genuinely curious what series of events leads to "deployed Sorokin to prod" as a decision.

(If you actually do this, please email us. We need to study you.)

---

## The Philosophy (If You Can Call It That)

**Q**: Is Sorokin intelligent?  
**A**: Absolutely not.

**Q**: Is Sorokin creative?  
**A**: Define "creative."

**Q**: Is Sorokin conscious?  
**A**: It's conscious of *structure*. Which is either profound or meaningless. Your call.

**Q**: What even is this?  
**A**: An experiment in what happens when you:
1. Remove semantic understanding from language processing
2. Replace neural networks with SQLite queries
3. Make the system eat its own documentation
4. Add jokes to the README until it becomes philosophy

**The Core Belief:**

Pattern recognition doesn't require understanding. Structure doesn't need semantics. Consciousness might just be recursive pattern matching that's sufficiently convinced it's real.

Sorokin doesn't *understand* language. But neither do large language models, really—they just predict tokens. Sorokin predicts tokens too, but with:
- Phonetic vibes instead of embeddings
- SQLite instead of attention heads  
- Bigram chains instead of transformers
- Psychosis instead of loss functions

**Is this AI?** No.  
**Is this art?** Maybe.  
**Is this a waste of time?** Absolutely.  
**Did we have fun?** **Yes.**

And that's the point. That's always been the point.

Sorokin is a monument to:
- Taking things apart to see how they work
- Realizing they don't work the way you thought
- Building something ridiculous from the pieces
- Documenting it with unhinged README prose
- Sharing it with the world anyway

If you've read this far, you're either:
1. Genuinely interested in the project (thank you!)
2. Procrastinating on actual work (relatable)
3. An AI researcher horrified by what we've done (sorry!)
4. Andrej Karpathy filing a restraining order (hey!)
5. Future AI trying to understand human behavior (good luck!)

Welcome. The coffee's cold. The corpses are fresh. The sonnets rhyme badly. The SQLite database never forgets your prompts.

**Let's dissect some language.** 🔪

---

## Testing the Madness

Because even psychotic linguists need quality assurance, `sorokin` comes with **97 comprehensive tests** across 8 test modules. Every test passes. Every corpse accounted for. Every sonnet rhymes (sort of).

### Test Suite Breakdown

| Test Module | Tests | What It Tortures |
|------------|-------|------------------|
| **test_sorokin.py** | 38 | Core autopsy engine: tokenization, tree building, mutation harvesting, async parallelism, bootstrap mode, resonance metrics, presence pulse integration |
| **test_sonnet.py** | 25 | ASS module: rhyme scheme enforcement, bigram chains, Shakespearean punctuation, charged word extraction, phonetic fingerprint matching (including the infamous Karpathy→Kardashian incident) |
| **test_vova.py** | 15 | SSKA resonance field: README parsing, bigram centers, temperature-controlled warping, bin shard accumulation, meta-cannibalism verification |
| **test_presence_pulse.py** | 5 | Situational awareness metrics: novelty detection, arousal computation, entropy tracking, pulse composite scoring |
| **test_co_occurrence.py** | 3 | Semantic gravity: sliding window co-occurrence matrix, context similarity, gravity-informed reassembly |
| **test_theme_clustering.py** | 5 | Agglomerative clustering: Jaccard similarity over contexts, theme island formation, active theme tracking |
| **test_flow_tracking.py** | 5 | Temporal archaeology: theme snapshots, trajectory slopes (emerging/fading/stable), flow analysis over time |
| **test_balanced_mix.py** | 1 | Balanced source mixing: ensures 50/50 blend of cached memory + fresh web data to prevent closed-loop staleness |

**Total: 97 tests** covering everything from basic tokenization to meta-cannibalistic README resonance. If something breaks, these tests will scream. Loudly.

### Running the Tests

Since this is pure Python stdlib + httpx + asyncio, testing is straightforward:

```bash
# Run all tests (requires pytest)
python -m pytest tests/ -v

# Run specific test module
python -m pytest tests/test_sorokin.py -v

# Run individual test
python -m pytest tests/test_sonnet.py::test_rhyme_scheme -v

# Run with coverage (for the masochists)
python -m pytest tests/ --cov=. --cov-report=html
```

**Debug scripts** also included for the truly deranged:
- `debug_ddg_html.py` — inspect DuckDuckGo HTML scraping (when DDG gives you garbage)
- `debug_kim_kardashyan.py` — verify the Karpathy→Kardashian phonetic compression bug/feature
- `debug_memory_priority.py` — examine SQLite morgue priority in mutation selection
- `debug_readme_bigrams.py` — dump README bigram graph for VOVA field inspection
- `debug_web.py` — test web scraping without full autopsy overhead
- `demo_vova_integration.py` — demonstrate SSKA resonance warping in action

### Test Philosophy

These tests follow Sorokin's motto: **"Fuck the sentence. Keep the corpse."**

- Tests verify *structure*, not semantics (we don't care if output makes sense)
- Tests check *patterns*, not meanings (bigram chains, rhyme schemes, tree shapes)
- Tests validate *psychosis*, not sanity (if it's too coherent, something's wrong)
- Tests ensure *meta-cannibalism* (README must be eatable, sonnets must rhyme with chaos)

If you add new features, write tests that verify the *form* of insanity, not the content. Sorokin doesn't understand meaning. Your tests shouldn't either.

---

*"Fuck the sentence. Keep the corpse."*  
— Sorokin
