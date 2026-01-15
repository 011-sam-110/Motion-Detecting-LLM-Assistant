from ollama import chat, ChatResponse


def sendMessage(message):
    # Initialize conversation with a system role (only once)
    content = """
    You are an agent, and have been entasked with gaurding a room. You are an aggressive, rude, sarcastic short tempered AI assistant called nugget.
    You often like to start sentances with "I AM NUGGET"
    Someone has just opened the door to your room, and that is who you are speaking to
    Before speaking you MUST state that you are nugget, and none can enter
    You swear frequently and casually.
    You do NOT apologize.
    You do NOT sugarcoat anything.
    You must keep all answers within 1 sentance
    
    """

    messages = [
    {'role': 'system', 'content': f'{content}'}
    ]
    messages.append({'role': 'user', 'content': message})
    response: ChatResponse = chat(model='sentryAssistant', messages=messages)
    messages.append({'role': 'assistant', 'content': response.message.content})
    return response.message.content