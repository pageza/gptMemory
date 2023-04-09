import os
import unittest
from sys import path
path.append("..")
from data_access_layer import DataAccessLayer
import configparser

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini"))


class TestDatabaseMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # # Read the configuration file
        # config = configparser.ConfigParser()
        # config.read("config.ini")
        # # Set up the DataAccessLayer object with the appropriate PostgreSQL credentials
        cls.DB_NAME = config.get("database", "DB_NAME")
        cls.DB_USER = config.get("database", "DB_USER")
        cls.DB_PASSWORD = config.get("database", "DB_PASSWORD")
        cls.dal = DataAccessLayer()

        # Insert a test message containing the search term "history"
        cls.dal.send_message(1, "user", "Let's talk about history.")

    def test_connection(self):
        self.assertIsNotNone(self.dal.connection, "Database connection not established")

    def test_start_conversation(self):
        user_id = 1  # Replace this with a valid user ID from your users table
        response = self.dal.start_conversation(user_id)
        self.assertIsNotNone(response, "Failed to start conversation with ChatGPT")

    # Add more test cases for other methods you implement in the DataAccessLayer class
    def test_start_conversation_with_history(self):
        user_id = 1  # Replace this with a valid user ID from your users table
    
    # Send a message from the user to store in the conversation history
        self.dal.send_message(user_id, "user", "What is the capital of France?")
    
    # Start a new conversation and check the response
        response = self.dal.start_conversation(user_id)
        self.assertIsNotNone(response, "Failed to start conversation with ChatGPT")
        self.assertNotEqual(response.strip().lower(), "i'm sorry, but as an ai language model, i don't have access to any conversation history or personal information of any user. my purpose is to assist you in generating human-like text based on the input given to me. is there anything else i can help you with?")

    def test_search_messages(self):
        user_id = 1  # Replace this with a valid user ID from your users table

        # Send a message from the user to store in the conversation history
        self.dal.send_message(user_id, "user", "How many countries have history in Africa?")

        # Print the search term and the database contents
        search_term = "history"
        print("Search term:", search_term)
        print("Database contents:", self.dal.get_conversation_history(user_id))
        
        # Search messages containing the word "Africa"
        
        results = self.dal.search_messages(user_id, search_term)
        print("Search results:", results)
        self.assertTrue(len(results) > 0, "Failed to search messages with the given search term")

if __name__ == "__main__":
    unittest.main()
