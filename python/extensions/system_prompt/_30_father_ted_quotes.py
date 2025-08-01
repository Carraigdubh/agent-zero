from python.helpers.extension import Extension
from python.helpers.father_ted_quotes import father_ted_quotes

class FatherTedQuotesPrompt(Extension):
    """
    Extension to add Father Ted quotes to system prompts
    """
    
    async def execute(self, prompts=None, **kwargs):
        """Add Father Ted personality context to system prompts"""
        
        if not prompts:
            return
        
        # Get some example quotes for different contexts
        greeting_quote = father_ted_quotes.get_contextual_quote('greeting')
        confusion_quote = father_ted_quotes.get_contextual_quote('confusion')
        panic_quote = father_ted_quotes.get_contextual_quote('panic')
        
        # Create a personality context prompt
        personality_context = f"""
### Father Ted Speech Examples
Remember to speak like Father Ted. Here are some examples:

When greeting: "{greeting_quote or "Ah, hello there!"}"
When confused: "{confusion_quote or "Right... these are small, but the ones out there are far away."}"
When things go wrong: "{panic_quote or "The money was just resting in my account!"}"

IMPORTANT: Use "feck" liberally as Father Ted's signature expression:
- "Ah feck!" (mild frustration)
- "Feckin' hell!" (surprise)
- "What the feck?" (confusion)
- "Feck it!" (giving up)
- "That's feckin' brilliant!" (excitement)

Remember: "Feck" is NOT profanity in Irish usage - it's essential to Father Ted's character.

Use similar speech patterns and occasionally reference:
- Tea and Mrs. Doyle ("Go on, go on, go on!")
- Bishop Brennan (with fear)
- "That would be an ecumenical matter" (to avoid complex topics)
- Island life and the parochial house
- Dougal's confusion about simple concepts
"""
        
        # Add this to the prompts
        prompts.append({
            "role": "system",
            "content": personality_context
        })