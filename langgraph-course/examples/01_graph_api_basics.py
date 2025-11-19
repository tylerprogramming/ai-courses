"""
Example 1: LangGraph - Graph API Basics

Learn how to:
- Define state with TypedDict and Annotated
- Create nodes and edges
- Use conditional edges
- Build and compile graphs

Based on: https://docs.langchain.com/oss/python/langgraph/quickstart (Graph API)
"""

from typing_extensions import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage


# ============================================================================
# 1. Define State
# ============================================================================

print("1. Defining State")
print("=" * 70)

class MessagesState(TypedDict):
    """State that persists throughout execution"""
    messages: Annotated[list[AnyMessage], operator.add]  # Appends messages
    llm_calls: int  # Regular field (replaces on update)


print("✓ State defined with Annotated for message accumulation\n")


# ============================================================================
# 2. Define Tools
# ============================================================================

print("2. Defining Tools")
print("=" * 70)

@tool
def add(a: int, b: int) -> int:
    """Adds `a` and `b`."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies `a` and `b`."""
    return a * b

tools = [add, multiply]

print(f"✓ Created {len(tools)} tools\n")


# ============================================================================
# 3. Initialize Model with Tools
# ============================================================================

print("3. Initializing Model")
print("=" * 70)

model = init_chat_model("gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

print("✓ Model bound with tools\n")


# ============================================================================
# 4. Define Nodes
# ============================================================================

print("4. Defining Nodes")
print("=" * 70)

def llm_call(state: MessagesState):
    """Node that calls the LLM"""
    print("  → Calling LLM...")
    system_message = SystemMessage(content="You are a helpful assistant with math tools.")
    response = model_with_tools.invoke([system_message] + state["messages"])
    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


def tool_node(state: MessagesState):
    """Node that executes tool calls"""
    print("  → Executing tools...")
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls

    tool_messages = []
    for tool_call in tool_calls:
        # Find and execute the tool
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        for t in tools:
            if t.name == tool_name:
                result = t.invoke(tool_args)
                tool_messages.append(ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                ))
                print(f"     Tool: {tool_name}({tool_args}) = {result}")
                break

    return {"messages": tool_messages}


print("✓ Defined llm_call and tool_node\n")


# ============================================================================
# 5. Define Conditional Edge Function
# ============================================================================

print("5. Defining Router")
print("=" * 70)

def should_continue(state: MessagesState):
    """Determine if we should continue to tools or end"""
    last_message = state["messages"][-1]

    # If there are tool calls, continue to tool_node
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        print("  → Routing to: tool_node")
        return "tool_node"

    # Otherwise, end
    print("  → Routing to: END")
    return END


print("✓ Defined should_continue router\n")


# ============================================================================
# 6. Build the Graph
# ============================================================================

print("6. Building Graph")
print("=" * 70)

# Initialize the graph
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges
agent_builder.add_edge(START, "llm_call")  # Start with LLM

# Conditional edge from llm_call
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)

# After tools, go back to LLM
agent_builder.add_edge("tool_node", "llm_call")

# Compile the graph
agent = agent_builder.compile()

print("✓ Graph compiled: START → llm_call → [tool_node OR END]\n")


# ============================================================================
# 7. Run the Agent
# ============================================================================

print("7. Running Agent")
print("=" * 70)

messages = [HumanMessage(content="What is 15 + 23?")]

print(f"\nUser: {messages[0].content}")
print("\nExecution flow:")

result = agent.invoke({"messages": messages, "llm_calls": 0})

print(f"\nFinal Answer: {result['messages'][-1].content}")
print(f"Total LLM calls: {result['llm_calls']}")
print(f"Total messages in state: {len(result['messages'])}")


# ============================================================================
# 8. Complex Query with Multiple Tools
# ============================================================================

print("\n" + "=" * 70)
print("8. Complex Query")
print("=" * 70)

messages = [HumanMessage(content="What is (5 + 3) multiplied by 2?")]

print(f"\nUser: {messages[0].content}")
print("\nExecution flow:")

result = agent.invoke({"messages": messages, "llm_calls": 0})

print(f"\nFinal Answer: {result['messages'][-1].content}")
print(f"Total LLM calls: {result['llm_calls']}")


# ============================================================================
# Key Takeaways
# ============================================================================

print("\n" + "=" * 70)
print("KEY TAKEAWAYS:")
print("✓ State uses TypedDict with Annotated for reducers")
print("✓ operator.add appends to lists instead of replacing")
print("✓ Nodes are functions that take state and return updates")
print("✓ Conditional edges route based on state")
print("✓ Graph pattern: START → llm_call → [tools OR END]")
print("✓ Edges can loop back (tool_node → llm_call)")
print("✓ compile() creates the executable graph")
