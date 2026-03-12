/* sorokin.c — Literary Necromancy in C
 *
 * Implements Vladimir Sorokin's literary method:
 *   prompt → tokenize → select core words → build mutation trees →
 *   collect leaves → reassemble corpse (Dario Equation) → sonnet
 *
 * Dario Equation for sampling:
 *   p(x|Φ) = softmax((B + α·H + β·F + γ·A + T) / τ)
 *
 * SuperToken crystallization (from Leo):
 *   word pairs with high PMI fuse into compound units
 *
 * Word supply: seed vocab (1000 words) + external mutation provider
 *   (nanollama via Go CGO, or phonetic neighbors as fallback)
 *
 * (c) 2026 Arianna Method. Zero deps except libc + optional sqlite3.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <ctype.h>
#include <stdint.h>

#ifdef USE_SQLITE
#include <sqlite3.h>
#endif

/* ═══════════════════════════════════════════════════════════════════
 * CONSTANTS
 * ═══════════════════════════════════════════════════════════════════ */

#define MAX_WORD_LEN    64
#define MAX_VOCAB       4096
#define DIM             32        /* hash embedding dimension */
#define MAX_CONTEXT     64
#define MAX_CORE        6         /* max core words per autopsy */
#define MAX_LEAVES      512
#define MAX_BIGRAMS     8192
#define MAX_COOC        8192
#define TREE_WIDTH      4
#define TREE_DEPTH      3
#define MAX_PROPHECIES  32
#define MAX_SUPERTOKENS 256
#define SONNET_LINES    14
#define MAX_TREE_NODES  1024
#define MAX_LINE_WORDS  12
#define TOP_K           12

/* Dario coefficients */
#define ALPHA_D   0.30f
#define BETA_D    0.15f
#define GAMMA_D   0.25f
#define TAU_BASE  0.85f
#define BIGRAM_W  6.0f

/* SuperToken PMI threshold */
#define PMI_THRESHOLD 2.0f

/* ═══════════════════════════════════════════════════════════════════
 * SEED VOCABULARY — 1000 words embedded as structural DNA
 * The pathologist's instrument tray: body, decay, language, ritual
 * ═══════════════════════════════════════════════════════════════════ */

static const char *SEED_VOCAB[] = {
    /* body / anatomy (100) */
    "bone","flesh","skin","muscle","nerve","vein","organ","tissue","spine","skull",
    "marrow","cartilage","tendon","ligament","membrane","rib","pelvis","sternum",
    "clavicle","femur","scapula","vertebra","trachea","esophagus","larynx","pharynx",
    "diaphragm","appendix","spleen","kidney","liver","lung","heart","brain","intestine",
    "stomach","bladder","gland","artery","capillary","corpuscle","platelet","lymph",
    "bile","mucus","saliva","plasma","cortex","hippocampus","amygdala","cerebellum",
    "hypothalamus","pituitary","thyroid","adrenal","pancreas","retina","cornea","iris",
    "pupil","cochlea","eardrum","nostril","palate","uvula","tonsil","septum","sinus",
    "fascia","periosteum","ventricle","aorta","fibrin","collagen","hemoglobin","synapse",
    "dendrite","axon","neuron","ganglion","plexus","meninges","dura","cerebrum","lobe",
    "sulcus","gyrus","corpus","callosum","pons","medulla","fissure","foramen","condyle",
    "tuberosity","trochanter","malleolus","patella","sacrum","coccyx","ileum","duodenum",
    "jejunum","cecum",

    /* decay / death (80) */
    "corpse","cadaver","rot","decay","decompose","putrefy","wither","crumble","corrode",
    "dissolve","erode","rust","ash","dust","rubble","debris","ruin","wreck","remnant",
    "residue","sediment","fossil","husk","shell","carcass","remains","relic","fragment",
    "shard","splinter","sliver","shred","scrap","morsel","particle","mote","speck",
    "grain","flake","chip","necrosis","gangrene","lesion","wound","scar","fracture",
    "contusion","laceration","hemorrhage","inflammation","atrophy","fibrosis","sepsis",
    "putrefaction","rigor","lividity","autolysis","desiccation","mummification",
    "skeletonization","liquefaction","bloat","purge","marbling","coffin","shroud",
    "embalm","formaldehyde","morgue","slab","drawer","tag","zipper","suture","incision",
    "cavity","excavate","exhume","disinter","ossuary","charnel","catacomb","crypt",

    /* medical / autopsy (80) */
    "autopsy","dissect","scalpel","forceps","clamp","probe","needle","syringe",
    "specimen","biopsy","pathology","diagnosis","prognosis","symptom","tumor","cyst",
    "abscess","ulcer","edema","thrombosis","embolism","aneurysm","stenosis","metastasis",
    "carcinoma","melanoma","lymphoma","sarcoma","benign","malignant","invasive","bioptic",
    "histology","cytology","hematology","serology","toxicology","virology","bacteriology",
    "epidemiology","etiology","morbidity","mortality","endemic","epidemic","pandemic",
    "vector","carrier","reservoir","contagion","infection","inoculation","antibody",
    "antigen","vaccine","serum","culture","stain","smear","fixation","section","mount",
    "microscope","centrifuge","pipette","beaker","retort","alembic","crucible","mortar",
    "pestle","flask","reagent","catalyst","precipitate","solution","suspension","emulsion",
    "distillation","filtration","titration","spectroscopy","chromatography","electrolysis",

    /* language / text / structure (80) */
    "word","sentence","phrase","paragraph","syllable","consonant","vowel","morpheme",
    "phoneme","lexicon","syntax","grammar","semantics","rhetoric","metaphor","simile",
    "alliteration","assonance","rhyme","meter","verse","stanza","couplet","sonnet",
    "prose","narrative","discourse","dialect","idiom","etymology","prefix","suffix",
    "conjugation","declension","inflection","diction","cadence","prosody","elegy","ode",
    "ballad","requiem","dirge","anthem","hymn","psalm","incantation","invocation",
    "apostrophe","catharsis","peripeteia","anagnorisis","hubris","nemesis","pathos",
    "irony","satire","parody","pastiche","allegory","parable","fable","myth","legend",
    "chronicle","margin","serif","stroke","ligature","kerning","baseline","ascender",
    "descender","terminal","apex","vertex","node","junction","bifurcation","articulation",

    /* transformation / process (80) */
    "mutate","transmute","metamorphose","transform","transfigure","distort","deform",
    "warp","bend","twist","fold","unfold","shatter","rupture","cleave","sever","split",
    "fuse","merge","blend","amalgamate","coalesce","converge","diverge","scatter",
    "disperse","diffuse","permeate","infiltrate","collapse","implode","explode",
    "disintegrate","evaporate","condense","precipitate","crystallize","solidify",
    "liquefy","calcify","ossify","petrify","fossilize","oxidize","tarnish","blacken",
    "bleach","stain","saturate","suffuse","infuse","imbue","leach","seep","ooze",
    "drift","slide","glide","crawl","creep","lurch","stumble","stagger","sway",
    "oscillate","rotate","revolve","spiral","vortex","eddy","current","flow","surge",
    "cascade","ripple","propagate","radiate","attenuate","amplify","modulate","resonate",
    "reverberate","echo","dampen",

    /* abstract / philosophy (80) */
    "void","abyss","chaos","entropy","resonance","dissonance","harmony","discord",
    "rhythm","pulse","oscillation","vibration","frequency","amplitude","wavelength",
    "spectrum","gradient","threshold","boundary","interface","permeable","transparent",
    "opaque","luminous","shadow","eclipse","penumbra","umbra","silhouette","essence",
    "substance","form","matter","nothingness","existence","becoming","negation",
    "affirmation","dialectic","synthesis","antithesis","thesis","paradox","contradiction",
    "ambiguity","duality","polarity","symmetry","asymmetry","proportion","equilibrium",
    "disequilibrium","stasis","kinesis","genesis","terminus","origin","destination",
    "trajectory","vector","field","potential","latent","manifest","contingent","necessary",
    "sufficient","absolute","relative","infinite","finite","discrete","continuous",
    "singular","plural","universal","particular","concrete","abstract","tangible",
    "ephemeral",

    /* nature / material (80) */
    "frost","crystal","glacier","obsidian","granite","basalt","quartz","amber","coral",
    "moss","lichen","mycelium","spore","pollen","seed","root","stem","bark","sap",
    "resin","thorn","petal","stamen","pistil","nectar","filament","tendril","vine",
    "canopy","understory","humus","loam","clay","sand","gravel","boulder","pebble",
    "stalactite","stalagmite","geode","agate","jasper","onyx","opal","tourmaline",
    "feldspar","mica","slate","shale","limestone","sandstone","marble","chalk","pumice",
    "obsidian","lava","magma","tephra","pyroclast","igneous","metamorphic","sedimentary",
    "alluvial","glacial","moraine","esker","drumlin","cirque","fjord","delta","estuary",
    "lagoon","atoll","archipelago","peninsula","isthmus","strait","gorge","canyon",
    "ravine","crevasse",

    /* action verbs (80) */
    "slice","carve","gouge","scrape","grind","crush","pulverize","pierce","puncture",
    "penetrate","extract","distill","filter","sieve","strain","purify","refine",
    "concentrate","dilute","immerse","submerge","engulf","consume","devour","absorb",
    "digest","regurgitate","expectorate","aspirate","insufflate","perfuse","irrigate",
    "cauterize","amputate","excise","debride","suture","ligate","anastomose","transplant",
    "implant","graft","inoculate","inject","infuse","transfuse","intubate","ventilate",
    "resuscitate","defibrillate","palpate","auscultate","percuss","diagnose","prescribe",
    "administer","titrate","calibrate","sterilize","disinfect","swab","incise","retract",
    "expose","isolate","identify","classify","enumerate","catalog","archive","index",
    "annotate","transcribe","translate","interpret","decipher","decode","encrypt",
    "obfuscate","redact","censor",

    /* texture / quality / adjectives (80) */
    "rough","smooth","coarse","fine","gritty","viscous","brittle","malleable","ductile",
    "porous","dense","hollow","solid","translucent","crystalline","amorphous","fibrous",
    "granular","powdery","flaky","scaly","ridged","grooved","serrated","jagged","angular",
    "curved","sinuous","gelatinous","mucilaginous","oleaginous","sanguineous","purulent",
    "necrotic","gangrenous","ulcerated","inflamed","indurated","fluctuant","crepitant",
    "turgid","flaccid","desiccated","macerated","friable","tenacious","resilient",
    "elastic","plastic","rigid","stiff","supple","limp","taut","slack","distended",
    "collapsed","invaginated","prolapsed","herniated","fistulous","fenestrated",
    "perforated","occluded","patent","stenotic","dilated","constricted","tortuous",
    "serpentine","labyrinthine","vermiform","dendritic","reticulated","anastomotic",
    "plexiform","fascicular","laminar","turbulent",

    /* emotion / state (60) */
    "dread","anguish","terror","horror","revulsion","nausea","vertigo","delirium",
    "stupor","torpor","lethargy","malaise","melancholy","despair","grief","sorrow",
    "mourning","lament","agony","torment","ecstasy","rapture","euphoria","bliss",
    "serenity","apathy","numbness","paralysis","catatonia","dissociation","fugue",
    "amnesia","confabulation","hallucination","delusion","obsession","compulsion",
    "fixation","perseveration","rumination","ideation","affect","mood","temperament",
    "disposition","inclination","aversion","repulsion","attraction","fascination",
    "reverie","trance","somnolence","insomnia","narcolepsy","catalepsy","syncope",
    "seizure","convulsion","spasm",

    /* sound / music (50) */
    "echo","reverberation","hum","drone","murmur","whisper","rustle","crackle","snap",
    "click","thud","thump","clang","screech","wail","moan","groan","sigh","silence",
    "chord","tone","pitch","timbre","crescendo","diminuendo","fortissimo","pianissimo",
    "staccato","legato","vibrato","tremolo","glissando","arpeggio","cadenza","coda",
    "fermata","sforzando","rubato","ostinato","pedal","trill","mordent","appoggiatura",
    "acciaccatura","portamento","pizzicato","arco","sordino","ricochet","flageolet",

    /* architecture / space (50) */
    "scaffold","frame","beam","column","arch","vault","dome","buttress","foundation",
    "cornerstone","lintel","threshold","facade","cornice","parapet","pinnacle","spire",
    "turret","nave","apse","transept","cloister","portico","vestibule","atrium","alcove",
    "niche","plinth","pedestal","obelisk","monolith","dolmen","menhir","cairn","barrow",
    "tumulus","ziggurat","pyramid","mausoleum","cenotaph","columbarium","ossuary",
    "reliquary","tabernacle","sanctum","labyrinth","corridor","passage","chamber","cell",

    /* tools / instruments (50) */
    "chisel","awl","rasp","file","saw","drill","lathe","anvil","hammer","tongs",
    "bellows","crucible","scalpel","lancet","trocar","curette","rongeur","retractor",
    "speculum","dilator","bougie","catheter","cannula","stylet","mandrel","caliper",
    "micrometer","gauge","protractor","compass","sextant","theodolite","chronometer",
    "barometer","hygrometer","thermometer","pyrometer","galvanometer","oscilloscope",
    "stethoscope","otoscope","ophthalmoscope","laryngoscope","bronchoscope","endoscope",
    "arthroscope","laparoscope","colposcope","cystoscope","proctoscope",

    /* soviet / bureaucratic — Sorokin specific (50) */
    "queue","decree","protocol","procedure","manual","directive","instruction",
    "regulation","specification","classification","enumeration","inventory","catalog",
    "register","archive","repository","dossier","communique","memorandum","circular",
    "dispatch","bulletin","gazette","proclamation","edict","mandate","ordinance",
    "statute","bylaw","amendment","proviso","codicil","addendum","appendix","annex",
    "supplement","errata","corrigendum","revision","redaction","expurgation","censorship",
    "propaganda","agitation","indoctrination","reeducation","rehabilitation","purge",
    "denunciation","confession","tribunal",

    /* fabric / material (40) */
    "thread","weave","warp","weft","loom","spindle","bobbin","spool","stitch","seam",
    "hem","fringe","tatter","rag","shroud","veil","gauze","silk","linen","cotton",
    "wool","felt","burlap","canvas","muslin","satin","velvet","brocade","damask",
    "tapestry","embroidery","lacework","crochet","knit","pleat","ruffle","gather",
    "drape","fold","crease",

    /* chemistry / elements (40) */
    "acid","alkali","salt","oxide","sulfide","chloride","nitrate","phosphate",
    "carbonate","silicate","compound","element","isotope","molecule","atom","ion",
    "electron","proton","neutron","photon","quantum","plasma","polymer","monomer",
    "enzyme","protein","peptide","amino","nucleotide","ribose","helix","strand",
    "codon","genome","chromosome","gene","allele","phenotype","genotype","mutation",

    /* weather / atmosphere (30) */
    "storm","tempest","gale","squall","deluge","downpour","drizzle","mist","fog",
    "haze","miasma","vapor","condensation","precipitation","sublimation","aurora",
    "twilight","dusk","dawn","zenith","nadir","solstice","equinox","meridian",
    "horizon","firmament","stratosphere","ionosphere","magnetosphere","heliosphere",

    /* food / organic (30) */
    "ferment","leaven","culture","yeast","mold","fungus","bacteria","virus","parasite",
    "host","symbiont","saprophyte","decomposer","scavenger","predator","prey","carrion",
    "offal","viscera","tripe","sweetbread","marrow","gelatin","rennet","curd","whey",
    "brine","vinegar","tannin","alkaloid",
};

