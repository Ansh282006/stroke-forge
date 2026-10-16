export type StyleOption = { name: string; label: string };

export type JobInfo = {
  job_id: string;
  status: string;
  style: string;
  name: string;
  total_ms: number;
  files: string[];
  preview_url: string;
  bundle_url: string;
};

const BASE = "";

export async function listStyles(): Promise<StyleOption[]> {
  return [
    { name: "outline",   label: "Outline" },
    { name: "neon",      label: "Neon" },
    { name: "sketch",    label: "Sketch" },
    { name: "pencil",    label: "Pencil" },
    { name: "lineart",   label: "Line Art" },
    { name: "blueprint", label: "Blueprint" },
    { name: "particle",  label: "Particle" }
  ];
}

export async function generate(
  file: File, style: string, loop: boolean, speed: number
): Promise<JobInfo> {
  const fd = new FormData();
  fd.append("image", file);
  fd.append("style", style);
  fd.append("loop", String(loop));
  fd.append("speed", String(speed));
  const r = await fetch(`${BASE}/api/generate`, { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export function previewUrl(info: JobInfo): string {
  return `${BASE}${info.preview_url}`;
}

export function bundleUrl(info: JobInfo): string {
  return `${BASE}${info.bundle_url}`;
}

export function fileUrl(info: JobInfo, name: string): string {
  return `${BASE}/api/jobs/${info.job_id}/files/${name}`;
}