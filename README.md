# gpt2apiserver
A local server that uses a fixed pyChatGPT library to allow API calls to ChatGPT Website.

You will need an ENV var  "CHATGPT_TOKEN" with your chatGPT access token.
This can be extracted from your local storage.

WIP. send_message currently takes POST data "message" and "id" and returns an 
object in the format returned by the OPENAI chat/completions endpoint. For a 
new conversation, send id "0". To continue a conversation, send the chat id.
reset_conversation also works, it starts a new conversation. Other functions
are currently untested.
