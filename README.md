# KittenTTS 😻 — Pinokio Launcher

A 1-click [Pinokio](https://pinokio.computer) launcher for
[KittenTTS](https://github.com/KittenML/KittenTTS), an ultra-lightweight
text-to-speech model that runs on CPU — no GPU required.

The launcher installs KittenTTS into an isolated virtual environment and serves
a Gradio web UI for generating speech.

## Install

1. Install [Pinokio](https://pinokio.computer).
2. In Pinokio, choose **Discover → Download from URL** and paste:
   ```
   https://github.com/PierrunoYT/KittenTTS-Pinokio
   ```
3. Click **Install**, then **Start** once it finishes.

The first launch downloads the default model, so give it a moment before the UI
becomes responsive.

## Using it

The UI exposes four controls:

| Control | Notes |
| --- | --- |
| **Text** | The text to synthesize. |
| **Model** | Nano (15M), Nano INT8 (15M), Micro (40M) or Mini (80M). Larger is slower but higher quality. |
| **Voice** | Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo. |
| **Speed** | 0.5×–2.0×. |

Output is 24 kHz mono WAV, playable and downloadable from the **Generated
Audio** panel. Models are cached in memory after their first use, so switching
back to a model you have already used is instant.

Generated clips live in Gradio's cache: clips older than a day are swept
hourly, and the whole cache is cleared when the app stops. Download anything
you want to keep.

## Menu actions

| Action | What it does |
| --- | --- |
| **Install** | Creates `app/env` and installs the dependencies. |
| **Start** | Launches the Gradio server; **Open Web UI** then appears in the menu. |
| **Update** | Pulls the latest launcher and re-runs the install. |
| **Save Disk Space** | Deduplicates redundant library files across Pinokio apps. |
| **Reset** | Deletes `app/env`, reverting to the pre-install state. |

## Running without Pinokio

The app is a plain Gradio script, so you can run it directly:

```bash
cd app
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
pip install -r requirements.txt
python app.py --port 7860
```

`--host` defaults to `127.0.0.1`. The server is not exposed to the network and
`share` is off.

## Repository layout

| Path | Purpose |
| --- | --- |
| `app/app.py` | The Gradio application. |
| `app/requirements.txt` | Python dependencies, including the pinned KittenTTS wheel. |
| `pinokio.js` | Menu definition and install-state detection. |
| `install.js` / `start.js` / `update.js` / `reset.js` / `link.js` | Pinokio launcher scripts. |

## Requirements

- Pinokio 7.0 or later
- Roughly 2 GB of free disk space for the environment and model weights
- No GPU

## License

MIT — see [LICENSE](LICENSE). KittenTTS itself is licensed separately by
[KittenML](https://github.com/KittenML/KittenTTS).
