document.getElementById("go").addEventListener("click", async () => {
  const style = document.getElementById("style").value;
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab?.id) return;
  chrome.tabs.sendMessage(tab.id, { type: "sf:preview", style });
  window.close();
});