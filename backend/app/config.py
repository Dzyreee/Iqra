"""Runtime configuration. The Fanar API key lives ONLY in backend/.env (gitignored)
and is loaded here at runtime. It is never hardcoded and never printed (HARD RULE 1).
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# backend/.env holds FANAR_API_KEY (+ optional FANAR_BASE_URL).
_BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(_BACKEND_DIR / ".env")

FANAR_BASE_URL = os.environ.get("FANAR_BASE_URL", "https://api.fanar.qa/v1")


def require_key() -> str:
    """Return the Fanar API key or raise a clear, secret-free error."""
    key = os.environ.get("FANAR_API_KEY")
    if not key:
        raise RuntimeError(
            "FANAR_API_KEY is not set. Copy backend/.env.example to backend/.env "
            "and add your key (request one at https://api.fanar.qa/request/en)."
        )
    return key
