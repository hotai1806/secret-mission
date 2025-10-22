"""
    Description: Handle file
"""

from html2text import HTML2Text
from slugify import slugify
import os

def html_to_markdown(html: str) -> str:
    """
    Convert cleaned HTML to Markdown using html2text.
    Keep code blocks intact.
    """
    h = HTML2Text()
    h.ignore_links = False       # preserve links
    h.ignore_images = False      # keep image links
    h.inline_links = False       # prefer reference links
    md = h.handle(html)

    # html2text can produce extra leading/trailing newlines; normalize:
    # md = md.strip() + "\n"
    return md
def save_file(article):
    """
    Save text to markdown file

    Args:
        article (_type_): _description_
    """
    slug_file = slugify(article["title"])
    markdown_text = html_to_markdown(article["body"])
    with open(f"articles/{slug_file}.md", "w", encoding="utf-8") as f:
        f.write(f"# {article['title']}\n\n")
        f.write(markdown_text)


def load_files_from_folder(folder_path):
    """Get file paths

    Args:
        folder_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    filepaths = []
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        if os.path.isfile(path):
            filepaths.append(path)
    return filepaths