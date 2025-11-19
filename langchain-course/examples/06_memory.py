"""
Topic 6: Memory Systems

Memory allows LLMs to remember previous interactions,
creating true conversational capabilities.

Modern approach: RunnableWithMessageHistory + MessagesPlaceholder
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

# Create prompt with message history placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Remember details from the conversation."),
    MessagesPlaceholder(variable_name="chat_history"),  # History goes here
    ("human", "{input}")
])

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
chain = prompt | model | StrOutputParser()

# Set up session-based memory storage
store = {}  # In production, use Redis/PostgreSQL

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Wrap chain with message history
chatbot = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

print("Example: Conversation with Memory")
print("=" * 60)

session_id = "user_123"

# Turn 1
print("\nUser: My favorite color is blue.")
response1 = chatbot.invoke(
    {"input": "My favorite color is blue."},
    config={"configurable": {"session_id": session_id}}
)
print(f"AI: {response1}")

# Turn 2
print("\nUser: I'm learning LangChain.")
response2 = chatbot.invoke(
    {"input": "I'm learning LangChain."},
    config={"configurable": {"session_id": session_id}}
)
print(f"AI: {response2}")

# Turn 3 - Test memory
print("\nUser: What's my favorite color?")
response3 = chatbot.invoke(
    {"input": "What's my favorite color?"},
    config={"configurable": {"session_id": session_id}}
)
print(f"AI: {response3}")
