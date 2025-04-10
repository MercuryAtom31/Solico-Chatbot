const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let flaskProcess;

function startFlask() {
  // Path to your compiled EXE (PyInstaller output)
  const exePath = path.join(__dirname, 'flask_backend', 'dist', 'app.exe');

  // IMPORTANT: Set cwd to the same dist folder containing app.exe, index.html, ollama.exe
  flaskProcess = spawn(exePath, [], {
    cwd: path.join(__dirname, 'flask_backend', 'dist'),
    windowsHide: true
  });

  // Optional logs for debugging
  flaskProcess.stdout.on('data', (data) => {
    console.log(`[Flask] ${data}`);
  });
  flaskProcess.stderr.on('data', (data) => {
    console.error(`[Flask Error] ${data}`);
  });
  flaskProcess.on('close', (code) => {
    console.log(`Flask process exited with code ${code}`);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });
  // Load the local Flask server
  mainWindow.loadURL('http://127.0.0.1:5000');
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startFlask();
  // Wait 12s for Flask + Ollama to spin up before creating the Electron window
  setTimeout(() => {
    createWindow();
  }, 12000);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (flaskProcess) {
      process.kill(flaskProcess.pid);
    }
    app.quit();
  }
});

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

