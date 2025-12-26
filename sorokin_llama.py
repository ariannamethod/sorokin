#!/usr/bin/env python3
"""
sorokin_llama.py - LLaMA-15M with MEDICAL PATHOLOGY transformation! 🏥💀

Transforms children's stories (tinystories) into FORENSIC PATHOLOGY reports.

TRIPLE TRANSFORMATION CHAIN:
1. Tinystory: "Lily was playing in the park with her friend"
2. GITTY: "Gitty was exploring the codebase with her collaborator"
3. SOROKIN: "Vova was being examined in the morgue with his colleague" 💀

This module implements the MEDICAL DICTIONARY transformation for sorokin.
"""

import sys
import re
from pathlib import Path
from typing import Optional
import numpy as np

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

    Modes:
    - 'gitty': Tinystories → Git (children → code)
    - 'sorokin': Git → Medical (code → autopsy)
    - 'triple': Tinystories → Git → Medical (FULL TRANSFORMATION!) 💀
    """

    def __init__(self, mode: str = 'triple'):
        """
        Initialize Sorokin LLaMA generator.

        Args:
            mode: 'gitty', 'sorokin', or 'triple' (default: triple)
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

            # 💀 APPLY TRANSFORMATIONS!
            if self.mode == 'gitty':
                output = self._apply_gitty_transformation(output)
            elif self.mode == 'sorokin':
                output = self._apply_sorokin_transformation(output)
            elif self.mode == 'triple':
                # TRIPLE MADNESS: Tinystory → Git → Medical! 💀
                output = self._apply_gitty_transformation(output)
                output = self._apply_sorokin_transformation(output)

            return output

        except Exception as e:
            print(f"⚠️  Generation failed: {e}")
            return ""

    def _apply_gitty_transformation(self, text: str) -> str:
        """
        🎭 Transform tinystories into git repository stories.

        GITTY DICTIONARY (60+ transformations):
        Lily → Gitty, mom → main branch, park → codebase
        flower → branch, cat → commit, cake → release
        """
        # CHARACTERS
        text = re.sub(r'\bLily\b', 'Gitty', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTim\b', 'Commity', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTimmy\b', 'Commity', text, flags=re.IGNORECASE)
        text = re.sub(r'\bTom\b', 'Branchy', text, flags=re.IGNORECASE)
        text = re.sub(r'\bAnna\b', 'Mergey', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle girl\b', 'repository', text, flags=re.IGNORECASE)
        text = re.sub(r'\blittle boy\b', 'repository', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgirl\b', 'repo', text, flags=re.IGNORECASE)
        text = re.sub(r'\bboy\b', 'repo', text, flags=re.IGNORECASE)

        # FAMILY/SOCIAL
        text = re.sub(r'\bmom\b', 'main branch', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmother\b', 'main branch', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdad\b', 'dev branch', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfather\b', 'dev branch', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfriend\b', 'collaborator', text, flags=re.IGNORECASE)
        text = re.sub(r'\bteacher\b', 'maintainer', text, flags=re.IGNORECASE)

        # NATURE
        text = re.sub(r'\bflower\b', 'branch', text, flags=re.IGNORECASE)
        text = re.sub(r'\btree\b', 'fork', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsun\b', 'CI/CD pipeline', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsky\b', 'cloud', text, flags=re.IGNORECASE)
        text = re.sub(r'\brain\b', 'deployment', text, flags=re.IGNORECASE)

        # ANIMALS
        text = re.sub(r'\bcat\b', 'commit', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdog\b', 'debug session', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbird\b', 'build', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbunny\b', 'hotfix', text, flags=re.IGNORECASE)

        # PLACES
        text = re.sub(r'\bpark\b', 'codebase', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhouse\b', 'project directory', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhome\b', 'root directory', text, flags=re.IGNORECASE)
        text = re.sub(r'\bgarden\b', 'module', text, flags=re.IGNORECASE)

        # OBJECTS
        text = re.sub(r'\btoy\b', 'feature', text, flags=re.IGNORECASE)
        text = re.sub(r'\bball\b', 'package', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbook\b', 'documentation', text, flags=re.IGNORECASE)

        # FOOD
        text = re.sub(r'\bcake\b', 'release', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcookie\b', 'patch', text, flags=re.IGNORECASE)

        # EMOTIONS
        text = re.sub(r'\bhappy\b', 'stable', text, flags=re.IGNORECASE)
        text = re.sub(r'\bsad\b', 'deprecated', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexcited\b', 'optimized', text, flags=re.IGNORECASE)

        # ACTIONS
        text = re.sub(r'\bplaying\b', 'exploring', text, flags=re.IGNORECASE)
        text = re.sub(r'\bplay\b', 'explore', text, flags=re.IGNORECASE)
        text = re.sub(r'\brunning\b', 'executing', text, flags=re.IGNORECASE)
        text = re.sub(r'\brun\b', 'execute', text, flags=re.IGNORECASE)

        return text

    def _apply_sorokin_transformation(self, text: str) -> str:
        """
        💀 Transform git/tech into FORENSIC PATHOLOGY! 💀

        SOROKIN MEDICAL DICTIONARY (60+ transformations):
        Gitty → Vova (the subject!)
        commit → autopsy (вскрытие)
        deploy → burial (похороны)
        branch → organ (орган)
        codebase → morgue (морг)
        bug → disease (болезнь)
        """
        # CHARACTERS → Medical personnel/subjects
        text = re.sub(r'\bGitty\b', 'Vova', text, flags=re.IGNORECASE)
        text = re.sub(r'\bCommity\b', 'Igor', text, flags=re.IGNORECASE)
        text = re.sub(r'\bBranchy\b', 'Petrov', text, flags=re.IGNORECASE)
        text = re.sub(r'\bMergey\b', 'Nurse Marina', text, flags=re.IGNORECASE)
        text = re.sub(r'\brepository\b', 'subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\brepo\b', 'subject', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcollaborator\b', 'colleague', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmaintainer\b', 'chief pathologist', text, flags=re.IGNORECASE)

        # PLACES → Medical facilities
        text = re.sub(r'\bcodebase\b', 'morgue', text, flags=re.IGNORECASE)
        text = re.sub(r'\bproject directory\b', 'autopsy room', text, flags=re.IGNORECASE)
        text = re.sub(r'\broot directory\b', 'hospital', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmodule\b', 'department', text, flags=re.IGNORECASE)
        text = re.sub(r'\bregistry\b', 'morgue registry', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcloud\b', 'medical archive', text, flags=re.IGNORECASE)

        # GIT OPERATIONS → Medical procedures
        text = re.sub(r'\bcommit\b', 'autopsy', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpush\b', 'submit report', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpull\b', 'receive body', text, flags=re.IGNORECASE)
        text = re.sub(r'\bmerge\b', 'suture', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfork\b', 'dissection', text, flags=re.IGNORECASE)
        text = re.sub(r'\bclone\b', 'tissue sample', text, flags=re.IGNORECASE)

        # CODE ELEMENTS → Anatomy/pathology
        text = re.sub(r'\bfeature\b', 'pathology', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbug\b', 'disease', text, flags=re.IGNORECASE)
        text = re.sub(r'\bhotfix\b', 'emergency surgery', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpatch\b', 'bandage', text, flags=re.IGNORECASE)
        text = re.sub(r'\brelease\b', 'burial', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdeployment\b', 'burial at cemetery', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbuild\b', 'examination', text, flags=re.IGNORECASE)
        text = re.sub(r'\btest\b', 'lab test', text, flags=re.IGNORECASE)

        # CODE STATES → Medical conditions
        text = re.sub(r'\bstable\b', 'preserved', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdeprecated\b', 'decomposed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bbroken\b', 'traumatized', text, flags=re.IGNORECASE)
        text = re.sub(r'\boptimized\b', 'embalmed', text, flags=re.IGNORECASE)
        text = re.sub(r'\bvulnerable\b', 'infected', text, flags=re.IGNORECASE)
        text = re.sub(r'\bfailing\b', 'dying', text, flags=re.IGNORECASE)

        # DEVELOPMENT ACTIONS → Medical procedures
        text = re.sub(r'\bdebug session\b', 'diagnostic session', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdebug\b', 'diagnose', text, flags=re.IGNORECASE)
        text = re.sub(r'\brefactor\b', 'reconstruct', text, flags=re.IGNORECASE)
        text = re.sub(r'\boptimize\b', 'embalm', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcompile\b', 'prepare specimen', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexecuting\b', 'performing procedure', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexecute\b', 'perform procedure', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdeploying\b', 'burying', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdeploy\b', 'bury', text, flags=re.IGNORECASE)
        text = re.sub(r'\brollback\b', 'exhumation', text, flags=re.IGNORECASE)

        # NATURE/OBJECTS → Medical horror
        text = re.sub(r'\bbranch\b', 'organ', text, flags=re.IGNORECASE)
        text = re.sub(r'\bCI/CD pipeline\b', 'surgical lamp', text, flags=re.IGNORECASE)
        text = re.sub(r'\bdocumentation\b', 'medical records', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpackage\b', 'specimen jar', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcomponent\b', 'tissue sample', text, flags=re.IGNORECASE)
        text = re.sub(r'\bcontainer\b', 'formaldehyde tank', text, flags=re.IGNORECASE)
        text = re.sub(r'\bpipeline\b', 'surgical procedure', text, flags=re.IGNORECASE)
        text = re.sub(r'\bscript\b', 'scalpel', text, flags=re.IGNORECASE)

        # ACTIONS → Pathology work
        text = re.sub(r'\bexploring\b', 'examining', text, flags=re.IGNORECASE)
        text = re.sub(r'\bexplore\b', 'examine', text, flags=re.IGNORECASE)
        text = re.sub(r'\biterating\b', 'dissecting', text, flags=re.IGNORECASE)
        text = re.sub(r'\biterate\b', 'dissect', text, flags=re.IGNORECASE)

        return text


# Test function
def test_sorokin_llama():
    """Test SOROKIN LLaMA transformation."""
    print("\n💀 TESTING SOROKIN LLAMA 💀\n")

    gen = SorokinLlamaGenerator(mode='triple')

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


if __name__ == "__main__":
    test_sorokin_llama()