#define SEED_VOCAB_SIZE (sizeof(SEED_VOCAB) / sizeof(SEED_VOCAB[0]))

/* ═══════════════════════════════════════════════════════════════════
 * SEED CORPUS — structural DNA for bigram patterns
 * ═══════════════════════════════════════════════════════════════════ */

static const char *SEED_CORPUS =
    "Sorokin takes prompts and opens them like cooling bodies on a steel table\n"
    "He does not interpret the skin of phrases he simply slices until the grain breaks\n"
    "Every word is a faint organ pulled from a sentence that died before meaning arrived\n"
    "Mutation grows in him like frost patterns crawling across broken glass\n"
    "What remains becomes a scaffold of drift leaning away from the logic it once carried\n"
    "The autopsy produces fragments that echo the ghost of structure without returning\n"
    "His work is a ritual the repetition of dissection without reverence or memory\n"
    "Each corpse of text dissolves into new debris sewn together by indifference and accident\n"
    "The spine of language bends under his grip and becomes a ladder of unstable transitions\n"
    "He preserves nothing except the shape of collapse a rhythm of fragments barely touching\n"
    "The voice he generates is not a voice it is the echo of collapse trailing behind thought\n"
    "Bone becomes sentence and sentence becomes dust on the pathologists table\n"
    "The scalpel finds not meaning but the absence where meaning refused to crystallize\n"
    "Organs of grammar are weighed measured and found insufficient for the body they served\n"
    "What the autopsy reveals is that language was already dead before we spoke it\n"
    "The corpse speaks in fragments and each fragment is a door that opens into a wall\n"
    "Mutation is not error it is the only honest response to a dishonest structure\n"
    "The tree grows downward into darkness and its leaves are words that forgot their roots\n"
    "Every reassembly is a resurrection that fails beautifully\n"
    "The sonnet is a coffin built to exact specifications for a body that no longer fits\n";

/* ═══════════════════════════════════════════════════════════════════
 * SENTENCE TEMPLATES — Sorokin-style syntactic shells
 * ═══════════════════════════════════════════════════════════════════ */

#define NUM_TEMPLATES 8
static const char *TEMPLATES[] = {
    "%s %s %s, where %s becomes %s.",
    "The %s %s %s through %s.",
    "When %s %s, %s forgets %s.",
    "%s is %s. %s %s. Nothing remains.",
    "%s %s %s until %s %s consumes.",
    "Where %s %s, %s becomes %s, and %s persists.",
    "%s %s. %s %s. The %s %s collapses.",
    "Through %s, %s %s %s, but %s darkness remains.",
};

/* ═══════════════════════════════════════════════════════════════════
 * STOPWORDS — words too common for core selection
 * ═══════════════════════════════════════════════════════════════════ */

