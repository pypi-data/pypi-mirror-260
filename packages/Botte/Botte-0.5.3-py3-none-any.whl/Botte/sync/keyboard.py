# keyboard.py
import json

class Keyboard:
    @staticmethod
    def create_reply_keyboard(keyboard_options, resize_keyboard=True, one_time_keyboard=True):
        reply_markup = {
            "keyboard": keyboard_options,
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard
        }
        return json.dumps(reply_markup)

    @staticmethod
    def create_remove_keyboard():
        reply_markup = {"remove_keyboard": True}
        return json.dumps(reply_markup)

    @staticmethod
    def modify_reply_markup(chat_id, message_id, reply_markup):
        # This functionality is more about modifying an existing message's reply markup,
        # which may not necessarily belong in a keyboard utility class.
        # Consider keeping it in TelegramClient or another class that handles message updates.
        return json.dumps(reply_markup)
