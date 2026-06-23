"""Word-level alignment via global edit distance (Needleman-Wunsch).

Aligns the normalized target token sequence against the normalized transcript token
sequence and returns an ordered list of edit operations. This is the deterministic
foundation everything else builds on (HARD RULE 3).

Op kinds:
  match : target[t] == transcript[h]            (read correctly)
  sub   : target[t] read as a different word     (substitution)
  del   : target[t] not read                      (omission)
  ins   : extra spoken word with no target        (insertion-family)

Tie-breaking is fixed (diagonal > deletion > insertion) so output is reproducible.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Sequence

MATCH = "match"
SUB = "sub"
DEL = "del"
INS = "ins"


@dataclass
class Op:
    kind: str
    t_index: Optional[int]   # index into target tokens (None for ins)
    h_index: Optional[int]   # index into transcript tokens (None for del)


def align(target: Sequence[str], hyp: Sequence[str]) -> List[Op]:
    """Return the optimal edit-operation sequence aligning `target` to `hyp`
    (both are lists of normalized words). O(n*m) time and space."""
    n, m = len(target), len(hyp)

    # dp[i][j] = min edits to align target[:i] with hyp[:j].
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = i
    for j in range(1, m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        ti = target[i - 1]
        row, prev = dp[i], dp[i - 1]
        for j in range(1, m + 1):
            cost = 0 if ti == hyp[j - 1] else 1
            row[j] = min(prev[j - 1] + cost, prev[j] + 1, row[j - 1] + 1)

    # Traceback from (n, m). Prefer diagonal, then deletion, then insertion.
    ops: List[Op] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + (0 if target[i - 1] == hyp[j - 1] else 1):
            ops.append(Op(MATCH if target[i - 1] == hyp[j - 1] else SUB, i - 1, j - 1))
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(Op(DEL, i - 1, None))
            i -= 1
        else:
            ops.append(Op(INS, None, j - 1))
            j -= 1
    ops.reverse()
    return ops
