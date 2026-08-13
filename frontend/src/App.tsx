import { Navigate, Route, Routes } from "react-router-dom";
import { AppShell } from "./components/layout/AppShell";
import { Auth } from "./pages/Auth";
import { Dashboard } from "./pages/Dashboard";
import { Instagram } from "./pages/Instagram";
import { Landing } from "./pages/Landing";
import { Library } from "./pages/Library";
import { Placeholder } from "./pages/Placeholder";
import { Settings } from "./pages/Settings";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route element={<AppShell />}>
        <Route path="/login" element={<Auth mode="login" />} />
        <Route path="/register" element={<Auth mode="register" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route
          path="/producao"
          element={
            <Placeholder
              title="Produção"
              capability="Reel factory and content creation are not implemented."
            />
          }
        />
        <Route path="/biblioteca" element={<Library />} />
        <Route
          path="/calendario"
          element={
            <Placeholder
              title="Calendário"
              capability="Planner and schedule queue are not implemented."
            />
          }
        />
        <Route
          path="/analytics"
          element={
            <Placeholder
              title="Analytics"
              capability="No Instagram insights connected. NO DATA."
            />
          }
        />
        <Route
          path="/receita"
          element={
            <Placeholder
              title="Receita"
              capability="No commerce provider connected. Revenue is NOT AVAILABLE."
            />
          }
        />
        <Route path="/instagram" element={<Instagram />} />
        <Route
          path="/ai-brain"
          element={
            <Placeholder
              title="AI Brain"
              capability="Master Brain is not implemented."
            />
          }
        />
        <Route path="/settings" element={<Settings />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
