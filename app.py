import gradio as gr
import soundfile as sf
from kittentts import KittenTTS
import numpy as np
import os
import tempfile

# Initialize KittenTTS model
model = None

def initialize_model():
    global model
    if model is None:
        try:
            model = KittenTTS("KittenML/kitten-tts-nano-0.1")
            print("KittenTTS model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    return model

def generate_speech(text, voice):
    try:
        # Initialize model if not already loaded
        tts_model = initialize_model()
        if tts_model is None:
            return None, "Error: Could not load KittenTTS model"
        
        # Generate audio
        audio = tts_model.generate(text, voice=voice)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        sf.write(temp_file.name, audio, 24000)
        
        return temp_file.name, "Audio generated successfully!"
        
    except Exception as e:
        return None, f"Error generating audio: {str(e)}"

# Available voices
VOICES = [
    'expr-voice-2-m', 'expr-voice-2-f', 
    'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f', 
    'expr-voice-5-m', 'expr-voice-5-f'
]

# Create Gradio interface
with gr.Blocks(title="KittenTTS 😻", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# KittenTTS 😻")
    gr.Markdown("Ultra-lightweight text-to-speech with just 15M parameters!")
    
    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Text to synthesize",
                placeholder="Enter text here...",
                lines=3,
                value="This high quality TTS model works without a GPU"
            )
            
            voice_dropdown = gr.Dropdown(
                label="Voice",
                choices=VOICES,
                value="expr-voice-2-f",
                info="Choose from available voice options"
            )
            
            generate_btn = gr.Button("Generate Speech 🎵", variant="primary")
            
        with gr.Column():
            audio_output = gr.Audio(label="Generated Audio")
            status_text = gr.Textbox(label="Status", interactive=False)
    
    # Examples
    gr.Examples(
        examples=[
            ["Hello world! This is KittenTTS speaking.", "expr-voice-2-f"],
            ["The quick brown fox jumps over the lazy dog.", "expr-voice-3-m"],
            ["KittenTTS is an ultra-lightweight text-to-speech model.", "expr-voice-4-f"],
            ["Welcome to the future of efficient speech synthesis!", "expr-voice-5-m"]
        ],
        inputs=[text_input, voice_dropdown],
    )
    
    # Event handlers
    generate_btn.click(
        fn=generate_speech,
        inputs=[text_input, voice_dropdown],
        outputs=[audio_output, status_text]
    )

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="KittenTTS Gradio Interface")
    parser.add_argument("--port", type=int, default=7860, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the server on")
    
    args = parser.parse_args()
    
    # Pre-load the model
    print("Initializing KittenTTS model...")
    initialize_model()
    
    demo.launch(
        server_name=args.host,
        server_port=args.port,
        share=False,
        inbrowser=False
    )