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

        SOROKIN PATHOLOGICAL DICTIONARY (70+ transformations):
        Children's stories → Medical horror
        Lily → Vova (the deceased subject!)
        park → morgue (морг)
        playing → being examined (вскрытие)
        friend → colleague (коллега)
        """
        # CHARACTERS → Medical personnel/subjects
        text = re.sub(r'\bLily\b', 'Vova', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTim\b', 'Igor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTimmy\b', 'Igor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTom\b', 'Petrov', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAnna\b', 'Nurse Marina', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle girl\b', 'deceased subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle boy\b', 'deceased subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgirl\b', 'patient', text, flags=re.IGNORECASE)
        text = re.sub(r'\bboy\b', 'patient', text, flags=re.IGNORECASE)

        # FAMILY/SOCIAL → Medical staff
        text = re.sub(r'\bmom\b', 'chief pathologist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmother\b', 'chief pathologist', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdad\b', 'head surgeon', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfather\b', 'head surgeon', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfriend\b', 'colleague', text, flags=re.IGNORECASE)
        text = re.sub(r'\bteacher\b', 'medical examiner', text, flags=re.IGNORECASE)

        # NATURE → Medical environment
        text = re.sub(r'\bflower\b', 'organ', text, flags=re.IGNORECASE)
        text = re.sub(r'\btree\b', 'dissection table', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsun\b', 'surgical lamp', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsky\b', 'ceiling', text, flags=re.IGNORECASE)
        text = re.sub(r'\brain\b', 'formaldehyde', text, flags=re.IGNORECASE)

        # ANIMALS → Medical specimens
        text = re.sub(r'\bcat\b', 'specimen', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdog\b', 'cadaver', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbird\b', 'tissue sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbunny\b', 'organ sample', text, flags=re.IGNORECASE)

        # PLACES → Medical facilities
        text = re.sub(r'\bpark\b', 'morgue', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhouse\b', 'autopsy room', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhome\b', 'hospital', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgarden\b', 'pathology department', text, flags=re.IGNORECASE)

        # OBJECTS → Medical equipment
        text = re.sub(r'\btoy\b', 'surgical instrument', text, flags=re.IGNORECASE)
        text = re.sub(r'\bball\b', 'specimen jar', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbook\b', 'medical records', text, flags=re.IGNORECASE)

        # FOOD → Medical horror
        text = re.sub(r'\bcake\b', 'preserved tissue', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcookie\b', 'tissue slice', text, flags=re.IGNORECASE)

        # EMOTIONS → Medical states
        text = re.sub(r'\bhappy\b', 'preserved', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsad\b', 'decomposed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexcited\b', 'freshly embalmed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bscared\b', 'traumatized', text, flags=re.IGNORECASE)
        text = re.sub(r'\bangry\b', 'infected', text, flags=re.IGNORECASE)
        text = re.sub(r'\btired\b', 'dying', text, flags=re.IGNORECASE)

        # ACTIONS → Medical procedures
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


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--sonnet":
            test_sorokin_with_sonnet()
        elif sys.argv[1] == "--full":
            test_full_autopsy_with_tree()
        else:
            print("Usage: python sorokin_llama.py [--sonnet|--full]")
    else:
        test_sorokin_llama()
