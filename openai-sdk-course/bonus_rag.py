from agents import Agent, Runner, FileSearchTool
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_ID = "insert_id_here"

rag_agent = Agent(
    name="RAG Researcher",
    instructions=(
        "You are a retrieval-augmented research assistant. "
        "Always use the file_search tool FIRST to gather relevant "
        "context from the vector store before answering. "
        "Cite the filenames used."
    ),
    tools=[
        FileSearchTool(vector_store_ids=[VECTOR_STORE_ID])
    ]
)

result = Runner.run_sync(
    rag_agent,
    "What does the file 'new_notes.txt' say about error handling and what is the exact sample code?"
)

print("=== Final Answer ===")
print(result.final_output)

print("\n=== Token Usage ===")
print(result.context_wrapper.usage.total_tokens)
