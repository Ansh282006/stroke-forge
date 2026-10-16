import type { Route } from "../App";

export default function Nav({ route, setRoute }: { route: Route; setRoute: (r: Route) => void }) {
  const items: { key: Route; label: string }[] = [
    { key: "home", label: "Upload" },
    { key: "preview", label: "Preview" },
    { key: "code", label: "Code" }
  ];
  return (
    <nav className="border-b border-white/10">
      <div className="container mx-auto max-w-6xl px-4 py-3 flex items-center gap-6">
        <span className="font-semibold tracking-tight">StrokeForge</span>
        <div className="flex gap-3 text-sm">
          {items.map((i) => (
            <button key={i.key} onClick={() => setRoute(i.key)}
              className={`px-3 py-1 rounded-md transition ${route === i.key ? "bg-white/10" : "hover:bg-white/5"}`}>
              {i.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}