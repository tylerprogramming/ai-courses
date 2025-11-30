from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from dotenv import load_dotenv

load_dotenv()

model = ChatOllama(
    model="deepseek-r1:1.5b"
)
 
agent = create_agent(
    model=model,
    system_prompt="You are a helpful assistant",
)

# Run the agent
response =agent.invoke(
    {"messages": [{"role": "user", "content": "What is a space fact?"}]}
)

print(response)