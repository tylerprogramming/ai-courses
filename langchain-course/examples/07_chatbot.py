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

# Disable LangSmith tracking to avoid warnings
os.environ["LANGCHAIN_TRACING_V2"] = "false"

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

print("Interactive Chatbot with Memory & Streaming")
print("=" * 60)
print("Type your messages and chat with the AI.")
print("Type 'quit', 'exit', or 'bye' to end the conversation.\n")

session_id = "interactive_session"

# Interactive chat loop
while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ['quit', 'exit', 'bye']:
        print("\nBot: Goodbye! Have a great day!")
        break

    print("Bot: ", end="", flush=True)

    # Stream the response
    for chunk in chatbot.stream(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}}
    ):
        print(chunk, end="", flush=True)

    print()  # New line after response
