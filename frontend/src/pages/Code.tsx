import { useEffect, useState } from "react";
import Editor from "@monaco-editor/react";
import { fileUrl } from "../api/client";
import { useJobStore } from "../store/useJobStore";

const FILES = ["index.html", "styles.css", "script.js", "tailwind.config.js"] as const;
type FName = typeof FILES[number];

export default function Code() {
  const job = useJobStore((s) => s.job);
  const [fname, setFname] = useState<FName>("index.html");
  const [text, setText] = useState<string>("");

  useEffect(() => {
    if (!job) return;
    fetch(fileUrl(job, fname)).then((r) => r.text()).then(setText).catch((e) => setText(String(e)));
  }, [job, fname]);

  if (!job) return <p className="text-slate-400">No job yet.</p>;

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        {FILES.map((f) => (
          <button key={f} onClick={() => setFname(f)}
            className={`px-3 py-1 rounded-md text-sm ${fname === f ? "bg-white/10" : "hover:bg-white/5"}`}>
            {f}
          </button>
        ))}
      </div>
      <div className="rounded-xl overflow-hidden border border-white/10">
        <Editor height="70vh" theme="vs-dark" value={text}
          language={fname.endsWith(".js") ? "javascript" : fname.endsWith(".css") ? "css" : "html"}
          options={{ readOnly: true, minimap: { enabled: false }, fontSize: 13 }} />
      </div>
    </div>
  );
}