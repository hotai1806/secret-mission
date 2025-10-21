
import os

from openai import OpenAI
from dotenv import load_dotenv
from tool import load_files_from_folder

load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not exist. Please check your .env")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)



# Create a vector store

vector_store = client.vector_stores.create(        # Create vector store
    name="Support FAQ for OptiSigns User",
)


# Get file paths to streaming file

files = load_files_from_folder("./articles")
file_streams = [open(path, "rb") for path in files]


try:
    # Code that might raise an exception
    file_batch = client.vector_stores.file_batches.upload_and_poll(
    vector_store_id=vector_store.id, files=file_streams)
except ZeroDivisionError:
    # Code to execute if a ZeroDivisionError occurs
    print("Error: Cannot divide by zero!")
except ValueError as e:
    # Code to execute if a ValueError occurs, capturing the error message
    print(f"Value error encountered: {e}")
except Exception as e:
    # A general except block to catch any other unhandled exception
    print(f"An unexpected error occurred: {e}")
else:
    # Code to execute if no exception occurs in the try block
    print("Operation successful!")
finally:
    # Code to execute regardless of whether an exception occurred or not
    print("This block always runs.")