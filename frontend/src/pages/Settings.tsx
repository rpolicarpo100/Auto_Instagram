import { StatusBlock } from "../components/ui/StatusBlock";
import { apiBase } from "../lib/api";

export function Settings() {
  return (
    <div>
      <h1 className="text-3xl tracking-tight">Settings</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Configuration is read from the environment. Secrets are not shown.
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        <StatusBlock
          label="VITE_API_BASE_URL"
          value={apiBase || "NOT CONFIGURED"}
          detail="Frontend build-time API origin"
        />
        <StatusBlock
          label="Auth"
          value="NOT IMPLEMENTED"
          detail="Sessions land in Phase 05"
        />
      </div>
    </div>
  );
}
