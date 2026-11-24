module.exports = {
  requires: {
    bundle: "ai"
  },
  run: [
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: [
          "uv pip install -r requirements.txt",
        ],
      },
    },
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          path: "app",
          venv: "env",
        },
      },
    },
    {
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "python -c \"from kittenml import KittenTTS; print('KittenTTS installed successfully!')\"",
      },
    },
    {
      method: "input",
      params: {
        title: "Install Complete!!",
        description: "Install Complete. (App is safe to click Save Disk Space)"
      }
    },
  ],
}
