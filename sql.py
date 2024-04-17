from sqlalchemy import create_engine, Column, Integer, Text, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, exc as orm_exc
from sqlalchemy.orm import session
from sqlalchemy.sql import exists
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DATABASE_URL = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# SQLAlchemy 설정
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)

# 데이터베이스 테이블 정의
class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)

# 데이터베이스 테이블 생성 테이블이 있는경우 무시
Base.metadata.create_all(engine, checkfirst=True)

# 데이터베이스 작업을 위한 클래스 데이터베이스에 텍스트 데이터를 삽입할때 중복된 데이터는 제외
class SQLModule:
    def __init__(self):
        self.session = Session()

    def insert_documents(self, texts):
        initial_count = self.session.query(Document).count()  # 삽입 전 문서 수
        for text in texts:
            # 중복된 데이터가 있는지 확인
            if not self.session.query(exists().where(Document.text == text)).scalar():
                try:
                    document = Document(text=text)
                    self.session.add(document)
                except exc.IntegrityError as e:
                    self.session.rollback()
                    print(f"Error inserting {text}: {e}")
        self.session.commit()
        final_count = self.session.query(Document).count()  # 삽입 후 문서 수
        print(f"{len(texts)}개의 데이터 중 {final_count - initial_count}개의 데이터가 삽입되었습니다.")

    def close(self):
        self.session.close()

# 사용 예 ---------main에 이식
if __name__ == '__main__':
    sql_module = SQLModule()
    texts = documents
    sql_module.insert_documents(texts)
    sql_module.close()
