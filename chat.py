import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage

class ChatBot:
    def __init__(self):
        os.environ["GOOGLE_API_KEY"] = ""
        self.chat = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0)

    def response(self, message, history):
        history_langchain_format = []
        for human, ai in history:
            history_langchain_format.append(HumanMessage(content=human))
            history_langchain_format.append(AIMessage(content=ai))
        history_langchain_format.append(HumanMessage(content=message))
        gpt_response = self.chat(history_langchain_format)
        return gpt_response.content

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
        
chatbot_instance = ChatBot()

chatbot_instance.launch_chat_interface()