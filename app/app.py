import threading

import gradio as gr
import numpy as np
from kittenml import KittenTTS

# Kitten TTS 2 (1.7B) supports presets and voice cloning; the tiny Kitten TTS 2
# models (Mini 82M, Nano 17M, Pico 7M; int8 ONNX) support languages and speed instead.
LARGE, TINY = "large", "tiny"

# label -> (repository, constructor kwargs, family). Only the selected
# variant's files are downloaded.
MODELS = {
    "Kitten TTS 2 (1.7B, 954 MB - Lossless)": ("KittenML/kitten-tts-2", {"weights": "packed"}, LARGE),
    "Kitten TTS 2 (1.7B, 492 MB - Compact)": ("KittenML/kitten-tts-2", {"weights": "emb4"}, LARGE),
    "Kitten TTS 2 Mini (82M, 83 MB - Fast, 16 languages)": ("KittenML/kitten-tts-2-mini", {}, TINY),
    "Kitten TTS 2 Nano (17M, 17 MB per language - Faster, 8 languages)": ("KittenML/kitten-tts-2-nano", {}, TINY),
    "Kitten TTS 2 Pico (7M, 8 MB per language - Fastest, 8 languages)": ("KittenML/kitten-tts-2-pico", {}, TINY),
}
DEFAULT_MODEL = "Kitten TTS 2 (1.7B, 954 MB - Lossless)"

PRESETS = ["stable", "expressive"]
MIN_SPEED, MAX_SPEED = 0.5, 2.0

# Speakers shared with KittenTTS 0.8; shown until the model reports its full list.
DEFAULT_VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]
DEFAULT_VOICE = "Luna"
DEFAULT_LANGUAGE = "en"

# Model cache. Loading is slow, so hold a lock to keep concurrent requests
# from loading the same model several times over.
loaded_models = {}
_model_lock = threading.Lock()

# Gradio writes every returned clip into its cache. Sweep it hourly for clips
# older than a day; Gradio also clears it when the server shuts down.
CACHE_SWEEP = (3600, 86400)


def get_model(model_name):
    repo, kwargs, _ = MODELS[model_name]
    with _model_lock:
        if model_name not in loaded_models:
            print(f"Loading model: {repo} {kwargs}...")
            loaded_models[model_name] = KittenTTS(repo, **kwargs)
            print(f"Model {repo} {kwargs} loaded successfully!")
        return loaded_models[model_name]


def voices_for(model, family, language):
    """Built-in voice names for the model (and language, for tiny models)."""
    if family == TINY:
        return list(model.available_voices.get(language, []))
    return sorted(model.available_voices)


def pick(choices, preferred):
    return preferred if preferred in choices else (choices[0] if choices else None)


def on_model_change(model_name):
    """Refresh voices/languages and show only the controls the model supports."""
    family = MODELS[model_name][2]
    is_tiny = family == TINY
    try:
        model = get_model(model_name)
        languages = list(model.languages) if is_tiny else [DEFAULT_LANGUAGE]
        language = pick(languages, DEFAULT_LANGUAGE)
        voices = voices_for(model, family, language)
    except Exception as e:
        print(f"Warning: could not list voices: {e}")
        languages, language, voices = [DEFAULT_LANGUAGE], DEFAULT_LANGUAGE, DEFAULT_VOICES
    return (
        gr.update(choices=voices, value=pick(voices, DEFAULT_VOICE)),
        gr.update(choices=languages, value=language, visible=is_tiny),
        gr.update(visible=is_tiny),
        gr.update(visible=not is_tiny),
        gr.update(visible=not is_tiny),
    )


def on_language_change(model_name, language):
    family = MODELS[model_name][2]
    if family != TINY:
        return gr.update()
    try:
        voices = voices_for(get_model(model_name), family, language)
    except Exception as e:
        print(f"Warning: could not list voices: {e}")
        return gr.update()
    return gr.update(choices=voices, value=pick(voices, None))


