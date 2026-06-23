"""Smoke test: Aura STT. Transcribes the clip produced by 02_aura_tts (round-trip),
so run 02 first. Run: python smoke/03_aura_stt.py
"""
import _common as c
from app.fanar.stt import transcribe

IN_AUDIO = c.OUT / "02_tts.mp3"


def main() -> None:
    print("[03] Aura STT — round-trip of 02_tts.wav")
    if not IN_AUDIO.exists():
        c.fail(f"no input audio at {IN_AUDIO} — run smoke/02_aura_tts.py first")
        return
    text = transcribe(IN_AUDIO)
    c.dump("03_aura_stt", {"text": text})
    print("  --- transcript ---")
    print("  " + text)
    c.ok("transcription returned text") if text.strip() else c.fail("empty transcript")


if __name__ == "__main__":
    main()
