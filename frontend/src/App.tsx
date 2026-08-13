import { useEffect, useState } from "react";

type Health = { status: string; service: string };
type LoadState =
  | { kind: "loading" }
  | { kind: "ok"; data: Health }
  | { kind: "unavailable"; detail: string };

const apiBase = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

export default function App() {
  const [health, setHealth] = useState<LoadState>({ kind: "loading" });

  useEffect(() => {
    const url = `${apiBase}/api/health`;
    fetch(url)
      .then(async (res) => {
        if (!res.ok) {
          setHealth({
            kind: "unavailable",
            detail: `API returned HTTP ${res.status}`,
          });
          return;
        }
        const data = (await res.json()) as Health;
        setHealth({ kind: "ok", data });
      })
      .catch(() => {
        setHealth({
          kind: "unavailable",
          detail: "API not reachable. Start the backend or set VITE_API_BASE_URL.",
        });
      });
  }, []);

  return (
    <>
      <main className="page">
        <div className="mark">Content operating system</div>
        <h1>INSTAGRAM AI FACTORY</h1>
        <p className="tagline">AI-powered Instagram content studio</p>
        <a className="cta" href="#get-started">
          Get Started
        </a>
        <div id="get-started" className="status">
          {health.kind === "loading" && <p>Checking API…</p>}
          {health.kind === "ok" && (
            <p>
              API <strong>{health.data.status}</strong> · {health.data.service}
            </p>
          )}
          {health.kind === "unavailable" && (
            <p>
              API <strong>NOT AVAILABLE</strong>
              <br />
              {health.detail}
            </p>
          )}
          <p>
            Instagram is <strong>NOT CONFIGURED</strong> in Phase 01. No account
            metrics are shown.
          </p>
        </div>
      </main>
      <div className="footer">Phase 01 · foundation only</div>
    </>
  );
}
