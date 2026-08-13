import { useEffect, useState } from "react";
import { StatusBlock } from "../components/ui/StatusBlock";
import { useNavigate } from "react-router-dom";
import { apiBase, authApi, dataApi } from "../lib/api";

export function Settings() {
  const nav = useNavigate();
  const [email, setEmail] = useState<string | null>(null);
  const [db, setDb] = useState("…");
  const [meta, setMeta] = useState("…");

  useEffect(() => {
    authApi
      .me()
      .then((m) => setEmail(m.email))
      .catch(() => setEmail(null));
    dataApi
      .config()
      .then((c) => {
        setDb(String(c.database));
        setMeta(String(c.meta_oauth));
      })
      .catch(() => {
        setDb("NOT AVAILABLE");
        setMeta("NOT AVAILABLE");
      });
  }, []);

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
          label="Signed-in user"
          value={email || "NOT AUTHENTICATED"}
        />
        <StatusBlock label="Database" value={db} />
        <StatusBlock label="Meta OAuth" value={meta} />
      </div>
      {email ? (
        <button
          type="button"
          className="mt-8 border border-line px-5 py-2.5 font-sans text-sm"
          onClick={async () => {
            await authApi.logout();
            nav("/");
          }}
        >
          Log out
        </button>
      ) : null}
    </div>
  );
}
