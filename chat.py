import os
from dotenv import load_dotenv

# 클래스 및 필요한 모듈 import
from vector_store import Vector_store
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain.callbacks.base import BaseCallbackHandler

from vector_store import Vector_store


load_dotenv()

class StreamCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end="", flush=True)
        
# 대화 기록을 저장하는 클래스
class ConversationMemoryBuffer:
    def __init__(self, capacity=10): # 10개의 메시지를 저장할 수 있는 버퍼 생성
        self.capacity = capacity
        self.buffer = []

    def add_message(self, message):
        if len(self.buffer) >= self.capacity:
            self.buffer.pop(0)
        self.buffer.append(message)

    def get_all_messages(self):
        return " ".join(self.buffer)

class Chat():
    def __init__(self):
        self.memory_buffer = ConversationMemoryBuffer()
        
    def ask(self, text):
        vector = Vector_store()
        retriever = vector.process_pdf()
        template = '''Answer the question based only on the following context:
        {context}

        Question: {question}
        '''

        prompt = ChatPromptTemplate.from_template(template)
        
        self.memory_buffer = ConversationMemoryBuffer()
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0,
            streaming=True,
            callbacks=[StreamCallback()],
        )

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        question_message = f"Question: {text}"
        response = rag_chain.invoke(text)
        answer_message = f"Answer: {response}"
        self.memory_buffer.add_message(question_message)
        self.memory_buffer.add_message(answer_message)

        return response

class Chat_SQL():
    def __init__(self):
        self.mysql_uri = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        self.db = SQLDatabase.from_uri(self.mysql_uri)
        
    def ask(self, user_question):
        template = '''Answer the question based only on the following context:
         {schema}
         Question: {question}
         SQL Query: {query}
         SQL Response: {response}'''

        prompt_response = ChatPromptTemplate.from_template(template)

        def get_schema():
            return self.db.get_table_info()

        def run_query(query):
            return self.db.run(query)

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0,
            streaming=True,
            callbacks=[StreamCallback()],
        )

        # Define your SQL query here based on the question
        sql_query = "SELECT text FROM documents"  # Example SQL query
        sql_result = run_query(sql_query)
        schema = get_schema()

        # Prepare the input for full_chain invocation
        chain_input = {
            "schema": schema,
            "question": user_question,
            "query": sql_query,
            "response": sql_result
        }

        sql_chain = (
            RunnablePassthrough.assign()
            | prompt_response
            | llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )
        
        # Make sure to pass a dictionary to invoke
        return sql_chain.invoke(chain_input)
    
    