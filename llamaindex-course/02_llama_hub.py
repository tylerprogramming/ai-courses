from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.readers.web import RssReader
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# 1. Set up LLM using Settings
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)

# 2. Load documents
loader = RssReader()

documents = loader.load_data(
    urls=['https://feeds.arstechnica.com/arstechnica/index']
)

# 3. Build index (Settings are used automatically)
index = VectorStoreIndex.from_documents(documents, show_progress=True)

# 4. Create query engine
query_engine = index.as_query_engine()

# 5. Run queries
while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit","quit"): break
    response = query_engine.query(user_input)
    print("Bot:", response.response)