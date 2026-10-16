import { bundleUrl, previewUrl } from "../api/client";
import { useJobStore } from "../store/useJobStore";

export default function Preview({ onCode }: { onCode: () => void }) {
  const job = useJobStore((s) => s.job);
  if (!job) return <p className="text-slate-400">No job yet. Upload an image first.</p>;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Preview</h1>
        <div className="flex gap-3">
          <a href={bundleUrl(job)} className="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-sm">Download bundle</a>
          <button onClick={onCode} className="px-4 py-2 rounded-lg bg-sf-accent text-black text-sm font-medium">View code</button>
        </div>
      </div>
      <div className="rounded-2xl border border-white/10 overflow-hidden bg-black">
        <iframe title="preview" src={previewUrl(job)} className="w-full h-[70vh] bg-black" />
      </div>
      <p className="text-sm text-slate-400">
        Style: <span className="text-slate-200">{job.style}</span> ·
        Total: <span className="text-slate-200">{job.total_ms} ms</span>
      </p>
    </div>
  );
}