import { useRef, useState } from "react";

export default function Uploader({ onFile }: { onFile: (f: File) => void }) {
  const [name, setName] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);
  const [drag, setDrag] = useState(false);

  function pick(f?: File | null) {
    if (!f) return;
    setName(f.name);
    onFile(f);
  }

  return (
    <div
      onClick={() => inputRef.current?.click()}
      onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
      onDragLeave={() => setDrag(false)}
      onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files?.[0]); }}
      className={`cursor-pointer rounded-2xl border-2 border-dashed p-10 text-center transition
        ${drag ? "border-sf-accent bg-white/5" : "border-white/15 hover:border-white/25"}`}>
      <input ref={inputRef} type="file" accept="image/*" className="hidden"
        onChange={(e) => pick(e.target.files?.[0])} />
      <p className="text-lg font-medium">Drop an image here</p>
      <p className="text-sm text-slate-400 mt-1">or click to browse</p>
      {name && <p className="mt-3 text-sm text-sf-accent">{name}</p>}
    </div>
  );
}