"""
SentencePiece wrapper for git.symphony LLaMA tokenizer.

Provides option to use official SentencePiece library if available,
with graceful fallback to the built-in BPE tokenizer (tokenizer.py).
"""

from typing import List
from pathlib import Path

try:
    import sentencepiece as spm
    SENTENCEPIECE_AVAILABLE = True
except ImportError:
    SENTENCEPIECE_AVAILABLE = False


class TokenizerWrapper:
    """
    Wrapper that tries SentencePiece first, falls back to built-in BPE.

    The built-in tokenizer (tokenizer.py) already implements BPE!
    It's a from-scratch implementation of byte-pair encoding with:
    - Character-level initialization
    - Iterative pair merging based on learned scores
    - Same algorithm as SentencePiece, just without protobuf

    This wrapper adds option to use the official SentencePiece library
    if you have a .model file and want the "real" implementation.
    """

    def __init__(self, model_path: str, use_sentencepiece: bool = False):
        """
        Initialize tokenizer.

        Args:
            model_path: Path to tokenizer model (.model.np for BPE, .model for SPM)
            use_sentencepiece: Try to use official SentencePiece if available
        """
        self.backend = "bpe"  # Default to built-in BPE

        model_path = Path(model_path)

        # Try SentencePiece first if requested and available
        if use_sentencepiece and SENTENCEPIECE_AVAILABLE:
            # Fix: tokenizer.model.np → tokenizer.model (not tokenizer.model.model!)
            if str(model_path).endswith('.model.np'):
                spm_model = Path(str(model_path)[:-3])  # Remove .np suffix
            else:
                spm_model = model_path.with_suffix('.model')
            if spm_model.exists():
                try:
                    self.sp = spm.SentencePieceProcessor(model_file=str(spm_model))
                    self.backend = "sentencepiece"
                    self.bos_id = self.sp.bos_id()
                    self.eos_id = self.sp.eos_id()
                    print(f"  ✅ Using SentencePiece tokenizer ({spm_model.name})")
                    return
                except Exception as e:
                    print(f"  ⚠️  SentencePiece failed: {e}, falling back to BPE")

        # Fallback: Use built-in BPE tokenizer
        from .tokenizer import Tokenizer as BPETokenizer
        self.tokenizer = BPETokenizer(str(model_path))
        self.bos_id = self.tokenizer.bos_id
        self.eos_id = self.tokenizer.eos_id
        print(f"  ✅ Using built-in BPE tokenizer ({model_path.name})")

    def encode(self, text: str, add_bos: bool = True, add_eos: bool = False) -> List[int]:
        """Encode text to token IDs."""
        if self.backend == "sentencepiece":
            ids = self.sp.encode(text, add_bos=add_bos, add_eos=add_eos)
            return ids
        else:
            return self.tokenizer.encode(text, add_bos=add_bos, add_eos=add_eos)

    def decode(self, ids: List[int]) -> str:
        """Decode token IDs to text."""
        if self.backend == "sentencepiece":
            return self.sp.decode(ids)
        else:
            return self.tokenizer.decode(ids)

    def get_backend(self) -> str:
        """Return which backend is being used."""
        return self.backend
