from bs4 import BeautifulSoup
import requests

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

if __name__ == "__main__":
    print(get_page_content("https://quotes.toscrape.com/"))