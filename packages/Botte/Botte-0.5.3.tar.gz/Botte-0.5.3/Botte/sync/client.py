import requests
import json
from .markdown import parse_markdown, unparse_html
from .keyboard import Keyboard

class TelegramClient:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.offset = None
        self.command_handlers = {}  # Dictionary to store command handlers
        self.openai_api_key = None
        self.openai_model = "gpt-3.5-turbo"

    def enable_openai_integration(self, openai_api_key, openai_model="gpt-3.5-turbo"):
        """Optionally enable OpenAI integration by providing an API key."""
        self.openai_api_key = openai_api_key
        self.openai_model = openai_model
        try:
            import openai
            openai.api_key = self.openai_api_key
            self.openai_available = True
        except ImportError:
            self.openai_available = False
            print("OpenAI library is not installed. Please install openai to use this feature.")

    def listen_for_messages(self, handler):
        while True:
            updates = self.get_updates(self.offset)
            for update in updates.get('result', []):
                chat_id = update['message']['chat']['id']
                text = update['message'].get('text', '')
                handler(self, chat_id, text)
                self.offset = update['update_id'] + 1

    def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        # Ensure the URL for sending a message is correctly formatted.
        url = self.base_url + "sendMessage"
        
        # Prepare the data payload for the request.
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "reply_markup": reply_markup
        }
        
        # Validate the parse_mode before proceeding.
        if parse_mode not in ["Markdown", "MarkdownV2", "HTML", None]:
            # If parse_mode is invalid, raise a ValueError.
            raise ValueError(f"Unsupported parse_mode: {parse_mode}")
        
        # Make the POST request to the Telegram API to send the message.
        response = requests.post(url, json=data)
        
        # Optional: Check the response for success and handle errors.
        if not response.ok:
            print(f"Failed to send message: {response.text}")
        else:
            print(f"Message sent successfully: {response.json()}")
    
    def send_photo(self, chat_id, photo, caption=None, parse_mode=None):
        url = self.base_url + "sendPhoto"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'photo': open(photo, 'rb')}  # Ensure 'photo' is the path to the photo file
        requests.post(url, data=data, files=files)


    def send_audio(self, chat_id, audio, caption=None, parse_mode=None):
        url = self.base_url + "sendAudio"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'audio': open(audio, 'rb')}
        requests.post(url, data=data, files=files)

    def send_video(self, chat_id, video, caption=None, parse_mode=None):
        url = self.base_url + "sendVideo"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'video': open(video, 'rb')}
        requests.post(url, data=data, files=files)

    def send_document(self, chat_id, document, caption=None, parse_mode=None):
        url = self.base_url + "sendDocument"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'document': open(document, 'rb')}
        requests.post(url, data=data, files=files)

    # Inside TelegramClient class in client.py

    def add_keyboard(self, chat_id, text, keyboard_options):
        reply_markup = Keyboard.create_reply_keyboard(keyboard_options)
        self.send_message(chat_id, text, reply_markup=reply_markup)

    def close_keyboard(self, chat_id, text="Keyboard closed"):
        reply_markup = Keyboard.create_remove_keyboard()
        self.send_message(chat_id, text, reply_markup=reply_markup)

    # Add more methods as needed for inline buttons, removing keyboards, handling commands, etc.
    def openai_chat(self, chat_id, message):
        """Generates a response using OpenAI and sends it back to the user, if enabled."""
        if not hasattr(self, 'openai_available') or not self.openai_available:
            self.send_message(chat_id, "OpenAI integration is not enabled.")
            return
        
        try:
            import openai
            response = openai.ChatCompletion.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
            ]
        )
            if response.choices:
                self.send_message(chat_id, response.choices[0].message['content'])
            else:
                self.send_message(chat_id, "I'm not sure how to respond to that.")
        except Exception as e:
            print(f"Error using OpenAI: {e}")
            self.send_message(chat_id, "Sorry, I couldn't process that. Please try again.")


    def modify_openai(self, model="gpt-3.5-turbo"):
        """Allows users to modify the OpenAI model used for chat responses."""
        self.openai_model = model

    def register_command(self, command, handler):
        """Register a command and its handler function."""
        self.command_handlers[command] = handler

    def handle_message(self, chat_id, text):
        """Default message handler."""
        if text.startswith("/") and text.split(" ")[0] in self.command_handlers:
            command = text.split(" ")[0]
            self.command_handlers[command](self, chat_id, text)
        elif text.startswith("/start"):
            self.send_message(chat_id, "Hello! I'm a Botte! Congratulations! for creating your new bot.")
        else:
            self.send_message(chat_id, "This is not a valid command")


    def get_updates(self, offset=None, timeout=30):
        url = self.base_url + "getUpdates"
        params = {"offset": offset, "timeout": timeout}
        response = requests.get(url, params=params)
        return response.json()
    
    def markdown_message(self, chat_id, markdown_text):
        """Sends a message with Markdown formatting converted to HTML."""
        html_text = parse_markdown(markdown_text)
        self.send_message(chat_id, html_text, parse_mode="HTML")

def runbot(token, message_handler):
    client = TelegramClient(token)
    client.listen_for_messages(message_handler)
    client.enable_openai_integration('your_openai_api_key')