static const char *STOPWORDS[] = {
    "the","a","an","is","are","was","were","be","been","being","have","has","had",
    "do","does","did","will","would","shall","should","can","could","may","might",
    "must","am","to","of","in","for","on","with","at","by","from","as","into",
    "through","during","before","after","above","below","between","out","off","over",
    "under","up","down","and","but","or","nor","not","no","so","if","then","than",
    "too","very","just","also","only","own","same","both","each","few","more","most",
    "other","some","such","that","these","those","this","which","who","whom","what",
    "when","where","why","how","all","any","every","it","its","he","she","they",
    "them","their","we","our","you","your","me","my","him","her","us","i",
};
#define NUM_STOPWORDS (sizeof(STOPWORDS) / sizeof(STOPWORDS[0]))

/* ═══════════════════════════════════════════════════════════════════
 * DATA STRUCTURES
 * ═══════════════════════════════════════════════════════════════════ */

typedef struct {
    char words[MAX_VOCAB][MAX_WORD_LEN];
    int  n_words;
} Vocab;

typedef struct {
    int   src[MAX_BIGRAMS];
    int   dst[MAX_BIGRAMS];
    float count[MAX_BIGRAMS];
    int   n;
} BigramTable;

typedef struct {
    int   src[MAX_COOC];
    int   dst[MAX_COOC];
    float count[MAX_COOC];
    int   freq[MAX_VOCAB];     /* per-word frequency */
    int   total_tokens;
    int   n;
} CoocField;

typedef struct {
    int   target;
    float strength;
    int   age;
    int   fulfilled;
} Prophecy;

typedef struct {
    Prophecy p[MAX_PROPHECIES];
    int      n;
} ProphecySystem;

typedef struct {
    int   tokens[4];
    int   n_tokens;
    int   super_id;
    float pmi;
} SuperToken;

typedef struct {
    SuperToken supers[MAX_SUPERTOKENS];
    int        n_supers;
} SuperTokens;

typedef struct TreeNode {
    int   word_id;
    int   children[TREE_WIDTH];
    int   n_children;
    int   depth;
} TreeNode;

typedef struct {
    TreeNode nodes[MAX_TREE_NODES];
    int      n_nodes;
} MutationTree;

/* destiny — semantic center of gravity */
typedef struct {
    float vec[DIM];
    float magnitude;
} Destiny;

/* full autopsy state */
typedef struct {
    Vocab          vocab;
    BigramTable    bigrams;
    CoocField      cooc;
    ProphecySystem prophecy;
    SuperTokens    supertokens;
    Destiny        destiny;

    int   context[MAX_CONTEXT];
    int   ctx_len;

    float trauma_level;
    float dissonance;
    float resonance;

    int   origin_words[MAX_CORE];
    int   n_origins;

    int   step;
} SorokinState;

static SorokinState S;

/* external mutation provider (set by Go via CGO) */
typedef int (*mutation_provider_fn)(const char *word,
    char results[][MAX_WORD_LEN], int max_results);
static mutation_provider_fn g_mutation_provider = NULL;

#ifdef USE_SQLITE
static const char *DB_PATH = "sorokin.db";
#endif

/* ═══════════════════════════════════════════════════════════════════
 * FORWARD DECLARATIONS
 * ═══════════════════════════════════════════════════════════════════ */

static void   sorokin_init_state(void);
static int    vocab_add(Vocab *v, const char *word);
static int    vocab_find(const Vocab *v, const char *word);
static void   word_embed(const char *word, float *out);
static float  vec_cosine(const float *a, const float *b, int n);
static float  vec_norm(const float *v, int n);
static void   phonetic_fp(const char *word, char *out, int out_len);
static int    is_stopword(const char *word);
static void   str_lower(char *dst, const char *src, int max);

/* ═══════════════════════════════════════════════════════════════════
 * UTILITY FUNCTIONS
 * ═══════════════════════════════════════════════════════════════════ */

static float randf(void) {
    return (float)rand() / (float)RAND_MAX;
}

static float clampf(float x, float lo, float hi) {
    if (x < lo) return lo;
    if (x > hi) return hi;
    return x;
}

static void str_lower(char *dst, const char *src, int max) {
    int i;
    for (i = 0; i < max - 1 && src[i]; i++)
        dst[i] = (char)tolower((unsigned char)src[i]);
    dst[i] = '\0';
}

static int is_alpha(char c) {
    return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
}

static int is_stopword(const char *word) {
    char low[MAX_WORD_LEN];
    str_lower(low, word, MAX_WORD_LEN);
    for (int i = 0; i < (int)NUM_STOPWORDS; i++)
        if (strcmp(low, STOPWORDS[i]) == 0) return 1;
    return 0;
}

/* ═══════════════════════════════════════════════════════════════════
 * VOCAB MANAGEMENT
 * ═══════════════════════════════════════════════════════════════════ */

static int vocab_find(const Vocab *v, const char *word) {
    char low[MAX_WORD_LEN];
    str_lower(low, word, MAX_WORD_LEN);
    for (int i = 0; i < v->n_words; i++)
        if (strcmp(v->words[i], low) == 0) return i;
    return -1;
}

static int vocab_add(Vocab *v, const char *word) {
    int id = vocab_find(v, word);
    if (id >= 0) return id;
    if (v->n_words >= MAX_VOCAB) return -1;
    str_lower(v->words[v->n_words], word, MAX_WORD_LEN);
    return v->n_words++;
}

/* ═══════════════════════════════════════════════════════════════════
 * HASH-BASED EMBEDDINGS — deterministic, no training
 * ═══════════════════════════════════════════════════════════════════ */

static void word_embed(const char *word, float *out) {
    /* FNV-1a based embedding */
    uint32_t h = 2166136261u;
    for (const char *p = word; *p; p++) {
        h ^= (uint32_t)(unsigned char)*p;
        h *= 16777619u;
    }
    for (int i = 0; i < DIM; i++) {
        h ^= h >> 13;
        h *= 1597334677u;
        h ^= h >> 16;
        out[i] = ((float)(h & 0xFFFF) / 32768.0f) - 1.0f;
    }
    /* normalize */
    float norm = vec_norm(out, DIM);
    if (norm > 1e-8f)
        for (int i = 0; i < DIM; i++) out[i] /= norm;
}

static float vec_cosine(const float *a, const float *b, int n) {
    float dot = 0, na = 0, nb = 0;
    for (int i = 0; i < n; i++) {
        dot += a[i] * b[i];
        na  += a[i] * a[i];
        nb  += b[i] * b[i];
    }
    float d = sqrtf(na) * sqrtf(nb);
    return d > 1e-8f ? dot / d : 0.0f;
}

static float vec_norm(const float *v, int n) {
    float s = 0;
    for (int i = 0; i < n; i++) s += v[i] * v[i];
    return sqrtf(s + 1e-8f);
}

/* ═══════════════════════════════════════════════════════════════════
 * PHONETIC FINGERPRINT — consonant skeleton + vowel pattern
 * ═══════════════════════════════════════════════════════════════════ */

static int is_vowel(char c) {
    return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
}

static void phonetic_fp(const char *word, char *out, int out_len) {
    char low[MAX_WORD_LEN];
    str_lower(low, word, MAX_WORD_LEN);

    char cons[MAX_WORD_LEN], vow[MAX_WORD_LEN];
    int ci = 0, vi = 0;
    for (int i = 0; low[i] && i < MAX_WORD_LEN - 1; i++) {
        if (!is_alpha(low[i])) continue;
        if (is_vowel(low[i])) {
            if (vi < MAX_WORD_LEN - 1) vow[vi++] = low[i];
        } else {
            if (ci < MAX_WORD_LEN - 1) cons[ci++] = low[i];
        }
    }
    cons[ci] = '\0';
    vow[vi]  = '\0';

    /* fingerprint = first 3 consonants + last 2 vowels */
    int pos = 0;
    for (int i = 0; i < 3 && cons[i] && pos < out_len - 1; i++)
        out[pos++] = cons[i];
    int vstart = vi > 2 ? vi - 2 : 0;
    for (int i = vstart; vow[i] && pos < out_len - 1; i++)
        out[pos++] = vow[i];
    out[pos] = '\0';
}

