import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { StatusBlock } from "../components/ui/StatusBlock";
import { dataApi } from "../lib/api";

type Item = {
  id: string;
  mime_type?: string;
  size?: number;
  checksum?: string;
  created_at?: string;
};

export function Library() {
  const [status, setStatus] = useState("…");
  const [items, setItems] = useState<Item[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      const r = await dataApi.mediaList();
      setStatus(r.status);
      setItems((r.items || []) as Item[]);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "FAILED");
    }
  }

  useEffect(() => {
    void load();
  }, []);

  async function onUpload(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const input = e.currentTarget.elements.namedItem("file") as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) {
      setError("NO FILE");
      return;
    }
    try {
      await dataApi.mediaUpload(file);
      input.value = "";
      await load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "UPLOAD_FAILED");
    }
  }

  return (
    <div>
      <h1 className="text-3xl tracking-tight">Biblioteca</h1>
      <p className="mt-2 font-sans text-sm text-mute">
        Uploads are validated by magic bytes. Invalid files are rejected.
      </p>
      <div className="mt-8 max-w-lg">
        <StatusBlock
          label="Library"
          value={status}
          detail="Source: media_assets (local storage metadata)"
        />
      </div>
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
      <form onSubmit={onUpload} className="mt-6 font-sans text-sm">
        <input type="file" name="file" accept="image/*,video/mp4,video/webm" />
        <button
          type="submit"
          className="ml-3 border border-sand px-4 py-2 hover:bg-sand hover:text-ink"
        >
          Upload
        </button>
      </form>
      <ul className="mt-8 space-y-2 font-sans text-sm">
        {items.length === 0 ? (
          <li className="text-mute">NO DATA</li>
        ) : (
          items.map((it) => (
            <li key={it.id} className="border border-line px-3 py-2">
              {it.mime_type} · {it.size} bytes · {it.checksum?.slice(0, 12)}
              <button
                type="button"
                className="ml-4 text-mute underline"
                onClick={async () => {
                  await dataApi.mediaDelete(it.id);
                  await load();
                }}
              >
                Delete
              </button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
}
