from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

VECTOR_STORE_ID = "vs_68e816175af88191aa35377b59081d2c"

# Add more documents
file_batch = client.vector_stores.file_batches.upload_and_poll(
    vector_store_id=VECTOR_STORE_ID,
    files=[
        open("data/new_notes.txt", "rb"),
        # open("data/meeting_transcript.pdf", "rb"),
        # open("data/marketing_plan.docx", "rb"),
    ]
)

print("Upload Status:", file_batch.status)
print("File Counts:", file_batch.file_counts)
