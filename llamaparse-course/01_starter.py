# pip install llama-index llama-index-llms-openai llama-parse

from llama_parse import LlamaParse
from dotenv import load_dotenv
import os
load_dotenv()

parser = LlamaParse(
    api_key=os.getenv("LLAMA_PARSE_API_KEY"),  # optional if using env var
    result_type="markdown",   # "text" or "markdown" or "json"
    language="en"   # preserves table layout
)

parsed_docs = parser.load_data("data/us-gov.pdf")

for page in parsed_docs.pages:
    print(page.text)
    print(page.md)
    print(page.images)
    print(page.layout)
    print(page.structuredData)