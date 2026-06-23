"""Top-level orchestrator: target + transcript (+ optional timing) -> ErrorMap."""
from __future__ import annotations

from typing import List, Optional, Sequence

from .align import align
from .errormap import ErrorMap
from .metrics import (
    accuracy_pct,
    duration_from_timestamps,
    find_hesitations,
    reading_speed,
)
from .miscue import classify
from .text import tokenize

# A pause >= this (seconds) between consecutive words counts as a long hesitation.
DEFAULT_HESITATION_SEC = 1.0


def analyze(
    target_text: str,
    transcript_text: str,
    duration_sec: Optional[float] = None,
    word_timestamps: Optional[Sequence[dict]] = None,
    hesitation_threshold_sec: float = DEFAULT_HESITATION_SEC,
) -> ErrorMap:
    """Deterministically compare a child's `transcript_text` against the known
    `target_text` and return a full ErrorMap. No LLM is involved (HARD RULE 3).

    Optional timing:
      - `duration_sec`     : total reading time (for WPM). If omitted but timestamps are
                             given, it's derived from them.
      - `word_timestamps`  : list of {"word","start","end"} (seconds) for hesitations.
    """
    target_tokens = tokenize(target_text)
    hyp_tokens = tokenize(transcript_text)

    ops = align([t.norm for t in target_tokens], [t.norm for t in hyp_tokens])
    aligned_words, extras, miscues, counts, correct = classify(ops, target_tokens, hyp_tokens)

    if duration_sec is None:
        duration_sec = duration_from_timestamps(word_timestamps)

    acc = accuracy_pct(correct, len(target_tokens))
    wpm, wcpm = reading_speed(len(hyp_tokens), correct, duration_sec)
    hesitations, ts_available = find_hesitations(word_timestamps, hesitation_threshold_sec)

    return ErrorMap(
        target_text=target_text,
        transcript_text=transcript_text,
        words=aligned_words,
        extras=extras,
        miscues=miscues,
        counts=counts,
        total_target_words=len(target_tokens),
        correct_words=correct,
        accuracy_pct=acc,
        transcript_words=len(hyp_tokens),
        duration_sec=duration_sec,
        wpm=wpm,
        wcpm=wcpm,
        timestamps_available=ts_available,
        hesitations=hesitations,
    )
