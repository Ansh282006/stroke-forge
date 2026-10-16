"""JS runtime builder (M6)."""
from __future__ import annotations
import json
from typing import Any, Dict, List
from animation_engine.timeline import AnimationTimeline

_TEMPLATE = r"""// StrokeForge generated runtime (M6)
const SF_DATA = __SF_DATA__;
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var stage = document.getElementById("sf-stage");
  var btnPP = document.getElementById("sf-playpause");
  var btnR = document.getElementById("sf-restart");
  var speed = document.getElementById("sf-speed");
  var speedVal = document.getElementById("sf-speed-val");
  var status = document.getElementById("sf-status");
  if (!stage || !btnPP || !btnR || !speed) return;

  var style = SF_DATA.style || {};
  var paths = SF_DATA.paths || [];
  var timeline = SF_DATA.timeline || { total_ms: 0, entries: [] };
  var opts = SF_DATA.options || {};
  var canvas = SF_DATA.canvas || {};
  var W = canvas.width || 512, H = canvas.height || 512;

  function el(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { if (attrs[k] != null) n.setAttribute(k, attrs[k]); });
    return n;
  }
  function toD(pts) {
    if (!pts || !pts.length) return "";
    var d = "M " + (+pts[0][0]).toFixed(2) + " " + (+pts[0][1]).toFixed(2);
    for (var i = 1; i < pts.length; i++) d += " L " + (+pts[i][0]).toFixed(2) + " " + (+pts[i][1]).toFixed(2);
    return d;
  }
  function len(pts) {
    var t = 0;
    for (var i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i-1][0], dy = pts[i][1] - pts[i-1][1];
      t += Math.sqrt(dx*dx + dy*dy);
    }
    return t;
  }

  var svg = el("svg", { xmlns: NS, viewBox: "0 0 " + W + " " + H, class: "sf-svg", preserveAspectRatio: "xMidYMid meet" });
  var defs = el("defs");
  var filter = el("filter", { id: "sf-glow", x: "-50%", y: "-50%", width: "200%", height: "200%" });
  filter.appendChild(el("feGaussianBlur", { stdDeviation: 3, result: "blur" }));
  var merge = el("feMerge");
  merge.appendChild(el("feMergeNode", { in: "blur" }));
  merge.appendChild(el("feMergeNode", { in: "blur" }));
  merge.appendChild(el("feMergeNode", { in: "SourceGraphic" }));
  filter.appendChild(merge); defs.appendChild(filter); svg.appendChild(defs);
  svg.appendChild(el("rect", { x: 0, y: 0, width: W, height: H, fill: style.background || "#05060a" }));

  var byId = {}; (timeline.entries || []).forEach(function (e) { byId[e.path_id] = e; });
  paths.forEach(function (p) {
    var entry = byId[p.id]; if (!entry) return;
    var l = +p.length || len(p.points || []) || 1;
    var node = el("path", {
      class: "sf-path", d: toD(p.points || []), fill: "none",
      stroke: style.stroke_color || "#00f0ff",
      "stroke-width": style.stroke_width != null ? style.stroke_width : 2.2,
      "stroke-linecap": style.linecap || "round",
      "stroke-linejoin": style.linejoin || "round",
      opacity: style.opacity != null ? style.opacity : 1,
      "data-order": entry.order, "data-path-id": p.id
    });
    if (style.glow) node.setAttribute("filter", "url(#sf-glow)");
    node.style.setProperty("--sf-len", l.toFixed(2));
    node.style.setProperty("--sf-dur", entry.duration_ms + "ms");
    node.style.setProperty("--sf-delay", entry.start_ms + "ms");
    node.style.setProperty("--sf-ease", entry.easing || "ease-in-out");
    svg.appendChild(node);
  });
  stage.appendChild(svg);

  var playing = false, loopTimer = null;
  function anims() { return svg.getAnimations ? svg.getAnimations({ subtree: true }) : []; }
  function rate() { return Math.max(0.01, parseFloat(speed.value) || 1); }
  function scheduleLoop() {
    if (!opts.loop) return;
    if (loopTimer) clearTimeout(loopTimer);
    var wait = ((+timeline.total_ms || 0) / rate()) + (+opts.loop_delay_ms || 0);
    loopTimer = setTimeout(function () { if (playing) restart(); }, Math.max(60, wait));
  }
  function setPlaying(state) {
    var r = rate();
    anims().forEach(function (a) { a.playbackRate = r; state ? a.play() : a.pause(); });
    playing = !!state;
    btnPP.textContent = playing ? "Pause" : "Play";
    if (status) status.textContent = playing ? "playing" : "paused";
    if (playing) scheduleLoop(); else if (loopTimer) { clearTimeout(loopTimer); loopTimer = null; }
  }
  function restart() {
    var r = rate();
    anims().forEach(function (a) { a.currentTime = 0; a.playbackRate = r; a.play(); });
    playing = true; btnPP.textContent = "Pause";
    if (status) status.textContent = "playing";
    scheduleLoop();
  }
  requestAnimationFrame(function () { setPlaying(opts.autoplay !== false); });
  btnPP.addEventListener("click", function () { setPlaying(!playing); });
  btnR.addEventListener("click", restart);
  speed.addEventListener("input", function () {
    var v = rate();
    if (speedVal) speedVal.textContent = v.toFixed(2) + "x";
    anims().forEach(function (a) { a.playbackRate = v; });
    if (playing) scheduleLoop();
  });
  if (speedVal) speedVal.textContent = rate().toFixed(2) + "x";
})();
"""

def _pick_paths(doc):
    out = []
    for p in doc.get("paths") or []:
        out.append({"id": p.get("id"), "points": p.get("points") or [],
                    "length": p.get("length"), "order": p.get("order")})
    return out

def build_js(styled_doc, timeline: AnimationTimeline, options) -> str:
    payload = {
        "canvas": styled_doc.get("canvas") or {"width": 512, "height": 512},
        "style": styled_doc.get("style") or {},
        "paths": _pick_paths(styled_doc),
        "timeline": timeline.to_dict(),
        "options": options,
    }
    return _TEMPLATE.replace("__SF_DATA__", json.dumps(payload, separators=(",", ":")))