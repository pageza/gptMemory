[] Change logic, we don't need to tell the chat about a user id, let the application handle that, just send the relevant message history.
[] when saving messages we can probably ignore very short ones and also only save messages that are selected
[] Modify the data access layer to use a 'User' parameter 