module.exports = {
  daemon: true,
  run: [
    // Start KittenTTS Gradio interface
    {
      method: "shell.run",
      params: {
        venv: "env",
        env: { },
        message: [
          "python app.py",
        ],
        on: [{
          // Monitor for Gradio server URL
          "event": "/http:\\/\\/\\S+/",
          "done": true
        }]
      }
    },
    // Set the local URL for the "Open WebUI" tab
    {
      method: "local.set",
      params: {
        // Use the captured URL from the previous step
        url: "{{input.event[0]}}"
      }
    },
  ]
}