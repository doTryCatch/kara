const { app, BrowserWindow, ipcMain } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let win;
let pythonProcess;

app.on("ready", () => {
  win = new BrowserWindow({
    fullscreen: true,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: false, // Allows Node.js integration
      contextIsolation: true, // Disable context isolation for simplicity
      preload: path.join(__dirname, "preload.js"),
    },

    transparent: true, // For transparency
    frame: false, // Remove frame for custom design
  });

  win.loadURL("http://localhost:3000/");
  win.setAlwaysOnTop(true, "screen-saver");
  // Spawn the Python process
  pythonProcess = spawn("python", [
    path.join(__dirname, "../", "server/main.py"),
  ]);


  // handle mouse bypass window screen on transparent area
  ipcMain.on("setMouseIgnore", (event, arg) => {
    if (arg) {
      win.setIgnoreMouseEvents(true, { forward: true });
    } else {
      win.setIgnoreMouseEvents(false);
    }
  });
  // Handle incoming messages from the Python procesf
  pythonProcess.stdout.on("data", (data) => {
    try {
      const response = data.toString();
      // console.log(`Received from Python: ${data}`);
      win.webContents.send("fromPython", response);
    } catch (error) {
      console.error("Error parsing JSON from Python:", error);
      console.error("Raw data received:", data.toString());
      win.webContents.send("fromPython", { error: "Invalid JSON received" });
    }
  });

  // Handle messages from the renderer process
  ipcMain.on("toPython", (event, arg) => {
    // console.log(`Sending to Python: ${arg}`);
    pythonProcess.stdin.write(`${arg}\n`);
  });
});
