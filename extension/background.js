// Service worker (M8). Currently a stub — all preview logic lives in
// the sandboxed iframe + content script. Kept so the manifest is valid
// and so future work (job fetching, notifications) has a home.
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ backendUrl: "http://127.0.0.1:8000" });
});