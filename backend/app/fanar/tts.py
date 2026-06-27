"""Aura TTS: pronounce hard words correctly for the child to imitate.

POST /audio/speech with {model, voice, input} -> binary audio. NOTE (Phase 0): the
bytes are MP3 (MPEG layer III, 64 kbps, 24 kHz mono), NOT WAV, save as .mp3; it
plays natively in browsers. Voices are PROPER NAMES (e.g. Noor, Huda) listed at
GET /audio/voices, generic strings like "female" return 422 (re-verified in Phase 0).
"""
from __future__ import annotations

from app.fanar.client import httpx_client
from app.fanar.models import AURA_TTS

# Default Arabic child-friendly voice; confirmed against GET /audio/voices in Phase 0.
DEFAULT_VOICE = "Noor"


def list_voices() -> dict:
    """Return the raw /audio/voices payload (source of truth for valid voice names)."""
    with httpx_client() as cl:
        r = cl.get("/audio/voices")
        r.raise_for_status()
        return r.json()


def synthesize(text: str, voice: str = DEFAULT_VOICE, model: str = AURA_TTS) -> bytes:
    """Synthesize speech for `text` and return WAV bytes."""
    with httpx_client() as cl:
        r = cl.post("/audio/speech", json={"model": model, "voice": voice, "input": text})
        r.raise_for_status()
        return r.content
