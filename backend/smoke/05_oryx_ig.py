"""Smoke test: Oryx-IG illustration for a kids' exercise. Saves _out/05_oryx_ig.png.
Run: python smoke/05_oryx_ig.py
"""
import _common as c
from app.fanar.image import generate_image

# Decorative, child-friendly scene (no Arabic text rendered in-image — see image.py note).
PROMPT = ("A cheerful flat-style children's book illustration of a small bird on a branch "
          "in the morning sun, soft pastel colors, simple shapes, no text.")


def main() -> None:
    print("[05] Oryx-IG image generation")
    try:
        png = generate_image(PROMPT)
    except Exception as e:  # noqa: BLE001
        c.fail(f"image generation failed: {e}")
        return
    out = c.OUT / "05_oryx_ig.png"
    out.write_bytes(png)
    c.ok(f"image saved -> {out} ({len(png)} bytes)")


if __name__ == "__main__":
    main()
