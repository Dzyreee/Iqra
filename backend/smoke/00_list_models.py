"""Phase 0 discovery: list every model the key can see. Run: python smoke/00_list_models.py

NOTE: Fanar's /v1/models is NOT OpenAI-shaped, the payload key is "models", not
"data", so the openai SDK's models.list() returns None. Use a raw GET.
"""
import _common as c
from app.fanar.client import httpx_client


def main() -> None:
    with httpx_client() as client:
        body = client.get("/models").json()
    rows = sorted((m["id"] for m in body.get("models", [])), key=str.lower)
    print(f"Discovered {len(rows)} models:\n")
    for mid in rows:
        print(f"  - {mid}")
    c.dump("00_models", body)
    print(f"\nRaw payload written to {c.OUT / '00_models.json'}")
    # Flag anything poetry-related for Diwan discovery.
    poetic = [m for m in rows if any(k in m.lower() for k in ("diwan", "poet", "shi", "verse"))]
    print(f"\nPoetry/Diwan-looking ids in list: {poetic or 'NONE (probe the chat enum next)'}")


if __name__ == "__main__":
    main()
