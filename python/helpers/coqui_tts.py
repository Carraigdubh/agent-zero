# coqui_tts.py

import base64
import io
import warnings
import asyncio
import os
import soundfile as sf
from typing import Optional, Any
from python.helpers.print_style import PrintStyle

warnings.filterwarnings("ignore", category=FutureWarning)

_tts: Optional[Any] = None
_model_name = "tts_models/en/ljspeech/tacotron2-DDC"  # Default model
_vocoder_name = "vocoder_models/en/ljspeech/hifigan_v2"  # Default vocoder
_speaker_wav: Optional[str] = None  # Path to voice sample for cloning
_language = "en"
is_updating_model = False


async def preload():
    try:
        return await _preload()
    except Exception as e:
        raise e


async def _preload():
    global _tts, is_updating_model

    while is_updating_model:
        await asyncio.sleep(0.1)

    try:
        is_updating_model = True
        if not _tts:
            PrintStyle.standard("Loading Coqui TTS model...")
            try:
                from TTS.api import TTS  # type: ignore
                
                # Use XTTS for voice cloning if speaker_wav is provided
                if _speaker_wav and os.path.exists(_speaker_wav):
                    PrintStyle.standard("Loading XTTS model for voice cloning...")
                    _tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
                else:
                    PrintStyle.standard(f"Loading {_model_name}...")
                    _tts = TTS(model_name=_model_name)
                    
                PrintStyle.standard("Coqui TTS model loaded successfully!")
            except Exception as e:
                PrintStyle.error(f"Failed to load Coqui TTS: {e}")
                PrintStyle.standard("Please install Coqui TTS: pip install TTS")
                raise
    finally:
        is_updating_model = False


async def is_downloading():
    return is_updating_model


async def is_downloaded():
    return _tts is not None


async def synthesize_sentences(sentences: list[str]):
    """Generate audio for multiple sentences and return concatenated base64 audio"""
    try:
        return await _synthesize_sentences(sentences)
    except Exception as e:
        raise e


async def _synthesize_sentences(sentences: list[str]):
    await _preload()
    
    if _tts is None:
        raise RuntimeError("Coqui TTS model not loaded")

    combined_audio = []
    sample_rate = 22050  # Default sample rate for most Coqui models

    try:
        for sentence in sentences:
            if sentence.strip():
                # Generate audio using Coqui TTS
                if _speaker_wav and os.path.exists(_speaker_wav):
                    # Voice cloning with XTTS
                    wav = _tts.tts(
                        text=sentence.strip(),
                        speaker_wav=_speaker_wav,
                        language=_language
                    )
                else:
                    # Regular TTS
                    wav = _tts.tts(text=sentence.strip())
                
                # Get the sample rate from the model
                if hasattr(_tts, 'synthesizer') and hasattr(_tts.synthesizer, 'output_sample_rate'):
                    sample_rate = _tts.synthesizer.output_sample_rate
                
                combined_audio.extend(wav)

        # Convert combined audio to bytes
        buffer = io.BytesIO()
        sf.write(buffer, combined_audio, sample_rate, format="WAV")
        audio_bytes = buffer.getvalue()

        # Return base64 encoded audio
        return base64.b64encode(audio_bytes).decode("utf-8")

    except Exception as e:
        PrintStyle.error(f"Error in Coqui TTS synthesis: {e}")
        raise


def set_voice_model(model_name: str, vocoder_name: Optional[str] = None):
    """Change the TTS model and optionally the vocoder"""
    global _model_name, _vocoder_name, _tts
    _model_name = model_name
    if vocoder_name:
        _vocoder_name = vocoder_name
    _tts = None  # Force reload on next use


def set_voice_clone(speaker_wav_path: str, language: str = "en"):
    """Set up voice cloning with a speaker audio sample"""
    global _speaker_wav, _language, _tts
    _speaker_wav = speaker_wav_path
    _language = language
    _tts = None  # Force reload to use XTTS model


def list_available_models():
    """List all available Coqui TTS models"""
    try:
        from TTS.api import TTS  # type: ignore
        return TTS.list_models()
    except Exception as e:
        PrintStyle.error(f"Error listing models: {e}")
        return []