import { Link } from "react-router-dom";

export function Landing() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <p className="font-sans text-[11px] uppercase tracking-[0.28em] text-mute">
        Content operating system
      </p>
      <h1 className="mt-4 text-4xl tracking-tight md:text-5xl">
        INSTAGRAM AI FACTORY
      </h1>
      <p className="mt-3 text-mute">AI-powered Instagram content studio</p>
      <Link
        to="/dashboard"
        className="mt-8 border border-sand px-6 py-3 font-sans text-sm tracking-wide hover:bg-sand hover:text-ink"
      >
        Get Started
      </Link>
      <p className="mt-10 max-w-md font-sans text-xs text-mute">
        Phase 02 · UI shell. Instagram is NOT CONFIGURED. No metrics are shown.
      </p>
    </main>
  );
}
