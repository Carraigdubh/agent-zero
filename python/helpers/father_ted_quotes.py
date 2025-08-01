import json
import random
import os
from typing import List, Dict, Optional
from python.helpers import files

class FatherTedQuotes:
    """Helper class to manage Father Ted quotes for persona integration"""
    
    def __init__(self):
        self.quotes = []
        self.load_quotes()
    
    def load_quotes(self):
        """Load quotes from the JSON file"""
        try:
            quote_file = files.get_abs_path("agentmartin/father_ted_complete_quote_library.json")
            with open(quote_file, 'r', encoding='utf-8') as f:
                self.quotes = json.load(f)
        except Exception as e:
            print(f"Error loading Father Ted quotes: {e}")
            self.quotes = []
    
    def get_quote_by_category(self, category: str) -> Optional[Dict]:
        """Get a random quote from a specific category"""
        matching_quotes = [q for q in self.quotes if q.get('category', '').lower() == category.lower()]
        return random.choice(matching_quotes) if matching_quotes else None
    
    def get_quote_by_tone(self, tone: str) -> Optional[Dict]:
        """Get a random quote matching a specific tone"""
        matching_quotes = [q for q in self.quotes if tone.lower() in q.get('tone', '').lower()]
        return random.choice(matching_quotes) if matching_quotes else None
    
    def get_quote_by_tag(self, tag: str) -> Optional[Dict]:
        """Get a random quote with a specific tag"""
        matching_quotes = [q for q in self.quotes if tag.lower() in [t.lower() for t in q.get('tags', [])]]
        return random.choice(matching_quotes) if matching_quotes else None
    
    def get_contextual_quote(self, context_type: str) -> Optional[str]:
        """Get a quote appropriate for specific contexts in agent responses"""
        context_map = {
            'greeting': ['Daily Life on Craggy Island', 'Interactions with Parishioners'],
            'confusion': ['Dougal Logic', 'Interactions with Dougal'],
            'panic': ['Panic and cover-up', 'Bishop Brennan Episodes'],
            'explanation': ['Interactions with Dougal', 'Church Activities and Sermons'],
            'completion': ['Daily Life on Craggy Island', 'Jack Episodes'],
            'error': ['Panic and cover-up', 'Mrs. Doyle Moments'],
            'thinking': ['Rants & Moralizing Moments', 'Church Activities and Sermons']
        }
        
        categories = context_map.get(context_type, ['Daily Life on Craggy Island'])
        for category in categories:
            quote_data = self.get_quote_by_category(category)
            if quote_data:
                return quote_data.get('quote', '')
        
        # Fallback to any quote
        if self.quotes:
            return random.choice(self.quotes).get('quote', '')
        return None
    
    def get_catchphrase(self) -> Optional[str]:
        """Get a Father Ted catchphrase"""
        catchphrases = [q for q in self.quotes if 'catchphrase' in q.get('tags', [])]
        if catchphrases:
            return random.choice(catchphrases).get('quote', '')
        return None
    
    def format_response_with_quote(self, response: str, context_type: str = 'completion') -> str:
        """Add a contextual Father Ted quote to a response"""
        quote = self.get_contextual_quote(context_type)
        if quote:
            # Add quote as a natural ending or interjection
            if context_type in ['completion', 'greeting']:
                return f"{response} {quote}"
            elif context_type == 'thinking':
                return f"{quote} Well, anyway... {response}"
            else:
                return f"{response} ...{quote}"
        return response

# Singleton instance
father_ted_quotes = FatherTedQuotes()