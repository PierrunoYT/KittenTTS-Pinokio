module.exports = {
  run: [
    // Install KittenTTS and dependencies
    {
      method: "shell.run",
      params: {
        venv: "env",
        message: [
          "uv pip install -r requirements.txt"
        ],
      }
    },
    
    // Test KittenTTS installation
    {
      method: "shell.run",
      params: {
        venv: "env",
        message: "python -c \"from kittentts import KittenTTS; print('KittenTTS installed successfully!')\""
      }
    },
    
    // Create a setup completion marker
    {
      method: "fs.write",
      params: {
        path: "INSTALLATION_COMPLETE.txt",
        text: "KittenTTS 😻 installation completed successfully.\n\nNext steps:\n1. Start the application using the Start button\n2. Open the web interface at the provided URL\n3. Begin generating audio with the ultra-lightweight TTS model\n\nFeatures:\n- Ultra-lightweight: Model size less than 25MB\n- CPU-optimized: Runs without GPU on any device\n- High-quality voices: 8 premium voice options available\n- Fast inference: Optimized for real-time speech synthesis\n\nFor support, visit: https://github.com/KittenML/KittenTTS"
      }
    }
  ]
}