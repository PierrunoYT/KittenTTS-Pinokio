import gradio as gr
import soundfile as sf
from kittentts import KittenTTS
import numpy as np
import tempfile

# Available models (ordered by quality/size)
MODELS = {
    "Mini (80M - Best Quality)": "KittenML/kitten-tts-mini-0.8",
    "Micro (40M - Balanced)": "KittenML/kitten-tts-micro-0.8",
    "Nano (15M - Fastest)": "KittenML/kitten-tts-nano-0.8",
    "Nano INT8 (15M - Smallest)": "KittenML/kitten-tts-nano-0.8-int8",
}

# Available voices
VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]

# Model cache
loaded_models = {}

def get_model(model_name):
    model_id = MODELS[model_name]
    if model_id not in loaded_models:
        print(f"Loading model: {model_id}...")
        loaded_models[model_id] = KittenTTS(model_id)
        print(f"Model {model_id} loaded successfully!")
    return loaded_models[model_id]

def generate_speech(text, voice, speed, model_name):
    try:
        tts_model = get_model(model_name)
        audio = tts_model.generate(text, voice=voice, speed=speed)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(temp_file.name, audio, 24000)

        return temp_file.name, "Audio generated successfully!"
    except Exception as e:
        return None, f"Error generating audio: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="KittenTTS 😻", theme=gr.themes.Default()) as demo:
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
                value="Nano (15M - Fastest)",
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
                minimum=0.5,
                maximum=2.0,
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

    # Pre-load the default model
    print("Initializing KittenTTS model...")
    get_model("Nano (15M - Fastest)")

    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=False,
        inbrowser=False,
    )
