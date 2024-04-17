import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = "AIzaSyC8NG7M4q27t9aV32h7a-fJkhebRHRt3mw"

class GeminiClient:
    def __init__(self, model='gemini-pro', temperature=1.0):
        self.chat_engine = ChatGoogleGenerativeAI(model=model, temperature=temperature) # chat engine으로 chat 클래스와 구분
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', 'Answer like lawyer.'),
            MessagesPlaceholder(variable_name='message')
        ])
        self.chain = self.prompt | self.chat_engine

    def get_response(self, input_prompt):
        response = self.chain.invoke({"message": [input_prompt]})
        return response.content
    