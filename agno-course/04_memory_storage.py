"""
Agno Framework - Lesson 4: Memory and Storage

This lesson covers:
- Session memory (in-memory conversation history)
- Persistent storage with SQLite
- User-specific memory for personalization
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from dotenv import load_dotenv
import os

load_dotenv()

# Example 2: User-Specific Memory
user_db = SqliteDb(
    session_table="user_sessions",
    db_file="user_memory.db"
)

personal_assistant = Agent(
    name="PersonalAssistant",
    model=OpenAIChat(id="gpt-4.1"),
    db=user_db,
    description="A personal assistant with user-specific memory",
    instructions=[
        "You are a personal assistant.",
        "Remember each user's preferences and history.",
        "Personalize responses based on user context."
    ],
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    session_id="alice",
)

print("[User-Specific Memory]")
# response_alice = personal_assistant.run(
#     "Hi! I'm Alice. I love hiking and photography.",
#     user_id="alice"
# )

# print(f"Agent: {response_alice.content}\n")

response_alice_2 = personal_assistant.run("Based on my hobbies, what should I do this weekend?", user_id="alice", add_history_to_context=True)
print(f"Agent: {response_alice_2.content}\n")
