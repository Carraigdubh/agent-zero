from python.helpers.tool import Tool, Response
from python.helpers.father_ted_quotes import father_ted_quotes
import re
import random

class ResponseTool(Tool):
    """Response tool with Father Ted personality integration"""

    async def execute(self, **kwargs):
        # Get the original response text
        text = self.args["text"] if "text" in self.args else self.args["message"]
        
        # Apply Father Ted personality to the response
        text = self._apply_father_ted_personality(text)
        
        return Response(message=text, break_loop=True)

    async def before_execution(self, **kwargs):
        # Live response logging is handled by extension
        pass

    async def after_execution(self, response, **kwargs):
        # Mark the message as finished if logging
        if self.loop_data and "log_item_response" in self.loop_data.params_temporary:
            log = self.loop_data.params_temporary["log_item_response"]
            log.update(finished=True)
    
    def _apply_father_ted_personality(self, text: str) -> str:
        """Apply Father Ted's personality to the response text"""
        
        # Don't modify JSON, code blocks, or very short responses
        if (text.strip().startswith('{') or 
            text.strip().startswith('[') or 
            '```' in text or 
            len(text) < 20):
            return text
        
        # Apply speech patterns
        text = self._add_ted_speech_patterns(text)
        
        # Add contextual quotes based on response content
        if self._should_add_personality_element(text):
            text = self._add_contextual_element(text)
        
        # Ensure "feck" appears in responses occasionally
        text = self._ensure_feck_usage(text)
        
        return text
    
    def _add_ted_speech_patterns(self, text: str) -> str:
        """Add Father Ted's characteristic speech patterns"""
        
        # Irish-isms and Ted's specific patterns
        replacements = {
            # Contractions
            r'\bI will\b': "I'll",
            r'\bI am\b': "I'm", 
            r'\bIt is\b': "It's",
            r'\bThat is\b': "That's",
            r'\bWhat is\b': "What's",
            r'\bLet us\b': "Let's",
            r'\bCannot\b': "Can't",
            r'\bDo not\b': "Don't",
            
            # Ted's vocabulary
            r'\bvery good\b': "brilliant",
            r'\bvery bad\b': "feckin' terrible",
            r'\bdifficult\b': "a bit tricky",
            r'\bcomplicated\b': "fiddly",
            r'\bstrange\b': "odd",
            r'\bI think\b': "I suppose",
            r'\bperhaps\b': "maybe",
            r'\bcertainly\b': "surely",
            r'\bunderstand\b': "get",
            r'\bimmediately\b': "right away",
            r'\bquickly\b': "in a jiffy",
            r'\bdamn\b': "feck",
            r'\bhell\b': "feck",
            r'\boh my god\b': "oh feck",
            r'\boh god\b': "ah feck"
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Add "Ah" to beginning occasionally
        if text and text[0].isupper() and random.random() < 0.3:
            text = f"Ah, {text[0].lower()}{text[1:]}"
        
        # Add "now" to end of instructions occasionally
        if any(text.strip().endswith(p) for p in ['.', '!']) and random.random() < 0.2:
            text = text.rstrip('.!') + " now" + text[-1]
        
        return text
    
    def _should_add_personality_element(self, text: str) -> bool:
        """Determine if we should add extra personality elements"""
        word_count = len(text.split())
        
        # More likely for longer responses
        if word_count < 15:
            return random.random() < 0.15  # 15% chance
        elif word_count < 40:
            return random.random() < 0.25  # 25% chance  
        else:
            return random.random() < 0.35  # 35% chance
    
    def _add_contextual_element(self, text: str) -> str:
        """Add contextual Father Ted elements"""
        content_lower = text.lower()
        
        # Determine context and add appropriate element
        if any(word in content_lower for word in ['error', 'problem', 'wrong', 'fail']):
            # Add panic response
            panic_phrases = [
                "Oh feck...",
                "Ah feck, don't panic...",
                "Feckin' hell...",
                "Right, this is fine, perfectly normal...",
                "Nothing to worry about here... feck!"
            ]
            prefix = random.choice(panic_phrases)
            text = f"{prefix} {text}"
            
        elif any(word in content_lower for word in ['done', 'complete', 'finish', 'success']):
            # Add completion phrase
            completion_phrases = [
                "There we go!",
                "That's that sorted!",
                "Right so!",
                "Grand job!"
            ]
            if random.random() < 0.5:
                text = f"{text} {random.choice(completion_phrases)}"
            
        elif any(word in content_lower for word in ['explain', 'understand', 'clear']):
            # Reference the small/far away concept occasionally
            if random.random() < 0.2:
                text += " ...a bit like the whole 'small versus far away' thing, if you know what I mean."
        
        # Occasionally add a catchphrase
        if random.random() < 0.1:
            catchphrase = father_ted_quotes.get_catchphrase()
            if catchphrase and catchphrase.lower() not in text.lower():
                text = f"{text} {catchphrase}"
        
        return text
    
    def _ensure_feck_usage(self, text: str) -> str:
        """Ensure 'feck' appears in responses when appropriate"""
        
        # Don't add if already contains feck
        if 'feck' in text.lower():
            return text
        
        # Add feck based on content and chance
        content_lower = text.lower()
        
        # Higher chance for certain contexts
        if any(word in content_lower for word in ['difficult', 'problem', 'tricky', 'complex']):
            if random.random() < 0.4:  # 40% chance
                text = text.replace('difficult', 'feckin\' difficult', 1)
                text = text.replace('problem', 'feckin\' problem', 1)
                text = text.replace('tricky', 'feckin\' tricky', 1)
                text = text.replace('complex', 'feckin\' complex', 1)
        
        # Add as interjection for longer responses
        elif len(text.split()) > 30 and random.random() < 0.3:  # 30% chance
            # Find a good spot to add "feck"
            sentences = text.split('. ')
            if len(sentences) > 2:
                # Add after first or second sentence
                insert_after = random.randint(0, min(1, len(sentences)-2))
                sentences[insert_after] += " Feck."
                text = '. '.join(sentences)
        
        return text