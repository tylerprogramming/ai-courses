from langgraph_sdk import get_client
import asyncio

# Connect to local server
client = get_client(url="http://localhost:2024")

async def main():
    # Stream agent execution
    async for chunk in client.runs.stream(
        None,                    # thread_id (None = new thread)
        "agent",                 # assistant_id from your graph
        input={"messages": [{"role": "human", "content": "What is LangGraph?"}]},
        stream_mode="values"     # Stream all state updates
    ):
        print(f"Event: {chunk.event}")
        print(f"Data: {chunk.data}")

asyncio.run(main())