import requests
from bs4 import BeautifulSoup

class Crawler:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def crawl(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 지정된 클래스를 가진 div 태그들 추출
        div_elements = soup.find_all('div', class_='DIV_S_HO')
        documents = []
        for div in div_elements:
            text = div.get_text(strip=True)
            documents.append(text)
            self.vector_store.add_document(text)
        return documents

# VectorStore 클래스는 여기서 단순화하여 정의합니다.
class VectorStore:
    def __init__(self):
        self.documents = []

    def add_document(self, doc):
        self.documents.append(doc)

# 사용 예
vector_store = VectorStore()
crawler = Crawler(vector_store)
url = 'http://yeslaw.com/lims/front/page/fulltext.html?pAct=view&pPromulgationNo=160392'  # 실제 크롤링할 URL로 교체 필요
documents = crawler.crawl(url)
print(documents)
