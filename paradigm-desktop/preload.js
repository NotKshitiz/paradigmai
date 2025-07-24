const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  onPythonMessage: (callback) => ipcRenderer.on('python-log', (event, message) => callback(message)),
  convertGGUF: () => ipcRenderer.send('convert-gguf') // 🚀 new line
});
