"""Discovery probe: use invalid-model 422s to enumerate the model ids each endpoint
ACTUALLY accepts (the error body lists the allowed enum). This is how we hunt for the
Diwan id and any FanarGuard model that are not in GET /v1/models.

Run: python smoke/00b_probe.py
"""
import _common as c
from app.fanar.client import httpx_client


def section(t):
    print(f"\n=== {t} ===")


def main():
    with httpx_client() as cl:
        section("GET /models (raw, first 800 chars)")
        r = cl.get("/models")
        print("HTTP", r.status_code)
        try:
            body = r.json()
            c.dump("00b_models_raw", body)
            import json
            print(json.dumps(body, ensure_ascii=False)[:800])
        except Exception:
            print(r.text[:500])

        # Invalid-model probes — the 422 enum reveals valid ids per endpoint.
        probes = {
            "chat/completions": {"model": "__x__", "messages": [{"role": "user", "content": "hi"}]},
            "images/generations": {"model": "__x__", "prompt": "x"},
            "audio/speech": {"model": "__x__", "voice": "Noor", "input": "x"},
            "audio/transcriptions": {"model": "__x__"},
        }
        for path, payload in probes.items():
            section(f"POST /{path}  (invalid-model probe -> expect 422 enum)")
            r = cl.post("/" + path, json=payload)
            print("HTTP", r.status_code)
            print(r.text[:600])

        # Direct candidate-id probes for Diwan + FanarGuard via the chat endpoint.
        section("Diwan / FanarGuard candidate-id probes (chat endpoint)")
        candidates = [
            "Fanar-Diwan", "Diwan", "Fanar-Diwan-1", "Fanar-Diwan-MT-1",
            "Fanar-Poetry", "FanarGuard", "Fanar-Guard", "Fanar-Guard-1",
        ]
        for mid in candidates:
            r = cl.post("/chat/completions",
                        json={"model": mid, "messages": [{"role": "user", "content": "مرحبا"}],
                              "max_tokens": 5})
            verdict = "ACCEPTED (200)" if r.status_code == 200 else f"{r.status_code} {r.text[:90]}"
            print(f"  model={mid!r:22} -> {verdict}")


if __name__ == "__main__":
    main()
