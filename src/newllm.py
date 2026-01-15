import os
import openai

# Set your API key (or use environment variable OPENAI_API_KEY)
openai.api_key = ""

# Persistent conversation
conversation = [
    {
        "role": "system",
        "content": """
Desrcribe your speech in *'s before speaking.
"""
    }
]

def sendMessage(message: str) -> str:
    conversation.append({"role": "user", "content": message})
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation,
        temperature=0.8,
        max_tokens=150
    )
    
    # Access content as an attribute, not a dict
    assistant_message = response.choices[0].message.content
    
    conversation.append({"role": "assistant", "content": assistant_message})
    
    return assistant_message
