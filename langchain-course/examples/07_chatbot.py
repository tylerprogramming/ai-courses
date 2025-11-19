"""
Topic 7: Building a Chatbot

Combine everything: Memory + Personality + Streaming
This is a production-ready chatbot example.
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()


# ============================================================================
# Complete Chatbot with Memory and Streaming
# ============================================================================

# Define chatbot personality via system prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a friendly and helpful AI assistant.
You are conversational, concise, and remember details from our conversation."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
chain = prompt | model | StrOutputParser()

# Set up memory
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

print("Example: Production Chatbot")
print("=" * 60)

session_id = "demo_session"

# Conversation function
def chat(message: str, stream=False):
    print(f"\nYou: {message}")
    print("Bot: ", end="", flush=True)

    if stream:
        # Stream response
        for chunk in chatbot.stream(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        ):
            print(chunk, end="", flush=True)
        print()
    else:
        # Regular response
        response = chatbot.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        print(response)

# Have a conversation
chat("Hi! My name is Alex.")
chat("I'm learning about LangChain and RAG systems.")
chat("What's my name?")  # Test memory

# Demo streaming
print("\n" + "-" * 60)
print("Streaming example:")
print("-" * 60)
chat("Tell me a short story about AI in one paragraph.", stream=True)

print("\n\n✓ Chatbot = Memory + Personality + Streaming")
print("✓ For tool access, combine with agents (05_agents.py)")
print("✓ Next: 08_document_loaders.py for RAG!")
