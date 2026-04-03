module.exports = {
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
        message: "python -c \"from kittentts import KittenTTS; print('KittenTTS installed successfully!')\"",
      },
    },
    {
      method: "fs.write",
      params: {
        path: "INSTALLATION_COMPLETE.txt",
        text: "KittenTTS 😻 installation completed successfully.\n\nNext steps:\n1. Start the application using the Start button\n2. Open the web interface at the provided URL\n3. Begin generating audio with the ultra-lightweight TTS model\n\nFeatures:\n- Models from 15M to 80M parameters\n- CPU-optimized: Runs without GPU on any device\n- 8 premium voices: Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo\n- Adjustable speech speed\n\nFor support, visit: https://github.com/KittenML/KittenTTS",
      },
    },
  ],
}
