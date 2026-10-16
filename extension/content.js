// Content script (M8). Listens for a popup request, opens an overlay
// iframe that hosts sandbox.html, then asks the sandbox to load the
// backend-served preview. Uses a unique id so repeated openings don't
// stack.

const OVERLAY_ID = "sf-overlay";

function closeOverlay() {
  const el = document.getElementById(OVERLAY_ID);
  if (el) el.remove();
}

function openOverlay(style) {
  closeOverlay();
  const wrap = document.createElement("div");
  wrap.id = OVERLAY_ID;
  wrap.style.cssText = [
    "position:fixed", "inset:0", "z-index:2147483647",
    "background:rgba(0,0,0,0.72)", "backdrop-filter:blur(6px)",
    "display:flex", "align-items:center", "justify-content:center"
  ].join(";");

  const box = document.createElement("div");
  box.style.cssText = [
    "width:min(1000px,92vw)", "height:min(80vh,720px)",
    "background:#05060a", "border-radius:14px",
    "border:1px solid rgba(255,255,255,0.1)", "overflow:hidden",
    "position:relative"
  ].join(";");

  const sandbox = document.createElement("iframe");
  sandbox.src = chrome.runtime.getURL("sandbox.html");
  sandbox.style.cssText = "border:0;width:100%;height:100%;";
  sandbox.setAttribute("sandbox", "allow-scripts");

  const close = document.createElement("button");
  close.textContent = "Close";
  close.style.cssText = [
    "position:absolute", "top:10px", "right:10px",
    "padding:6px 10px", "border-radius:8px", "border:none",
    "background:#00f0ff", "color:#000", "font-weight:600", "cursor:pointer"
  ].join(";");
  close.addEventListener("click", closeOverlay);

  box.appendChild(sandbox);
  box.appendChild(close);
  wrap.appendChild(box);
  document.body.appendChild(wrap);

  // Tell the sandbox to load the backend preview for this style.
  chrome.storage.local.get("backendUrl").then((r) => {
    const base = r.backendUrl || "http://127.0.0.1:8000";
    const url = `${base}/api/preview?style=${encodeURIComponent(style)}`;
    const send = () => sandbox.contentWindow?.postMessage({ type: "sf:load", url }, "*");
    // The sandbox may not be ready yet; retry briefly.
    let tries = 0;
    const iv = setInterval(() => {
      send();
      if (++tries > 20) clearInterval(iv);
    }, 100);
  });
}

chrome.runtime.onMessage.addListener((msg) => {
  if (msg && msg.type === "sf:preview") openOverlay(msg.style || "neon");
});