"""Standalone HTML player (M5)."""
from __future__ import annotations
import html, json

def render_player_html(svg_markup, title="StrokeForge", autoplay=True, loop=False, loop_delay_ms=0, total_ms=0):
    safe = html.escape(title)
    cfg = json.dumps({"autoplay": bool(autoplay), "loop": bool(loop),
                      "loopDelayMs": int(loop_delay_ms), "totalMs": int(total_ms)})
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{safe}</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>html,body{{background:#05060a;color:#e7e9ee;}}.sf-stage svg{{display:block;width:100%;height:auto;max-height:78vh;}}</style>
</head><body class="min-h-screen flex flex-col items-center justify-center gap-6 p-6">
<header class="text-center"><h1 class="text-2xl font-semibold">{safe}</h1>
<p class="text-sm text-slate-400">StrokeForge animated preview</p></header>
<div class="sf-stage w-full max-w-3xl rounded-2xl border border-white/10 bg-black/40 p-4 shadow-2xl">{svg_markup}</div>
<div class="w-full max-w-3xl flex flex-wrap items-center gap-3 justify-center">
<button id="sf-playpause" class="px-4 py-2 rounded-lg bg-cyan-500/90 hover:bg-cyan-400 text-black font-medium">Pause</button>
<button id="sf-restart" class="px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white font-medium">Restart</button>
<label class="flex items-center gap-2 text-sm text-slate-300">Speed
<input id="sf-speed" type="range" min="0.25" max="3" step="0.05" value="1" class="accent-cyan-400"/>
<span id="sf-speed-val" class="w-10 text-right tabular-nums">1.00x</span></label>
</div>
<script>
(function () {{
  const cfg = {cfg};
  const svg = document.querySelector('svg.sf-svg'); if (!svg) return;
  const btnPP = document.getElementById('sf-playpause');
  const btnR  = document.getElementById('sf-restart');
  const speed = document.getElementById('sf-speed');
  const speedVal = document.getElementById('sf-speed-val');
  let playing = false, loopTimer = null;
  function anims(){{ return svg.getAnimations ? svg.getAnimations({{subtree:true}}) : []; }}
  function scheduleLoop(){{
    if (!cfg.loop) return; if (loopTimer) clearTimeout(loopTimer);
    const rate = Math.max(0.01, parseFloat(speed.value));
    const wait = (cfg.totalMs / rate) + cfg.loopDelayMs;
    loopTimer = setTimeout(function(){{ if (playing) restart(); }}, Math.max(60, wait));
  }}
  function setPlayState(state){{
    const rate = Math.max(0.01, parseFloat(speed.value));
    anims().forEach(function(a){{ a.playbackRate = rate; state==='running' ? a.play() : a.pause(); }});
    playing = (state === 'running'); btnPP.textContent = playing ? 'Pause' : 'Play';
    if (playing) scheduleLoop(); else if (loopTimer) {{ clearTimeout(loopTimer); loopTimer = null; }}
  }}
  function restart(){{
    const rate = Math.max(0.01, parseFloat(speed.value));
    anims().forEach(function(a){{ a.currentTime = 0; a.playbackRate = rate; a.play(); }});
    playing = true; btnPP.textContent = 'Pause'; scheduleLoop();
  }}
  requestAnimationFrame(function(){{ cfg.autoplay ? setPlayState('running') : setPlayState('paused'); }});
  btnPP.addEventListener('click', function(){{ setPlayState(playing ? 'paused' : 'running'); }});
  btnR.addEventListener('click', restart);
  speed.addEventListener('input', function(){{
    const v = Math.max(0.01, parseFloat(speed.value));
    speedVal.textContent = v.toFixed(2) + 'x';
    anims().forEach(function(a){{ a.playbackRate = v; }});
    if (playing) scheduleLoop();
  }});
}})();
</script></body></html>
"""