from chat import Chat, Chat_SQL
import os

def main():
    os.environ.setdefault("GOOGLE_API_KEY", "Your_API_Key")
    question_text = input("질문을 입력하세요: ")

    chat = Chat()   
    response = chat.ask(question_text)
    print(f"chat: {response}")
    all_messages = chat.memory_buffer.get_all_messages()
    print(all_messages)
    
    chat_sql = Chat_SQL()
    response = chat_sql.ask(question_text)
    print(f"sql: {response}")

if __name__ == "__main__":
    main()

