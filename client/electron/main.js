const { app, BrowserWindow, screen } = require("electron");
const path = require("path");
require("electron-reload")(path.join(__dirname), {
    electron: path.join(__dirname, "node_modules", ".bin", "electron"),
});

let mainWindow;

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    // Create the Electron window
    mainWindow = new BrowserWindow({
        width: width,
        height: height,
        transparent: true, // Makes the window fully transparent
        frame: false, // Removes the window frame
        alwaysOnTop: true, // Keeps the window on top
        fullscreen: true, // Ensures the window covers the entire screen
        skipTaskbar: true, // Hides the window from the taskbar (optional)
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    // Load your Next.js application
    mainWindow.loadURL("http://localhost:3000");

    // Enable click-through on transparent areas
    mainWindow.setIgnoreMouseEvents(true, { forward: true });

    // Handle window events
    mainWindow.on("closed", function() {
        mainWindow = null;
    });

    // Allow dragging on specific areas
    mainWindow.webContents.on("did-finish-load", () => {
        // mainWindow.setIgnoreMouseEvents(false); // Allow mouse events on the entire window
        mainWindow.webContents.executeJavaScript(`
      const c
      document.body.addEventListener('click', (event) => {
        if (event.target.id !== 'content') {
          currentWindow.setIgnoreMouseEvents(true, { forward: true });
        } else {
          currentWindow.setIgnoreMouseEvents(false);
        }
      });

      document.body.addEventListener('mousemove', (event) => {
        if (event.target.id !== 'content') {
          currentWindow.setIgnoreMouseEvents(true, { forward: true });
        }
      });
  urrentWindow = require('electron').remote.getCurrentWindow();
  `);
    });
}

app.on("ready", createWindow);

app.on("window-all-closed", function() {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

app.on("activate", function() {
    if (mainWindow === null) {
        createWindow();
    }
});
