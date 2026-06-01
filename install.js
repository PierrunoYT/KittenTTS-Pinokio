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
      method: "shell.run",
      params: {
        venv: "env",
        path: "app",
        message: "python -c \"from kittentts import KittenTTS; print('KittenTTS installed successfully!')\"",
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
