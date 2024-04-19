import requests
from bs4 import BeautifulSoup
import re

class Crawler:
    def __init__(self, url):
        self.url = url

    def crawl(self):
        response = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all('table', id=re.compile("^TBL"))
        all_texts = [table.get_text(strip=True) for table in tables if table.get_text(strip=True)]
        return all_texts