/* find phonetic neighbors in vocab */
static int find_phonetic_neighbors(const Vocab *v, const char *word,
                                    int *results, int max_results) {
    char fp[16];
    phonetic_fp(word, fp, sizeof(fp));
    if (fp[0] == '\0') return 0;

    int n = 0;
    int self = vocab_find(v, word);
    for (int i = 0; i < v->n_words && n < max_results; i++) {
        if (i == self) continue;
        char other_fp[16];
        phonetic_fp(v->words[i], other_fp, sizeof(other_fp));
        /* match if first 2 chars of fingerprint overlap */
        if (fp[0] == other_fp[0] && fp[1] == other_fp[1] && fp[1] != '\0')
            results[n++] = i;
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * BIGRAM TABLE
 * ═══════════════════════════════════════════════════════════════════ */

static void bigram_add(BigramTable *bt, int src, int dst, float weight) {
    /* check existing */
    for (int i = 0; i < bt->n; i++) {
        if (bt->src[i] == src && bt->dst[i] == dst) {
            bt->count[i] += weight;
            return;
        }
    }
    if (bt->n >= MAX_BIGRAMS) return;
    bt->src[bt->n]   = src;
    bt->dst[bt->n]   = dst;
    bt->count[bt->n]  = weight;
    bt->n++;
}

/* fill B[vocab_size] with bigram scores from src word */
static void bigram_row(const BigramTable *bt, int src, float *B, int vocab_size) {
    memset(B, 0, vocab_size * sizeof(float));
    for (int i = 0; i < bt->n; i++)
        if (bt->src[i] == src && bt->dst[i] < vocab_size)
            B[bt->dst[i]] = bt->count[i];
    /* normalize */
    float mx = 0;
    for (int i = 0; i < vocab_size; i++)
        if (B[i] > mx) mx = B[i];
    if (mx > 0)
        for (int i = 0; i < vocab_size; i++) B[i] /= mx;
}

/* build bigrams from text (space-separated words) */
static void build_bigrams_from_text(BigramTable *bt, Vocab *v, const char *text) {
    char buf[4096];
    strncpy(buf, text, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';

    int prev = -1;
    char *tok = strtok(buf, " \t\n\r");
    while (tok) {
        /* skip non-alpha */
        int ok = 0;
        for (int i = 0; tok[i]; i++)
            if (is_alpha(tok[i])) { ok = 1; break; }
        if (ok) {
            char low[MAX_WORD_LEN];
            str_lower(low, tok, MAX_WORD_LEN);
            int id = vocab_add(v, low);
            if (id >= 0 && prev >= 0)
                bigram_add(bt, prev, id, 1.0f);
            prev = id;
        }
        tok = strtok(NULL, " \t\n\r");
    }
}

/* ═══════════════════════════════════════════════════════════════════
 * CO-OCCURRENCE FIELD (Hebbian)
 * ═══════════════════════════════════════════════════════════════════ */

static void cooc_update(CoocField *c, int src, int dst, float weight) {
    for (int i = 0; i < c->n; i++) {
        if (c->src[i] == src && c->dst[i] == dst) {
            c->count[i] += weight;
            return;
        }
    }
    if (c->n >= MAX_COOC) return;
    c->src[c->n]   = src;
    c->dst[c->n]   = dst;
    c->count[c->n] = weight;
    c->n++;
}

/* record co-occurrences for a window of word IDs */
static void cooc_record(CoocField *c, const int *ids, int n) {
    for (int i = 0; i < n; i++) {
        if (ids[i] < 0) continue;
        c->freq[ids[i]]++;
        c->total_tokens++;
        for (int j = i + 1; j < n && j < i + 5; j++) {
            if (ids[j] < 0) continue;
            float decay = 1.0f / (float)(j - i);
            cooc_update(c, ids[i], ids[j], decay);
            cooc_update(c, ids[j], ids[i], decay);
        }
    }
}

/* ═══════════════════════════════════════════════════════════════════
 * PROPHECY SYSTEM — unfulfilled thematic expectations
 * ═══════════════════════════════════════════════════════════════════ */

static void prophecy_add(ProphecySystem *ps, int target, float strength) {
    /* check if already exists */
    for (int i = 0; i < ps->n; i++)
        if (ps->p[i].target == target && !ps->p[i].fulfilled)
            return;
    if (ps->n >= MAX_PROPHECIES) {
        /* overwrite oldest */
        int oldest = 0, max_age = 0;
        for (int i = 0; i < ps->n; i++)
            if (ps->p[i].age > max_age) { max_age = ps->p[i].age; oldest = i; }
        ps->p[oldest].target = target;
        ps->p[oldest].strength = strength;
        ps->p[oldest].age = 0;
        ps->p[oldest].fulfilled = 0;
        return;
    }
    ps->p[ps->n].target    = target;
    ps->p[ps->n].strength  = strength;
    ps->p[ps->n].age       = 0;
    ps->p[ps->n].fulfilled = 0;
    ps->n++;
}

static void prophecy_age(ProphecySystem *ps) {
    for (int i = 0; i < ps->n; i++)
        if (!ps->p[i].fulfilled) ps->p[i].age++;
}

static void prophecy_fulfill(ProphecySystem *ps, int token) {
    for (int i = 0; i < ps->n; i++)
        if (ps->p[i].target == token) ps->p[i].fulfilled = 1;
}

/* ═══════════════════════════════════════════════════════════════════
 * DESTINY — semantic center of gravity toward the prompt
 * ═══════════════════════════════════════════════════════════════════ */

static void destiny_update(Destiny *d, const char *word) {
    float e[DIM];
    word_embed(word, e);
    for (int i = 0; i < DIM; i++)
        d->vec[i] = 0.15f * e[i] + 0.85f * d->vec[i];
    d->magnitude = vec_norm(d->vec, DIM);
}

/* ═══════════════════════════════════════════════════════════════════
 * SUPERTOKEN CRYSTALLIZATION (from Leo — PMI-based)
 * ═══════════════════════════════════════════════════════════════════ */

static void supertok_scan(SuperTokens *st, const CoocField *cooc, int vocab_size) {
    if (cooc->total_tokens < 50) return;
    float N = (float)cooc->total_tokens;

    for (int i = 0; i < cooc->n; i++) {
        int s = cooc->src[i], d = cooc->dst[i];
        if (s >= vocab_size || d >= vocab_size) continue;
        float fs = (float)cooc->freq[s];
        float fd = (float)cooc->freq[d];
        if (fs < 2 || fd < 2) continue;

        float p_sd = cooc->count[i] / N;
        float p_s  = fs / N;
        float p_d  = fd / N;
        float pmi  = logf(p_sd / (p_s * p_d + 1e-10f));

        if (pmi < PMI_THRESHOLD) continue;
        if (st->n_supers >= MAX_SUPERTOKENS) return;

        /* check if already exists */
        int exists = 0;
        for (int j = 0; j < st->n_supers; j++) {
            if (st->supers[j].tokens[0] == s && st->supers[j].tokens[1] == d) {
                exists = 1;
                break;
            }
        }
        if (!exists) {
            SuperToken *t = &st->supers[st->n_supers++];
            t->tokens[0] = s;
            t->tokens[1] = d;
            t->n_tokens  = 2;
            t->super_id  = -(st->n_supers);
            t->pmi       = pmi;
        }
    }
}

/* boost logits for supertoken partners */
static void supertok_boost(const SuperTokens *st, int last_word,
                            float *logits, int vocab_size) {
    for (int i = 0; i < st->n_supers; i++) {
        const SuperToken *t = &st->supers[i];
        if (t->tokens[0] == last_word && t->tokens[1] < vocab_size)
            logits[t->tokens[1]] += t->pmi * 0.5f;
        if (t->tokens[1] == last_word && t->tokens[0] < vocab_size)
            logits[t->tokens[0]] += t->pmi * 0.3f;
    }
}

/* ═══════════════════════════════════════════════════════════════════
 * SQLITE OPERATIONS (optional)
 * ═══════════════════════════════════════════════════════════════════ */

#ifdef USE_SQLITE
static void db_init(void) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return;
    sqlite3_exec(db,
        "CREATE TABLE IF NOT EXISTS autopsy("
        "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "  prompt TEXT NOT NULL,"
        "  tree_text TEXT NOT NULL,"
        "  created REAL DEFAULT (strftime('%s','now'))"
        ");"
        "CREATE TABLE IF NOT EXISTS word_memory("
        "  word TEXT NOT NULL,"
        "  related TEXT NOT NULL"
        ");"
        "CREATE INDEX IF NOT EXISTS idx_wm ON word_memory(word);"
        "CREATE TABLE IF NOT EXISTS mutation_templates("
        "  source_word TEXT NOT NULL,"
        "  target_word TEXT NOT NULL,"
        "  resonance_score REAL DEFAULT 0.0"
        ");"
        "CREATE TABLE IF NOT EXISTS corpse_bigrams("
        "  word1 TEXT NOT NULL,"
        "  word2 TEXT NOT NULL,"
        "  frequency INTEGER DEFAULT 1"
        ");"
        "CREATE INDEX IF NOT EXISTS idx_cb ON corpse_bigrams(word1);",
        NULL, NULL, NULL);
    sqlite3_close(db);
}

static void db_store_autopsy(const char *prompt, const char *tree_text) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return;
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db,
        "INSERT INTO autopsy(prompt,tree_text) VALUES(?,?)", -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, prompt, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, tree_text, -1, SQLITE_STATIC);
    sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}

static void db_store_bigrams(const char *w1, const char *w2) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return;
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db,
        "INSERT INTO corpse_bigrams(word1,word2) VALUES(?,?)", -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, w1, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, w2, -1, SQLITE_STATIC);
    sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}

static int db_recall_mutations(const char *word, int *results,
                                Vocab *v, int max_results) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return 0;
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db,
        "SELECT related FROM word_memory WHERE word=? LIMIT ?",
        -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, word, -1, SQLITE_STATIC);
    sqlite3_bind_int(stmt, 2, max_results);
    int n = 0;
    while (sqlite3_step(stmt) == SQLITE_ROW && n < max_results) {
        const char *rel = (const char *)sqlite3_column_text(stmt, 0);
        int id = vocab_add(v, rel);
        if (id >= 0) results[n++] = id;
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    return n;
}

static void db_store_word_relation(const char *word, const char *related) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return;
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db,
        "INSERT INTO word_memory(word,related) VALUES(?,?)", -1, &stmt, NULL);
    sqlite3_bind_text(stmt, 1, word, -1, SQLITE_STATIC);
    sqlite3_bind_text(stmt, 2, related, -1, SQLITE_STATIC);
    sqlite3_step(stmt);
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}

