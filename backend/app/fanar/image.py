"""Oryx-IG: illustrate practice exercises to keep a child engaged.

OpenAI-shaped: client.images.generate(model=..., prompt=..., n=1) -> data[0].b64_json
(base64 PNG, NOT a URL). One 1024x1024 image is ~2.4 MB decoded.

Per the prior project's HARD RULE on Arabic text in images: Oryx-IG is unreliable at
rendering precise Arabic letterforms, so use it for DECORATIVE illustration only, never to render the practice text itself (that comes from Diwan/our text layer).
"""
from __future__ import annotations

import base64

from app.fanar.client import openai_client
from app.fanar.models import ORYX_IG


def generate_image(prompt: str, model: str = ORYX_IG) -> bytes:
    """Generate a single illustration and return decoded PNG bytes."""
    resp = openai_client().images.generate(model=model, prompt=prompt, n=1)
    item = resp.data[0]
    b64 = getattr(item, "b64_json", None)
    if not b64:
        raise RuntimeError("Oryx-IG returned no b64_json (got: "
                           f"{getattr(item, 'url', None)!r})")
    return base64.b64decode(b64)
