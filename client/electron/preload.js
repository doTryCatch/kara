const { contextBridge, ipcRenderer } = require("electron");
window.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("clickThroughElement");
  el.addEventListener("mouseenter", () => {
    ipcRenderer.send("set-ignore-mouse-events", true, { forward: true });
  });
  el.addEventListener("mouseleave", () => {
    ipcRenderer.send("set-ignore-mouse-events", false);
  });
});
contextBridge.exposeInMainWorld("electronAPI", {
  on: (channel, callback) => {
    ipcRenderer.on(channel, callback);
  },
  send: (channel, args) => {
    ipcRenderer.send(channel, args);
  },
});
   
