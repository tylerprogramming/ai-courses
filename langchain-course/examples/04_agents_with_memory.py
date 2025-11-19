"""
Example 4: Agents with Memory

Learn how to:
- Add memory to agents with checkpointers
- Maintain conversation state across interactions
- Use thread_id for separate conversations
- Stream agent responses

Based on: https://docs.langchain.com/oss/python/langchain/quickstart
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()


# ============================================================================
# 1. Define Tools
# ============================================================================

@tool
def get_user_preferences(user_id: str) -> str:
    """Get user preferences from the database.

    Args:
        user_id: The user's ID
    """
    preferences = {
        "user_123": "Prefers email communication, interested in Enterprise plan",
        "user_456": "Prefers phone support, currently on Basic plan"
    }
    return preferences.get(user_id, "No preferences found")


@tool
def save_note(note: str) -> str:
    """Save a note about the conversation.

    Args:
        note: The note to save
    """
    # In real app, this would save to database
    return f"Note saved: {note}"


tools = [get_user_preferences, save_note]

# ============================================================================
# 2. Create Agent with Memory
# ============================================================================

model = init_chat_model("gpt-4o-mini", temperature=0)

system_prompt = """You are a helpful assistant with memory.

You can:
- Remember conversation history
- Look up user preferences
- Save notes about the conversation

Use the conversation history to provide context-aware responses."""

# Create checkpointer for memory
checkpointer = MemorySaver()

# Create agent with checkpointer
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=checkpointer
)

# ============================================================================
# 3. Conversation with Memory
# ============================================================================

# Use thread_id to maintain conversation state
config = {"configurable": {"thread_id": "conversation_1"}}

conversation = [
    "Hi, my name is Alice",
    "What's my name?",
    "I'm interested in your Enterprise plan",
    "What did I just say I was interested in?"
]

for message in conversation:
    print(f"\nUser: {message}")

    result = agent.invoke(
        {"messages": [{"role": "user", "content": message}]},
        config=config
    )

    answer = result['messages'][-1].content
    print(f"Agent: {answer}")


# ============================================================================
# 4. Separate Conversations with Different thread_ids
# ============================================================================

# Thread 1
config_thread1 = {"configurable": {"thread_id": "alice"}}
result1 = agent.invoke(
    {"messages": [{"role": "user", "content": "My favorite color is blue"}]},
    config=config_thread1
)
print("Alice: My favorite color is blue")
print(f"Agent: {result1['messages'][-1].content}\n")

# Thread 2 (separate conversation)
config_thread2 = {"configurable": {"thread_id": "bob"}}
result2 = agent.invoke(
    {"messages": [{"role": "user", "content": "My favorite color is red"}]},
    config=config_thread2
)
print("Bob: My favorite color is red")
print(f"Agent: {result2['messages'][-1].content}\n")

# Back to Thread 1 - memory is preserved
result3 = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my favorite color?"}]},
    config=config_thread1
)
print("Alice: What's my favorite color?")
print(f"Agent: {result3['messages'][-1].content}")
