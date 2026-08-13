import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { authApi } from "../lib/api";

export function Auth({ mode }: { mode: "login" | "register" }) {
  const nav = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    try {
      if (mode === "register") await authApi.register(email, password);
      else await authApi.login(email, password);
      nav("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "FAILED");
    }
  }

  return (
    <div className="mx-auto max-w-md">
      <h1 className="text-3xl tracking-tight">
        {mode === "register" ? "Create account" : "Sign in"}
      </h1>
      <p className="mt-2 font-sans text-sm text-mute">
        App account only. This is not Instagram login.
      </p>
      <form onSubmit={onSubmit} className="mt-8 space-y-4 font-sans">
        <label className="block text-sm">
          Email
          <input
            className="mt-1 w-full border border-line bg-transparent px-3 py-2 text-paper"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block text-sm">
          Password (min 8)
          <input
            className="mt-1 w-full border border-line bg-transparent px-3 py-2 text-paper"
            type="password"
            required
            minLength={8}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        {error ? <p className="text-sm text-sand">{error}</p> : null}
        <button
          type="submit"
          className="border border-sand px-5 py-2.5 text-sm hover:bg-sand hover:text-ink"
        >
          {mode === "register" ? "Register" : "Login"}
        </button>
      </form>
      <p className="mt-6 font-sans text-sm text-mute">
        {mode === "register" ? (
          <Link to="/login">Already have an account</Link>
        ) : (
          <Link to="/register">Create an account</Link>
        )}
      </p>
    </div>
  );
}
