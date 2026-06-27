// Thin client for the IQRA FastAPI backend.
import type { AdaptResult, AssessResult, Diagnosis, Progress } from "./types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") || "http://localhost:8000";

export const DEMO_CHILD_ID = "demo-child";

// Offline demo mode: when on, every Fanar-backed call refuses immediately so the UI
// can fall back to canned data with zero network. Toggled from the dev panel.
let _offline = false;
export function setOfflineMode(v: boolean) {
  _offline = v;
}

// Finite timeouts so a stalled Fanar call fails with a clear message instead of hanging
// forever. Generous, because real generation (verse, image) legitimately takes a while.
async function withTimeout(run: (signal: AbortSignal) => Promise<Response>, ms: number): Promise<Response> {
  const ctrl = new AbortController();
  const id = setTimeout(() => ctrl.abort(), ms);
  try {
    return await run(ctrl.signal);
  } catch (e) {
    if ((e as Error).name === "AbortError") {
      throw new Error("Request timed out. The Fanar service may be slow or unavailable.");
    }
    throw e;
  } finally {
    clearTimeout(id);
  }
}

function guardOffline() {
  if (_offline) throw new Error("Offline demo mode is on (no live AI calls).");
}

async function asJson<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = `${res.status}`;
    try {
      detail = (await res.json()).detail ?? detail;
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.json() as Promise<T>;
}

export async function health(): Promise<boolean> {
  try {
    const r = await withTimeout(
      (signal) => fetch(`${API_BASE}/health`, { cache: "no-store", signal }),
      5000,
    );
    return r.ok;
  } catch {
    return false;
  }
}

/** Assess from a recorded audio blob (real child flow). */
export async function assessAudio(
  targetText: string,
  audio: Blob,
  childId?: string,
  childName?: string,
): Promise<AssessResult> {
  guardOffline();
  const fd = new FormData();
  fd.append("target_text", targetText);
  fd.append("audio", audio, "reading.webm");
  if (childId) fd.append("child_id", childId);
  if (childName) fd.append("child_name", childName);
  const res = await withTimeout(
    (signal) => fetch(`${API_BASE}/assess`, { method: "POST", body: fd, signal }),
    45000,
  );
  return asJson<AssessResult>(res);
}

/** Assess from a transcript (demo / no-mic flow). */
export async function assessTranscript(
  targetText: string,
  transcript: string,
  childId?: string,
  childName?: string,
): Promise<AssessResult> {
  guardOffline();
  const fd = new FormData();
  fd.append("target_text", targetText);
  fd.append("transcript", transcript);
  if (childId) fd.append("child_id", childId);
  if (childName) fd.append("child_name", childName);
  const res = await withTimeout(
    (signal) => fetch(`${API_BASE}/assess`, { method: "POST", body: fd, signal }),
    45000,
  );
  return asJson<AssessResult>(res);
}

export async function adapt(
  diagnosis: Diagnosis,
  opts: { includeImage?: boolean; includeAudio?: boolean } = {},
): Promise<AdaptResult> {
  guardOffline();
  const res = await withTimeout(
    (signal) =>
      fetch(`${API_BASE}/adapt`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          diagnosis,
          include_image: opts.includeImage ?? true,
          include_audio: opts.includeAudio ?? true,
        }),
        signal,
      }),
    90000,
  );
  return asJson<AdaptResult>(res);
}

/** Fanar picks the most relevant pre-generated illustration for `text`. */
export async function pickIllustration(
  text: string,
  candidates: { id: string; description: string }[],
): Promise<{ id: string }> {
  guardOffline();
  const res = await withTimeout(
    (signal) =>
      fetch(`${API_BASE}/pick-illustration`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, candidates }),
        signal,
      }),
    20000,
  );
  return asJson<{ id: string }>(res);
}

/** Aura TTS for arbitrary text. base64 MP3 for the Diwan full-verse playback and the
 *  per-word reading hints (lazy, on tap). */
export async function speak(text: string): Promise<{ b64: string; mime: string }> {
  guardOffline();
  const res = await withTimeout(
    (signal) =>
      fetch(`${API_BASE}/speak`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
        signal,
      }),
    30000,
  );
  return asJson<{ b64: string; mime: string }>(res);
}

export async function getProgress(childId = DEMO_CHILD_ID): Promise<Progress> {
  const res = await withTimeout(
    (signal) =>
      fetch(`${API_BASE}/progress?child_id=${encodeURIComponent(childId)}`, {
        cache: "no-store",
        signal,
      }),
    10000,
  );
  return asJson<Progress>(res);
}
