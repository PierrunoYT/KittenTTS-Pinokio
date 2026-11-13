import threading

import gradio as gr
import numpy as np
from kittenml import KittenTTS

MODEL_ID = "KittenML/kitten-tts-2"

# Weight packings of Kitten TTS 2; only the selected one is downloaded.
WEIGHTS = {
    "Standard (954 MB - Lossless)": "packed",
    "Compact (492 MB - Quantised embedding)": "emb4",
}
DEFAULT_WEIGHTS = "Standard (954 MB - Lossless)"

PRESETS = ["stable", "expressive"]

# Speakers shared with KittenTTS 0.8; shown until the model reports its full list.
DEFAULT_VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]
DEFAULT_VOICE = "Luna"

# Model cache. Loading is slow, so hold a lock to keep concurrent requests
# from loading the same model several times over.
loaded_models = {}
_model_lock = threading.Lock()

# Gradio writes every returned clip into its cache. Sweep it hourly for clips
# older than a day; Gradio also clears it when the server shuts down.
CACHE_SWEEP = (3600, 86400)


def get_model(weights_name):
    weights = WEIGHTS[weights_name]
    with _model_lock:
        if weights not in loaded_models:
            print(f"Loading model: {MODEL_ID} ({weights})...")
            loaded_models[weights] = KittenTTS(MODEL_ID, weights=weights)
            print(f"Model {MODEL_ID} ({weights}) loaded successfully!")
        return loaded_models[weights]


def list_voices(weights_name):
    try:
        voices = sorted(get_model(weights_name).available_voices)
    except Exception as e:
        print(f"Warning: could not list voices: {e}")
        voices = DEFAULT_VOICES
    value = DEFAULT_VOICE if DEFAULT_VOICE in voices else voices[0]
    return gr.update(choices=voices, value=value)


def generate_speech(text, voice, reference, reference_text, preset, weights_name):
    try:
        if not isinstance(text, str) or not text.strip():
            return None, "Error: Input text cannot be empty"

        if weights_name not in WEIGHTS:
            return None, "Error: Invalid model selection"

        if preset not in PRESETS:
            return None, "Error: Invalid preset selection"

        tts_model = get_model(weights_name)

        if reference:
            # Cloning: the recording replaces the built-in speaker.
            kwargs = {"reference": reference}
            if isinstance(reference_text, str) and reference_text.strip():
                kwargs["reference_text"] = reference_text.strip()
        else:
            if voice not in tts_model.available_voices:
                return None, "Error: Invalid voice selection"
            kwargs = {"voice": voice}

        audio = tts_model.generate(text, preset=preset, **kwargs)

        # Ensure type/shape/range are valid before encoding
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim == 0:
            audio = audio.reshape(1)
        if audio.size == 0:
            return None, "Error: Model returned empty audio"
        audio = np.nan_to_num(audio, nan=0.0, posinf=1.0, neginf=-1.0)
        audio = np.clip(audio, -1.0, 1.0)

        # Hand Gradio 16-bit PCM directly; it writes the WAV into its own
        # cache, so an intermediate temp file would only be a second copy.
        pcm = (audio * 32767).astype(np.int16)

        source = "cloned voice" if reference else voice
        return (tts_model.sample_rate, pcm), f"Audio generated successfully ({source})!"
    except Exception as e:
        return None, f"Error generating audio: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="KittenTTS 😻", delete_cache=CACHE_SWEEP) as demo:
    gr.Markdown("# KittenTTS 😻")
    gr.Markdown(
        "Kitten TTS 2 — 1.7B text-to-speech with voice cloning and expression control. "
        "Model weights are under the "
        "[Stellon Labs Community License](https://huggingface.co/KittenML/kitten-tts-2/blob/main/LICENSE.md). "
        "Powered by Stellon Labs."
    )

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to synthesize",
                placeholder="Enter text here...",
                lines=3,
                value="This high quality TTS model works without a GPU",
                info="Supports [emotion] tags, <laugh>-style events and (((emphasis)))",
            )

            model_dropdown = gr.Dropdown(
                label="Model weights",
                choices=list(WEIGHTS.keys()),
                value=DEFAULT_WEIGHTS,
                info="Compact halves the download at a small quality cost",
            )

            voice_dropdown = gr.Dropdown(
                label="Voice",
                choices=DEFAULT_VOICES,
                value=DEFAULT_VOICE,
                info="Built-in voice; ignored when a reference clip is given",
            )

            preset_radio = gr.Radio(
                label="Preset",
                choices=PRESETS,
                value="stable",
                info="Trade stability against expressiveness",
            )

            with gr.Accordion("Voice cloning", open=False):
                reference_audio = gr.Audio(
                    label="Reference clip (5-30 s, one speaker)",
                    type="filepath",
                    sources=["upload", "microphone"],
                )
                reference_text_input = gr.Textbox(
                    label="Reference transcript (optional)",
                    placeholder="Leave empty to auto-transcribe with Whisper",
                    lines=2,
                )

            generate_btn = gr.Button("Generate Speech 🎵", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio")
            status_text = gr.Textbox(label="Status", interactive=False)

    gr.Examples(
        examples=[
            ["Hello world! This is Kitten TTS 2 speaking.", "Luna", "stable"],
            ["The quick brown fox jumps over the lazy dog.", "Bruno", "stable"],
            ["[joyful] We actually won the grant <laugh> I can (((hardly))) believe it!", "Kiki", "expressive"],
            ["Welcome to the future of efficient speech synthesis!", "Hugo", "stable"],
        ],
        inputs=[text_input, voice_dropdown, preset_radio],
    )

    demo.load(fn=list_voices, inputs=model_dropdown, outputs=voice_dropdown)
    model_dropdown.change(fn=list_voices, inputs=model_dropdown, outputs=voice_dropdown)

    generate_btn.click(
        fn=generate_speech,
        inputs=[
            text_input,
            voice_dropdown,
            reference_audio,
            reference_text_input,
            preset_radio,
            model_dropdown,
        ],
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
    print("Initializing Kitten TTS 2 model...")
    try:
        get_model(DEFAULT_WEIGHTS)
    except Exception as e:
        print(f"Warning: could not preload the default model: {e}")

    demo.queue().launch(
        server_name=args.host,
        server_port=args.port,
        share=False,
        inbrowser=False,
    )
