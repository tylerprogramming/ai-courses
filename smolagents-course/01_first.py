from smolagents import CodeAgent, InferenceClientModel

# Initialize a model (using Hugging Face Inference API)
# hf login to get the token
# signup to huggingface to get the token
model = InferenceClientModel()  # Uses a default model

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)