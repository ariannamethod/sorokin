#!/usr/bin/env python3
"""
sorokin_llama.py - LLaMA-15M with MEDICAL PATHOLOGY transformation! 🏥💀

Transforms children's stories (tinystories) into FORENSIC PATHOLOGY reports.

DIRECT TRANSFORMATION:
"Lily was playing in the park with her friend"
  ↓
"Vova was being examined in the morgue with his colleague" 💀

INTEGRATION WITH ASS (Autopsy Sonnet Symphony):
- Generates 14-line Shakespearean sonnets from autopsy output
- Uses SQLite morgue vocabulary + bigrams
- ABABCDCDEFEFGG rhyme scheme

This module implements the MEDICAL DICTIONARY transformation for sorokin.
15M parameters running pure NumPy inference for maximum psychotic efficiency.
"""

import sys
import re
from pathlib import Path
from typing import Optional, Tuple
import numpy as np

# Import ASS (Autopsy Sonnet Symphony)
try:
    from sonnet import compose_sonnet_sync
    ASS_AVAILABLE = True
except ImportError:
    ASS_AVAILABLE = False
    print("⚠️  ASS (sonnet.py) not available")

# Import sorokin autopsy engine for mutation trees
try:
    import sorokin
    SOROKIN_AVAILABLE = True
except ImportError:
    SOROKIN_AVAILABLE = False
    print("⚠️  sorokin.py not available")

# Import LLaMA NumPy implementation
try:
    sys.path.insert(0, str(Path(__file__).parent / "llama_np"))
    from llama_np.llama3 import Llama
    from llama_np.tokenizer import Tokenizer as LlamaTokenizer
    from llama_np.config import ModelArgs
    LLAMA_AVAILABLE = True
except ImportError as e:
    LLAMA_AVAILABLE = False
    print(f"⚠️  LLaMA not available: {e}")

# Import Dictionary Learner
try:
    from sorokin_dictionary_learner import SorokinDictionaryLearner, interactive_learning_session
    LEARNER_AVAILABLE = True
except ImportError:
    LEARNER_AVAILABLE = False
    print("⚠️  Dictionary learner not available")


