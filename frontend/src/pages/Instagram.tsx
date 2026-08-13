import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatusBlock } from "../components/ui/StatusBlock";
import { dataApi } from "../lib/api";

export function Instagram() {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const [media, setMedia] = useState<Array<Record<string, unknown>>>([]);
  const [mediaStatus, setMediaStatus] = useState("NO DATA");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    dataApi
      .instagramStatus()
      .then(setStatus)
      .catch((e) => setError(e.message || "FAILED"));
    dataApi
      .instagramMedia()
      .then((r) => {
        setMediaStatus(r.status);
        setMedia(r.items || []);
      })
      .catch(() => setMediaStatus("NOT AVAILABLE"));
  }, []);

  const account = (status?.account as Record<string, string | null>) || {};
  const configured = status?.meta_configured === true;
  const params = new URLSearchParams(window.location.search);
  const oauthError = params.get("error");

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

  async function refresh() {
    setBusy(true);
    try {
      await dataApi.instagramRefresh();
      const s = await dataApi.instagramStatus();
      setStatus(s);
      const m = await dataApi.instagramMedia();
      setMediaStatus(m.status);
      setMedia(m.items || []);
    } catch (e) {
      setError(e instanceof Error ? e.message : "FAILED");
    } finally {
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
          detail="Requires META_APP_ID, META_APP_SECRET, META_REDIRECT_URI on the API service"
        />
        <StatusBlock
          label="Account"
          value={account.status || "NO DATA"}
          detail={account.username || "No token stored"}
        />
      </div>
      {oauthError ? (
        <p className="mt-4 font-sans text-sm text-sand">OAuth: {oauthError}</p>
      ) : null}
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
      <div className="mt-8 flex flex-wrap gap-3">
        <button
          type="button"
          disabled={!configured || busy}
          onClick={connect}
          className="border border-sand px-5 py-2.5 font-sans text-sm enabled:hover:bg-sand enabled:hover:text-ink disabled:cursor-not-allowed disabled:border-line disabled:text-mute"
        >
          {configured ? "Connect Instagram" : "Connect (META_NOT_CONFIGURED)"}
        </button>
        <button
          type="button"
          disabled={busy || account.status !== "CONNECTED"}
          onClick={refresh}
          className="border border-line px-5 py-2.5 font-sans text-sm disabled:text-mute"
        >
          Refresh account data
        </button>
      </div>
      <h2 className="mt-10 text-xl">Published media</h2>
      <p className="mt-1 font-sans text-xs text-mute">Status: {mediaStatus}</p>
      <ul className="mt-4 space-y-2 font-sans text-sm">
        {media.length === 0 ? (
          <li className="text-mute">NO DATA</li>
        ) : (
          media.map((it) => (
            <li key={String(it.id)} className="border border-line px-3 py-2">
              {String(it.media_type || "MEDIA")} · {String(it.timestamp || "")}
              {it.permalink ? (
                <a
                  className="ml-2 underline"
                  href={String(it.permalink)}
                  target="_blank"
                  rel="noreferrer"
                >
                  open
                </a>
              ) : null}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
