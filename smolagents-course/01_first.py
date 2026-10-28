from smolagents import CodeAgent, InferenceClientModel

# The smolagents 1.26 default (Qwen3-Next-80B-A3B-Thinking) is not served by Inference Providers; see README
HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"

# Initialize a model (using Hugging Face Inference API)
# hf login to get the token
# signup to huggingface to get the token
model = InferenceClientModel(model_id=HF_MODEL_ID)

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)