# pip install 'smolagents[e2b]'
# https://e2b.dev/

from smolagents import InferenceClientModel, CodeAgent
from dotenv import load_dotenv

load_dotenv()

with CodeAgent(model=InferenceClientModel(), tools=[], executor_type="e2b") as agent:
    agent.run("Can you give me the 100th Fibonacci number?")