// preload.js
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electron", {
    sendToPython: (data) => ipcRenderer.send(data.event, data.message),
    onFromPython: (callback) => ipcRenderer.on("fromPython", callback),
});