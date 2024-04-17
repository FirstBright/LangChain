import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv
from gemini import GeminiClient

class ChatBot:
    def __init__(self):
        # api = load_dotenv()
        # if "GOOGLE_API_KEY" not in os.environ:
        #     os.environ["GOOGLE_API_KEY"] = api

        self.chat = GeminiClient()
        self.history_langchain_format = []
      

    def response(self, message, history):        
        for human, ai in history:
            self.history_langchain_format.append(HumanMessage(content=human))
            self.history_langchain_format.append(AIMessage(content=ai))
        self.history_langchain_format.append(HumanMessage(content=message))
        response = self.chat.get_response(self.history_langchain_format)
        return response
    
    def launch_chat_interface(self):
        gr.ChatInterface(
            fn=self.response,
            textbox=gr.Textbox(placeholder="Message ChatBot..", container=False, scale=7),
            chatbot=gr.Chatbot(height=600),
            title="Chat Bot",
            description="대한민국 건축 법령 챗봇입니다.",
            theme="soft",
            retry_btn="다시보내기",
            undo_btn="이전챗 삭제",
            clear_btn="전챗 삭제"
        ).launch()

# chatbot_instance = ChatBot()
# chatbot_instance.launch_chat_interface()