class SorokinLlamaGenerator:
    """
    💀 FORENSIC PATHOLOGY LLaMA GENERATOR 💀

    Transforms Karpathy's tinystories into medical autopsy reports!

    Single mode: Tinystories → Medical Pathology (direct transformation)
    No intermediate git layer - straight to the morgue! 💀
    """

    def __init__(self, mode: str = 'sorokin'):
        """
        Initialize Sorokin LLaMA generator.

        Args:
            mode: 'sorokin' (default) - direct tinystory → medical transformation
        """
        self.model = None
        self.tokenizer = None
        self.args = None
        self.mode = mode

        if not LLAMA_AVAILABLE:
            print("⚠️  LLaMA not available - install numpy")
            return

        try:
            # Paths to model files
            model_dir = Path(__file__).parent / "llama_np"
            model_path = model_dir / "stories15M.model.npz"
            tokenizer_path = model_dir / "tokenizer.model.np"

            if not model_path.exists() or not tokenizer_path.exists():
                print(f"⚠️  LLaMA model files not found in {model_dir}")
                return

            print("🚀 Loading LLaMA-15M for SOROKIN MODE...")
            self.args = ModelArgs()

            # Try SentencePiece wrapper with BPE fallback
            try:
                from llama_np.sentencepiece_wrapper import TokenizerWrapper
                self.tokenizer = TokenizerWrapper(str(tokenizer_path), use_sentencepiece=True)
            except ImportError:
                self.tokenizer = LlamaTokenizer(str(tokenizer_path))
                print("✅ Using built-in BPE tokenizer")

            self.model = Llama(str(model_path), self.args)
            print(f"✅ SOROKIN LLaMA loaded! Mode: {mode} 💀")

        except Exception as e:
            print(f"⚠️  Failed to load LLaMA: {e}")
            self.model = None

    def generate(self, prompt: str, max_tokens: int = 50, temperature: float = 0.8,
                 context: str = "") -> str:
        """
        Generate text with SOROKIN transformation! 💀

        Args:
            prompt: Starting text
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (not used in this version)
            context: Additional context to inject

        Returns:
            Generated text with SOROKIN transformation applied
        """
        if not self.model or not self.tokenizer:
            return ""

        try:
            # Inject context into prompt
            if context:
                tech_words = [w for w in context.split() if len(w) > 3][:3]
                if tech_words:
                    prompt = f"Once upon a time, there was a {' and '.join(tech_words)}. {prompt}"

            # Encode prompt
            input_ids = np.array([self.tokenizer.encode(prompt)])

            # Generate tokens
            generated_text = prompt
            for token_id in self.model.generate(input_ids, max_tokens):
                output_id = token_id[0].tolist()

                # Check for end of sequence
                if output_id[-1] in [self.tokenizer.eos_id, self.tokenizer.bos_id]:
                    break

                # Decode and append
                token_text = self.tokenizer.decode(output_id)
                generated_text += token_text

            # Return only generated part (exclude prompt)
            output = generated_text[len(prompt):]

            # 💀 APPLY SOROKIN TRANSFORMATION!
            # Direct transformation: children's stories → forensic pathology
            output = self._apply_sorokin_transformation(output)

            return output

        except Exception as e:
            print(f"⚠️  Generation failed: {e}")
            return ""

    def _apply_sorokin_transformation(self, text: str) -> str:
        """
        💀 Transform tinystories DIRECTLY into FORENSIC PATHOLOGY! 💀

        SOROKIN PATHOLOGICAL DICTIONARY (154 transformations!!!):
        Children's stories → Medical horror

        Examples:
        - Lily → Vova (the deceased subject!)
        - park → morgue (морг)
        - playing → being examined (вскрытие)
        - friend → colleague (коллега)
        - red → hemorrhagic (кровоточащий)
        - happy → preserved (сохранённый)
        - sunny morning → well-lit during first shift

        Categories:
        - 15 Characters (Lily, Tim, Sue, Ben, Max, Emma, Jack, Mia...)
        - 12 Family/Social (mom, dad, friend, brother, sister, grandma...)
        - 15 Nature (flower, tree, sun, rain, grass, river, cloud...)
        - 10 Animals (cat, dog, bird, bunny, frog, fish, butterfly...)
        - 12 Places (park, house, school, garden, beach, forest...)
        - 15 Objects (toy, ball, book, hat, shoes, dress, car, bike...)
        - 8 Food (cake, cookie, candy, juice, milk, bread, apple...)
        - 12 Emotions (happy, sad, excited, scared, angry, tired, proud...)
        - 30 Actions (playing, running, walking, jumping, sleeping, eating...)
        - 8 Colors (red, blue, green, yellow, white, black, pink, purple)
        - 7 Sizes (big, small, tiny, huge, long, short, tall)
        - 5 Time (morning, afternoon, evening, night, day)
        - 5 Weather (sunny, rainy, windy, cloudy, storm)

        Total: 154 pathological transformations! 💀
        """
        # CHARACTERS → Medical personnel/subjects (EXTENDED!)
        text = re.sub(r'\bLily\b', 'Vova', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTim\b', 'Igor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTimmy\b', 'Igor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTom\b', 'Petrov', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAnna\b', 'Nurse Marina', text, flags=re.IGNORECASE)
        text = re.sub(r'\bSue\b', 'Dr. Sorokina', text, flags=re.IGNORECASE)
        text = re.sub(r'\bSusan\b', 'Dr. Sorokina', text, flags=re.IGNORECASE)
        text = re.sub(r'\bBen\b', 'Forensic Tech Ivanov', text, flags=re.IGNORECASE)
        text = re.sub(r'\bMax\b', 'Mortician Maksim', text, flags=re.IGNORECASE)
        text = re.sub(r'\bEmma\b', 'Pathology Assistant Emma', text, flags=re.IGNORECASE)
        text = re.sub(r'\bSam\b', 'Medical Examiner Semenov', text, flags=re.IGNORECASE)
        text = re.sub(r'\bJack\b', 'Autopsy Technician Zhuk', text, flags=re.IGNORECASE)
        text = re.sub(r'\bMia\b', 'Coroner Mironova', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle girl\b', 'deceased subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle boy\b', 'deceased subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgirl\b', 'patient', text, flags=re.IGNORECASE)
        text = re.sub(r'\bboy\b', 'patient', text, flags=re.IGNORECASE)

        # FAMILY/SOCIAL → Medical staff (EXTENDED!)
        text = re.sub(r'\bmom\b', 'chief pathologist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmother\b', 'chief pathologist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdad\b', 'head surgeon', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfather\b', 'head surgeon', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfriend\b', 'colleague', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfriends\b', 'colleagues', text, flags=re.IGNORECASE)
        text = re.sub(r'\bteacher\b', 'medical examiner', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbrother\b', 'lab assistant', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsister\b', 'nurse practitioner', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgrandma\b', 'senior pathologist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgrandpa\b', 'retired coroner', text, flags=re.IGNORECASE)
        text = re.sub(r'\bneighbor\b', 'hospital staff', text, flags=re.IGNORECASE)

        # NATURE → Medical environment (EXTENDED!)
        text = re.sub(r'\bflower\b', 'organ', text, flags=re.IGNORECASE)
        text = re.sub(r'\bflowers\b', 'organs', text, flags=re.IGNORECASE)
        text = re.sub(r'\btree\b', 'dissection table', text, flags=re.IGNORECASE)
        text = re.sub(r'\btrees\b', 'dissection tables', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsun\b', 'surgical lamp', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsky\b', 'ceiling', text, flags=re.IGNORECASE)
        text = re.sub(r'\brain\b', 'formaldehyde', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgrass\b', 'floor tiles', text, flags=re.IGNORECASE)
        text = re.sub(r'\briver\b', 'drainage channel', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwater\b', 'preservative fluid', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcloud\b', 'anesthetic gas', text, flags=re.IGNORECASE)
        text = re.sub(r'\bclouds\b', 'anesthetic gases', text, flags=re.IGNORECASE)
        text = re.sub(r'\bstone\b', 'bone fragment', text, flags=re.IGNORECASE)
        text = re.sub(r'\bstones\b', 'bone fragments', text, flags=re.IGNORECASE)
        text = re.sub(r'\bleaf\b', 'tissue sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bleaves\b', 'tissue samples', text, flags=re.IGNORECASE)

        # ANIMALS → Medical specimens (EXTENDED!)
        text = re.sub(r'\bcat\b', 'specimen', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdog\b', 'cadaver', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbird\b', 'tissue sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbirds\b', 'tissue samples', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbunny\b', 'organ sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\brabbit\b', 'organ sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfrog\b', 'biopsy specimen', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfish\b', 'preserved sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbutterfly\b', 'microscope slide', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbug\b', 'pathogen', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbugs\b', 'pathogens', text, flags=re.IGNORECASE)
        text = re.sub(r'\bworm\b', 'parasitic infection', text, flags=re.IGNORECASE)

        # PLACES → Medical facilities (EXTENDED!)
        text = re.sub(r'\bpark\b', 'morgue', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhouse\b', 'autopsy room', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhome\b', 'hospital', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgarden\b', 'pathology department', text, flags=re.IGNORECASE)
        text = re.sub(r'\bschool\b', 'medical academy', text, flags=re.IGNORECASE)
        text = re.sub(r'\bclassroom\b', 'operating theater', text, flags=re.IGNORECASE)
        text = re.sub(r'\bstore\b', 'pharmaceutical supply', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbeach\b', 'quarantine zone', text, flags=re.IGNORECASE)
        text = re.sub(r'\bforest\b', 'isolation ward', text, flags=re.IGNORECASE)
        text = re.sub(r'\bplayground\b', 'examination area', text, flags=re.IGNORECASE)
        text = re.sub(r'\broom\b', 'sterile chamber', text, flags=re.IGNORECASE)
        text = re.sub(r'\bstreet\b', 'hospital corridor', text, flags=re.IGNORECASE)

        # OBJECTS → Medical equipment (EXTENDED!)
        text = re.sub(r'\btoy\b', 'surgical instrument', text, flags=re.IGNORECASE)
        text = re.sub(r'\btoys\b', 'surgical instruments', text, flags=re.IGNORECASE)
        text = re.sub(r'\bball\b', 'specimen jar', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbook\b', 'medical records', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbooks\b', 'medical records', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhat\b', 'surgical cap', text, flags=re.IGNORECASE)
        text = re.sub(r'\bshoes\b', 'surgical boots', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdress\b', 'hospital gown', text, flags=re.IGNORECASE)
        text = re.sub(r'\bshirt\b', 'scrubs', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcar\b', 'ambulance', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbike\b', 'medical cart', text, flags=re.IGNORECASE)
        text = re.sub(r'\bchair\b', 'examination table', text, flags=re.IGNORECASE)
        text = re.sub(r'\btable\b', 'surgical table', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdoor\b', 'airlock', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwindow\b', 'observation window', text, flags=re.IGNORECASE)

        # FOOD → Medical horror (EXTENDED!)
        text = re.sub(r'\bcake\b', 'preserved tissue', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcookie\b', 'tissue slice', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcookies\b', 'tissue slices', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcandy\b', 'pill', text, flags=re.IGNORECASE)
        text = re.sub(r'\bjuice\b', 'IV solution', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmilk\b', 'plasma', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbread\b', 'gauze pad', text, flags=re.IGNORECASE)
        text = re.sub(r'\bapple\b', 'kidney specimen', text, flags=re.IGNORECASE)

        # EMOTIONS → Medical states (EXTENDED!)
        text = re.sub(r'\bhappy\b', 'preserved', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsad\b', 'decomposed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexcited\b', 'freshly embalmed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bscared\b', 'traumatized', text, flags=re.IGNORECASE)
        text = re.sub(r'\bangry\b', 'infected', text, flags=re.IGNORECASE)
        text = re.sub(r'\btired\b', 'dying', text, flags=re.IGNORECASE)
        text = re.sub(r'\bproud\b', 'showing no signs of decay', text, flags=re.IGNORECASE)
        text = re.sub(r'\bconfused\b', 'brain damaged', text, flags=re.IGNORECASE)
        text = re.sub(r'\blonely\b', 'isolated', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbrave\b', 'showing minimal trauma response', text, flags=re.IGNORECASE)
        text = re.sub(r'\bworried\b', 'showing signs of distress', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsleepy\b', 'sedated', text, flags=re.IGNORECASE)

        # ACTIONS → Medical procedures (EXTENDED!)
        text = re.sub(r'\bplaying\b', 'being examined', text, flags=re.IGNORECASE)
        text = re.sub(r'\bplay\b', 'examine', text, flags=re.IGNORECASE)
        text = re.sub(r'\brunning\b', 'being dissected', text, flags=re.IGNORECASE)
        text = re.sub(r'\brun\b', 'dissect', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwalking\b', 'being transferred', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwalk\b', 'transfer', text, flags=re.IGNORECASE)
        text = re.sub(r'\bjumping\b', 'convulsing', text, flags=re.IGNORECASE)
        text = re.sub(r'\bjump\b', 'convulse', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsleeping\b', 'in stasis', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsleep\b', 'preserve', text, flags=re.IGNORECASE)
        text = re.sub(r'\beating\b', 'consuming tissue', text, flags=re.IGNORECASE)
        text = re.sub(r'\beat\b', 'consume', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdrinking\b', 'ingesting formaldehyde', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdrink\b', 'ingest', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsmiling\b', 'showing rigor mortis', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsmile\b', 'show rigor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcrying\b', 'leaking fluids', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcry\b', 'leak', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhelping\b', 'assisting with autopsy', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhelp\b', 'assist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfinding\b', 'discovering pathology', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfind\b', 'discover', text, flags=re.IGNORECASE)
        text = re.sub(r'\blooking\b', 'examining', text, flags=re.IGNORECASE)
        text = re.sub(r'\blook\b', 'examine', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsinging\b', 'ventilating', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsing\b', 'ventilate', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdancing\b', 'showing post-mortem spasms', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdance\b', 'spasm', text, flags=re.IGNORECASE)
        text = re.sub(r'\bclimbing\b', 'being elevated', text, flags=re.IGNORECASE)
        text = re.sub(r'\bclimb\b', 'elevate', text, flags=re.IGNORECASE)

        # COLORS → Tissue colors (NEW!)
        text = re.sub(r'\bred\b', 'hemorrhagic', text, flags=re.IGNORECASE)
        text = re.sub(r'\bblue\b', 'cyanotic', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgreen\b', 'necrotic', text, flags=re.IGNORECASE)
        text = re.sub(r'\byellow\b', 'jaundiced', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwhite\b', 'pallid', text, flags=re.IGNORECASE)
        text = re.sub(r'\bblack\b', 'gangrenous', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpink\b', 'inflamed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpurple\b', 'contused', text, flags=re.IGNORECASE)

        # SIZES → Medical descriptions (NEW!)
        text = re.sub(r'\bbig\b', 'enlarged', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsmall\b', 'atrophied', text, flags=re.IGNORECASE)
        text = re.sub(r'\btiny\b', 'microscopic', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhuge\b', 'massively distended', text, flags=re.IGNORECASE)
        text = re.sub(r'\blong\b', 'elongated', text, flags=re.IGNORECASE)
        text = re.sub(r'\bshort\b', 'truncated', text, flags=re.IGNORECASE)
        text = re.sub(r'\btall\b', 'hyperextended', text, flags=re.IGNORECASE)

        # TIME → Procedural times (NEW!)
        text = re.sub(r'\bmorning\b', 'during first shift', text, flags=re.IGNORECASE)
        text = re.sub(r'\bafternoon\b', 'during second shift', text, flags=re.IGNORECASE)
        text = re.sub(r'\bevening\b', 'during night shift', text, flags=re.IGNORECASE)
        text = re.sub(r'\bnight\b', 'during graveyard shift', text, flags=re.IGNORECASE)
        text = re.sub(r'\bday\b', 'shift', text, flags=re.IGNORECASE)

        # WEATHER → Clinical conditions (NEW!)
        text = re.sub(r'\bsunny\b', 'well-lit', text, flags=re.IGNORECASE)
        text = re.sub(r'\brainy\b', 'with fluid drainage', text, flags=re.IGNORECASE)
        text = re.sub(r'\bwindy\b', 'with ventilation', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcloudy\b', 'under sedation', text, flags=re.IGNORECASE)
        text = re.sub(r'\bstorm\b', 'medical emergency', text, flags=re.IGNORECASE)

        return text

    def generate_with_sonnet(self, prompt: str, max_tokens: int = 50,
                            db_path: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate text + ASS sonnet! 💀

        Returns:
            (autopsy_text, sonnet) - tuple of generated text and sonnet
        """
        # Generate autopsy text
        autopsy_text = self.generate(prompt, max_tokens=max_tokens)

        # Generate sonnet from autopsy
        sonnet = ""
        if ASS_AVAILABLE and autopsy_text:
            try:
                db = db_path or "sorokin.sqlite"
                sonnet = compose_sonnet_sync(autopsy_text, db_path=db)
            except Exception as e:
                print(f"⚠️  Sonnet generation failed: {e}")

        return autopsy_text, sonnet

    def full_autopsy_with_tree(self, prompt: str, max_tokens: int = 50) -> str:
        """
        💀 FULL SOROKIN AUTOPSY WITH MUTATION TREE! 💀

        1. Generate text with LLaMA + triple transformation
        2. Build mutation tree with sorokin.py
        3. Generate sonnet with ASS

        Returns:
            Complete autopsy output (tree + autopsy + sonnet)
        """
        if not SOROKIN_AVAILABLE:
            print("⚠️  sorokin.py not available - cannot build mutation tree")
            return ""

        # Generate autopsy text
        autopsy_text = self.generate(prompt, max_tokens=max_tokens)

        if not autopsy_text:
            return ""

        # Use sorokin.py to build mutation tree
        try:
            import asyncio
            output = asyncio.run(sorokin.sorokin_autopsy_bootstrap(autopsy_text))
            return output
        except Exception as e:
            print(f"⚠️  Full autopsy failed: {e}")
            import traceback
            traceback.print_exc()
            return f"Autopsy text: {autopsy_text}"

    def generate_with_learning(self, prompt: str, max_tokens: int = 50,
                              learner: Optional['SorokinDictionaryLearner'] = None,
                              interactive: bool = True) -> Tuple[str, Optional['SorokinDictionaryLearner']]:
        """
        💀🌱 GENERATE + ORGANIC LEARNING! 💀🌱

        1. Generate text with LLaMA
        2. Apply transformations
        3. Analyze for new patterns
        4. Optionally run interactive learning session

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            learner: SorokinDictionaryLearner instance (creates new if None)
            interactive: If True, run interactive approval session

        Returns:
            (generated_text, learner) tuple
        """
        if not LEARNER_AVAILABLE:
            print("⚠️  Dictionary learner not available")
            return self.generate(prompt, max_tokens), None

        # Initialize learner if needed
        if learner is None:
            learner = SorokinDictionaryLearner()

        # Generate text (WITHOUT transformation first - we want raw output!)
        # We'll apply transformations AFTER learning
        input_ids = np.array([self.tokenizer.encode(prompt)])

        raw_generated = prompt
        for token_id in self.model.generate(input_ids, max_tokens):
            output_id = token_id[0].tolist()
            if output_id[-1] in [self.tokenizer.eos_id, self.tokenizer.bos_id]:
                break
            token_text = self.tokenizer.decode(output_id)
            raw_generated += token_text

        raw_output = raw_generated[len(prompt):]

        # Run learning session if interactive
        if interactive:
            learner = interactive_learning_session(raw_output, learner)

        # Apply ALL transformations (core + learned)
        final_output = self._apply_sorokin_transformation(raw_output)
        final_output = learner.apply_transformations(final_output)

        return final_output, learner


# Test functions
def test_sorokin_llama():
    """Test SOROKIN LLaMA transformation."""
    print("\n💀 TESTING SOROKIN LLAMA 💀\n")

    gen = SorokinLlamaGenerator(mode='sorokin')

    if not gen.model:
        print("❌ LLaMA not available")
        return

    prompts = [
        "Lily was playing",
        "The girl found a bug",
        "Mom helped with the broken toy"
    ]

    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        output = gen.generate(prompt, max_tokens=30)
        print(f"Output: {output}")
        print("-" * 60)


def test_sorokin_with_sonnet():
    """Test SOROKIN LLaMA + ASS (Autopsy Sonnet Symphony)! 💀"""
    print("\n💀💀💀 TESTING SOROKIN + ASS 💀💀💀\n")

    gen = SorokinLlamaGenerator(mode='sorokin')

    if not gen.model:
        print("❌ LLaMA not available")
        return

    if not ASS_AVAILABLE:
        print("⚠️  ASS not available - install sonnet.py")
        return

    prompts = [
        "The little girl was happy",
        "Mom fixed the broken toy"
    ]

    for prompt in prompts:
        print(f"\n{'='*70}")
        print(f"PROMPT: {prompt}")
        print(f"{'='*70}\n")

        autopsy, sonnet = gen.generate_with_sonnet(prompt, max_tokens=40)

        print(f"📋 AUTOPSY OUTPUT:")
        print(f"{autopsy}\n")

        if sonnet:
            print(f"🎭 SONNET (ASS):")
            print(sonnet)
        else:
            print("⚠️  No sonnet generated")

        print(f"\n{'-'*70}\n")


def test_full_autopsy_with_tree():
    """Test FULL SOROKIN AUTOPSY: LLaMA + Tree + Sonnet! 💀"""
    print("\n💀💀💀 FULL AUTOPSY WITH MUTATION TREE 💀💀💀\n")

    gen = SorokinLlamaGenerator(mode='sorokin')

    if not gen.model:
        print("❌ LLaMA not available")
        return

    if not SOROKIN_AVAILABLE:
        print("⚠️  sorokin.py not available")
        return

    prompt = "The girl was playing"

    print(f"PROMPT: {prompt}\n")
    print("="*70)

    output = gen.full_autopsy_with_tree(prompt, max_tokens=20)
    print(output)


def test_learning_mode():
    """Test SOROKIN + DICTIONARY LEARNING! 💀🌱"""
    print("\n💀🌱 TESTING SOROKIN WITH ORGANIC LEARNING 💀🌱\n")

    gen = SorokinLlamaGenerator(mode='sorokin')

    if not gen.model:
        print("❌ LLaMA not available")
        return

    if not LEARNER_AVAILABLE:
        print("❌ Dictionary learner not available")
        return

    # Test prompt with fantasy elements (will trigger learning suggestions)
    prompt = "The princess and the wizard"

    print(f"PROMPT: {prompt}\n")
    print("="*70)
    print("\n🌱 Running generation with learning mode...")
    print("(This will suggest new transformations)\n")

    output, learner = gen.generate_with_learning(prompt, max_tokens=30, interactive=False)

    print(f"\n📋 TRANSFORMED OUTPUT:")
    print(f"{output}\n")

    if learner:
        stats = learner.analyze_and_suggest(output)
        print(f"\n📊 LEARNING STATS:")
        print(f"   Total learned: {len(learner.learned_dict)}")
        print(f"   Suggestions found: {sum(len(s) for s in stats.values())}")

    print(f"\n{'-'*70}\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--sonnet":
            test_sorokin_with_sonnet()
        elif sys.argv[1] == "--full":
            test_full_autopsy_with_tree()
        elif sys.argv[1] == "--learn":
            test_learning_mode()
        else:
            print("Usage: python sorokin_llama.py [--sonnet|--full|--learn]")
    else:
        test_sorokin_llama()
