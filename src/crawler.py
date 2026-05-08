from bs4 import BeautifulSoup
import requests
from collections import deque
import time
from urllib.parse import urljoin, urldefrag, urlparse

def get_page_content(url: str) -> str:
    """
    Get the HTML content of a page from the URL

    Args:
        url (str): The URL of the page to fetch

    Returns:
        str: The HTML content of the page or None if there was an error
    """

    # Try to fetch the page content and handle errors
    try:
        response = requests.get(url)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Could not load page. Code: {response.status_code}")
            return None
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def crawl(url: str) -> list[dict]:
    """
    Crawls the website from the given url, extracts text and follows links.
    Respects 6 second politeness window between requests.

    Args:
        url (str): The URL to start crawling from

    Returns: list[dict]: A list of dictionaries containing the URL and extracted text
    """

    start = urlparse(url).netloc

    # Use a set to track visited URLs and deque for URLs to visit
    visited_urls = set()
    to_visit = deque([url])
    data = []

    # Crawl until there are no more URLs to visit
    while to_visit:
        current_url = to_visit.popleft()

        if current_url in visited_urls: # skip if visited already
            continue

        content = get_page_content(current_url)

        # Get the text content and find the next link to follow
        if content is not None:
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            data.append({"url": current_url, "text": text})

            for link in soup.find_all("a", href=True):
                href = link["href"]
                absolute_link = requests.compat.urljoin(current_url, href)

                clean_url, _ = urldefrag(absolute_link)
                
                if urlparse(clean_url).netloc == start:
                    if clean_url not in visited_urls and clean_url not in to_visit:
                        to_visit.append(clean_url)

        visited_urls.add(current_url)
        time.sleep(6) # 6 second politeness window

    return data

if __name__ == "__main__":
    print(crawl("https://quotes.toscrape.com/"))