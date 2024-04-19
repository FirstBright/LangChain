import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain.callbacks.base import BaseCallbackHandler
from sqlalchemy import create_engine

from sqlalchemy.orm import scoped_session, sessionmaker
from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import gradio as gr

# 환경 변수 로드
load_dotenv()

class StreamCallback(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print(token, end='', flush=True)

class ChatUni:
    def __init__(self, db_uri=None):
        # 환경 변수에서 데이터베이스 URL을 구성하거나 매개변수에서 제공된 URI를 사용합니다.
        self.db_uri = db_uri or f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME_U')}"
        
        # SQLAlchemy 엔진과 세션을 초기화합니다.
        self.engine = create_engine(self.db_uri, echo=True)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        
        # SQLDatabase 인스턴스를 초기화합니다.
        self.db = SQLDatabase(self.engine)

    def ask(self, user_question):
        template = '''Answer the question based only on the following context:
         {schema}
         Question: {question}
         SQL Query: {query}
         SQL Response: {response}'''
        
        prompt_template = ChatPromptTemplate.from_template(template)
        schema = self.db.get_table_info()  # Retrieves database schema info
        sql_query = "SELECT * FROM tablename WHERE columnname = 'value"  # Example SQL query
        
        try:
            sql_result = self.db.run(sql_query)
        except Exception as e:
            return f"Error executing SQL query: {str(e)}"

        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0,
            streaming=True,
            callbacks=[StreamCallback()],
        )

        chain_input = {
            "schema": schema,
            "question": user_question,
            "query": sql_query,
            "response": sql_result
        }

        sql_chain = (
            RunnablePassthrough.assign()
            | prompt_template
            | llm.bind(stop=["\nSQLResult:"])
            | StrOutputParser()
        )

        return sql_chain.invoke(chain_input)

def inference(message, *args):
    chat = ChatUni()
    return f"Chat response: {chat.ask(message)}"

demo = gr.ChatInterface(
    fn=inference,
    textbox=gr.Textbox(placeholder="Message ChatBot..", container=False, scale=5),
    chatbot=gr.Chatbot(height=700),
    title="Chat Bot",
    description="대한민국 건축 법령 챗봇입니다.",
    theme="soft",
    retry_btn="다시보내기",
    undo_btn="이전챗 삭제",
    clear_btn="전챗 삭제"
)

if __name__ == "__main__":
    demo.launch(debug=True, share=True)
