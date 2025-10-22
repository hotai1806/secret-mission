"""
Description: This file include feature create a assistant, vector_store
             Link tool file_search's assistant to vector_store

"""
import os
import json

from openai import OpenAI
from dotenv import load_dotenv
from app.tool import load_files_from_folder

load_dotenv()

SYSTEM_PROMPT = """You are OptiBot, the customer-support bot for OptiSigns.com.
• Tone: helpful, factual, concise.
• Only answer using the uploaded docs.
• Max 5 bullet points; else link to the doc.
• Cite up to 3 "Article URL:" lines per reply.
"""
METADATA_PATH = "optibot.json"

# Get API key from environment variable
def get_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not exist. Please check your .env")
    return api_key

class OptiBotManager:
    def __init__(self, api_key: str, metadata_path=METADATA_PATH):
        self.client = OpenAI(api_key=api_key)
        self.instructions = SYSTEM_PROMPT
        self.assistant = None
        self.vector_store = None
        self.metadata_path = metadata_path

    def _load_metadata(self):
        if not os.path.exists(self.metadata_path):
            return None
        try:
            with open(self.metadata_path, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            return None

    def _save_metadata(self, assistant_id: str, vector_store_id: str):
        data = {"assistant_id": assistant_id, "vector_store_id": vector_store_id}
        with open(self.metadata_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        # Make file readable only by current user (optional)
        try:
            os.chmod(self.metadata_path, 0o600)
        except Exception:
            pass

    # -------------------------
    # Assistant helpers
    # -------------------------
    def _fetch_assistant_by_id(self, assistant_id: str):
        return self.client.beta.assistants.retrieve(assistant_id=assistant_id)
    
    def create_assistant(self, assistant_name= "OptiBot",instructions=None,model="gpt-4.1-nano", tools=[{"type": "file_search"}]):
        if instructions is not None:
            self.instructions = instructions
        self.assistant = self.client.beta.assistants.create(
            name=assistant_name,
            instructions=self.instructions,
            model=model,
            tools=tools,
        )
        return self.assistant
    
    def create_or_get_assistant(self, assistant_name="OptiBot", instructions=None, model="gpt-4.1-nano", tools=[{"type": "file_search"}]):
        if instructions is not None:
            self.instructions = instructions

        meta = self._load_metadata()
        if meta and meta.get("assistant_id"):
            try:
                fetched = self._fetch_assistant_by_id(meta["assistant_id"])
                self.assistant = fetched
                return self.assistant
            except Exception as e:
                # auto-recreate (Q2: a)
                print(f"[OptiBotManager] existing assistant_id fetch failed: {e}. Recreating assistant...")

        # If no metadata or fetch failed -> create new assistant and update metadata later
        self.assistant = self.create_assistant(assistant_name=assistant_name, instructions=instructions, model=model, tools=tools)
        # If we have a vector_store id already in metadata keep it; otherwise we will save both when vector store created
        existing_vs_id = meta.get("vector_store_id") if meta else None
        if existing_vs_id:
            # save both in metadata (assistant changed)
            self._save_metadata(self.assistant.id, existing_vs_id)
        else:
            # save just assistant and placeholder for vector store (vector saved later)
            self._save_metadata(self.assistant.id, "")
        return self.assistant


    # -------------------------
    # Vector store helpers
    # -------------------------
    def _fetch_vector_store_by_id(self, vector_store_id: str):
        # Use retrieve - depending on SDK this might be client.beta.vector_stores.retrieve(...)
        return self.client.vector_stores.retrieve(vector_store_id=vector_store_id)

    def create_vector_store(self,vs_name="Support FAQ for OptiSigns User"):
        self.vector_store = self.client.vector_stores.create(        # Create vector store
                        name="Support FAQ for OptiSigns User",
                        )
        return self.vector_store

    def create_or_get_vector_store(self, vs_name="Support FAQ for OptiSigns User"):
        meta = self._load_metadata()
        if meta and meta.get("vector_store_id"):
            try:
                fetched = self._fetch_vector_store_by_id(meta["vector_store_id"])
                self.vector_store = fetched
                return self.vector_store
            except Exception as e:
                # auto-recreate (Q2: a)
                print(f"[OptiBotManager] existing vector_store_id fetch failed: {e}. Recreating vector store...")

        # create new and update metadata
        self.vector_store = self.create_vector_store(vs_name=vs_name)
        existing_asst_id = meta.get("assistant_id") if meta else None
        if existing_asst_id:
            self._save_metadata(existing_asst_id, self.vector_store.id)
        else:
            self._save_metadata("", self.vector_store.id)
        return self.vector_store

    def upload_file_vector_store(self, file_streams, vector_store):
        self.client.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id, files=file_streams)

    def link_assistant_to_vector_store(self, assistant, vector_store):
        self.client.beta.assistants.update(
            assistant_id=assistant.id,
            tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
        )