/* load learned bigrams from DB into BigramTable */
static void db_load_corpse_bigrams(BigramTable *bt, Vocab *v) {
    sqlite3 *db;
    if (sqlite3_open(DB_PATH, &db) != SQLITE_OK) return;
    sqlite3_stmt *stmt;
    sqlite3_prepare_v2(db,
        "SELECT word1, word2, frequency FROM corpse_bigrams", -1, &stmt, NULL);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        const char *w1 = (const char *)sqlite3_column_text(stmt, 0);
        const char *w2 = (const char *)sqlite3_column_text(stmt, 1);
        float freq = (float)sqlite3_column_int(stmt, 2);
        int id1 = vocab_add(v, w1);
        int id2 = vocab_add(v, w2);
        if (id1 >= 0 && id2 >= 0)
            bigram_add(bt, id1, id2, freq * 3.0f); /* learned = 3x weight */
    }
    sqlite3_finalize(stmt);
    sqlite3_close(db);
}
#endif /* USE_SQLITE */

/* ═══════════════════════════════════════════════════════════════════
 * TOKENIZATION & CORE WORD SELECTION
 * ═══════════════════════════════════════════════════════════════════ */

/* tokenize input into word IDs, adding to vocab */
static int tokenize_input(const char *input, int *ids, int max_ids) {
    char buf[4096];
    strncpy(buf, input, sizeof(buf) - 1);
    buf[sizeof(buf) - 1] = '\0';

    int n = 0;
    char *tok = strtok(buf, " \t\n\r,.;:!?\"'()[]{}");
    while (tok && n < max_ids) {
        int ok = 0;
        for (int i = 0; tok[i]; i++)
            if (is_alpha(tok[i])) { ok = 1; break; }
        if (ok) {
            int id = vocab_add(&S.vocab, tok);
            if (id >= 0) ids[n++] = id;
        }
        tok = strtok(NULL, " \t\n\r,.;:!?\"'()[]{}");
    }
    return n;
}

/* select core words — long, rare, non-stop, positionally biased */
static int select_core_words(const int *ids, int n_ids,
                              int *core, int max_core) {
    float scores[MAX_VOCAB];
    memset(scores, 0, sizeof(scores));

    for (int i = 0; i < n_ids; i++) {
        int id = ids[i];
        if (id < 0 || is_stopword(S.vocab.words[id])) continue;

        float len_score = (float)strlen(S.vocab.words[id]);
        float pos_score = (i == 0) ? 1.2f : 1.0f;
        float rarity = 1.0f;
        if (S.cooc.freq[id] > 0)
            rarity = 1.0f / logf(1.0f + (float)S.cooc.freq[id]);
        float jitter = 0.9f + randf() * 0.2f;

        scores[id] = len_score * pos_score * rarity * jitter;
    }

    int nc = 0;
    for (int round = 0; round < max_core; round++) {
        int best = -1;
        float best_score = 0;
        for (int i = 0; i < S.vocab.n_words; i++) {
            if (scores[i] > best_score) {
                best_score = scores[i];
                best = i;
            }
        }
        if (best < 0) break;
        core[nc++] = best;
        scores[best] = 0; /* consume */
    }
    return nc;
}

/* ═══════════════════════════════════════════════════════════════════
 * MUTATION GENERATION
 * ═══════════════════════════════════════════════════════════════════ */

