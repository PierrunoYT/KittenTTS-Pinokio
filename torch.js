// Swaps the PyPI PyTorch for a GPU build where one helps. Adapted from the
// Pinokio examples (Kokoro-TTS/torch.js). kittenml needs torch>=2.6, so the
// Intel-Mac (torch 2.2) and DirectML (older torch) variants are left out;
// macOS and every other machine keep the PyPI build from requirements.txt.
module.exports = {
  run: [
    // nvidia windows (PyPI only ships CPU wheels for Windows)
    {
      "when": "{{gpu === 'nvidia' && platform === 'win32'}}",
      "method": "shell.run",
      "params": {
        "venv": "{{args && args.venv ? args.venv : null}}",
        "path": "{{args && args.path ? args.path : '.'}}",
        "message": "uv pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128 --force-reinstall --no-deps"
      },
      "next": null
    },
    // nvidia linux
    {
      "when": "{{gpu === 'nvidia' && platform === 'linux'}}",
      "method": "shell.run",
      "params": {
        "venv": "{{args && args.venv ? args.venv : null}}",
        "path": "{{args && args.path ? args.path : '.'}}",
        "message": "uv pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128 --force-reinstall"
      },
      "next": null
    },
    // amd linux (rocm)
    {
      "when": "{{gpu === 'amd' && platform === 'linux'}}",
      "method": "shell.run",
      "params": {
        "venv": "{{args && args.venv ? args.venv : null}}",
        "path": "{{args && args.path ? args.path : '.'}}",
        "message": "uv pip install torch==2.7.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/rocm6.3 --force-reinstall --no-deps"
      },
      "next": null
    }
  ]
}
