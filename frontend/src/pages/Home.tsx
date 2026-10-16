import { useEffect, useState } from "react";
import Uploader from "../components/Uploader";
import StylePicker from "../components/StylePicker";
import { generate, listStyles, type StyleOption } from "../api/client";
import { useJobStore } from "../store/useJobStore";

export default function Home({ onDone }: { onDone: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [styles, setStyles] = useState<StyleOption[]>([]);
  const [style, setStyle] = useState("neon");
  const [loop, setLoop] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState("");
  const setJob = useJobStore((s) => s.setJob);

  useEffect(() => { listStyles().then(setStyles).catch(() => {}); }, []);

  async function go() {
    if (!file) return;
    setBusy(true); setErr("");
    try {
      const info = await generate(file, style, loop, speed);
      setJob(info);
      onDone();
    } catch (e: any) {
      setErr(String(e?.message || e));
    } finally { setBusy(false); }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Upload an image</h1>
      <Uploader onFile={setFile} />
      <div className="space-y-3">
        <p className="text-sm text-slate-400">Style</p>
        <StylePicker styles={styles} value={style} onChange={setStyle} />
      </div>
      <div className="flex flex-wrap items-center gap-4 text-sm">
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={loop} onChange={(e) => setLoop(e.target.checked)} />
          Loop
        </label>
        <label className="flex items-center gap-2">
          Speed
          <input type="range" min={0.25} max={3} step={0.05} value={speed}
            onChange={(e) => setSpeed(parseFloat(e.target.value))} />
          <span className="tabular-nums">{speed.toFixed(2)}x</span>
        </label>
      </div>
      <button disabled={!file || busy} onClick={go}
        className="px-5 py-2 rounded-lg bg-sf-accent text-black font-medium disabled:opacity-40">
        {busy ? "Generating..." : "Generate"}
      </button>
      {err && <p className="text-sm text-red-400">{err}</p>}
    </div>
  );
}