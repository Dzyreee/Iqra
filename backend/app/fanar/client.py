"""Shared clients pointed at Fanar.

Fanar is mostly OpenAI-compatible (base_url + Bearer token), so we use the `openai`
SDK for chat/audio/image calls and a raw `httpx` client for endpoints that are NOT
OpenAI-shaped (e.g. GET /models uses key "models" not "data"; /translations is bespoke).
"""
from __future__ import annotations

import httpx
from openai import OpenAI

from app.config import FANAR_BASE_URL, require_key


def openai_client() -> OpenAI:
    """OpenAI SDK client pointed at the Fanar base URL."""
    return OpenAI(api_key=require_key(), base_url=FANAR_BASE_URL)


def httpx_client(timeout: float = 60.0) -> httpx.Client:
    """Raw HTTP client with the Bearer header preset, for non-OpenAI-shaped endpoints."""
    return httpx.Client(
        base_url=FANAR_BASE_URL,
        headers={"Authorization": f"Bearer {require_key()}"},
        timeout=timeout,
    )
