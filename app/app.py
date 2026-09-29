import atexit
import os
import shutil
import tempfile
import threading

import gradio as gr
import numpy as np
import soundfile as sf
from kittentts import KittenTTS

# Available models (ordered by quality/size)
MODELS = {
    "Mini (80M - Best Quality)": "KittenML/kitten-tts-mini-0.8",
    "Micro (40M - Balanced)": "KittenML/kitten-tts-micro-0.8",
    "Nano (15M - Fastest)": "KittenML/kitten-tts-nano-0.8",
    "Nano INT8 (15M - Smallest)": "KittenML/kitten-tts-nano-0.8-int8",
}

# Available voices
VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]

DEFAULT_MODEL = "Nano (15M - Fastest)"
SAMPLE_RATE = 24000
MIN_SPEED, MAX_SPEED = 0.5, 2.0

# Model cache. Loading is slow, so hold a lock to keep concurrent requests
# from loading the same model several times over.
loaded_models = {}
_model_lock = threading.Lock()

# Generated clips live here so they can all be removed on exit instead of
# accumulating in the system temp directory for the life of the machine.
OUTPUT_DIR = tempfile.mkdtemp(prefix="kittentts-")
atexit.register(shutil.rmtree, OUTPUT_DIR, True)


def get_model(model_name):
    model_id = MODELS[model_name]
    with _model_lock:
        if model_id not in loaded_models:
            print(f"Loading model: {model_id}...")
            loaded_models[model_id] = KittenTTS(model_id)
            print(f"Model {model_id} loaded successfully!")
        return loaded_models[model_id]


def generate_speech(text, voice, speed, model_name):
    try:
        if not isinstance(text, str) or not text.strip():
            return None, "Error: Input text cannot be empty"

        if voice not in VOICES:
            return None, "Error: Invalid voice selection"

        if model_name not in MODELS:
            return None, "Error: Invalid model selection"

        try:
            speed = float(speed)
        except (TypeError, ValueError):
            return None, "Error: Speed must be a number"
        if not np.isfinite(speed):
            return None, "Error: Speed must be a number"
        speed = min(max(speed, MIN_SPEED), MAX_SPEED)

        tts_model = get_model(model_name)
        audio = tts_model.generate(text, voice=voice, speed=speed)

        # Ensure type/shape/range are valid for soundfile writing
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim == 0:
            audio = audio.reshape(1)
        if audio.size == 0:
            return None, "Error: Model returned empty audio"
        audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
        audio = np.clip(audio, -1.0, 1.0)

        # Close the handle before soundfile opens the path: on Windows an
        # open NamedTemporaryFile cannot be reopened by another writer.
        fd, output_path = tempfile.mkstemp(suffix=".wav", dir=OUTPUT_DIR)
        os.close(fd)
        sf.write(output_path, audio, SAMPLE_RATE)

        return output_path, "Audio generated successfully!"
    except Exception as e:
        return None, f"Error generating audio: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="KittenTTS 😻") as demo:
    gr.Markdown("# KittenTTS 😻")
    gr.Markdown("Ultra-lightweight text-to-speech — CPU optimized, high-quality voice synthesis")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to synthesize",
                placeholder="Enter text here...",
                lines=3,
                value="This high quality TTS model works without a GPU",
            )

            model_dropdown = gr.Dropdown(
                label="Model",
                choices=list(MODELS.keys()),
                value=DEFAULT_MODEL,
                info="Larger models produce higher quality audio",
            )

            voice_dropdown = gr.Dropdown(
                label="Voice",
                choices=VOICES,
                value="Luna",
                info="Choose from available voice options",
            )

            speed_slider = gr.Slider(
                label="Speed",
                minimum=MIN_SPEED,
                maximum=MAX_SPEED,
                value=1.0,
                step=0.1,
                info="Adjust speech speed",
            )

            generate_btn = gr.Button("Generate Speech 🎵", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio")
            status_text = gr.Textbox(label="Status", interactive=False)

    gr.Examples(
        examples=[
            ["Hello world! This is KittenTTS speaking.", "Luna", 1.0, "Nano (15M - Fastest)"],
            ["The quick brown fox jumps over the lazy dog.", "Bruno", 1.0, "Nano (15M - Fastest)"],
            ["KittenTTS is an ultra-lightweight text-to-speech model.", "Bella", 0.9, "Nano (15M - Fastest)"],
            ["Welcome to the future of efficient speech synthesis!", "Hugo", 1.0, "Nano (15M - Fastest)"],
        ],
        inputs=[text_input, voice_dropdown, speed_slider, model_dropdown],
    )

    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, voice_dropdown, speed_slider, model_dropdown],
        outputs=[audio_output, status_text],
    )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="KittenTTS Gradio Interface")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")

    args = parser.parse_args()

    # Pre-load the default model. A failure here must not stop the server from
    # starting: the launcher waits for the printed URL, and the UI reports the
    # load error per request anyway.
    print("Initializing KittenTTS model...")
    try:
        get_model(DEFAULT_MODEL)
    except Exception as e:
        print(f"Warning: could not preload the default model: {e}")

    demo.queue().launch(
        server_name=args.host,
        server_port=args.port,
        share=False,
        inbrowser=False,
    )
