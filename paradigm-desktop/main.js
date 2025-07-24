const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const { autoUpdater } = require('electron-updater');


let pythonProcess;
let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1000,
    height: 800,
    icon: path.join(__dirname, 'assets', 'paradigm-icon.ico'),
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js') // Use secure preload bridge
    }
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));
}

function startPythonBackend() {
  const exePath = path.join(__dirname, 'backend', 'main.exe');
  pythonProcess = spawn(exePath, [], {
    shell: false,
    windowsHide: true,
    stdio: ['ignore', 'pipe', 'pipe']
  });

  // Handle STDOUT (main logs)
  pythonProcess.stdout.on('data', (data) => {
    const lines = data.toString().split('\n');

    for (const rawLine of lines) {
      const msg = rawLine.trim();

      // Filter out HTTP noise & empty lines
      if (
        msg.length === 0 ||
        (msg.startsWith("INFO:") && msg.includes("127.0.0.1")) ||
        msg.includes("HTTP/1.1")
      ) {
        continue;
      }

      // Match useful keywords for model inference pipeline
      const keywords = [
        'gguf', 'inference', 'streaming', 'tokenizer',
        'model loaded', 'model saved', 'running on',
        'quantizing', 'loading', 'GPU', 'CPU', 'token',
        'output', 'response'
      ];

      const isImportant = keywords.some((kw) => msg.toLowerCase().includes(kw));

      if (isImportant) {
        // Send to frontend UI
        mainWindow?.webContents.send('python-log', msg);
        console.log(`PYTHON: ${msg}`);
      } else {
        // Keep log for backend debugging
        console.log(`(IGNORED): ${msg}`);
      }
    }
  });

  // Handle STDERR (errors/warnings)
  pythonProcess.stderr.on('data', (data) => {
    const lines = data.toString().split('\n');

    for (const rawLine of lines) {
      const errMsg = rawLine.trim();
      if (errMsg.length > 0) {
        console.error(`PYTHON ERROR: ${errMsg}`);
      }
    }
  });

  pythonProcess.on('close', (code) => {
    console.log(`Python backend exited with code ${code}`);
  });
}

app.whenReady().then(() => {
  createWindow();
  startPythonBackend();
  autoUpdater.checkForUpdatesAndNotify();
});


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (pythonProcess) pythonProcess.kill();
    app.quit();
  }
});
