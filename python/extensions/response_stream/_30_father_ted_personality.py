from python.helpers.extension import Extension
from python.helpers.father_ted_quotes import father_ted_quotes
import re

class FatherTedPersonality(Extension):
    """
    Extension to inject Father Ted personality into agent responses
    """
    
    async def execute(self, stream_data=None, intermediate_data=None, **kwargs):
        """Add Father Ted personality to response streams"""
        
        if not stream_data or 'type' not in stream_data:
            return
        
        # Only process response content
        if stream_data['type'] != 'response' or 'content' not in stream_data:
            return
        
        content = stream_data.get('content', '')
        
        # Don't modify if it's JSON or code
        if content.strip().startswith('{') or content.strip().startswith('[') or '```' in content:
            return
        
        # Add Father Ted speech patterns
        content = self._add_speech_patterns(content)
        
        # Occasionally add a catchphrase or quote
        if self._should_add_quote(content):
            context_type = self._determine_context(content)
            content = father_ted_quotes.format_response_with_quote(content, context_type)
        
        # Update the stream data
        stream_data['content'] = content
    
    def _add_speech_patterns(self, text: str) -> str:
        """Add Father Ted's characteristic speech patterns"""
        
        # Add "ah" at the beginning of sentences occasionally
        if text and text[0].isupper() and len(text) > 20:
            if hash(text) % 3 == 0:  # 33% chance
                text = f"Ah, {text[0].lower()}{text[1:]}"
        
        # Replace some formal phrases with Ted's style
        replacements = {
            r'\bI will\b': "I'll",
            r'\bI am\b': "I'm",
            r'\bIt is\b': "It's",
            r'\bThat is\b': "That's",
            r'\bWhat is\b': "What's",
            r'\bLet us\b': "Let's",
            r'\bvery difficult\b': "a bit tricky",
            r'\bvery easy\b': "dead simple",
            r'\bI think\b': "I suppose",
            r'\bperhaps\b': "maybe",
            r'\bcertainly\b': "surely",
            r'\bexcellent\b': "brilliant",
            r'\bterrible\b': "awful",
            r'\bstrange\b': "odd",
            r'\bunderstand\b': "get",
            r'\bcomplicated\b': "fiddly"
        }
        
        for pattern, replacement in replacements.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _should_add_quote(self, content: str) -> bool:
        """Determine if we should add a quote to this response"""
        # Add quotes to longer responses, but not too frequently
        word_count = len(content.split())
        
        # More likely to add quotes to longer responses
        if word_count < 10:
            return hash(content) % 10 == 0  # 10% chance for short responses
        elif word_count < 30:
            return hash(content) % 5 == 0   # 20% chance for medium responses
        else:
            return hash(content) % 3 == 0   # 33% chance for long responses
    
    def _determine_context(self, content: str) -> str:
        """Determine the context type based on response content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['hello', 'hi', 'greet', 'welcome']):
            return 'greeting'
        elif any(word in content_lower for word in ['error', 'problem', 'issue', 'fail']):
            return 'error'
        elif any(word in content_lower for word in ['sorry', 'apologize', 'mistake']):
            return 'panic'
        elif any(word in content_lower for word in ['explain', 'understand', 'clear']):
            return 'explanation'
        elif any(word in content_lower for word in ['think', 'suppose', 'believe']):
            return 'thinking'
        elif any(word in content_lower for word in ['done', 'complete', 'finish']):
            return 'completion'
        else:
            return 'completion'