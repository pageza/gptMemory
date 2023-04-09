import os
import cli
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import configparser
from prompt_toolkit import PromptSession

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.ini"))


class TestCLI(unittest.TestCase):

    @patch('cli.is_asking_about_history', return_value=False)
    @patch('cli.ask_to_save_message', return_value="no")
    @patch('cli.PromptSession.prompt', side_effect=["hello", "quit"])


    def test_main_loop(self, mock_print, mock_prompt, mock_ask_to_save_message):
        with patch('cli.ask_to_save_message', return_value="no") as mock_ask_to_save_message, \
             patch('cli.PromptSession.prompt', side_effect=["Hello! How can I assist you today?", "quit"]) as mock_prompt, \
             patch('builtins.print') as mock_print:

            def mock_is_asking_about_history(input_text):
                return False

            cli.is_asking_about_history = mock_is_asking_about_history
            print("Before calling main")
            cli.main()
            print("After calling main")
            mock_prompt.assert_called_with("You: ")
            mock_print.assert_any_call("ChatGPT is ready to chat!")
        # Check if the methods were called with the expected arguments
        # mock_dal.start_conversation.assert_called_once_with(1, "Hello, ChatGPT!")
        # mock_dal.send_message.assert_called_once_with(1, "user", "Hello, ChatGPT!")

        # # Check if the output is as expected
        # mock_print.assert_any_call("ChatGPT is ready to chat!")
        # mock_print.assert_any_call("Goodbye!")
        # mock_print.assert_any_call("ChatGPT: Hello, user!")

if __name__ == "__main__":
    unittest.main()
