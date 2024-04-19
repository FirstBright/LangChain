import os
import gradio as gr
from chat import Chat, Chat_SQL
from logger import Logger

def inference(message, *args):
    # *args는 추가적인 인자를 처리하기 위해 사용됩니다.
    # 필요에 따라 이를 활용하거나 무시할 수 있습니다.
    return main(message)

def main(text):
    os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyA1g9sPAwHcScfVT_uu_UZWO14JKWWlmdE")
    chat = Chat()
    chat_sql = Chat_SQL()
    logger = Logger()

    logger.log_message("User : " + text)
    response_chat = chat.ask(text)
    logger.log_message("Answer : " + response_chat)
    response_chat_sql = chat_sql.ask(text)
    logger.log_message("Answer : " + response_chat_sql)

    #저장된 메세지 출력하는 부분
    all_messages = chat.memory_buffer.get_all_messages()
    print(all_messages)
    
    return f"Chat response: {response_chat}\nChat_SQL response: {response_chat_sql}"



demo = gr.ChatInterface(fn=inference,
                        textbox=gr.Textbox(placeholder="Message ChatBot..", container=False, scale=5),
                        chatbot=gr.Chatbot(height=700),
                        title="Chat Bot",
                        description="대한민국 건축 법령 챗봇입니다.",
                        theme="soft",
                        retry_btn="다시보내기",
                        undo_btn="이전챗 삭제",
                        clear_btn="전챗 삭제")

if __name__ == "__main__":
    demo.launch(debug=True, share=True)

