from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.sql import exists
from dotenv import load_dotenv
from crawler import Crawler
load_dotenv()

# Database configuration
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = scoped_session(sessionmaker(bind=engine))

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text = Column(String)

class EmbeddingService:
    def __init__(self, model_name='all-mpnet-base-v2'):
        self.embeddings = SentenceTransformer(model_name)
        self.index = faiss.IndexFlatL2(768)  # 임베딩 차원

    def encode(self, text):
        return self.embeddings.encode([text])[0]

    def add_to_index(self, vector):
        self.index.add(np.array([vector], dtype='float32'))

class DocumentManager:
    def __init__(self, session, embedding_service, url):
        self.session = session
        self.embedding_service = embedding_service
        self.crawler = Crawler(url)

    def crawl_and_store(self):
        texts = self.crawler.crawl()
        for text in texts:
            self.add_document(text)

    def add_document(self, text):
        if not self.session.query(exists().where(Document.text == text)).scalar():
            document = Document(text=text)
            self.session.add(document)
            self.session.commit()

            embedding = self.embedding_service.encode(text)
            self.embedding_service.add_to_index(embedding)
            # 데이터베이스에 저장된 문서 개수 출력
            print(f"문서가 성공적으로 추가되었습니다. 현재 저장된 문서 개수: {self.session.query(Document).count()}")
        else:
            # 데이터베이스에 저장되지 않은 문서 개수 출력
            print(f"문서가 이미 존재합니다. 현재 저장된 문서 개수: {self.session.query(Document).count()}")

    def close(self):
        self.session.remove()

