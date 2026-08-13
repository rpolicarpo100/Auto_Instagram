export const apiBase = (import.meta.env.VITE_API_BASE_URL || "").replace(
  /\/$/,
  ""
);

export type Health = { status: string; service: string };

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`${apiBase}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(init.headers || {}),
    },
    ...init,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  if (!res.ok) {
    const err = new Error(data.detail || `HTTP ${res.status}`) as Error & {
      status?: number;
      payload?: unknown;
    };
    err.status = res.status;
    err.payload = data;
    throw err;
  }
  return data as T;
}

export async function fetchHealth(): Promise<
  | { kind: "ok"; data: Health }
  | { kind: "unavailable"; detail: string }
> {
  try {
    const data = await request<Health>("/api/health");
    return { kind: "ok", data };
  } catch (e) {
    return {
      kind: "unavailable",
      detail: e instanceof Error ? e.message : "API not reachable",
    };
  }
}

export type Me = { id: string; email: string };

export const authApi = {
  me: () => request<Me>("/api/v1/auth/me"),
  register: (email: string, password: string) =>
    request<Me>("/api/v1/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  login: (email: string, password: string) =>
    request<Me>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  logout: () => request<{ ok: boolean }>("/api/v1/auth/logout", { method: "POST" }),
};

export type Metric = {
  status: string;
  value: unknown;
  source: string | null;
  collected_at: string | null;
};

export const dataApi = {
  config: () => request<Record<string, unknown>>("/api/v1/config"),
  dashboard: () => request<Record<string, Metric | unknown>>("/api/v1/dashboard"),
  instagramStatus: () => request<Record<string, unknown>>("/api/v1/instagram/status"),
  instagramConnect: () =>
    request<{ authorization_url: string }>("/api/v1/instagram/connect"),
};
