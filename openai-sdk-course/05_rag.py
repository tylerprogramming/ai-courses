from agents import Agent, Runner, FileSearchTool, WebSearchTool, function_tool
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_ID = "vs_68e816175af88191aa35377b59081d2c"

# Optional custom function tool
@function_tool
def summarize_numbers(a: int, b: int) -> int:
    """Example: A simple arithmetic tool."""
    return a + b

# Create RAG agent
rag_agent = Agent(
    name="RAG Researcher",
    instructions=(
        "You are a retrieval-augmented research assistant. "
        "Always use the file_search tool FIRST to gather relevant "
        "context from the vector store before answering. "
        "Cite the filenames used."
    ),
    tools=[
        FileSearchTool(vector_store_ids=[VECTOR_STORE_ID]),
        summarize_numbers,
    ]
)

result = Runner.run_sync(
    rag_agent,
    "What does the file 'new_notes.txt' say about Python?"
)

print("=== Final Answer ===")
print(result.final_output)

print("\n=== Token Usage ===")
print(result.context_wrapper.usage.total_tokens)
