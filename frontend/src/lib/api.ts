export const apiBase = (import.meta.env.VITE_API_BASE_URL || "").replace(
  /\/$/,
  ""
);

export type Health = { status: string; service: string };

export async function fetchHealth(): Promise<
  | { kind: "ok"; data: Health }
  | { kind: "unavailable"; detail: string }
> {
  const url = `${apiBase}/api/health`;
  try {
    const res = await fetch(url);
    if (!res.ok) {
      return { kind: "unavailable", detail: `API returned HTTP ${res.status}` };
    }
    const data = (await res.json()) as Health;
    if (!data.status || !data.service) {
      return { kind: "unavailable", detail: "Unexpected health payload" };
    }
    return { kind: "ok", data };
  } catch {
    return {
      kind: "unavailable",
      detail: "API not reachable. Set VITE_API_BASE_URL on the static site.",
    };
  }
}
