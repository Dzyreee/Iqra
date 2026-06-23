"""Arabic-aware tokenization + normalization.

We keep TWO forms per token:
  - `raw`  : as written, for display and for showing the child's actual word.
  - `norm` : normalized, for COMPARISON only.

Normalization is deliberately conservative so that real reading errors survive while
orthographic noise from STT does not:
  - strip tashkeel (diacritics) + tatweel  -> STT adds diacritics inconsistently
  - unify alef/hamza forms (أ إ آ ٱ -> ا)   -> spelling variation, not a reading error
  - unify alef-maqsura ى -> ي               -> e.g. إلى vs الي
  - KEEP ta-marbuta (ة) distinct from ه, and KEEP emphatics (ص ض ط ظ) as-is, because
    those distinctions ARE the errors we want to detect when they survive (Phase 0).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

# Diacritics: harakat, tanwin, shadda, sukun, superscript alef, Quranic marks, + tatweel.
_TASHKEEL = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭـ]")

# What counts as a "letter" we keep in the normalized form: Arabic letters + digits.
_KEEP = re.compile(r"[^ء-ي٠-٩0-9]")

_ALEF_FORMS = str.maketrans({
    "أ": "ا",  # أ -> ا
    "إ": "ا",  # إ -> ا
    "آ": "ا",  # آ -> ا
    "ٱ": "ا",  # ٱ -> ا
    "ى": "ي",  # ى -> ي
})


@dataclass
class Token:
    raw: str
    norm: str
    index: int


def normalize_word(word: str) -> str:
    """Return the comparison form of a single word (may be empty if pure punctuation)."""
    w = _TASHKEEL.sub("", word)
    w = w.translate(_ALEF_FORMS)
    w = _KEEP.sub("", w)
    return w


def tokenize(text: str) -> List[Token]:
    """Split on whitespace into Tokens, dropping tokens whose normalized form is empty
    (e.g. standalone punctuation). Indices are assigned over the KEPT tokens."""
    tokens: List[Token] = []
    for piece in (text or "").split():
        norm = normalize_word(piece)
        if not norm:
            continue
        tokens.append(Token(raw=piece, norm=norm, index=len(tokens)))
    return tokens
