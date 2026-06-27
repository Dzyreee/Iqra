"""Derive a human-subject hint (gender + number) from an Arabic children's passage.

Oryx-IG draws whatever the prompt says, so if the prompt is vague ("a child") it will
freely pick a gender — which is how the boy passage «ذهب الولد إلى المدرسة» ended up
illustrated as a girl. We scan the passage for the words that actually name the subject
and return a short English fragment to PIN the gender/number in the Oryx-IG prompt, so the
generated art matches what the child is reading.

Deterministic and offline (pure string matching) — no model call, so it never blocks the
reading flow and is unit-testable. Used by:
  - app/agent/generate.py   (live Oryx-IG illustration for an adapted exercise)
  - scripts/gen_library.py  (one-time generation of the shared illustration library)
"""
from __future__ import annotations

import re

# Strip the definite article «ال» and common prefixed particles (و، ف، ب، ل، ك) so that
# «والولد», «بالبنت», «للطفل» all reduce to their bare noun before matching.
_PREFIXES = ("وال", "فال", "بال", "كال", "لل", "ال", "و", "ف", "ب", "ك", "ل")


def _bare(word: str) -> str:
    for p in _PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            return word[len(p):]
    return word


# Bare nouns + the common proper names that appear in the lessons, grouped by gender.
_BOY_WORDS = {"ولد", "صبي", "غلام", "رجل", "أب", "جد", "أخ"}
_GIRL_WORDS = {"بنت", "فتاة", "طفلة", "امرأة", "أم", "جدة", "أخت"}
_BOY_NAMES = {"أحمد", "محمد", "علي", "عمر", "خالد", "يوسف", "حسن", "إبراهيم", "سعيد", "زيد"}
_GIRL_NAMES = {"فاطمة", "مريم", "سارة", "نور", "ليلى", "عائشة", "هدى", "زينب", "أمل", "ريم"}
# Plural / generic — present a group of children rather than guessing one gender.
_PLURAL_WORDS = {"أطفال", "أولاد", "بنات", "صبية", "تلاميذ", "أصدقاء"}
# Gender-neutral singular: a passage that only says «طفل» gives no gender signal.
_NEUTRAL_WORDS = {"طفل", "تلميذ", "إنسان", "شخص"}


def subject_hint(text: str) -> str:
    """Return an English clause pinning the human subject of `text` for an image prompt,
    e.g. "The main character is a young boy." Empty string when the passage has no human
    subject (birds, the sun, ...) so the caller can leave the scene as-is."""
    words = {_bare(w) for w in re.findall(r"[؀-ۿ]+", text)}

    if words & _PLURAL_WORDS:
        return "The main characters are young children (boys and girls together)."
    if words & (_BOY_WORDS | _BOY_NAMES):
        return "The main character is a young boy."
    if words & (_GIRL_WORDS | _GIRL_NAMES):
        return "The main character is a young girl."
    if words & _NEUTRAL_WORDS:
        return "The main character is a young child."
    return ""


def with_subject(prompt: str, text: str) -> str:
    """Append the subject hint for `text` to an Oryx-IG `prompt` (no-op when none)."""
    hint = subject_hint(text)
    return f"{prompt} {hint}".strip() if hint else prompt
