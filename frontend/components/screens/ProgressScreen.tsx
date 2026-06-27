"use client";
import { useApp } from "@/components/AppProvider";
import { Jad } from "@/components/Jad";
import { useLang } from "@/components/LanguageProvider";
import { BookIcon, FlameIcon, StarIcon, TrendingUpIcon, XIcon } from "@/components/icons";
import type { SoundProgress } from "@/lib/types";

// One labelled meter row (Started vs Now). Forced LTR so the fill always grows rightward.
function Bar({ label, pct, solid }: { label: string; pct: number; solid?: boolean }) {
  return (
    <div className="flex items-center gap-2" dir="ltr">
      <span className="w-16 shrink-0 text-end text-xs font-bold text-slate-400">{label}</span>
      <div className="h-3.5 flex-1 overflow-hidden rounded-full bg-sky-100">
        <div
          className={`h-full rounded-full transition-[width] duration-700 ease-out ${solid ? "bg-brand" : "bg-brand/30"}`}
          style={{ width: `${Math.max(0, Math.min(100, pct))}%` }}
        />
      </div>
      <span className="w-10 shrink-0 font-display text-sm font-extrabold text-ink">{pct}%</span>
    </div>
  );
}

function SoundCard({ s }: { s: SoundProgress }) {
  const { t } = useLang();
  return (
    <div className="card p-4">
      <div className="mb-3 flex items-center gap-3">
        <span
          dir="rtl"
          className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl border-b-4 border-brand-dark bg-brand font-display text-2xl font-extrabold text-white"
        >
          {s.sound}
        </span>
        <span className="flex-1 font-bold text-ink">
          {t("letter_label")} «{s.sound}»
        </span>
        {s.delta > 0 && (
          <span className="chip bg-emerald-50 text-sm text-emerald-700">
            <TrendingUpIcon className="h-4 w-4" /> +{s.delta}%
          </span>
        )}
      </div>
      <div className="space-y-2">
        <Bar label={t("started_label")} pct={s.first} />
        <Bar label={t("now_label")} pct={s.latest} solid />
      </div>
    </div>
  );
}

export function ProgressScreen() {
  const { t } = useLang();
  const { progress, game, childName, go } = useApp();

  const sounds = progress?.sounds ?? [];
  const tiles = [
    { icon: <FlameIcon className="h-7 w-7 text-accent" fill="currentColor" />, value: game.streak, label: t("streak_label") },
    { icon: <BookIcon className="h-7 w-7 text-brand" />, value: progress?.sessions_count ?? 0, label: t("sessions_label") },
    { icon: <StarIcon className="h-7 w-7 text-accent" fill="currentColor" />, value: game.stars, label: t("stars_label") },
  ];

  return (
    <div className="mx-auto flex min-h-dvh w-full max-w-md flex-col px-5 pb-10 pt-6 lg:max-w-5xl xl:max-w-6xl">
      {/* header */}
      <div className="flex items-center justify-between">
        <button
          type="button"
          onClick={() => go("path")}
          aria-label={t("back_to_path")}
          className="grid h-10 w-10 cursor-pointer place-items-center rounded-2xl border-2 border-sky-100 bg-white text-slate-400 transition-colors hover:text-brand"
        >
          <XIcon className="h-5 w-5" />
        </button>
        <span className="font-display text-xl font-extrabold text-ink">{t("my_progress")}</span>
        <span className="h-10 w-10" />
      </div>

      <div className="mt-5 lg:grid lg:grid-cols-[360px_1fr] lg:gap-8 lg:items-start">
        {/* left: profile + stat tiles */}
        <div className="space-y-4 lg:sticky lg:top-6">
          <div className="flex items-center gap-4 rounded-[1.75rem] border-2 border-sky-100 bg-gradient-to-br from-sky-100/70 to-white p-5 shadow-soft">
            <Jad pose="jad-holding-star" size={104} />
            <div>
              <p className="font-display text-3xl font-extrabold text-ink">{childName}</p>
              <p className="text-base font-bold text-slate-500">{t("child_age")}</p>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-3">
            {tiles.map((tile, i) => (
              <div key={i} className="card flex flex-col items-center gap-1 p-4">
                {tile.icon}
                <span className="font-display text-3xl font-extrabold text-ink">{tile.value}</span>
                <span className="text-center text-xs font-bold text-slate-500">{tile.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* right: sound improvement */}
        <div className="mt-6 lg:mt-0">
          <h2 className="mb-3 flex items-center gap-2 font-display text-xl font-extrabold text-ink">
            <TrendingUpIcon className="h-6 w-6 text-brand" />
            {t("sounds_progress_title")}
          </h2>

          {sounds.length > 0 ? (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-1 xl:grid-cols-2">
              {sounds.map((s) => (
                <SoundCard key={s.sound} s={s} />
              ))}
            </div>
          ) : (
            <div className="card flex flex-col items-center gap-3 p-8 text-center">
              <Jad pose="jad-reading" size={96} />
              <p className="font-bold text-slate-500">{t("no_progress_yet")}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
