import requests
from .markdown import parse_markdown
from .keyboard import Keyboard
import logging

class TelegramClient:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.offset = None
        self.command_handlers = {}
        self.logger = logging.getLogger(__name__)

    def listen_for_messages(self, handler):
        while True:
            try:
                updates = self.get_updates(self.offset)
                for update in updates.get('result', []):
                    chat_id = update['message']['chat']['id']
                    text = update['message'].get('text', '')
                    handler(self, chat_id, text)
                    self.offset = update['update_id'] + 1
            except Exception as e:
                self.logger.exception("Error in listening for messages: %s", e)

    def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        url = self.base_url + "sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": parse_mode, "reply_markup": reply_markup}
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            self.logger.info("Message sent successfully: %s", response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send message: %s", e)

    def send_photo(self, chat_id, photo, caption=None, parse_mode=None):
        url = self.base_url + "sendPhoto"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'photo': open(photo, 'rb')}
        try:
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            self.logger.info("Photo sent successfully: %s", response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send photo: %s", e)

    def send_audio(self, chat_id, audio, caption=None, parse_mode=None):
        url = self.base_url + "sendAudio"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'audio': open(audio, 'rb')}
        try:
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            self.logger.info("Audio sent successfully: %s", response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send audio: %s", e)

    def send_video(self, chat_id, video, caption=None, parse_mode=None):
        url = self.base_url + "sendVideo"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'video': open(video, 'rb')}
        try:
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            self.logger.info("Video sent successfully: %s", response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send video: %s", e)

    def send_document(self, chat_id, document, caption=None, parse_mode=None):
        url = self.base_url + "sendDocument"
        data = {"chat_id": chat_id, "caption": caption, "parse_mode": parse_mode}
        files = {'document': open(document, 'rb')}
        try:
            response = requests.post(url, data=data, files=files)
            response.raise_for_status()
            self.logger.info("Document sent successfully: %s", response.json())
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to send document: %s", e)

    def add_keyboard(self, chat_id, text, keyboard_options):
        reply_markup = Keyboard.create_reply_keyboard(keyboard_options)
        self.send_message(chat_id, text, reply_markup=reply_markup)

    def close_keyboard(self, chat_id, text="Keyboard closed"):
        reply_markup = Keyboard.create_remove_keyboard()
        self.send_message(chat_id, text, reply_markup=reply_markup)

    def register_command(self, command, handler):
        self.command_handlers[command] = handler

    def handle_message(self, chat_id, text):
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
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error("Failed to get updates: %s", e)

    def markdown_message(self, chat_id, markdown_text):
        html_text = parse_markdown(markdown_text)
        self.send_message(chat_id, html_text, parse_mode="HTML")

def runbot(token, message_handler):
    client = TelegramClient(token)
    client.listen_for_messages(message_handler)
    client.enable_openai_integration('your_openai_api_key')
