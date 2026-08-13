import { StatusBlock } from "../components/ui/StatusBlock";

export function Placeholder({
  title,
  capability,
}: {
  title: string;
  capability: string;
}) {
  return (
    <div>
      <h1 className="text-3xl tracking-tight">{title}</h1>
      <p className="mt-2 font-sans text-sm text-mute">{capability}</p>
      <div className="mt-8 max-w-lg">
        <StatusBlock
          label="Status"
          value="NOT IMPLEMENTED"
          detail="UI shell only. Backend for this area is not wired."
          tone="warn"
        />
      </div>
    </div>
  );
}
