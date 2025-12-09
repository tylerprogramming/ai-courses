# pip install llama-index llama-index-llms-openai llama-index-multi-modal-llms-openai llama-parse

import hashlib
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.llms.openai import OpenAI
# from llama_index.multi_modal_llms.openai import OpenAIMultiModal
from llama_index.core.schema import ImageNode
from dotenv import load_dotenv
import os
import shutil
import json

load_dotenv()

def file_hash(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()

# 1. Compute hash
PERSIST_DIR = "./storage"
HASH_FILE = os.path.join(PERSIST_DIR, "document_hash.json")
path = "data/us-gov.pdf"
current_hash = file_hash(path)

try:
    if os.path.exists(PERSIST_DIR) and os.path.exists(HASH_FILE):
        print("[Storage] Loading existing storage...")

        # Check if the hash matches
        with open(HASH_FILE, "r") as f:
            stored_hash = json.load(f).get("hash")

        if stored_hash == current_hash:
            print("[Storage] Document hash matches, loading from cache...")
            storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
            index = load_index_from_storage(storage_context)
            llm = OpenAI(model="gpt-4o", temperature=0.1)
            query_engine = index.as_query_engine(llm=llm, similarity_top_k=3)
        else:
            raise ValueError(f"Document hash mismatch (stored: {stored_hash}, current: {current_hash})")
    else:
        raise FileNotFoundError("No storage directory or hash file found")

except Exception as e:
    print(f"[Storage] Could not load from cache ({e}), rebuilding...")

    # Clean up old storage
    if os.path.exists(PERSIST_DIR):
        shutil.rmtree(PERSIST_DIR)
    os.makedirs(PERSIST_DIR)

    # Initialize LlamaParse with advanced features
    parser = LlamaParse(
        api_key=os.getenv("LLAMA_PARSE_API_KEY"),
        result_type="markdown",

        # Advanced parsing configuration
        parse_mode="parse_page_with_agent",  # Use agent-based parsing for better understanding
        model="openai-gpt-4-1-mini",         # Specify parsing model

        # OCR and table handling
        high_res_ocr=True,                   # Enable high-resolution OCR for images
        adaptive_long_table=True,            # Detect tables spanning multiple pages
        outlined_table_extraction=True,      # Extract tables with outline structure
        output_tables_as_HTML=True,          # Format tables as HTML for better structure

        # Visual capture
        take_screenshot=True,                # Capture page screenshots for multimodal retrieval

        language="en"
    )

    # Parse the document
    print("Parsing document with advanced features...")
    parsed_docs = parser.load_data(path)

    # Separate markdown and image nodes
    markdown_nodes = [doc for doc in parsed_docs if not isinstance(doc, ImageNode)]
    image_nodes = [doc for doc in parsed_docs if isinstance(doc, ImageNode)]

    print(f"Extracted {len(markdown_nodes)} markdown pages")
    print(f"Extracted {len(image_nodes)} screenshot images")

    # Create vector index from markdown nodes
    print("\nBuilding vector index...")
    index = VectorStoreIndex.from_documents(markdown_nodes)

    # Create query engine with multimodal support
    llm = OpenAI(model="gpt-4o", temperature=0.1)
    query_engine = index.as_query_engine(llm=llm, similarity_top_k=3)

    # Persist the index
    print("[Storage] Persisting index to disk...")
    index.storage_context.persist(PERSIST_DIR)

    # Save the document hash
    with open(HASH_FILE, "w") as f:
        json.dump({"hash": current_hash, "path": path}, f)

    print("[Storage] Index and hash saved successfully!")

# Interactive query loop
print("\n" + "="*60)
print("INTERACTIVE QUERY MODE")
print("="*60)
print("Type your questions below (or 'quit' to exit)\n")

while True:
    query = input("Query: ").strip()

    if query.lower() in ['quit', 'exit', 'q']:
        print("Exiting...")
        break

    if not query:
        continue

    print("-" * 60)
    response = query_engine.query(query)
    print(f"Response: {response}")
    print()