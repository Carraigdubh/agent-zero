import asyncio
from python.helpers import runtime, whisper, settings
from python.helpers.print_style import PrintStyle
from python.helpers import kokoro_tts, coqui_tts
import models


async def preload():
    try:
        set = settings.get_default_settings()

        # preload whisper model
        async def preload_whisper():
            try:
                return await whisper.preload(set["stt_model_size"])
            except Exception as e:
                PrintStyle().error(f"Error in preload_whisper: {e}")

        # preload embedding model
        async def preload_embedding():
            if set["embed_model_provider"] == models.ModelProvider.HUGGINGFACE.name:
                try:
                    # Use the new LiteLLM-based model system
                    emb_mod = models.get_embedding_model(
                        models.ModelProvider.HUGGINGFACE, set["embed_model_name"]
                    )
                    emb_txt = await emb_mod.aembed_query("test")
                    return emb_txt
                except Exception as e:
                    PrintStyle().error(f"Error in preload_embedding: {e}")

        # preload TTS model based on provider
        async def preload_tts():
            tts_provider = set.get("tts_provider", "kokoro")
            
            if tts_provider == "coqui":
                try:
                    PrintStyle().print("Preloading Coqui TTS...")
                    # Configure Coqui with settings
                    if set.get("tts_coqui_voice_sample"):
                        coqui_tts.set_voice_clone(set["tts_coqui_voice_sample"])
                    if set.get("tts_coqui_model"):
                        coqui_tts.set_voice_model(set["tts_coqui_model"])
                    return await coqui_tts.preload()
                except Exception as e:
                    PrintStyle().error(f"Error in preload_coqui: {e}")
            elif set["tts_kokoro"]:
                try:
                    return await kokoro_tts.preload()
                except Exception as e:
                    PrintStyle().error(f"Error in preload_kokoro: {e}")

        # async tasks to preload
        tasks = [
            preload_embedding(),
            preload_whisper(),
            preload_tts()
        ]

        await asyncio.gather(*tasks, return_exceptions=True)
        PrintStyle().print("Preload completed")
    except Exception as e:
        PrintStyle().error(f"Error in preload: {e}")


# preload transcription model
if __name__ == "__main__":
    PrintStyle().print("Running preload...")
    runtime.initialize()
    asyncio.run(preload())
