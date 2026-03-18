from bs4 import BeautifulSoup
import requests
from collections import deque
import time

def get_page_content(url):
    """
    Get the HTML content of a page from the URL
    """

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
    
def crawl(url):
    """
    Crawl a page from the URL, get text and links, respect the 6 second delay
    """

    visited_urls = set()
    to_visit = deque([url])
    data = []

    while to_visit:
        current_url = to_visit.popleft()

        if current_url in visited_urls: # skip if visited already
            continue

        content = get_page_content(current_url)

        if content is not None:
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)
            data.append({"url": current_url, "text": text})

            next_link = soup.select_one("li.next a")
            if next_link and "href" in next_link.attrs:
                absolute_link = requests.compat.urljoin(current_url, next_link["href"])
                
                if absolute_link not in visited_urls and absolute_link not in to_visit:
                    to_visit.append(absolute_link)

        visited_urls.add(current_url)
        time.sleep(6)

    return data

if __name__ == "__main__":
    print(crawl("https://quotes.toscrape.com/"))