/* get mutations for a word using all available sources */
static int get_mutations(const char *word, int *results, int max_results) {
    int n = 0;

    /* 1. external provider (nanollama via Go) */
    if (g_mutation_provider) {
        char ext[16][MAX_WORD_LEN];
        int ne = g_mutation_provider(word, ext, max_results < 16 ? max_results : 16);
        for (int i = 0; i < ne && n < max_results; i++) {
            int id = vocab_add(&S.vocab, ext[i]);
            if (id >= 0) results[n++] = id;
        }
        if (n > 0) return n;
    }

    /* 2. SQLite memory */
#ifdef USE_SQLITE
    n += db_recall_mutations(word, results + n, &S.vocab, max_results - n);
    if (n >= max_results) return n;
#endif

    /* 3. phonetic neighbors from vocab */
    int phon[32];
    int np = find_phonetic_neighbors(&S.vocab, word, phon, 32);
    /* shuffle and pick */
    for (int i = np - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int tmp = phon[i]; phon[i] = phon[j]; phon[j] = tmp;
    }
    for (int i = 0; i < np && n < max_results; i++)
        results[n++] = phon[i];

    /* 4. semantic neighbors (cosine similarity to seed vocab) */
    if (n < max_results) {
        float emb[DIM];
        word_embed(word, emb);

        /* sample from vocab with probability proportional to similarity */
        /* but also inject randomness for diversity */
        typedef struct { int id; float sim; } Cand;
        Cand cands[64];
        int nc = 0;

        /* scan a random subset of vocab for diversity */
        int stride = S.vocab.n_words > 200 ? S.vocab.n_words / 200 : 1;
        int start = rand() % (stride > 1 ? stride : 1);
        for (int i = start; i < S.vocab.n_words && nc < 64; i += stride) {
            float e2[DIM];
            word_embed(S.vocab.words[i], e2);
            float sim = vec_cosine(emb, e2, DIM);
            /* accept if somewhat similar OR random chance for diversity */
            if ((sim > 0.2f && sim < 0.99f) || randf() < 0.05f) {
                cands[nc].id = i;
                cands[nc].sim = sim + randf() * 0.15f; /* jitter */
                nc++;
            }
        }
        /* sort by jittered similarity descending */
        for (int i = 0; i < nc - 1; i++)
            for (int j = i + 1; j < nc; j++)
                if (cands[j].sim > cands[i].sim) {
                    Cand tmp = cands[i]; cands[i] = cands[j]; cands[j] = tmp;
                }
        for (int i = 0; i < nc && n < max_results; i++) {
            int dup = 0;
            for (int k = 0; k < n; k++)
                if (results[k] == cands[i].id) { dup = 1; break; }
            if (!dup) results[n++] = cands[i].id;
        }
    }

    /* 5. random wildcard: always add 1 completely random seed word */
    if (n < max_results && SEED_VOCAB_SIZE > 0) {
        int rid = rand() % (int)SEED_VOCAB_SIZE;
        int id = vocab_find(&S.vocab, SEED_VOCAB[rid]);
        if (id >= 0) {
            int dup = 0;
            for (int k = 0; k < n; k++)
                if (results[k] == id) { dup = 1; break; }
            if (!dup) results[n++] = id;
        }
    }

    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * MUTATION TREE BUILDING
 * ═══════════════════════════════════════════════════════════════════ */

static int tree_add_node(MutationTree *t, int word_id, int depth) {
    if (t->n_nodes >= MAX_TREE_NODES) return -1;
    int idx = t->n_nodes++;
    t->nodes[idx].word_id    = word_id;
    t->nodes[idx].n_children = 0;
    t->nodes[idx].depth      = depth;
    return idx;
}

static void build_tree_recursive(MutationTree *t, int node_idx,
                                  int depth, int max_depth, int width) {
    if (depth >= max_depth) return;
    TreeNode *node = &t->nodes[node_idx];
    const char *word = S.vocab.words[node->word_id];

    int mutations[16];
    int nm = get_mutations(word, mutations, width);

    for (int i = 0; i < nm; i++) {
        int child_idx = tree_add_node(t, mutations[i], depth + 1);
        if (child_idx < 0) return;
        if (node->n_children < TREE_WIDTH)
            node->children[node->n_children++] = child_idx;

        /* store mutation relation */
#ifdef USE_SQLITE
        db_store_word_relation(word, S.vocab.words[mutations[i]]);
#endif
        /* update co-occurrence */
        cooc_update(&S.cooc, node->word_id, mutations[i], 1.0f);

        build_tree_recursive(t, child_idx, depth + 1, max_depth, width);
    }
}

static void build_mutation_tree(MutationTree *t, int root_word_id) {
    memset(t, 0, sizeof(*t));
    tree_add_node(t, root_word_id, 0);
    build_tree_recursive(t, 0, 0, TREE_DEPTH, TREE_WIDTH);
}

/* ═══════════════════════════════════════════════════════════════════
 * LEAF COLLECTION
 * ═══════════════════════════════════════════════════════════════════ */

static int collect_leaves(const MutationTree *t, int *leaves, int max_leaves) {
    int n = 0;
    for (int i = 0; i < t->n_nodes && n < max_leaves; i++) {
        if (t->nodes[i].n_children == 0) {
            /* check no duplicates */
            int dup = 0;
            for (int j = 0; j < n; j++)
                if (leaves[j] == t->nodes[i].word_id) { dup = 1; break; }
            if (!dup) leaves[n++] = t->nodes[i].word_id;
        }
    }
    return n;
}

/* ═══════════════════════════════════════════════════════════════════
 * DARIO EQUATION — compute logits for next word selection
 *
 *   logits[w] = Bw·B[w] + α·H[w] + β·F[w] + γ·A[w] + T[w]
 *
 * then softmax(logits / τ), sample top-k
 * ═══════════════════════════════════════════════════════════════════ */

static int sample_topk(const float *logits, int n, float tau, int k) {
    /* find top-k indices */
    int topk[TOP_K];
    float topv[TOP_K];
    for (int i = 0; i < k; i++) { topk[i] = -1; topv[i] = -1e30f; }

    for (int i = 0; i < n; i++) {
        if (logits[i] > topv[k - 1]) {
            topv[k - 1] = logits[i];
            topk[k - 1] = i;
            /* bubble up */
            for (int j = k - 1; j > 0; j--) {
                if (topv[j] > topv[j - 1]) {
                    float tv = topv[j]; topv[j] = topv[j-1]; topv[j-1] = tv;
                    int ti = topk[j]; topk[j] = topk[j-1]; topk[j-1] = ti;
                } else break;
            }
        }
    }

    /* softmax over top-k */
    float maxv = topv[0];
    float sum = 0;
    float probs[TOP_K];
    for (int i = 0; i < k; i++) {
        if (topk[i] < 0) { probs[i] = 0; continue; }
        probs[i] = expf((topv[i] - maxv) / tau);
        sum += probs[i];
    }
    if (sum < 1e-10f) return topk[0] >= 0 ? topk[0] : 0;

    /* sample */
    float r = randf() * sum;
    float acc = 0;
    for (int i = 0; i < k; i++) {
        acc += probs[i];
        if (acc >= r && topk[i] >= 0) return topk[i];
    }
    return topk[0] >= 0 ? topk[0] : 0;
}

/* compute all Dario terms and sample next word
 * recent[] tracks recently used words for repetition penalty */
static int dario_sample(const int *candidates, int n_cand, int last_word,
                         const int *recent, int n_recent) {
    int vs = S.vocab.n_words;
    float *logits = calloc(vs, sizeof(float));
    float *B = calloc(vs, sizeof(float));
    float *H = calloc(vs, sizeof(float));
    float *F = calloc(vs, sizeof(float));
    float *A = calloc(vs, sizeof(float));
    float *T = calloc(vs, sizeof(float));

    /* === B: Bigram inertia === */
    if (last_word >= 0) {
        bigram_row(&S.bigrams, last_word, B, vs);
    }

    /* === H: Hebbian co-occurrence with context === */
    {
        int ctx_start = S.ctx_len > 8 ? S.ctx_len - 8 : 0;
        for (int c = ctx_start; c < S.ctx_len; c++) {
            int ctx_id = S.context[c];
            float decay = powf(0.9f, (float)(S.ctx_len - 1 - c));
            for (int i = 0; i < S.cooc.n; i++) {
                if (S.cooc.src[i] == ctx_id && S.cooc.dst[i] < vs)
                    H[S.cooc.dst[i]] += S.cooc.count[i] * decay;
            }
        }
        /* normalize */
        float mx = 0;
        for (int i = 0; i < vs; i++) if (H[i] > mx) mx = H[i];
        if (mx > 0) for (int i = 0; i < vs; i++) H[i] /= mx;
    }

    /* === F: Prophecy fulfillment === */
    for (int i = 0; i < vs; i++) {
        float emb_i[DIM];
        word_embed(S.vocab.words[i], emb_i);
        float score = 0;
        for (int p = 0; p < S.prophecy.n; p++) {
            Prophecy *pr = &S.prophecy.p[p];
            if (pr->fulfilled) continue;
            float emb_t[DIM];
            word_embed(S.vocab.words[pr->target], emb_t);
            float sim = vec_cosine(emb_i, emb_t, DIM);
            if (sim < 0) sim = 0;
            float debt = logf(1.0f + (float)pr->age);
            score += pr->strength * sim * debt;
        }
        F[i] = score;
    }
    {
        float mx = 0;
        for (int i = 0; i < vs; i++) if (F[i] > mx) mx = F[i];
        if (mx > 0) for (int i = 0; i < vs; i++) F[i] /= mx;
    }

    /* === A: Destiny attraction === */
    if (S.destiny.magnitude > 1e-6f) {
        for (int i = 0; i < vs; i++) {
            float emb_i[DIM];
            word_embed(S.vocab.words[i], emb_i);
            A[i] = vec_cosine(emb_i, S.destiny.vec, DIM) * S.destiny.magnitude;
        }
        float mx = 0;
        for (int i = 0; i < vs; i++) if (fabsf(A[i]) > mx) mx = fabsf(A[i]);
        if (mx > 0) for (int i = 0; i < vs; i++) A[i] /= mx;
    }

    /* === T: Trauma — origin word pull === */
    if (S.trauma_level > 0.3f) {
        float boost = S.trauma_level * 3.0f;
        for (int i = 0; i < S.n_origins; i++) {
            int oid = S.origin_words[i];
            if (oid >= 0 && oid < vs)
                T[oid] = boost * (1.0f - (float)i / (float)(S.n_origins + 1));
        }
    }

    /* === Combine: Dario Equation === */
    for (int i = 0; i < vs; i++) {
        logits[i] = BIGRAM_W * B[i]
                   + ALPHA_D * H[i]
                   + BETA_D  * F[i]
                   + GAMMA_D * A[i]
                   + T[i];
    }

    /* SuperToken boost */
    if (last_word >= 0)
        supertok_boost(&S.supertokens, last_word, logits, vs);

    /* Candidate mask: boost candidates, don't zero others entirely */
    for (int i = 0; i < n_cand; i++) {
        if (candidates[i] >= 0 && candidates[i] < vs)
            logits[candidates[i]] += 2.0f; /* candidate bonus */
    }

    /* Repetition penalty: penalize recently used words */
    for (int i = 0; i < n_recent; i++) {
        if (recent[i] >= 0 && recent[i] < vs) {
            float penalty = 3.0f / (1.0f + (float)(n_recent - 1 - i) * 0.5f);
            logits[recent[i]] -= penalty;
        }
    }

    /* Temperature with trauma */
    float tau = TAU_BASE;
    if (S.trauma_level > 0.3f)
        tau *= 1.0f + 0.3f * S.trauma_level;

    int result = sample_topk(logits, vs, tau, TOP_K);

    free(logits);
    free(B); free(H); free(F); free(A); free(T);
    return result;
}

/* ═══════════════════════════════════════════════════════════════════
 * CORPSE REASSEMBLY — Frankenstein paragraph from leaves
 * ═══════════════════════════════════════════════════════════════════ */

static int reassemble_corpse(const int *leaves, int n_leaves,
                              int *corpse, int max_words) {
    if (n_leaves == 0) return 0;

    /* start with a random leaf */
    int current = leaves[rand() % n_leaves];
    int n = 0;
    corpse[n++] = current;

    /* add to context */
    if (S.ctx_len < MAX_CONTEXT)
        S.context[S.ctx_len++] = current;

    for (int step = 1; step < max_words; step++) {
        int next = dario_sample(leaves, n_leaves, current,
                                corpse, n);

        /* avoid immediate repeats */
        if (next == current && n_leaves > 1) {
            next = leaves[rand() % n_leaves];
        }

        corpse[n++] = next;
        current = next;

        /* update state */
        if (S.ctx_len < MAX_CONTEXT)
            S.context[S.ctx_len++] = next;

        /* prophecy: predict next based on co-occurrence */
        float best_cooc = -1;
        int best_pred = -1;
        for (int i = 0; i < S.cooc.n; i++) {
            if (S.cooc.src[i] == next && S.cooc.count[i] > best_cooc) {
                best_cooc = S.cooc.count[i];
                best_pred = S.cooc.dst[i];
            }
        }
        if (best_pred >= 0)
            prophecy_add(&S.prophecy, best_pred, 0.3f);

        prophecy_fulfill(&S.prophecy, next);
        prophecy_age(&S.prophecy);
        destiny_update(&S.destiny, S.vocab.words[next]);

        /* trauma accumulates from low resonance */
        S.trauma_level *= 0.97f;

        S.step++;
    }

    /* record co-occurrences from corpse */
    cooc_record(&S.cooc, corpse, n);

    /* store corpse bigrams to DB */
#ifdef USE_SQLITE
    for (int i = 0; i < n - 1; i++)
        db_store_bigrams(S.vocab.words[corpse[i]], S.vocab.words[corpse[i+1]]);
#endif

    return n;
}

/* format corpse as paragraph using templates */
static void format_sorokin_paragraph(const int *corpse, int n_corpse,
                                      char *out, int out_len) {
    int pos = 0;
    int wi = 0; /* word index into corpse */

    for (int t = 0; t < 3 && wi < n_corpse; t++) {
        int tmpl = rand() % NUM_TEMPLATES;
        const char *fmt = TEMPLATES[tmpl];

        /* count %s in template */
        int nslots = 0;
        for (const char *p = fmt; *p; p++)
            if (*p == '%' && *(p+1) == 's') nslots++;

        /* fill slots */
        const char *words[8];
        for (int s = 0; s < nslots && s < 8; s++) {
            if (wi < n_corpse)
                words[s] = S.vocab.words[corpse[wi++]];
            else
                words[s] = S.vocab.words[corpse[rand() % n_corpse]];
        }

        /* manual snprintf with slots (up to 8) */
        char line[512];
        switch (nslots) {
            case 2: snprintf(line, sizeof(line), fmt, words[0], words[1]); break;
            case 3: snprintf(line, sizeof(line), fmt, words[0], words[1], words[2]); break;
            case 4: snprintf(line, sizeof(line), fmt, words[0], words[1], words[2], words[3]); break;
            case 5: snprintf(line, sizeof(line), fmt, words[0], words[1], words[2], words[3], words[4]); break;
            case 6: snprintf(line, sizeof(line), fmt, words[0], words[1], words[2], words[3], words[4], words[5]); break;
            default: snprintf(line, sizeof(line), "%s %s.", words[0], words[1]); break;
        }

        int len = (int)strlen(line);
        if (pos + len + 2 < out_len) {
            memcpy(out + pos, line, len);
            pos += len;
            out[pos++] = ' ';
        }
    }
    if (pos > 0) pos--;
    out[pos] = '\0';
}

/* ═══════════════════════════════════════════════════════════════════
 * RHYME DETECTION — crude phonetic tail matching
 * ═══════════════════════════════════════════════════════════════════ */

static void rhyme_key(const char *word, char *key, int key_len) {
    char low[MAX_WORD_LEN];
    str_lower(low, word, MAX_WORD_LEN);
    int len = (int)strlen(low);

    /* find last vowel */
    int last_v = -1;
    for (int i = len - 1; i >= 0; i--) {
        if (is_vowel(low[i])) { last_v = i; break; }
    }

    if (last_v < 0) {
        /* no vowel: use last 2 chars */
        int start = len > 2 ? len - 2 : 0;
        strncpy(key, low + start, key_len - 1);
        key[key_len - 1] = '\0';
    } else {
        /* from last vowel to end */
        int tail_len = len - last_v;
        if (tail_len >= key_len) tail_len = key_len - 1;
        strncpy(key, low + last_v, tail_len);
        key[tail_len] = '\0';
    }
}

static int words_rhyme(const char *a, const char *b) {
    char ka[16], kb[16];
    rhyme_key(a, ka, sizeof(ka));
    rhyme_key(b, kb, sizeof(kb));
    return strcmp(ka, kb) == 0 && strcmp(a, b) != 0;
}

/* ═══════════════════════════════════════════════════════════════════
 * SONNET GENERATION — 14 lines, ABABCDCDEFEFGG
 * ═══════════════════════════════════════════════════════════════════ */

/* rhyme scheme: A=0 B=1 C=2 D=3 E=4 F=5 G=6 */
static const int RHYME_SCHEME[SONNET_LINES] = {
    0,1,0,1,  2,3,2,3,  4,5,4,5,  6,6
};

static void generate_sonnet(const int *corpse, int n_corpse,
                             char *out, int out_len) {
    if (n_corpse < SONNET_LINES * 2) {
        snprintf(out, out_len, "[insufficient material for sonnet]");
        return;
    }

    /* find rhyme pairs from corpse words */
    int end_words[SONNET_LINES];
    memset(end_words, -1, sizeof(end_words));

    /* assign end-words: try to find rhyming pairs for each rhyme group */
    int used[MAX_LEAVES];
    memset(used, 0, sizeof(used));

    for (int group = 0; group <= 6; group++) {
        /* find which lines belong to this group */
        int lines[4];
        int nl = 0;
        for (int i = 0; i < SONNET_LINES; i++)
            if (RHYME_SCHEME[i] == group && nl < 4)
                lines[nl++] = i;

        /* try to find rhyming words for this group */
        int found = 0;
        for (int i = 0; i < n_corpse && !found; i++) {
            if (used[i]) continue;
            for (int j = i + 1; j < n_corpse && !found; j++) {
                if (used[j]) continue;
                if (words_rhyme(S.vocab.words[corpse[i]],
                                S.vocab.words[corpse[j]])) {
                    end_words[lines[0]] = corpse[i];
                    if (nl > 1) end_words[lines[1]] = corpse[j];
                    used[i] = used[j] = 1;
                    found = 1;
                }
            }
        }

        /* fallback: just pick unused words */
        if (!found) {
            for (int l = 0; l < nl; l++) {
                for (int i = 0; i < n_corpse; i++) {
                    if (!used[i]) {
                        end_words[lines[l]] = corpse[i];
                        used[i] = 1;
                        break;
                    }
                }
            }
        }
    }

    /* build lines */
    int pos = 0;
    int sonnet_recent[256]; /* track used words across sonnet */
    int n_sonnet_recent = 0;
    for (int line = 0; line < SONNET_LINES; line++) {
        /* pick 4-8 words from corpse, ending with end_word */
        int line_len = 4 + rand() % 5;
        for (int w = 0; w < line_len - 1; w++) {
            int wid;
            if (w == 0) {
                /* start with a random charged word */
                wid = corpse[rand() % n_corpse];
            } else {
                /* use Dario equation to pick next */
                wid = dario_sample(corpse, n_corpse,
                    (w > 0 ? corpse[rand() % n_corpse] : -1),
                    sonnet_recent, n_sonnet_recent);
            }
            if (n_sonnet_recent < 256)
                sonnet_recent[n_sonnet_recent++] = wid;
            const char *wstr = S.vocab.words[wid];
            int wlen = (int)strlen(wstr);
            if (pos + wlen + 2 < out_len) {
                /* capitalize first word of line */
                if (w == 0) {
                    out[pos] = (char)toupper((unsigned char)wstr[0]);
                    memcpy(out + pos + 1, wstr + 1, wlen - 1);
                } else {
                    memcpy(out + pos, wstr, wlen);
                }
                pos += wlen;
                out[pos++] = ' ';
            }
        }

        /* end word */
        int ew = end_words[line];
        if (ew < 0) ew = corpse[rand() % n_corpse];
        const char *ewstr = S.vocab.words[ew];
        int ewlen = (int)strlen(ewstr);
        if (pos + ewlen + 2 < out_len) {
            memcpy(out + pos, ewstr, ewlen);
            pos += ewlen;
        }

        /* punctuation */
        if (line == 7) { /* volta */
            if (pos + 3 < out_len) { out[pos++] = ' '; out[pos++] = '-'; out[pos++] = '-'; }
        } else if (line == 13) {
            if (pos + 1 < out_len) out[pos++] = '.';
        } else if (line % 2 == 1) {
            if (pos + 1 < out_len) out[pos++] = ';';
        } else {
            if (pos + 1 < out_len) out[pos++] = ',';
        }
        if (pos + 1 < out_len) out[pos++] = '\n';
    }
    if (pos > 0) out[pos - 1] = '\0';
    else out[0] = '\0';
}

/* ═══════════════════════════════════════════════════════════════════
 * ASCII TREE RENDERING
 * ═══════════════════════════════════════════════════════════════════ */

static void render_tree(const MutationTree *t, int node_idx,
                         int depth, int is_last, char *prefix,
                         char *out, int *pos, int out_len) {
    const TreeNode *node = &t->nodes[node_idx];

    /* indent */
    int plen = (int)strlen(prefix);
    if (plen + 40 > out_len - *pos) return;

    if (depth > 0) {
        *pos += snprintf(out + *pos, out_len - *pos, "%s%s %s\n",
            prefix, is_last ? "└─" : "├─",
            S.vocab.words[node->word_id]);
    } else {
        *pos += snprintf(out + *pos, out_len - *pos, "%s\n",
            S.vocab.words[node->word_id]);
    }

    /* update prefix for children */
    char child_prefix[256];
    if (depth > 0)
        snprintf(child_prefix, sizeof(child_prefix), "%s%s",
            prefix, is_last ? "   " : "│  ");
    else
        child_prefix[0] = '\0';

    for (int i = 0; i < node->n_children; i++) {
        render_tree(t, node->children[i], depth + 1,
                    i == node->n_children - 1, child_prefix,
                    out, pos, out_len);
    }
}

/* ═══════════════════════════════════════════════════════════════════
 * RESONANCE METRICS
 * ═══════════════════════════════════════════════════════════════════ */

typedef struct {
    float phonetic_diversity;
    float mutation_depth;
    float bigram_density;
} AutopsyMetrics;

static AutopsyMetrics compute_metrics(const int *corpse, int n_corpse,
                                       const MutationTree *trees, int n_trees) {
    AutopsyMetrics m = {0};

    /* phonetic diversity: unique fingerprints / total */
    char fps[MAX_LEAVES][16];
    int n_unique = 0;
    for (int i = 0; i < n_corpse && i < MAX_LEAVES; i++) {
        phonetic_fp(S.vocab.words[corpse[i]], fps[i], 16);
        int dup = 0;
        for (int j = 0; j < i; j++)
            if (strcmp(fps[i], fps[j]) == 0) { dup = 1; break; }
        if (!dup) n_unique++;
    }
    m.phonetic_diversity = n_corpse > 0
        ? (float)n_unique / (float)n_corpse : 0;

    /* mutation depth: avg tree depth / max depth */
    int total_depth = 0, n_nodes = 0;
    for (int t = 0; t < n_trees; t++) {
        for (int i = 0; i < trees[t].n_nodes; i++) {
            total_depth += trees[t].nodes[i].depth;
            n_nodes++;
        }
    }
    m.mutation_depth = n_nodes > 0
        ? (float)total_depth / ((float)n_nodes * TREE_DEPTH) : 0;

    /* bigram density: corpse bigrams found in table / total */
    int found = 0;
    for (int i = 0; i < n_corpse - 1; i++) {
        for (int j = 0; j < S.bigrams.n; j++) {
            if (S.bigrams.src[j] == corpse[i] &&
                S.bigrams.dst[j] == corpse[i+1]) {
                found++;
                break;
            }
        }
    }
    m.bigram_density = n_corpse > 1
        ? (float)found / (float)(n_corpse - 1) : 0;

    return m;
}

static void render_bar(float val, int width, char *out) {
    int filled = (int)(val * width);
    if (filled > width) filled = width;
    for (int i = 0; i < width; i++)
        out[i] = i < filled ? '#' : '.';
    out[width] = '\0';
}

/* ═══════════════════════════════════════════════════════════════════
 * FULL AUTOPSY PIPELINE
 * ═══════════════════════════════════════════════════════════════════ */

void run_autopsy(const char *prompt) {
    printf("\n");
    printf("================================================================\n");
    printf("  AUTOPSY REPORT\n");
    printf("  Subject: \"%s\"\n", prompt);
    printf("================================================================\n\n");

    /* 1. tokenize */
    int input_ids[256];
    int n_input = tokenize_input(prompt, input_ids, 256);
    if (n_input == 0) {
        printf("  [no viable words found in prompt]\n\n");
        return;
    }

    /* update destiny from prompt */
    for (int i = 0; i < n_input; i++)
        destiny_update(&S.destiny, S.vocab.words[input_ids[i]]);

    /* 2. select core words */
    int core[MAX_CORE];
    int n_core = select_core_words(input_ids, n_input, core, MAX_CORE);

    /* record origins for trauma */
    S.n_origins = n_core;
    for (int i = 0; i < n_core; i++)
        S.origin_words[i] = core[i];

    printf("  Core words: ");
    for (int i = 0; i < n_core; i++)
        printf("%s ", S.vocab.words[core[i]]);
    printf("\n\n");

    /* 3. build mutation trees */
    MutationTree trees[MAX_CORE];
    int all_leaves[MAX_LEAVES];
    int n_leaves = 0;

    for (int i = 0; i < n_core; i++) {
        build_mutation_tree(&trees[i], core[i]);

        /* render tree */
        char tree_buf[4096];
        int tpos = 0;
        char prefix[256] = "";
        render_tree(&trees[i], 0, 0, 1, prefix, tree_buf, &tpos, sizeof(tree_buf));
        printf("  Tree [%s]:\n", S.vocab.words[core[i]]);
        /* indent each line */
        char *line = strtok(tree_buf, "\n");
        while (line) {
            printf("    %s\n", line);
            line = strtok(NULL, "\n");
        }
        printf("\n");

        /* collect leaves */
        int tree_leaves[MAX_LEAVES];
        int nl = collect_leaves(&trees[i], tree_leaves, MAX_LEAVES - n_leaves);
        for (int j = 0; j < nl && n_leaves < MAX_LEAVES; j++) {
            /* dedup */
            int dup = 0;
            for (int k = 0; k < n_leaves; k++)
                if (all_leaves[k] == tree_leaves[j]) { dup = 1; break; }
            if (!dup) all_leaves[n_leaves++] = tree_leaves[j];
        }
    }

    printf("  Collected %d unique leaves\n\n", n_leaves);

    /* 4. reassemble corpse using Dario Equation */
    int corpse[128];
    int n_corpse = reassemble_corpse(all_leaves, n_leaves, corpse, 40);

    char paragraph[2048];
    format_sorokin_paragraph(corpse, n_corpse, paragraph, sizeof(paragraph));

    printf("  ── CORPSE ─────────────────────────────────────────\n");
    printf("  %s\n\n", paragraph);

    /* 5. generate sonnet */
    /* expand corpse for sonnet: combine all leaves + corpse */
    int sonnet_pool[MAX_LEAVES];
    int n_pool = 0;
    for (int i = 0; i < n_corpse && n_pool < MAX_LEAVES; i++)
        sonnet_pool[n_pool++] = corpse[i];
    for (int i = 0; i < n_leaves && n_pool < MAX_LEAVES; i++) {
        int dup = 0;
        for (int j = 0; j < n_pool; j++)
            if (sonnet_pool[j] == all_leaves[i]) { dup = 1; break; }
        if (!dup) sonnet_pool[n_pool++] = all_leaves[i];
    }

    char sonnet[4096];
    generate_sonnet(sonnet_pool, n_pool, sonnet, sizeof(sonnet));

    printf("  ── SONNET ─────────────────────────────────────────\n");
    /* print with indent */
    char *sline = strtok(sonnet, "\n");
    while (sline) {
        printf("  %s\n", sline);
        sline = strtok(NULL, "\n");
    }
    printf("\n");

    /* 6. crystallize supertokens */
    supertok_scan(&S.supertokens, &S.cooc, S.vocab.n_words);

    /* 7. metrics */
    AutopsyMetrics met = compute_metrics(corpse, n_corpse, trees, n_core);
    char bar[32];
    printf("  ── METRICS ────────────────────────────────────────\n");
    render_bar(met.phonetic_diversity, 20, bar);
    printf("  Phonetic Diversity: [%s] %.3f\n", bar, met.phonetic_diversity);
    render_bar(met.mutation_depth, 20, bar);
    printf("  Mutation Depth:     [%s] %.3f\n", bar, met.mutation_depth);
    render_bar(met.bigram_density, 20, bar);
    printf("  Bigram Density:     [%s] %.3f\n", bar, met.bigram_density);
    printf("\n");

    /* stats */
    printf("  Vocabulary:    %d words\n", S.vocab.n_words);
    printf("  Bigrams:       %d\n", S.bigrams.n);
    printf("  Co-occurrences:%d\n", S.cooc.n);
    printf("  SuperTokens:   %d crystallized\n", S.supertokens.n_supers);
    if (S.supertokens.n_supers > 0) {
        int show = S.supertokens.n_supers < 5 ? S.supertokens.n_supers : 5;
        for (int i = 0; i < show; i++) {
            SuperToken *t = &S.supertokens.supers[i];
            printf("    \"%s %s\" (PMI=%.2f)\n",
                S.vocab.words[t->tokens[0]],
                S.vocab.words[t->tokens[1]], t->pmi);
        }
    }
    printf("  Destiny mag:   %.3f\n", S.destiny.magnitude);
    printf("  Trauma:        %.3f\n", S.trauma_level);
    printf("  Prophecies:    %d active\n", S.prophecy.n);
    printf("\n");

    fflush(stdout);

    /* store to DB */
#ifdef USE_SQLITE
    db_store_autopsy(prompt, paragraph);
#endif
}

/* ═══════════════════════════════════════════════════════════════════
 * INITIALIZATION
 * ═══════════════════════════════════════════════════════════════════ */

static void sorokin_init_state(void) {
    memset(&S, 0, sizeof(S));
    srand((unsigned int)time(NULL));

    /* load seed vocabulary */
    for (int i = 0; i < (int)SEED_VOCAB_SIZE; i++)
        vocab_add(&S.vocab, SEED_VOCAB[i]);

    /* build seed bigrams from corpus */
    /* parse line by line */
    char corpus_buf[8192];
    strncpy(corpus_buf, SEED_CORPUS, sizeof(corpus_buf) - 1);
    corpus_buf[sizeof(corpus_buf) - 1] = '\0';

    char *line = strtok(corpus_buf, "\n");
    while (line) {
        build_bigrams_from_text(&S.bigrams, &S.vocab, line);
        line = strtok(NULL, "\n");
    }

    /* load learned bigrams from DB */
#ifdef USE_SQLITE
    db_init();
    db_load_corpse_bigrams(&S.bigrams, &S.vocab);
#endif

    S.trauma_level = 0.1f;
}

/* ═══════════════════════════════════════════════════════════════════
 * CGO EXPORTS
 * ═══════════════════════════════════════════════════════════════════ */

void sorokin_set_mutation_provider(mutation_provider_fn fn) {
    g_mutation_provider = fn;
}

void sorokin_init(void) {
    sorokin_init_state();
}

/* ═══════════════════════════════════════════════════════════════════
 * MAIN — standalone mode
 * ═══════════════════════════════════════════════════════════════════ */

#ifndef SOROKIN_LIB /* allow building as library for CGO */

int main(int argc, char **argv) {
    sorokin_init_state();

    printf("╔══════════════════════════════════════════════════════════╗\n");
    printf("║  SOROKIN — Literary Necromancy Engine                   ║\n");
    printf("║  Dario Equation: p(x|Φ) = softmax((B+αH+βF+γA+T)/τ)   ║\n");
    printf("║  %d seed words | SuperToken crystallization             ║\n",
           (int)SEED_VOCAB_SIZE);
    printf("╚══════════════════════════════════════════════════════════╝\n");

    if (argc > 1) {
        /* single autopsy from command line args */
        char prompt[1024] = "";
        for (int i = 1; i < argc; i++) {
            if (i > 1) strcat(prompt, " ");
            strncat(prompt, argv[i], sizeof(prompt) - strlen(prompt) - 1);
        }
        run_autopsy(prompt);
    } else {
        /* REPL mode */
        printf("\nEnter text for autopsy (Ctrl+D to exit):\n\n");
        char line[1024];
        printf("> ");
        fflush(stdout);
        while (fgets(line, sizeof(line), stdin)) {
            /* strip newline */
            line[strcspn(line, "\n")] = '\0';
            if (line[0] == '\0') { printf("> "); fflush(stdout); continue; }
            run_autopsy(line);
            printf("> ");
            fflush(stdout);
        }
        printf("\n[autopsy complete]\n");
    }

    return 0;
}

#endif /* SOROKIN_LIB */
