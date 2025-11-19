"""
Example 2: LangGraph - Functional API

Learn how to:
- Use @task and @entrypoint decorators
- Build agents with functional control flow
- Stream agent execution
- Use standard Python loops instead of explicit edges

Based on: https://docs.langchain.com/oss/python/langgraph/quickstart (Functional API)
"""

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.func import entrypoint, task
from langgraph.graph import add_messages


# ============================================================================
# 1. Define Tools
# ============================================================================

print("1. Defining Tools")
print("=" * 70)

@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies `a` and `b`."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divides `a` by `b`."""
    if b == 0:
        return "Error: Division by zero"
    return a / b

tools = [add, multiply, divide]

print(f"✓ Created {len(tools)} tools\n")


# ============================================================================
# 2. Initialize Model with Tools
# ============================================================================

print("2. Initializing Model")
print("=" * 70)

model = init_chat_model("gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

print("✓ Model bound with tools\n")


# ============================================================================
# 3. Define Task (Async Node)
# ============================================================================

print("3. Defining Task")
print("=" * 70)

@task
def call_llm(messages: list[BaseMessage]):
    """Task that calls the LLM with tools"""
    system_message = SystemMessage(content="You are a helpful math assistant.")
    return model_with_tools.invoke([system_message] + messages)


print("✓ Defined call_llm task\n")


# ============================================================================
# 4. Define Agent with @entrypoint (Control Flow)
# ============================================================================

print("4. Defining Agent Entrypoint")
print("=" * 70)

@entrypoint()
def agent(messages: list[BaseMessage]):
    """
    Agent with functional control flow.
    Uses standard Python while loop instead of graph edges.
    """
    # Call LLM
    model_response = call_llm(messages).result()
    messages = add_messages(messages, model_response)

    # Loop while there are tool calls
    while True:
        # Check if we should continue
        if not model_response.tool_calls:
            break

        # Execute tools
        tool_messages = []
        for tool_call in model_response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            # Find and execute the tool
            for t in tools:
                if t.name == tool_name:
                    result = t.invoke(tool_args)
                    tool_messages.append(ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"]
                    ))
                    print(f"  → Executed: {tool_name}({tool_args}) = {result}")
                    break

        # Add tool results to messages
        messages = add_messages(messages, tool_messages)

        # Call LLM again with tool results
        model_response = call_llm(messages).result()
        messages = add_messages(messages, model_response)

    return messages


print("✓ Defined agent with while-loop control flow\n")


# ============================================================================
# 5. Run Agent with Streaming
# ============================================================================

print("5. Running Agent with Streaming")
print("=" * 70)

query = "What is 15 + 23?"
messages = [HumanMessage(content=query)]

print(f"\nUser: {query}")
print("\nAgent execution:")

# Stream the agent's execution
for chunk in agent.stream(messages, stream_mode="updates"):
    print(f"  Update: {chunk}")

# Get final result
result = agent.invoke(messages)
final_message = result[-1]

print(f"\nFinal Answer: {final_message.content}\n")


# ============================================================================
# 6. Complex Multi-step Query
# ============================================================================

print("6. Complex Multi-step Query")
print("=" * 70)

query = "Calculate (12 + 8) * 3, then divide by 5"
messages = [HumanMessage(content=query)]

print(f"\nUser: {query}")
print("\nAgent execution:")

result = agent.invoke(messages)
final_message = result[-1]

print(f"\nFinal Answer: {final_message.content}\n")


# ============================================================================
# 7. Comparison: Graph API vs Functional API
# ============================================================================

print("7. Graph API vs Functional API")
print("=" * 70)

print("""
Graph API (Example 1):
  ✓ Explicit nodes and edges
  ✓ Declarative graph structure
  ✓ Better for complex routing
  ✓ Visual graph representation
  ✓ More control over execution

Functional API (This example):
  ✓ Standard Python control flow (while, if)
  ✓ More concise for simple agents
  ✓ Easier to understand for Python developers
  ✓ Less boilerplate
  ✓ Natural imperative style
""")


# ============================================================================
# Key Takeaways
# ============================================================================

print("=" * 70)
print("KEY TAKEAWAYS:")
print("✓ @task decorator defines async nodes")
print("✓ @entrypoint() defines the agent entry point")
print("✓ Use standard Python loops (while) for control flow")
print("✓ add_messages() helper appends to message list")
print("✓ .result() waits for task completion")
print("✓ stream() with stream_mode='updates' shows execution steps")
print("✓ Functional API is more concise than Graph API")
print("✓ Choose Graph API for complex routing, Functional for simple agents")
