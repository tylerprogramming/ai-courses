"""
Example 2: Tools and Structured Output

Learn how to:
- Create tools with @tool decorator
- Bind tools to models
- Use structured output with Pydantic
- Handle tool calls and responses

Based on: https://docs.langchain.com/oss/python/langchain/models
"""

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from pydantic import BaseModel, Field

load_dotenv()


# ============================================================================
# 1. Define Tools
# ============================================================================

print("1. Creating Tools with @tool Decorator")
print("=" * 70)

@tool
def get_current_weather(location: str) -> str:
    """Get the current weather for a location.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    # In real app, this would call a weather API
    weather_data = {
        "san francisco": "sunny, 72°F",
        "new york": "cloudy, 65°F",
        "london": "rainy, 58°F"
    }
    return weather_data.get(location.lower(), "Unknown location")


@tool
def calculate(operation: str, a: float, b: float) -> float:
    """Perform a mathematical operation.

    Args:
        operation: The operation (add, subtract, multiply, divide)
        a: First number
        b: Second number
    """
    operations = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: Division by zero"
    }
    return operations.get(operation, "Invalid operation")


tools = [get_current_weather, calculate]

print(f"✓ Created {len(tools)} tools")
for t in tools:
    print(f"  - {t.name}: {t.description}\n")


# ============================================================================
# 2. Bind Tools to Model
# ============================================================================

print("2. Binding Tools to Model")
print("=" * 70)

model = init_chat_model("gpt-4o-mini", temperature=0)
model_with_tools = model.bind_tools(tools)

print("✓ Model can now request tool calls\n")


# ============================================================================
# 3. Basic Tool Calling
# ============================================================================

print("3. Basic Tool Calling")
print("=" * 70)

response = model_with_tools.invoke([
    HumanMessage(content="What's the weather in San Francisco?")
])

print(f"Tool calls: {response.tool_calls}\n")

if response.tool_calls:
    tool_call = response.tool_calls[0]
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")

    # Execute the tool
    for t in tools:
        if t.name == tool_call['name']:
            result = t.invoke(tool_call['args'])
            print(f"Result: {result}\n")
            break

# ============================================================================
# 4. Structured Output with Pydantic
# ============================================================================

print("4. Structured Output")
print("=" * 70)

class Person(BaseModel):
    """Information about a person"""
    name: str = Field(description="The person's name")
    age: int = Field(description="The person's age")
    occupation: str = Field(description="The person's occupation")
    hobbies: list[str] = Field(description="List of hobbies")


# Use with_structured_output for guaranteed schema compliance
structured_model = model.with_structured_output(Person)

result = structured_model.invoke(
    "John is a 35-year-old teacher who enjoys reading, hiking, and photography."
)

print(f"Structured output: {result}")
print(f"Name: {result.name}")
print(f"Age: {result.age}")
print(f"Hobbies: {', '.join(result.hobbies)}\n")


# ============================================================================
# 6. Parallel Tool Calls
# ============================================================================

print("6. Parallel Tool Calls")
print("=" * 70)

response = model_with_tools.invoke([
    HumanMessage(content="What's the weather in London and New York?")
])

print(f"Number of tool calls: {len(response.tool_calls)}")

for tool_call in response.tool_calls:
    print(f"\nTool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")

    for t in tools:
        if t.name == tool_call['name']:
            result = t.invoke(tool_call['args'])
            print(f"Result: {result}")
            break


# ============================================================================
# Key Takeaways
# ============================================================================

print("\n" + "=" * 70)
print("KEY TAKEAWAYS:")
print("✓ Use @tool decorator to create tools (requires docstrings!)")
print("✓ bind_tools() enables function calling on models")
print("✓ Models return tool_calls when they want to use a tool")
print("✓ Execute tools and return results with ToolMessage")
print("✓ with_structured_output() guarantees Pydantic schema compliance")
print("✓ Models can make multiple tool calls in parallel")
