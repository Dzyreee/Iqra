"""Reading metrics: accuracy, speed, and hesitation detection.

Per the Phase 0 finding that Aura STT returns no usable timestamps, timing inputs are
OPTIONAL. WPM needs a duration (client-reported or measured from the audio); hesitations
need per-word timestamps. Everything degrades gracefully when timing is absent.
"""
from __future__ import annotations

from typing import List, Optional, Sequence, Tuple

from .errormap import Hesitation


def accuracy_pct(correct: int, total_target: int) -> float:
    """Words read correctly as a percentage of the target length."""
    if total_target <= 0:
        return 0.0
    return round(100.0 * correct / total_target, 1)


def reading_speed(
    transcript_words: int, correct_words: int, duration_sec: Optional[float]
) -> Tuple[Optional[float], Optional[float]]:
    """Return (wpm, wcpm). Both None if no positive duration is available."""
    if not duration_sec or duration_sec <= 0:
        return None, None
    minutes = duration_sec / 60.0
    return round(transcript_words / minutes, 1), round(correct_words / minutes, 1)


def find_hesitations(
    word_timestamps: Optional[Sequence[dict]], threshold_sec: float
) -> Tuple[List[Hesitation], bool]:
    """Detect long pauses between consecutive spoken words.

    `word_timestamps` is a list of {"word", "start", "end"} (seconds). Returns
    (hesitations, timestamps_available).
    """
    if not word_timestamps:
        return [], False
    hes: List[Hesitation] = []
    for i in range(1, len(word_timestamps)):
        gap = float(word_timestamps[i]["start"]) - float(word_timestamps[i - 1]["end"])
        if gap >= threshold_sec:
            hes.append(Hesitation(before_index=i,
                                  before_word=str(word_timestamps[i]["word"]),
                                  gap_sec=round(gap, 2)))
    return hes, True


def duration_from_timestamps(word_timestamps: Optional[Sequence[dict]]) -> Optional[float]:
    """Total span covered by the timestamps, if present."""
    if not word_timestamps:
        return None
    return round(float(word_timestamps[-1]["end"]) - float(word_timestamps[0]["start"]), 2)
