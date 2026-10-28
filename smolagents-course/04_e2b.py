# pip install 'smolagents[e2b]'
# https://e2b.dev/

from smolagents import InferenceClientModel, CodeAgent
from dotenv import load_dotenv

# The smolagents 1.26 default (Qwen3-Next-80B-A3B-Thinking) is not served by Inference Providers; see README
HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"

load_dotenv()

with CodeAgent(model=InferenceClientModel(model_id=HF_MODEL_ID), tools=[], executor_type="e2b") as agent:
    agent.run("Can you give me the 100th Fibonacci number?")