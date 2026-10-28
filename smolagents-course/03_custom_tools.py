from smolagents import tool
from huggingface_hub import list_models

task = "text-to-video"

most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
print(most_downloaded_model.id)

@tool
def model_download_tool(task: str) -> str:
    """
    This is a tool that returns the most downloaded model of a given task on the Hugging Face Hub.
    It returns the name of the checkpoint.

    Args:
        task: The task for which to get the download count.
    """
    most_downloaded_model = next(iter(list_models(filter=task, sort="downloads", direction=-1)))
    return most_downloaded_model.id

from smolagents import CodeAgent, InferenceClientModel

# The smolagents 1.26 default (Qwen3-Next-80B-A3B-Thinking) is not served by Inference Providers; see README
HF_MODEL_ID = "Qwen/Qwen3-235B-A22B-Instruct-2507"
agent = CodeAgent(tools=[model_download_tool], model=InferenceClientModel(model_id=HF_MODEL_ID))
result = agent.run(
    "Can you give me the name of the model that has the most downloads in the 'text-to-video' task on the Hugging Face Hub?"
)