import type { StyleOption } from "../api/client";

export default function StylePicker({
  styles, value, onChange
}: { styles: StyleOption[]; value: string; onChange: (v: string) => void }) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
      {styles.map((s) => (
        <button key={s.name} onClick={() => onChange(s.name)}
          className={`px-3 py-2 rounded-lg text-sm border transition
            ${value === s.name ? "border-sf-accent bg-white/10" : "border-white/10 hover:bg-white/5"}`}>
          {s.label}
        </button>
      ))}
    </div>
  );
}