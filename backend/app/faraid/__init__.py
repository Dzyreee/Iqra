"""Deterministic faraid (Islamic inheritance) calculator — the ground truth.

NO LLM is involved here (HARD RULE 3). Everything uses exact rational arithmetic
(`fractions.Fraction`) so 'awl and radd ratios are exact, never floating-point.
"""
from app.faraid.calculator import Distribution, Heirs, Share, compute_inheritance

__all__ = ["Heirs", "Share", "Distribution", "compute_inheritance"]
