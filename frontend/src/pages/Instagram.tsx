import { StatusBlock } from "../components/ui/StatusBlock";

export function Instagram() {
  return (
    <div>
      <h1 className="text-3xl tracking-tight">Instagram</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Official Meta OAuth only. Passwords are never collected.
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        <StatusBlock
          label="Connection"
          value="NOT CONFIGURED"
          detail="Phase 08 — OAuth not implemented"
        />
        <StatusBlock
          label="Account"
          value="NO DATA"
          detail="No token stored. No account discovery."
        />
      </div>
      <button
        type="button"
        disabled
        className="mt-8 cursor-not-allowed border border-line px-5 py-2.5 font-sans text-sm text-mute"
      >
        Connect (NOT IMPLEMENTED)
      </button>
    </div>
  );
}
