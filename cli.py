import os
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from data_access_layer import DataAccessLayer
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini"))
DB_NAME = config.get("database", "DB_NAME")
DB_USER = config.get("database", "DB_USER")
DB_PASSWORD = config.get("database", "DB_PASSWORD")       

def ask_to_save_message(prompt):
    while True:
        save_choice = input(prompt).lower()
        if save_choice in ('y', 'n', 'yes', 'no'):
            return save_choice in ('y', 'yes')
        print("Please enter 'yes' or 'no'")

def is_asking_about_history(user_input):
    history_keywords = ["history", "previously", "talked about", "past", "before"]
    for keyword in history_keywords:
        if keyword in user_input.lower():
            return keyword
    return None

def list_conversations(dal, user_id):
    conversations = dal.get_user_conversations(user_id)

    if len(conversations) == 0:
        print("No existing conversations found.")
    else:
        print("Existing conversations:")
        for i, conversation in enumerate(conversations):
            print(f"{i + 1}. Conversation ID: {conversation['id']}, Last message: {conversation['last_message']}")


def conversation_loop(dal, session, user_id):
    while True:
        user_input = session.prompt("You: ")
        dal.send_message(user_id, "user", user_input)
        if user_input.lower() in ("quit", "exit", "bye"):
            print("Goodbye!")
            break

        if is_asking_about_history(user_input):
            keyword = is_asking_about_history(user_input)
            past_messages = dal.search_messages(user_id, keyword)
            print(f"Search term: {keyword}")
            print(f"Past messages: {past_messages}")
            user_input += f" Here is some {keyword}: {past_messages}"

        response = dal.start_conversation(user_id, user_input)
        print(f"ChatGPT: {response}")

        save_message = ask_to_save_message("Do you want to save this message? (yes/no): ")
        if save_message:
            dal.send_message(user_id, "chatgpt", response)
            print("Message saved.")
        else:
            print("Message not saved.")

def main():

    # Set up the DataAccessLayer object with the appropriate PostgreSQL credentials

    dal = DataAccessLayer(DB_NAME, DB_USER, DB_PASSWORD)

    # Initialize the PromptSession
    session = PromptSession(history=FileHistory(".chat_history"))

    user_id = 1  # Replace this with a valid user ID from your users table

    print("ChatGPT is ready to chat!")

    while True:
        print("What would you like to do?")
        action = input("1. Start a new conversation\n2. Continue an existing conversation\n3. Quit\nEnter your choice: ")

        if action == "1":
            dal.start_conversation(user_id)
            conversation_loop(dal, session, user_id)
        elif action == "2":
            list_conversations(dal, user_id)
            conversation_id = int(input("Enter the conversation ID to continue or 0 to go back: "))
            if conversation_id != 0:
                dal.set_active_conversation(user_id, conversation_id)
                conversation_loop(dal, session, user_id)
        elif action == "3":
            break
        else:
            print("Invalid input, please try again.")

        
        response = dal.start_conversation(user_id, user_input)
        print(f"ChatGPT: {response}")

        save_message = ask_to_save_message("Do you want to save this message? (yes/no): ")
        if save_message:
            dal.send_message(user_id, "chatgpt", response)
            print("Message saved.")
        else:
            print("Message not saved.")
    
if __name__ == "__main__":
    main()


