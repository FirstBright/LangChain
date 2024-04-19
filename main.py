from chat import Chat, Chat_SQL
import os
from logger import Logger
def main():
    os.environ.setdefault("GOOGLE_API_KEY", "Your_API_Key")
    chat = Chat()
    chat_sql = Chat_SQL()
    logger = Logger()
    for i in range(5):
        question_text = input("질문을 입력하세요: ")
        logger.log_message(question_text)
        response = chat.ask(question_text)
        print(f"{response}")
        print()
        response = chat_sql.ask(question_text)
        print(f"{response}")

if __name__ == "__main__":
    main()