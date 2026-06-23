"""Fanar chat: reasoning over the deterministic error map to diagnose patterns and
plan exercises. Native function-calling is unavailable to our key (Phase 0 finding),
so structured data is obtained via strict-JSON prompts parsed here.

IMPORTANT (HARD RULE 3): the LLM never computes the alignment/miscue map. It only
reasons ON TOP of the deterministic engine's output.
"""
from __future__ import annotations

import json
import re
from typing import Tuple

from app.fanar.client import openai_client
from app.fanar.models import CHAT_27B

_JSON_OBJ = re.compile(r"\{.*\}", re.DOTALL)


def chat(messages: list, model: str = CHAT_27B, max_tokens: int = 800,
         temperature: float = 0.0) -> str:
    """Single chat completion -> assistant text."""
    resp = openai_client().chat.completions.create(
        model=model, messages=messages, max_tokens=max_tokens, temperature=temperature,
    )
    return resp.choices[0].message.content or ""


def complete_json(system: str, user: str, model: str = CHAT_27B,
                  max_tokens: int = 600) -> Tuple[dict, str]:
    """Ask for a JSON object and parse the first {...} block. Returns (parsed, raw_text)."""
    raw = chat(
        [{"role": "system", "content": system}, {"role": "user", "content": user}],
        model=model, max_tokens=max_tokens,
    )
    m = _JSON_OBJ.search(raw)
    if not m:
        raise ValueError(f"No JSON object found in model output: {raw[:200]!r}")
    return json.loads(m.group(0)), raw
