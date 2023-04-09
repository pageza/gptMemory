import os
import openai
import psycopg2
import configparser


# Read the configuration file
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
config.read(config_path)

# Configure OpenAI API key
openai.api_key = config.get("openai", "OPENAI_API_KEY")

class DataAccessLayer:
    def __init__(self, db_name=None, db_user=None, db_password=None, db_host="localhost", db_port="5432"):
        self.db_name = db_name or config.get("database", "DB_NAME")
        self.db_user = db_user or config.get("database", "DB_USER")
        self.db_password = db_password or config.get("database", "DB_PASSWORD")
        self.connection = psycopg2.connect(
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password,
            host=db_host,
            port=db_port,
        )



    def _execute_query(self, query, fetch=False):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            if fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = None
        return result

    # Add more methods to interact with the database, e.g., insert_message, get_conversation_history, etc.
    
    def start_conversation(self, user_id, user_input=None):
        conversation_history = self.get_conversation_history(user_id)

        if not conversation_history:
            conversation_history.append({"role": "system", "content": "You are now chatting with ChatGPT."})
        
        if user_input:
            conversation_history.append({"role": "user", "content": user_input})

        # Prepare the message input for ChatGPT
        messages = [{"role": message["role"], "content": message["content"]} for message in conversation_history]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.8,
        )

        response_text = response.choices[0]['message']['content'].strip()

        # Save ChatGPT's response to the database
        self.send_message(user_id, "chatgpt", response_text)

        return response_text

    def get_user_conversations(self, user_id):
        with self.connection.cursor() as cursor:
           sql = """SELECT c.id, m.content as last_message
                    FROM conversations c
                    JOIN messages m ON c.id = m.conversation_id
                    WHERE c.user_id = %s AND m.id = (SELECT MAX(id) FROM messages WHERE conversation_id = c.id)
                    ORDER BY m.timestamp DESC"""
        cursor.execute(sql, (user_id,))
        return cursor.fetchall()

    def set_active_conversation(self, user_id, conversation_id):
        with self.connection.cursor() as cursor:
            # Set all conversations to inactive
            sql = "UPDATE conversations SET is_active = 0 WHERE user_id = %s"
            cursor.execute(sql, (user_id,))

            # Set the chosen conversation to active
            sql = "UPDATE conversations SET is_active = 1 WHERE user_id = %s AND id = %s"
            cursor.execute(sql, (user_id, conversation_id))
            self.connection.commit()

    # Implement other methods to handle user requests and generate new data before generating a response

    def get_conversation_history(self, user_id):
        conn = psycopg2.connect(dbname=self.db_name, user=self.db_user, password=self.db_password)
        cursor = conn.cursor()

        query = """
           SELECT messages.sender, messages.content
           FROM messages
           JOIN conversations ON messages.conversation_id = conversations.id
           WHERE conversations.user_id = %s
           ORDER BY messages.created_at;
        """
        cursor.execute(query, (user_id,))
        history = cursor.fetchall()

        formatted_history = [{"role": message[0], "content": message[1]} for message in history]

        cursor.close()
        conn.close()

        return formatted_history

    def send_message(self, user_id, sender, content):
        with self.connection.cursor() as cursor:
            # Insert the new message into the messages table
            insert_query = """
                INSERT INTO messages (conversation_id, sender, content)
                VALUES ((SELECT id FROM conversations WHERE user_id = %s), %s, %s);
            """
            cursor.execute(insert_query, (user_id, sender, content))
            self.connection.commit()
        return content
    
    def search_messages(self, user_id, search_terms):
        with self.connection.cursor() as cursor:
            query = """
                SELECT messages.sender, messages.content
                FROM messages
                JOIN conversations ON messages.conversation_id = conversations.id
                WHERE conversations.user_id = %s AND messages.content ILIKE %s
                ORDER BY messages.created_at;
            """
            search_pattern = f"%{search_terms}%"
            cursor.execute(query, (user_id, search_pattern))
            results = cursor.fetchall()

        return [{"role": message[0], "content": message[1]} for message in results]

if __name__ == "__main__":
    # Replace these values with your PostgreSQL credentials
    config = configparser.ConfigParser()
    config.read("config.ini")
    DB_NAME = config.get("database", "DB_NAME")
    DB_USER = config.get("database", "DB_USER")
    DB_PASSWORD = config.get("database", "DB_PASSWORD")
    
    dal = DataAccessLayer(DB_NAME, DB_USER, DB_PASSWORD)
    user_id = 1  # Replace this with a valid user ID from your users table
    response = dal.start_conversation(user_id)
    print("ChatGPT response:", response)
