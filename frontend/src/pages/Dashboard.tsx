import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatusBlock } from "../components/ui/StatusBlock";
import { fetchHealth } from "../lib/api";

export function Dashboard() {
  const [api, setApi] = useState("Checking…");
  const [apiDetail, setApiDetail] = useState("Process health only");
  const [tone, setTone] = useState<"ok" | "warn" | "neutral">("neutral");

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
  }, []);

  return (
    <div>
      <h1 className="text-3xl tracking-tight">Dashboard</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Account metrics require an official Instagram connection. None exists yet.
      </p>
      <div className="mt-8 grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        <StatusBlock label="API" value={api} detail={apiDetail} tone={tone} />
        <StatusBlock
          label="Account status"
          value="NOT CONFIGURED"
          detail="Connect Instagram in a later phase"
        />
        <StatusBlock label="Followers" value="NO DATA" detail="Source: Instagram API" />
        <StatusBlock label="Content" value="NO DATA" detail="Source: Instagram API" />
        <StatusBlock label="Reach" value="NO DATA" detail="Source: Instagram API" />
        <StatusBlock
          label="Engagement"
          value="NO DATA"
          detail="Source: Instagram Insights"
        />
      </div>
      <Link
        to="/instagram"
        className="mt-8 inline-block border border-sand px-5 py-2.5 font-sans text-sm hover:bg-sand hover:text-ink"
      >
        CONNECT INSTAGRAM
      </Link>
    </div>
  );
}
