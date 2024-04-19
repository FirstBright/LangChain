# from chat import Chat, Chat_SQL
# import os
# import gradio as gr
# from logger import Logger

# def main():
#     os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyA1g9sPAwHcScfVT_uu_UZWO14JKWWlmdE")
#     chat = Chat()
#     chat_sql = Chat_SQL()
#     logger = Logger()
#     for i in range(5):
#         question_text = input("질문을 입력하세요: ")
#         logger.log_message("User : "+question_text)
#         response = chat.ask(question_text)
#         logger.log_message("Answer : "+response)
#         print(f"{response}")
#         print()
#         response = chat_sql.ask(question_text)
#         logger.log_message("Answer : "+response)
#         print(f"{response}")
        
# def inference(text):
#     prompt = main(text)
#     return prompt

# demo = gr.Interface(fn=inference, inputs='text', outputs='text')

# demo.launch(debug=True, share=True)

# if __name__ == "__main__":
#     main()
# -----------------------------
# import os
# import gradio as gr
# from chat import Chat, Chat_SQL
# from logger import Logger

# def main(text=None):
#     os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyA1g9sPAwHcScfVT_uu_UZWO14JKWWlmdE")
#     chat = Chat()
#     chat_sql = Chat_SQL()
#     logger = Logger()

#     if text is not None:
#         question_texts = [text]
#     else:
#         question_texts = [input("질문을 입력하세요: ") for _ in range(5)]

#     for question_text in question_texts:
#         logger.log_message("User : " + question_text)
#         response = chat.ask(question_text)
#         logger.log_message("Answer : " + response)
#         print(f"{response}\n")
#         response = chat_sql.ask(question_text)
#         logger.log_message("Answer : " + response)
#         print(f"{response}\n")
        
# def inference(text):
#     main(text)
#     return "Check the console for responses"

# demo = gr.Interface(fn=inference, inputs='text', outputs='text')

# if __name__ == "__main__":
#     demo.launch(debug=True, share=True)


import os
import gradio as gr
from chat import Chat, Chat_SQL
from logger import Logger

def inference(message, *args):
    # *args는 추가적인 인자를 처리하기 위해 사용됩니다.
    # 필요에 따라 이를 활용하거나 무시할 수 있습니다.
    return main(message)

# def main(text=None):
#     os.environ.setdefault("GOOGLE_API_KEY", "AIzaSyA1g9sPAwHcScfVT_uu_UZWO14JKWWlmdE")
#     chat = Chat()
#     chat_sql = Chat_SQL()
#     logger = Logger()
    
#     responses = []

#     if text is not None:
#         question_texts = [text]
#     else:
#         question_texts = [input("질문을 입력하세요: ") for _ in range(5)]

#     for question_text in question_texts:
#         logger.log_message("User : " + question_text)
#         response = chat.ask(question_text)
#         logger.log_message("Answer : " + response)
#         responses.append(f"Chat response: {response}\n")
        
#         response = chat_sql.ask(question_text)
#         logger.log_message("Answer : " + response)
#         responses.append(f"Chat_SQL response: {response}\n")    

    # return "\n".join(responses)
    
# main 함수를 간단하게 재정의
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

