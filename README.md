## gptMemory README

### Introduction
gptMemory is a conversational AI program built to engage with users and provide helpful responses to their prompts.

### Core functionality

The program uses PostgreSQL to store user information, conversation histories, and messages. Users can start new conversations, continue existing conversations, and ask about past conversations.

The program prompts the user to enter a message, responds with an appropriate message using NLP and deep learning techniques, and saves the message with the conversation history if desired.

### Requirements
 - Python 3.x
 - prompt_toolkit
 - configparser
 - psycopg2

### Configuration
- Rename ```config-example.ini``` to ```config.ini```
- Fill out the database credentials in ```config.ini```

### How to run
- Run ```main.py``` to start the program
- Follow the on-screen prompts to start a new conversation, continue an existing one, or quit the program.