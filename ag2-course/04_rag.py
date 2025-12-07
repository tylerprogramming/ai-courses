import os
from typing import Any

from autogen import ConversableAgent, LLMConfig
from dotenv import load_dotenv

load_dotenv()

llm_config = LLMConfig.from_json(path="OAI_CONFIG_LIST.json")

base_system_message = "You are a helpful agent, answering questions about the files in a directory:\n{filelisting}"

def give_agent_file_listing(agent: ConversableAgent, messages: list[dict[str, Any]]) -> None:
    # Get the list of files in the current directory
    files = os.listdir()

    # Put them in a string
    files_str = "\n".join(files)

    # Use the system message template and update the agent's system message to include the file listing
    agent.update_system_message(base_system_message.format(filelisting=files_str))
    
files_agent = ConversableAgent(
    name="files_agent",
    system_message="""You are a helpful agent, answering questions about the files in a directory.""",
    llm_config=llm_config,
    )

files_agent.register_hook(
    hookable_method="update_agent_state",
    hook=give_agent_file_listing,
    )

human = ConversableAgent(
    name="human",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    )

human.initiate_chat(
    recipient=files_agent,
    message="Tell me about the files in my directory.",
    max_turns=1,
    )