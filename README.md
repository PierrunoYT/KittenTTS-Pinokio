# KittenTTS 😻 — Pinokio Launcher

A 1-click [Pinokio](https://pinokio.computer) launcher for
[Kitten TTS 2](https://huggingface.co/KittenML/kitten-tts-2), a 1.7B
text-to-speech model with voice cloning and expression control, and
[Kitten TTS 2 Mini](https://huggingface.co/KittenML/kitten-tts-2-mini), an 82M
model covering 16 languages. Both run on CPU — no GPU required.

The launcher installs the `kittenml` package (with PyTorch) into an isolated
virtual environment and serves a Gradio web UI for generating speech.

## Install

1. Install [Pinokio](https://pinokio.computer).
2. In Pinokio, choose **Discover → Download from URL** and paste:
   ```
   https://github.com/PierrunoYT/KittenTTS-Pinokio
   ```
3. Click **Install**, then **Start** once it finishes.

The first launch downloads the default model (~954 MB), so give it a moment
before the UI becomes responsive. Other models download when first selected.

## Using it

| Control | Notes |
| --- | --- |
| **Text** | The text to synthesize. Kitten TTS 2 supports `[emotion]` tags, `<laugh>`-style events and `(((emphasis)))`. |
| **Model** | Kitten TTS 2 Standard (954 MB, lossless), Kitten TTS 2 Compact (492 MB, quantised embedding) or Kitten TTS 2 Mini (83 MB, int8 ONNX, much faster). |
| **Language** | Mini only: en, de, es, it, pt, ru, hi, da, fi, fr, ja, ko, nl, sv, sw, tr. |
| **Voice** | The selected model's built-in voices (for Mini, the selected language's voices). |
| **Speed** | Mini only: 0.5×–2.0×. |
| **Preset** | Kitten TTS 2 only: `stable` or `expressive`. |
| **Voice cloning** | Kitten TTS 2 only: optional 5–30 s reference clip of one speaker, plus an optional transcript (auto-transcribed by Whisper when empty). Overrides the voice. |

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
Kitten TTS 2 Mini weights are Apache 2.0.
