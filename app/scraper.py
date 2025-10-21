import os
import requests
from dotenv import load_dotenv

from logger import log_decorator
from tool import  html_to_markdown, save_file

load_dotenv() 

api_key = os.getenv("API_KEY")
DOMAIN_TARGET = os.getenv("DOMAIN_TARGET") or "https://support.optisigns.com/"

api_endpoint_sections = "api/v2/help_center/en-us/sections"
api_endpoint_articles = "api/v2/help_center/en-us/sections/{}/articles"

# create folder articles
os.makedirs("articles", exist_ok=True)

@log_decorator
def fetch_list_sections():
    """
    Get All Sections for download articles

    Returns:
        List of section
        _type_: List
    """
    url = DOMAIN_TARGET + api_endpoint_sections
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error cannot fetch sections: {response.status_code}")
        return []
    sections = response.json().get('sections', [])
    

    return response.json()['sections']


@log_decorator
def fetch_articles_from_section(section_id):
    """Get list article from section

    Args:
        section_id (string): _description_

    Returns:
        _type_: List[articles]
    """
    articles = []

    url = DOMAIN_TARGET + api_endpoint_articles.format(section_id)
    option = "?sort_by=position&sort_order=desc&per_page=100"

    response = requests.get(url+option)
    if response.status_code != 200:
        print(f"Error cannot fetch articles: {response.status_code}")

    data = response.json()
    articles.extend(data.get("articles", []))
    return articles

def iter_all_articles(limit=None):
    count = 0
    for section in fetch_list_sections():
        raw_articles = fetch_articles_from_section(section["id"])
        for raw in raw_articles:
            if limit and count >= limit:
                return
            count += 1
            yield raw, section["name"]

@log_decorator
def get_all_articles():

    for raw, section_name in iter_all_articles():
        # a = html_to_markdown(raw["body"])
        save_file(article=raw)




get_all_articles()