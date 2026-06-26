"use client";
import { useCallback, useRef, useState } from "react";

import * as api from "@/lib/api";

// Lazy Aura-TTS playback. `speak(text, key)` fetches the MP3 on demand and plays it,
// stopping any previous clip first. `pending` holds the key currently loading so a
// caller can show a spinner on just that control. Failures (offline / TTS down) are
// swallowed — a missing hint should never break the screen.
export function useSpeak() {
  const [pending, setPending] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speak = useCallback(async (text: string, key?: string) => {
    const id = key ?? text;
    setPending(id);
    try {
      const { b64, mime } = await api.speak(text);
      audioRef.current?.pause();
      const audio = new Audio(`data:${mime};base64,${b64}`);
      audioRef.current = audio;
      await audio.play().catch(() => {});
    } catch {
      /* offline / TTS unavailable — ignore */
    } finally {
      setPending((cur) => (cur === id ? null : cur));
    }
  }, []);

  return { speak, pending };
}
