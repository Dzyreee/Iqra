"use client";
import { useApp } from "@/components/AppProvider";
import { AgentTrace } from "@/components/AgentTrace";
import { useLang } from "@/components/LanguageProvider";
import { XIcon } from "@/components/icons";

// Hidden "How it works" view (for judges): the live agent trace, moved out of the
// kid-facing flow. Reuses the existing AgentTrace renderer.
export function TraceScreen() {
  const { t } = useLang();
  const { assess, adapt, go, randomizeDemo, offline, toggleOffline } = useApp();

  const steps = [...(assess?.trace.steps ?? []), ...(adapt?.trace.steps ?? [])];
  const totalMs =
    (assess?.trace.total_latency_ms ?? 0) + (adapt?.trace.total_latency_ms ?? 0);

  return (
    <div className="mx-auto flex min-h-dvh w-full max-w-md flex-col px-5 pb-10 pt-6 md:max-w-2xl lg:max-w-3xl">
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => go("path")}
          aria-label={t("back_to_path")}
          className="grid h-10 w-10 cursor-pointer place-items-center rounded-2xl border-2 border-sky-100 bg-white text-slate-400 transition-colors hover:text-brand"
        >
          <XIcon className="h-5 w-5" />
        </button>
        <span className="font-display text-xl font-extrabold text-ink">{t("judge_view")}</span>
        <span className="h-10 w-10" />
      </div>

      <p className="mt-3 mb-3 text-center text-sm text-slate-500">{t("judge_sub")}</p>

      <AgentTrace steps={steps} totalMs={totalMs} />

      {/* Developer tools, NOT a real feature. Fenced off (dashed amber) so a parent or
          judge browsing the app can immediately tell it is not a normal option. */}
      <div className="mt-6 rounded-2xl border-2 border-dashed border-amber-300 bg-amber-50/60 p-4" dir="ltr">
        <p className="mb-3 text-xs font-extrabold uppercase tracking-wide text-amber-700">
          Developer tools (testing only)
        </p>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            onClick={randomizeDemo}
            className="inline-flex cursor-pointer items-center gap-2 rounded-xl border-b-4 border-amber-600 bg-amber-400 px-4 py-2.5 font-bold text-amber-950 transition-[filter] hover:brightness-105 active:translate-y-[2px] active:border-b-2"
          >
            Dev: Randomize Demo Data
          </button>
          <button
            type="button"
            onClick={toggleOffline}
            aria-pressed={offline}
            className={`inline-flex cursor-pointer items-center gap-2 rounded-xl border-b-4 px-4 py-2.5 font-bold transition-[filter] hover:brightness-105 active:translate-y-[2px] active:border-b-2 ${
              offline
                ? "border-emerald-700 bg-emerald-500 text-white"
                : "border-amber-600 bg-white text-amber-800"
            }`}
          >
            Dev: Offline demo {offline ? "ON" : "OFF"}
          </button>
        </div>
        <p className="mt-3 text-xs text-amber-700/80">
          Randomize: random name, streak and stars, resets the path to Level 1. Offline
          demo: runs the whole flow on canned data with no Fanar calls (use if Fanar is down).
        </p>
      </div>
    </div>
  );
}
