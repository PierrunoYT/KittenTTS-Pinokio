# KittenTTS 😻 Pinokio Integration

Ultra-lightweight text-to-speech with just 15 million parameters, designed for lightweight deployment and high-quality voice synthesis. This Pinokio integration provides an easy-to-use web interface for KittenTTS.

## Features

### ✨ KittenTTS Highlights
- **Ultra-lightweight**: Model size less than 25MB
- **CPU-optimized**: Runs without GPU on any device  
- **High-quality voices**: 8 premium voice options available
- **Fast inference**: Optimized for real-time speech synthesis
- **No authentication required**: Works out of the box

### 🎭 Available Voices
- `expr-voice-2-m` / `expr-voice-2-f` - Expressive male/female voices
- `expr-voice-3-m` / `expr-voice-3-f` - Natural male/female voices  
- `expr-voice-4-m` / `expr-voice-4-f` - Clear male/female voices
- `expr-voice-5-m` / `expr-voice-5-f` - Warm male/female voices

### 🖥️ Pinokio Integration Features
- **One-click installation**: Automated setup through Pinokio
- **Web interface**: Clean Gradio-based UI
- **Example prompts**: Pre-loaded examples to get started
- **Real-time generation**: Instant audio playback
- **File download**: Save generated audio as WAV files

## About KittenTTS

KittenTTS is an open-source realistic text-to-speech model that:
- Uses only 15 million parameters (ultra-lightweight)
- Runs efficiently on CPU without requiring GPU
- Provides high-quality voice synthesis
- Works literally everywhere with minimal system requirements
- Currently in developer preview with more features coming

## Installation

### 🚀 Pinokio Installation (Recommended)

1. **Install Pinokio** from [pinokio.computer](https://pinokio.computer)
2. **Clone this repository** in Pinokio or download the files
3. **Click "Install"** - Pinokio will handle everything automatically
4. **Click "Start"** to launch the web interface
5. **Open the web UI** when the interface is ready

That's it! Pinokio handles all dependencies, virtual environments, and model downloads.

### 💻 Manual Installation

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/your-username/KittenTTS-Pinokio.git
cd KittenTTS-Pinokio

# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the interface
python app.py
```

## Usage

### 🎯 Quick Start

1. **Launch the interface** (via Pinokio or manually)
2. **Enter your text** in the text input field
3. **Select a voice** from the dropdown (8 options available)
4. **Click "Generate Speech"** 
5. **Listen to the audio** and download if desired

### 🎭 Voice Selection Guide

- **expr-voice-2-f/m**: Expressive and dynamic voices
- **expr-voice-3-f/m**: Natural, conversational tones  
- **expr-voice-4-f/m**: Clear, professional voices
- **expr-voice-5-f/m**: Warm, friendly voices

### 📝 Example Prompts

Try these examples to get started:
- "Hello world! This is KittenTTS speaking."
- "The quick brown fox jumps over the lazy dog."
- "Welcome to the future of efficient speech synthesis!"
- "KittenTTS is an ultra-lightweight text-to-speech model."

## System Requirements

### ⚡ Minimum Requirements (CPU)
- **CPU**: Any modern processor
- **RAM**: 4GB
- **Storage**: 1GB free space
- **OS**: Windows 10+, macOS 10.15+, or Linux

### 🚀 Recommended (Still CPU!)
- **CPU**: Multi-core processor
- **RAM**: 8GB+
- **Storage**: SSD with 2GB+ free space
- **Network**: For initial model download (~25MB)

**Note**: KittenTTS is designed to run efficiently on CPU - no GPU required!


## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'kittentts'":**
- Ensure the virtual environment is activated
- Run: `pip install -r requirements.txt` to reinstall dependencies

**Model download fails:**
- Check internet connection
- The model downloads automatically on first use (~25MB)
- Ensure sufficient disk space

**Audio generation is slow:**
- This is normal on first run (model loading)
- Subsequent generations are much faster
- Close other applications to free up resources

**Interface appears black:**
- Try refreshing the browser
- Check if Gradio updated the theme
- The interface should use a light theme by default

### Performance Tips

- **First run**: Model download takes ~30 seconds (only 25MB)
- **CPU optimized**: Designed to run efficiently on CPU
- **Memory usage**: Uses minimal RAM compared to large TTS models
- **Generation speed**: Very fast inference after initial model loading
- **Multiple generations**: Subsequent audio generations are near-instant

## Project Structure

```
KittenTTS-Pinokio/
├── app.py                      # Main Gradio web interface
├── requirements.txt            # KittenTTS and dependencies
├── pinokio.js                  # Pinokio configuration
├── install.js                  # Installation script
├── start.js                    # Startup script
├── reset.js                    # Reset script
├── link.js                     # Environment linking
├── update.js                   # Update script
├── torch.js                    # PyTorch installation
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── icon.png                    # Pinokio app icon
└── env/                        # Virtual environment (auto-created)
```

## Configuration

The interface can be customized by modifying `app.py`:

```python
# Available voices (8 total)
VOICES = [
    'expr-voice-2-m', 'expr-voice-2-f', 
    'expr-voice-3-m', 'expr-voice-3-f',
    'expr-voice-4-m', 'expr-voice-4-f', 
    'expr-voice-5-m', 'expr-voice-5-f'
]

# Modify server settings
demo.launch(
    share=True,           # Enable public sharing
    server_name="0.0.0.0", # Allow external connections
    server_port=7860      # Change port number
)
```

## Links

- **KittenTTS GitHub**: https://github.com/KittenML/KittenTTS
- **KittenTTS Discord**: [Join the community](https://discord.gg/kittentts)
- **Pinokio**: https://pinokio.computer
- **Gradio**: https://gradio.app

## License

This Pinokio integration is licensed under the [MIT License](LICENSE). 

**Note**: KittenTTS model has its own separate license terms. Please refer to the [KittenTTS repository](https://github.com/KittenML/KittenTTS) for model licensing information.

## Credits

- **KittenTTS**: Developed by KittenML
- **Model**: Ultra-lightweight 15M parameter TTS
- **Integration**: Pinokio-compatible setup
- **Interface**: Gradio web UI

## Support

- **KittenTTS issues**: Visit the [KittenTTS repository](https://github.com/KittenML/KittenTTS)
- **Pinokio issues**: Check [Pinokio documentation](https://docs.pinokio.computer)
- **Integration issues**: Open an issue in this repository