from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3:1b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response.message.content)
