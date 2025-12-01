from agents import Agent, Runner, function_tool, WebSearchTool, FileSearchTool
from dotenv import load_dotenv

load_dotenv()

# 1. Define a custom tool (optional)
@function_tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

# 2. Create the agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    tools=[
        add,
        WebSearchTool(),
    ],
)

# 3. Run the agent with a prompt
if __name__ == "__main__":
    result = Runner.run_sync(agent, "What is 42 + 73? And tell me something about OpenAI.")
    print("Output:", result.final_output)
    print("Token usage:", result.context_wrapper.usage.total_tokens)
