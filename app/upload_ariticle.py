"""
Description: This file include feature create a assistant, vector_store
             Link tool file_search's assistant to vector_store
             
"""
import os

from openai import OpenAI
from dotenv import load_dotenv
from tool import load_files_from_folder

load_dotenv()
SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
"""

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not exist. Please check your .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Create an assistant
assistant = client.beta.assistants.create(
  name="OptiBot",
  instructions=SYSTEM_PROMPT,
  model="gpt-4.1-nano",
  tools=[{"type": "file_search"}],
)

# Create a vector store
vector_store = client.vector_stores.create(        # Create vector store
    name="Support FAQ for OptiSigns User",
)


# Get file paths to streaming file
files = load_files_from_folder("./articles")
file_streams = [open(path, "rb") for path in files]
file_batch = client.vector_stores.file_batches.upload_and_poll(
vector_store_id=vector_store.id, files=file_streams)

# Link vector store to tool file_search for assistant
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