def generate_speech(text, voice, language, speed, reference, reference_text, preset, model_name):
    try:
        if not isinstance(text, str) or not text.strip():
            return None, "Error: Input text cannot be empty"

        if model_name not in MODELS:
            return None, "Error: Invalid model selection"
        family = MODELS[model_name][2]

        tts_model = get_model(model_name)

        if family == TINY:
            if language not in tts_model.languages:
                return None, "Error: Invalid language selection"
            if voice not in tts_model.available_voices[language]:
                return None, "Error: Invalid voice selection"
            try:
                speed = float(speed)
            except (TypeError, ValueError):
                return None, "Error: Speed must be a number"
            if not np.isfinite(speed):
                return None, "Error: Speed must be a number"
            speed = min(max(speed, MIN_SPEED), MAX_SPEED)
            audio = tts_model.generate(text, voice=voice, language=language, speed=speed)
            source = f"{voice}, {language}"
        else:
            if preset not in PRESETS:
                return None, "Error: Invalid preset selection"
            if reference:
                # Cloning: the recording replaces the built-in speaker.
                kwargs = {"reference": reference}
                if isinstance(reference_text, str) and reference_text.strip():
                    kwargs["reference_text"] = reference_text.strip()
                source = "cloned voice"
            else:
                if voice not in tts_model.available_voices:
                    return None, "Error: Invalid voice selection"
                kwargs = {"voice": voice}
                source = voice
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

        return (tts_model.sample_rate, pcm), f"Audio generated successfully ({source})!"
    except Exception as e:
        return None, f"Error generating audio: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="KittenTTS 😻", delete_cache=CACHE_SWEEP) as demo:
    gr.Markdown("# KittenTTS 😻")
    gr.Markdown(
        "Kitten TTS 2 — 1.7B text-to-speech with voice cloning and expression control, "
        "or the tiny Kitten TTS 2 Mini (82M, 16 languages), Nano (17M, 8 languages) and Pico (7M, 8 languages), fast on CPU. "
        "Kitten TTS 2 weights are under the "
        "[Stellon Labs Community License](https://huggingface.co/KittenML/kitten-tts-2/blob/main/LICENSE.md) "
        "(Powered by Stellon Labs); Mini, Nano and Pico are Apache 2.0."
    )

    default_is_tiny = MODELS[DEFAULT_MODEL][2] == TINY

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to synthesize",
                placeholder="Enter text here...",
                lines=3,
                value="This high quality TTS model works without a GPU",
                info="Kitten TTS 2 supports [emotion] tags, <laugh>-style events and (((emphasis)))",
            )

            model_dropdown = gr.Dropdown(
                label="Model",
                choices=list(MODELS.keys()),
                value=DEFAULT_MODEL,
                info="Mini, Nano and Pico are much faster and smaller; the 1.7B model adds cloning and expression",
            )

            language_dropdown = gr.Dropdown(
                label="Language",
                choices=[DEFAULT_LANGUAGE],
                value=DEFAULT_LANGUAGE,
                visible=default_is_tiny,
            )

            voice_dropdown = gr.Dropdown(
                label="Voice",
                choices=DEFAULT_VOICES,
                value=DEFAULT_VOICE,
                info="Built-in voice; ignored when a reference clip is given",
            )

            speed_slider = gr.Slider(
                label="Speed",
                minimum=MIN_SPEED,
                maximum=MAX_SPEED,
                value=1.0,
                step=0.1,
                visible=default_is_tiny,
            )

            preset_radio = gr.Radio(
                label="Preset",
                choices=PRESETS,
                value="stable",
                info="Trade stability against expressiveness",
                visible=not default_is_tiny,
            )

            with gr.Accordion("Voice cloning", open=False, visible=not default_is_tiny) as cloning:
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
            ["Hello world! This is Kitten TTS 2 speaking.", "stable"],
            ["The quick brown fox jumps over the lazy dog.", "stable"],
            ["[joyful] We actually won the grant <laugh> I can (((hardly))) believe it!", "expressive"],
            ["Welcome to the future of efficient speech synthesis!", "stable"],
        ],
        inputs=[text_input, preset_radio],
    )

    model_outputs = [voice_dropdown, language_dropdown, speed_slider, preset_radio, cloning]
    demo.load(fn=on_model_change, inputs=model_dropdown, outputs=model_outputs)
    model_dropdown.change(fn=on_model_change, inputs=model_dropdown, outputs=model_outputs)
    language_dropdown.change(
        fn=on_language_change,
        inputs=[model_dropdown, language_dropdown],
        outputs=voice_dropdown,
    )

    generate_btn.click(
        fn=generate_speech,
        inputs=[
            text_input,
            voice_dropdown,
            language_dropdown,
            speed_slider,
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
        get_model(DEFAULT_MODEL)
    except Exception as e:
        print(f"Warning: could not preload the default model: {e}")

    demo.queue().launch(
        server_name=args.host,
        server_port=args.port,
        share=False,
        inbrowser=False,
    )
