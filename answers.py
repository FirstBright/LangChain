import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv

# 데이터베이스 모델 정의
Base = declarative_base()

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# SQLAlchemy 설정
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey('questions.id'))
    answers = relationship('Answer', back_populates='document')

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    token = Column(String)
    document_id = Column(Integer, ForeignKey('documents.id'))
    document = relationship('Document', back_populates='answers')

class DocumentProcessor:
    def __init__(self):
        self.session = Session()

    def process_documents(self):
        try:
            documents = self.session.query(Document).all()
            vectorizer = TfidfVectorizer()
            texts = [doc.text for doc in documents]
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()

            # document 별로 top 10 token을 Answer 테이블에 저장
            for doc, row in zip(documents, tfidf_matrix):
                top_indices = row.nonzero()[1]
                top_terms = [(feature_names[i], row[0, i]) for i in top_indices]
                top_terms.sort(key=lambda x: x[1], reverse=True)  # 유사도 순으로 정렬

                # 상위 10개의 토큰을 저장
                for term, _ in top_terms[:10]:  # 상위 10개의 토큰만 저장
                    answer = Answer(token=term, document_id=doc.id)  # 문서 ID 저장
                    self.session.add(answer)

            self.session.commit()
            logger.info("Document processing and token storing complete.")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Error processing documents: {str(e)}")
        finally:
            self.session.close()

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.process_documents()
