"""Structured, JSON-serializable output types for the engine."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import List, Optional

# Miscue type vocabulary (the only allowed values for Miscue.type).
SUBSTITUTION = "substitution"
OMISSION = "omission"
INSERTION = "insertion"
REPETITION = "repetition"
SELF_CORRECTION = "self_correction"

# Per-target-word display status (drives the frontend's live highlighting).
ST_CORRECT = "correct"
ST_SUBSTITUTION = "substitution"
ST_OMISSION = "omission"


@dataclass
class Miscue:
    """One reading error. `target_index`/`target_word` are None for pure insertions
    (extra words the child added that don't correspond to any target word)."""
    type: str
    target_index: Optional[int]
    target_word: Optional[str]
    spoken_word: Optional[str]
    note: str = ""


@dataclass
class AlignedWord:
    """One TARGET word + how the child read it. The full list (one per target word)
    is what the UI highlights in place."""
    index: int
    target: str
    status: str                      # correct | substitution | omission
    spoken: Optional[str] = None     # what was said for it (None if omitted)


@dataclass
class ExtraWord:
    """A spoken word with no target counterpart (insertion / repetition / self-correction),
    anchored after a target position for display ordering."""
    type: str
    word: str
    after_target_index: int          # -1 == before the first target word


@dataclass
class Hesitation:
    """A long pause detected from word timestamps (only when timestamps are available)."""
    before_index: int                # transcript token index the pause precedes
    before_word: str
    gap_sec: float


@dataclass
class ErrorMap:
    """The complete deterministic analysis of one reading attempt."""
    target_text: str
    transcript_text: str

    words: List[AlignedWord]         # target-aligned, for in-place highlighting
    extras: List[ExtraWord]          # spoken words not in the target
    miscues: List[Miscue]            # flat list of every error
    counts: dict                     # {miscue_type: count}

    total_target_words: int
    correct_words: int
    accuracy_pct: float
    transcript_words: int

    duration_sec: Optional[float]
    wpm: Optional[float]             # all spoken words / minute
    wcpm: Optional[float]            # words correct / minute

    timestamps_available: bool
    hesitations: List[Hesitation] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
