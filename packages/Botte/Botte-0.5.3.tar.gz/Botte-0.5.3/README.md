# Botte
The most easiest telegram package that helps you to connect with the telegram api.

# Example How to send message

```
!pip install botte

```
```

from telegram_client.client import runbot

def my_message_handler(client, chat_id, text):
    # Define how you want to handle incoming messages here
    # For example, echoing the received message back to the user:
    client.send_message(chat_id, f"Echo: {text}")

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
token = 'YOUR_BOT_TOKEN'
runbot(token, my_message_handler)

```
