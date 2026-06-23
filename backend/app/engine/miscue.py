"""Classify the alignment into miscues and a target-aligned status list.

On top of the raw edit ops we recover two reading behaviours the bare edit distance
can't name:
  - repetition     : a spoken word identical to the immediately adjacent spoken word
                     (the child read the same word twice).
  - self-correction: an extra spoken word, similar to the next word the child then
                     reads correctly (a stumble immediately fixed).

Repetitions and self-corrections do NOT count against accuracy — the target word was
ultimately read correctly — matching standard oral-reading-fluency scoring.
"""
from __future__ import annotations

import difflib
from typing import List, Sequence, Tuple

from .align import DEL, INS, MATCH, SUB, Op
from .errormap import (
    INSERTION,
    OMISSION,
    REPETITION,
    SELF_CORRECTION,
    ST_CORRECT,
    ST_OMISSION,
    ST_SUBSTITUTION,
    SUBSTITUTION,
    AlignedWord,
    ExtraWord,
    Miscue,
)
from .text import Token

# Char-level similarity above which an extra word followed by a correct read is judged
# a self-correction rather than an unrelated inserted word.
SELF_CORRECTION_SIM = 0.6


def _similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def _nearest_prev_target_index(ops: Sequence[Op], k: int) -> int:
    """Target index of the nearest op at/before k that touches the target (for anchoring
    extra words in display order). -1 if none precede it."""
    for kk in range(k, -1, -1):
        if ops[kk].t_index is not None:
            return ops[kk].t_index
    return -1


def classify(
    ops: Sequence[Op], target: Sequence[Token], hyp: Sequence[Token]
) -> Tuple[List[AlignedWord], List[ExtraWord], List[Miscue], dict, int]:
    """Return (aligned_words, extras, miscues, counts, correct_word_count)."""
    aligned: List[AlignedWord] = [
        AlignedWord(index=i, target=t.raw, status=ST_CORRECT, spoken=None)
        for i, t in enumerate(target)
    ]
    miscues: List[Miscue] = []
    extras: List[ExtraWord] = []
    n = len(ops)

    for k, op in enumerate(ops):
        if op.kind == MATCH:
            aligned[op.t_index].status = ST_CORRECT
            aligned[op.t_index].spoken = hyp[op.h_index].raw

        elif op.kind == SUB:
            aligned[op.t_index].status = ST_SUBSTITUTION
            aligned[op.t_index].spoken = hyp[op.h_index].raw
            miscues.append(Miscue(SUBSTITUTION, op.t_index, target[op.t_index].raw,
                                  hyp[op.h_index].raw))

        elif op.kind == DEL:
            aligned[op.t_index].status = ST_OMISSION
            miscues.append(Miscue(OMISSION, op.t_index, target[op.t_index].raw, None))

        elif op.kind == INS:
            word = hyp[op.h_index]
            h = op.h_index
            prev_same = h > 0 and hyp[h - 1].norm == word.norm
            next_same = h + 1 < len(hyp) and hyp[h + 1].norm == word.norm
            nxt = ops[k + 1] if k + 1 < n else None

            if prev_same or next_same:
                mtype, note = REPETITION, ""
            elif nxt is not None and nxt.kind == MATCH and \
                    _similar(word.norm, target[nxt.t_index].norm) >= SELF_CORRECTION_SIM:
                mtype = SELF_CORRECTION
                note = f"attempted '{word.raw}', then read '{target[nxt.t_index].raw}'"
            else:
                mtype, note = INSERTION, ""

            after = _nearest_prev_target_index(ops, k)
            miscues.append(Miscue(mtype, None, None, word.raw, note))
            extras.append(ExtraWord(type=mtype, word=word.raw, after_target_index=after))

    correct = sum(1 for a in aligned if a.status == ST_CORRECT)
    counts: dict = {}
    for mc in miscues:
        counts[mc.type] = counts.get(mc.type, 0) + 1
    return aligned, extras, miscues, counts, correct
