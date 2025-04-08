const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let mainWindow;
let flaskProcess;

function startFlask() {
  // On Windows, you can just use 'python'
  const python = process.platform === 'win32' ? 'python' : 'python3';
  flaskProcess = spawn(python, ['app.py'], {
    cwd: path.join(__dirname, 'flask_backend'), // Where app.py resides
    //detached: true
  });

  flaskProcess.stdout.on('data', data => {
    console.log(`[Flask] ${data}`);
  });
  flaskProcess.stderr.on('data', data => {
    console.error(`[Flask Error] ${data}`);
  });
  flaskProcess.on('close', code => {
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
  mainWindow.loadURL('http://127.0.0.1:5000');
  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startFlask();
  // Give Flask a couple seconds to spin up before loading the page
  setTimeout(() => {
    createWindow();
  }, 12000);
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (flaskProcess) {
      // Kills the entire child process group
      // process.kill(-flaskProcess.pid);
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
