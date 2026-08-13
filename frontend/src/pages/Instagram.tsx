import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatusBlock } from "../components/ui/StatusBlock";
import { dataApi } from "../lib/api";

export function Instagram() {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    dataApi
      .instagramStatus()
      .then(setStatus)
      .catch((e) => setError(e.message || "FAILED"));
  }, []);

  const account = (status?.account as Record<string, string | null>) || {};
  const configured = status?.meta_configured === true;

  async function connect() {
    setBusy(true);
    setError(null);
    try {
      const r = await dataApi.instagramConnect();
      window.location.href = r.authorization_url;
    } catch (e) {
      setError(e instanceof Error ? e.message : "FAILED");
      setBusy(false);
    }
  }

  return (
    <div>
      <h1 className="text-3xl tracking-tight">Instagram</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Official Meta OAuth only. Passwords are never collected.
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2">
        <StatusBlock
          label="Meta OAuth"
          value={configured ? "CONFIGURED" : "NOT CONFIGURED"}
          detail="Requires META_APP_ID, META_APP_SECRET, META_REDIRECT_URI"
        />
        <StatusBlock
          label="Account"
          value={account.status || "NO DATA"}
          detail={account.username || "No token stored"}
        />
      </div>
      {error ? (
        <p className="mt-4 font-sans text-sm text-sand">
          {error === "NOT_AUTHENTICATED" ? (
            <>
              Sign in first. <Link to="/login">Login</Link>
            </>
          ) : (
            error
          )}
        </p>
      ) : null}
      <button
        type="button"
        disabled={!configured || busy}
        onClick={connect}
        className="mt-8 border border-sand px-5 py-2.5 font-sans text-sm enabled:hover:bg-sand enabled:hover:text-ink disabled:cursor-not-allowed disabled:border-line disabled:text-mute"
      >
        {configured ? "Connect Instagram" : "Connect (META_NOT_CONFIGURED)"}
      </button>
    </div>
  );
}
