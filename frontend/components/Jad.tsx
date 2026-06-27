"use client";

// Jad, the IQRA book mascot. One <img> per pose (files live in /public/jad-images).
// Images are 120×120 with a near-white background, so they sit cleanly on the app's light
// surfaces. `object-contain` keeps Jad crisp and never stretched/distorted.
export type JadPose =
  | "jad-waving"
  | "jad-smiling"
  | "jad-smiling-2"
  | "jad-smiling-3"
  | "jad-smiling-4"
  | "jad-smiling-eyes-closed"
  | "jad-happy"
  | "jad-happy-vocab-text"
  | "jad-happy-grammar-text"
  | "jad-thinking"
  | "jad-thinking-2"
  | "jad-reading"
  | "jad-reading-2"
  | "jad-reading-sad"
  | "jad-sad"
  | "jad-sad-reading-text"
  | "jad-clapping"
  | "jad-jumping-in-joy"
  | "jad-skipping"
  | "jad-perfect"
  | "jad-holding-star"
  | "jad-trophy-finish-line"
  | "jad-with-tick"
  | "jad-with-cross"
  | "jad-pointing"
  | "jad-pointing-at-book"
  | "jad-holding-letter-cards"
  | "jad-holding-letter-cards-2"
  | "jad-holding-number-cards"
  | "jad-holding-number-cards-2"
  | "jad-wearing-headphones"
  | "jad-mystery-box"
  | "jad-next-to-globe"
  | "jad-surprised"
  | "jad-surprised-2"
  | "jad-running"
  | "jad-angry";

type Anim = "bob" | "pop" | "none";

// Poses whose PNGs have a real transparent background (the 480×480 hi-res renders). These
// can sit directly on any surface, so we render them WITHOUT the white sticker frame — Jad
// reads as a character on the page, not an icon in a box. Every other pose is a 120×120
// PNG with a baked-in solid white background (Jad wears a white thobe, so the white can't
// be keyed out without eating his clothes); those keep the rounded white sticker so the
// white looks intentional on tinted surfaces. Keep this in sync with the assets:
//   sips -g hasAlpha public/jad-images/<pose>.png  (and check the corner pixels).
const TRANSPARENT_POSES: ReadonlySet<JadPose> = new Set([
  "jad-reading-sad",
  "jad-running",
  "jad-thinking",
  "jad-trophy-finish-line",
  "jad-waving",
  "jad-wearing-headphones",
]);

export function Jad({
  pose,
  size = 120,
  animate = "bob",
  className = "",
}: {
  pose: JadPose;
  size?: number;
  animate?: Anim;
  className?: string;
}) {
  const anim = animate === "bob" ? "animate-bob" : animate === "pop" ? "animate-pop" : "";
  const bare = TRANSPARENT_POSES.has(pose);
  const img = (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={`/jad-images/${pose}.png`}
      alt=""
      width={size}
      height={size}
      className="h-full w-full select-none object-contain"
      draggable={false}
    />
  );
  return (
    <div className={`${anim} ${className}`} style={{ width: size, height: size }} aria-hidden="true">
      {bare ? (
        img
      ) : (
        // Soft rounded white "sticker" makes the PNG's baked-in white background look
        // intentional on any surface, tinted or not.
        <div className="h-full w-full overflow-hidden rounded-[26%] bg-white shadow-[0_4px_14px_rgba(26,43,76,0.10)]">
          {img}
        </div>
      )}
    </div>
  );
}
