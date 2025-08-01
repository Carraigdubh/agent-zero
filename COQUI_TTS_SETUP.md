# Coqui TTS Setup Guide for Agent Zero

This guide explains how to set up Coqui TTS with voice cloning capabilities in your Father Ted Agent Zero instance.

## Installation

1. **Install Coqui TTS**:
   ```bash
   pip install TTS>=0.22.0
   ```

2. **Verify Installation**:
   ```bash
   python -c "from TTS.api import TTS; print('Coqui TTS installed successfully!')"
   ```

## Basic Configuration

1. **Access Settings**: Go to http://localhost:50001/settings
2. **Navigate to Speech Section**
3. **Configure TTS Provider**:
   - Set "TTS Provider" to "Coqui TTS"
   - Set "Coqui TTS Model" to one of:
     - `tts_models/en/ljspeech/tacotron2-DDC` (fast, good quality)
     - `tts_models/en/vctk/vits` (multiple speakers)
     - `tts_models/multilingual/multi-dataset/xtts_v2` (voice cloning)

## Voice Cloning Setup

### Step 1: Prepare Voice Sample
Create a high-quality audio sample of the voice you want to clone:
- **Format**: WAV or MP3
- **Duration**: 10-30 seconds minimum
- **Quality**: Clear, no background noise
- **Content**: Natural speech with varied intonation

For Father Ted character voice, record something like:
> "Hello there! I'm Father Ted Crilly, and I'm delighted to help you with whatever you need. Down with this sort of thing!"

### Step 2: Configure Voice Cloning
1. Save your audio file to `/root/father_ted_voice.wav`
2. In settings, set:
   - **TTS Provider**: "Coqui TTS"
   - **Coqui TTS Model**: `tts_models/multilingual/multi-dataset/xtts_v2`
   - **Coqui Voice Sample Path**: `/root/father_ted_voice.wav`

### Step 3: Test the Setup
1. Restart the Agent Zero server
2. Ask Father Ted a question in the web UI
3. Click the speaker icon to hear the cloned voice

## Available Models

### English Models:
- `tts_models/en/ljspeech/tacotron2-DDC` - Single speaker, fast
- `tts_models/en/ljspeech/glow-tts` - Single speaker, natural
- `tts_models/en/vctk/vits` - Multi-speaker English
- `tts_models/en/jenny/jenny` - Jenny voice model

### Multi-language with Voice Cloning:
- `tts_models/multilingual/multi-dataset/xtts_v2` - 17 languages, voice cloning

## Performance Tips

1. **GPU Acceleration**: Install PyTorch with CUDA support for faster generation
2. **Model Caching**: First run downloads models automatically (~1GB)
3. **Memory Usage**: XTTS requires ~4GB RAM, lighter models use ~1GB

## Troubleshooting

### Common Issues:

1. **"No module named 'TTS'"**:
   ```bash
   pip install TTS>=0.22.0
   ```

2. **CUDA/GPU errors**:
   - Install CPU-only version: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu`

3. **Voice sample not found**:
   - Check file path in settings
   - Ensure file is accessible by the server

4. **Poor voice cloning quality**:
   - Use longer, clearer audio samples
   - Try different models
   - Ensure sample has varied speech patterns

## Father Ted Voice Tips

For the best Father Ted character voice:
- Record with an Irish accent if possible
- Include characteristic phrases like "Ah go on", "Feck", "That would be an ecumenical matter"
- Use animated, expressive speech patterns
- Keep background completely silent

## Switching Back to Kokoro

To switch back to Kokoro TTS:
1. Go to Settings → Speech
2. Set "TTS Provider" to "Kokoro TTS"
3. Restart the server

## Advanced Usage

### List Available Models:
```python
from TTS.api import TTS
models = TTS.list_models()
for model in models:
    print(model)
```

### Voice Cloning with Custom Language:
Set language in voice sample path field: `/path/to/voice.wav|en`

Available languages: en, es, fr, de, it, pt, pl, tr, ru, nl, cs, ar, zh-cn, ja, hu, ko