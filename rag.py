from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging
import os

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# SQLAlchemy 설정
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentRetriever:
    def __init__(self):
        self.session = Session()

    def fetch_answer(self, question_text): # 질문 텍스트를 입력으로 받아서 가장 유사한 문서 5개를 반환
        try:
            # 질문 저장 
            self.session.execute(text("INSERT INTO questions (text) VALUES (:text)").bindparams(text=question_text))
            self.session.commit()

            # 모든 문서와 질문 토큰화 및 벡터화
            documents = self.session.execute(text("SELECT id, text FROM documents")).fetchall()
            doc_texts = [doc[1] for doc in documents] + [question_text]
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(doc_texts)

            # 질문과 모든 문서 간의 코사인 유사도 계산
            cosine_sim = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
            sim_scores = list(enumerate(cosine_sim))
            sim_scores.sort(key=lambda x: x[1], reverse=True)
            # 상위 5개 문서를 줄바꾸기로 구분하여 반환
            results = ""
            for i in range(min(5, len(sim_scores))):
                doc_id, sim_score = sim_scores[i]
                results += f"{documents[doc_id][1]} (Similarity Score: {sim_score:.2f})\n\n"              
            return results
        except Exception as e:
            self.session.rollback()
            return f"Error: {str(e)}"
        finally:
            self.session.close()
