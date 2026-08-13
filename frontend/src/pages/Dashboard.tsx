import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatusBlock } from "../components/ui/StatusBlock";
import { Metric, authApi, dataApi, fetchHealth } from "../lib/api";

function label(m?: Metric) {
  if (!m) return { value: "NO DATA", detail: undefined as string | undefined };
  if (m.value === null || m.value === undefined) {
    return { value: m.status, detail: m.source || undefined };
  }
  return { value: String(m.value), detail: `${m.status} · ${m.source || ""}` };
}

export function Dashboard() {
  const [api, setApi] = useState("Checking…");
  const [apiDetail, setApiDetail] = useState("Process health only");
  const [tone, setTone] = useState<"ok" | "warn" | "neutral">("neutral");
  const [authed, setAuthed] = useState<boolean | null>(null);
  const [metrics, setMetrics] = useState<Record<string, Metric> | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth().then((r) => {
      if (r.kind === "ok") {
        setApi(r.data.status);
        setApiDetail(r.data.service);
        setTone("ok");
      } else {
        setApi("NOT AVAILABLE");
        setApiDetail(r.detail);
        setTone("warn");
      }
    });
    authApi
      .me()
      .then(() => {
        setAuthed(true);
        return dataApi.dashboard();
      })
      .then((d) => {
        if (d) setMetrics(d as Record<string, Metric>);
      })
      .catch((e) => {
        if (e.status === 401) setAuthed(false);
        else if (e.status === 503) {
          setAuthed(true);
          setError(String(e.message));
        } else setError(String(e.message));
      });
  }, []);

  const followers = label(metrics?.followers);
  const content = label(metrics?.content);
  const reach = label(metrics?.reach);
  const engagement = label(metrics?.engagement);
  const account = label(metrics?.account_status);

  return (
    <div>
      <h1 className="text-3xl tracking-tight">Dashboard</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Values are REAL, CALCULATED, or explicitly unavailable. Nothing is invented.
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <StatusBlock label="API" value={api} detail={apiDetail} tone={tone} />
        <StatusBlock
          label="Account status"
          value={authed === false ? "Sign in required" : account.value}
          detail={account.detail}
        />
        <StatusBlock label="Followers" value={followers.value} detail={followers.detail} />
        <StatusBlock label="Content" value={content.value} detail={content.detail} />
        <StatusBlock label="Reach" value={reach.value} detail={reach.detail} />
        <StatusBlock
          label="Engagement"
          value={engagement.value}
          detail={engagement.detail}
        />
      </div>
      {error ? (
        <p className="mt-4 font-sans text-sm text-sand">{error}</p>
      ) : null}
      {authed === false ? (
        <Link
          to="/login"
          className="mt-8 inline-block border border-sand px-5 py-2.5 font-sans text-sm hover:bg-sand hover:text-ink"
        >
          Sign in
        </Link>
      ) : (
        <Link
          to="/instagram"
          className="mt-8 inline-block border border-sand px-5 py-2.5 font-sans text-sm hover:bg-sand hover:text-ink"
        >
          CONNECT INSTAGRAM
        </Link>
      )}
    </div>
  );
}
