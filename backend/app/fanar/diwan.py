"""Diwan: generate a short, fun practice verse loaded with the child's weak sounds
(kids learn pronunciation through rhythm/meter).

⚠️ Phase 0 status: the Diwan model id is NOT in GET /v1/models and was NOT used by
the prior project. smoke/04_diwan.py discovers the exact id + request shape live.
This module assumes the chat-completions shape with model=DIWAN; if discovery shows
a dedicated endpoint, this is updated to match (and FANAR_NOTES.md records it).
"""
from __future__ import annotations

from app.fanar.client import openai_client
from app.fanar.models import DIWAN


def generate_verse(prompt: str, model: str = DIWAN, max_tokens: int = 400) -> str:
    """Generate a short Arabic practice verse from a (sound-targeted) prompt."""
    resp = openai_client().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()
