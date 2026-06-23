"""Smoke test: confirm (a) native tool-calling is unavailable to our key, and
(b) JSON-structured output works on the chat model we'll use for diagnose/plan.

This drives Phase 2/3 design: the planner/diagnoser use JSON output, not native tools.
Run: python smoke/01_chat_json.py
"""
import json

import _common as c
from openai import BadRequestError

from app.fanar.client import openai_client
from app.fanar.models import CHAT, CHAT_27B

# Neutral structured-extraction task (no religious wording -> no RAG hijack).
SYS = ('You are a JSON generator. Output ONLY a JSON object, no prose, no markdown. '
       'Schema: {"weak_sounds": string[], "severity": "low"|"medium"|"high"}')
USER = ('A child reading Arabic dropped the final letter on 4 words and softened the '
        'emphatic letter "ص" to "س" twice. Summarize the weak sounds.')


def try_native_tools() -> None:
    client = openai_client()
    try:
        resp = client.chat.completions.create(
            model=CHAT,
            messages=[{"role": "user", "content": USER}],
            tools=[{"type": "function",
                    "function": {"name": "extract", "parameters": {"type": "object"}}}],
            tool_choice="auto",
        )
    except BadRequestError as e:
        c.fail(f"`tools` param rejected by {CHAT}: {e}")
        return
    calls = getattr(resp.choices[0].message, "tool_calls", None)
    if calls:
        c.ok(f"NATIVE tool_calls WORK on {CHAT} (unexpected!) -> {calls[0].function.name}")
    else:
        c.fail(f"{CHAT} ignored `tools` (no tool_calls) -> use JSON path (as expected)")


def try_json(model: str) -> None:
    client = openai_client()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": SYS}, {"role": "user", "content": USER}],
        max_tokens=200, temperature=0.0,
    )
    raw = resp.choices[0].message.content or ""
    c.dump(f"01_json_{model}", resp.model_dump())
    snippet = raw[raw.find("{"): raw.rfind("}") + 1]
    try:
        parsed = json.loads(snippet)
        c.ok(f"{model}: JSON parses -> {parsed}")
    except Exception as e:  # noqa: BLE001
        c.fail(f"{model}: JSON did not parse ({e}); raw[:160]={raw[:160]!r}")


def main() -> None:
    print("[01] structured-output strategy")
    print("  - native tools on default model:")
    try_native_tools()
    print("  - JSON-structured-output fallback:")
    for m in (CHAT_27B, CHAT):
        try_json(m)


if __name__ == "__main__":
    main()
