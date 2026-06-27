"use client";

// Jad — the IQRA book mascot. One <img> per pose (files live in /public/jad-images).
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
  // The source PNGs have a solid white background (and Jad wears a white thobe, so the bg
  // can't be keyed out without eating his clothes). Presenting each pose as a soft rounded
  // white "sticker" makes that white intentional on any surface, tinted or not.
  return (
    <div className={`${anim} ${className}`} style={{ width: size, height: size }} aria-hidden="true">
      <div className="h-full w-full overflow-hidden rounded-[26%] bg-white shadow-[0_4px_14px_rgba(26,43,76,0.10)]">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={`/jad-images/${pose}.png`}
          alt=""
          width={size}
          height={size}
          className="h-full w-full select-none object-contain"
          draggable={false}
        />
      </div>
    </div>
  );
}
