# api/synthesize.py

from python.helpers.api import ApiHandler, Request, Response

from python.helpers import settings, kokoro_tts, coqui_tts

class Synthesize(ApiHandler):
    async def process(self, input: dict, request: Request) -> dict | Response:
        text = input.get("text", "")
        ctxid = input.get("ctxid", "")
        
        context = self.get_context(ctxid)
        
        # Get TTS settings
        set = settings.get_settings()
        tts_provider = set.get("tts_provider", "kokoro")
        
        try:
            if tts_provider == "coqui":
                # Use Coqui TTS
                if not await coqui_tts.is_downloaded():
                    context.log.log(type="info", content="Coqui TTS model is currently being initialized, please wait...")
                
                # Configure Coqui with settings
                if set.get("tts_coqui_voice_sample"):
                    coqui_tts.set_voice_clone(set["tts_coqui_voice_sample"])
                if set.get("tts_coqui_model"):
                    coqui_tts.set_voice_model(set["tts_coqui_model"])
                
                audio = await coqui_tts.synthesize_sentences([text])
                return {"audio": audio, "success": True}
            else:
                # Use Kokoro TTS (default)
                if not await kokoro_tts.is_downloaded():
                    context.log.log(type="info", content="Kokoro TTS model is currently being initialized, please wait...")
                
                audio = await kokoro_tts.synthesize_sentences([text])
                return {"audio": audio, "success": True}
                
        except Exception as e:
            return {"error": str(e), "success": False}
    
    # def _clean_text(self, text: str) -> str:
    #     """Clean text by removing markdown, tables, code blocks, and other formatting"""
    #     # Remove code blocks
    #     text = re.sub(r'```[\s\S]*?```', '', text)
    #     text = re.sub(r'`[^`]*`', '', text)
        
    #     # Remove markdown links
    #     text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        
    #     # Remove markdown formatting
    #     text = re.sub(r'[*_#]+', '', text)
        
    #     # Remove tables (basic cleanup)
    #     text = re.sub(r'\|[^\n]*\|', '', text)
        
    #     # Remove extra whitespace and newlines
    #     text = re.sub(r'\n+', ' ', text)
    #     text = re.sub(r'\s+', ' ', text)
        
    #     # Remove URLs
    #     text = re.sub(r'https?://[^\s]+', '', text)
        
    #     # Remove email addresses
    #     text = re.sub(r'\S+@\S+', '', text)
        
    #     return text.strip()
    
    # def _chunk_text(self, text: str) -> list[str]:
    #     """Split text into manageable chunks for TTS"""
    #     # If text is short enough, return as single chunk
    #     if len(text) <= 300:
    #         return [text]
        
    #     # Split into sentences first
    #     sentences = re.split(r'(?<=[.!?])\s+', text)
        
    #     chunks = []
    #     current_chunk = ""
        
    #     for sentence in sentences:
    #         sentence = sentence.strip()
    #         if not sentence:
    #             continue
                
    #         # If adding this sentence would make chunk too long, start new chunk
    #         if current_chunk and len(current_chunk + " " + sentence) > 300:
    #             chunks.append(current_chunk.strip())
    #             current_chunk = sentence
    #         else:
    #             current_chunk += (" " if current_chunk else "") + sentence
        
    #     # Add the last chunk if it has content
    #     if current_chunk.strip():
    #         chunks.append(current_chunk.strip())
        
    #     return chunks if chunks else [text]