from app.scraper import save_all_articles
from app.tool import load_files_from_folder
from app.upload_ariticle import OptiBotManager, get_api_key
# from app.upload_ariticle import
def main():
    try:
        # Fetch all articles and save to folder articles
        save_all_articles()

        api_key = get_api_key()
        opticbot = OptiBotManager(api_key)

        assistant = opticbot.create_or_get_assistant()
        vector_store = opticbot.create_or_get_vector_store()

        # Get file paths to streaming file for upload batch
        files = load_files_from_folder("./articles")
        file_streams = [open(path, "rb") for path in files]

        #Upload file to vector store and link to assistant bot
        # TODO missin check delta file to upload
        opticbot.upload_file_vector_store(file_streams,vector_store)
        opticbot.link_assistant_to_vector_store(assistant, vector_store)


    except Exception as e:
        # Code to handle any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
