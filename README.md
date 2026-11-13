# KittenTTS 😻 — Pinokio Launcher

A 1-click [Pinokio](https://pinokio.computer) launcher for
[Kitten TTS 2](https://huggingface.co/KittenML/kitten-tts-2), a 1.7B
text-to-speech model with voice cloning and expression control that runs on
CPU — no GPU required.

The launcher installs the `kittenml` package (with PyTorch) into an isolated
virtual environment and serves a Gradio web UI for generating speech.

## Install

1. Install [Pinokio](https://pinokio.computer).
2. In Pinokio, choose **Discover → Download from URL** and paste:
   ```
   https://github.com/PierrunoYT/KittenTTS-Pinokio
   ```
3. Click **Install**, then **Start** once it finishes.

The first launch downloads the model (~954 MB, or ~492 MB for the Compact
weights), so give it a moment before the UI becomes responsive.

## Using it

| Control | Notes |
| --- | --- |
| **Text** | The text to synthesize. Supports `[emotion]` tags, `<laugh>`-style events and `(((emphasis)))`. |
| **Model weights** | Standard (954 MB, lossless) or Compact (492 MB, quantised embedding). |
| **Voice** | Any of the model's built-in voices (Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo and many more). |
| **Preset** | `stable` or `expressive`. |
| **Voice cloning** | Optional 5–30 s reference clip of one speaker, plus an optional transcript (auto-transcribed by Whisper when empty). Overrides the voice. |

Output is 24 kHz mono WAV, playable and downloadable from the **Generated
Audio** panel. Models are cached in memory after their first use, so switching
back to weights you have already used is instant.

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
| `app/requirements.txt` | Python dependencies, including the pinned `kittenml` package. |
| `pinokio.js` | Menu definition and install-state detection. |
| `install.js` / `start.js` / `update.js` / `reset.js` / `link.js` | Pinokio launcher scripts. |

## Requirements

- Pinokio 7.0 or later
- Roughly 5 GB of free disk space for the environment (PyTorch) and model weights
- About 6 GB of RAM; no GPU needed

## License

MIT — see [LICENSE](LICENSE). The `kittenml` code is Apache 2.0; the Kitten TTS 2
weights are under the
[Stellon Labs Community License](https://huggingface.co/KittenML/kitten-tts-2/blob/main/LICENSE.md)
(commercial users must register; attribution "Powered by Stellon Labs" required).
