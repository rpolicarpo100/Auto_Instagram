import { cn } from "../../lib/cn";

type Tone = "neutral" | "ok" | "warn";

export function StatusBlock({
  label,
  value,
  detail,
  tone = "neutral",
}: {
  label: string;
  value: string;
  detail?: string;
  tone?: Tone;
}) {
  return (
    <div className="border border-line p-4">
      <p className="font-sans text-[11px] uppercase tracking-[0.18em] text-mute">
        {label}
      </p>
      <p
        className={cn(
          "mt-2 text-lg",
          tone === "ok" && "text-sand",
          tone === "warn" && "text-mute"
        )}
      >
        {value}
      </p>
      {detail ? <p className="mt-1 font-sans text-xs text-mute">{detail}</p> : null}
    </div>
  );
}
