import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

os.environ["GOOGLE_API_KEY"] = "AIzaSyDvw9GE_kiApe3IhFLP4EligibR-Oh-fEU"

chat = ChatGoogleGenerativeAI(model='gemini-pro', temperature=0)

def response(message, history, additional_input_info):
        history_langchain_format = []
        # additional_input_info로 받은 시스템 프롬프트를 랭체인에게 전달할 메시지에 포함시킨다.
        history_langchain_format.append(SystemMessage(content= additional_input_info))
        for human, ai in history:
                history_langchain_format.append(HumanMessage(content=human))
                history_langchain_format.append(AIMessage(content=ai))
        history_langchain_format.append(HumanMessage(content=message))
        gpt_response = chat(history_langchain_format)
        return gpt_response.content

gr.ChatInterface(
        fn=response,
        textbox=gr.Textbox(placeholder="Message ChatBot..", container=False, scale=7),
        # 채팅창의 크기를 조절한다.
        chatbot=gr.Chatbot(height=800),
        title="Chat Bot",
        description="대한민국 건축 법령 챗봇입니다.",
        theme="soft",
        retry_btn="다시보내기",
        undo_btn="이전챗 삭제",
        clear_btn="전챗 삭제",
        additional_inputs=[
            gr.Textbox("", label="System Prompt를 입력해주세요", placeholder="I'm lovely chatbot.")
        ]
).launch()