import { NavLink, Outlet } from "react-router-dom";
import { cn } from "../../lib/cn";

const nav = [
  { to: "/dashboard", label: "Dashboard" },
  { to: "/producao", label: "Produção" },
  { to: "/biblioteca", label: "Biblioteca" },
  { to: "/calendario", label: "Calendário" },
  { to: "/analytics", label: "Analytics" },
  { to: "/receita", label: "Receita" },
  { to: "/instagram", label: "Instagram" },
  { to: "/ai-brain", label: "AI Brain" },
  { to: "/settings", label: "Settings" },
  { to: "/login", label: "Login" },
];

export function AppShell() {
  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[240px_1fr]">
      <aside className="border-b border-line px-5 py-6 lg:border-b-0 lg:border-r">
        <p className="font-sans text-[10px] uppercase tracking-[0.28em] text-mute">
          Instagram AI Factory
        </p>
        <p className="mt-2 text-sm text-paper">Content OS</p>
        <nav className="mt-8 flex flex-wrap gap-2 lg:flex-col lg:gap-1">
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                cn(
                  "px-3 py-2 font-sans text-sm text-mute hover:text-paper",
                  isActive && "bg-line/60 text-paper"
                )
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="px-6 py-8 lg:px-10">
        <Outlet />
      </main>
    </div>
  );
}
