<<<<<<< HEAD
import os
from dotenv import load_dotenv
=======
>>>>>>> yangjaejun
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader

<<<<<<< HEAD
class PDFProcessor:
    def __init__(self, pdf_path):
        # 환경 변수 로드
        load_dotenv()
        # API 키 가져오기
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in .env file")
        os.environ["GOOGLE_API_KEY"] = api_key
        self.pdf_path = pdf_path

    def process_pdf(self):
        # PDF 파일 로드
        loader = PyPDFLoader(self.pdf_path)
        docs = loader.load()

        # 텍스트 스플리터 생성
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)

        # 스플리트된 텍스트들의 리스트 반환
        splits = text_splitter.split_documents(docs)

        # split 해놓은 텍스트 데이터를 embedding한 VectorDB를 생성
        # 문서에 대한 Chroma 객체를 생성하고, Google Generative AI Embeddings 모델을 사용하여 문장을 임베딩
        vectordb = Chroma.from_documents(documents=splits, 
                                          embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

        # 사용자 입력(질문)과 비교해서 가까운 K개의 결과 찾기
        retriever = vectordb.as_retriever()

        # 검색
        input_prompt = input("사용자 질문 : ")

        # 사용자 질문에 대한 답을 받아 저장
        response = retriever.invoke(input=input_prompt)

        # 결과 출력
        print(response)

# PDF 파일 경로
pdf_path = "./건축법2.pdf"

# PDFProcessor 클래스 인스턴스 생성
pdf_processor = PDFProcessor(pdf_path)

# PDF 파일 처리
pdf_processor.process_pdf()
=======
class Vector_store:   
    def process_pdf(self):
        # PDF 파일 로드
        loader = PyPDFLoader("./건축법2.pdf")
        docs = loader.load()
        # print(docs)
        # 텍스트 스플리터 생성
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)

        # 스플리트된 텍스트들의 리스트 반환
        splits = text_splitter.split_documents(docs)
        # print(len(splits))

        # split 해놓은 텍스트 데이터를 embedding한 VectorDB를 생성
        # 문서에 대한 Chroma 객체를 생성하고, Google Generative AI Embeddings 모델을 사용하여 문장을 임베딩
        vectordb = Chroma.from_documents(documents=splits, 
                                          embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
      
        # 사용자 입력(질문)과 비교해서 가까운 K개의 결과 찾기        
        return  vectordb.as_retriever(k=1)

        # 검색
        # input_prompt = input("사용자 질문 : ")

        # # 사용자 질문에 대한 답을 받아 저장
        # response = retriever.invoke(input=input_prompt)

        # # 결과 출력
        # print(response)

>>>>>>> yangjaejun
