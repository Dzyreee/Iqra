"use client";
import { useLang } from "@/components/LanguageProvider";

// Difficulty/level indicator, "Level N" + a small filled bar (completed nodes / total).
// Deliberately distinct from the streak chip so current level + progress read at a glance.
export function LevelBadge({
  level,
  completed,
  total,
}: {
  level: number;
  completed: number;
  total: number;
}) {
  const { t } = useLang();
  const pct = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="inline-flex items-center gap-2 rounded-full border-2 border-brand/20 bg-white px-2.5 py-1.5 shadow-soft">
      <span className="grid h-7 w-7 place-items-center rounded-full border-b-2 border-brand-dark bg-brand font-display text-sm font-extrabold text-white">
        {level}
      </span>
      <div className="flex flex-col gap-1">
        <span className="text-xs font-extrabold leading-none text-ink">
          {t("level_label")} {level}
        </span>
        <div className="h-1.5 w-16 overflow-hidden rounded-full bg-sky-100" role="presentation">
          <div
            className="h-full rounded-full bg-brand transition-[width] duration-500 ease-out"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}
