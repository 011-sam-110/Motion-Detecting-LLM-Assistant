from ollama import chat, ChatResponse

messages = []
def sendMessage(role, message):
    global messages

    messages.append({
        'role': f'{role}',
        'content': f'{message}'
    })

    response: ChatResponse = chat(model='sentryAssistant', messages=messages)
    
    messages.append({
        'role': f'assistant',
        'content': f'{response.message.content}'
    })
    print(response.message.content)
    return response.message.content

print(sendMessage('user', "hello nugget"))
