import aiohttp
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AsyncTelegramClient:
    def __init__(self, token):
        self.base_url = f"https://api.telegram.org/bot{token}/"
        self.session = aiohttp.ClientSession()
        self.offset = None

    async def listen_for_messages(self, handler):
        while True:
            try:
                updates = await self.get_updates(self.offset)
                for update in updates.get('result', []):
                    chat_id = update['message']['chat']['id']
                    text = update['message'].get('text', '')
                    await handler(self, chat_id, text)
                    self.offset = update['update_id'] + 1
            except Exception as e:
                logger.error(f"Error in listen_for_messages: {e}")
                await asyncio.sleep(1)

    async def send_message(self, chat_id, text, parse_mode=None, reply_markup=None):
        try:
            url = self.base_url + "sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "reply_markup": reply_markup
            }
            async with self.session.post(url, data=data) as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Error in send_message: {e}")

    async def get_updates(self, offset=None):
        try:
            url = self.base_url + "getUpdates"
            params = {"offset": offset} if offset else {}
            async with self.session.get(url, params=params) as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Error in get_updates: {e}")
            return {}
        
    async def _send_request(self, method, params, is_file=False):
        url = self.base_url + method
        try:
            if is_file:
                # Assuming one of the params is a file path for simplicity
                file_param = next((key for key in params if isinstance(params[key], str) and params[key].startswith("file_")), None)
                if file_param:
                    with open(params[file_param], 'rb') as file:
                        params[file_param] = file
                        async with self.session.post(url, data=params) as response:
                            response.raise_for_status()
                            print(await response.json())
            else:
                async with self.session.post(url, json=params) as response:
                    response.raise_for_status()
                    print(await response.json())
        except aiohttp.ClientResponseError as e:
            print(f"Failed to send {method}: {e.message}")
        except Exception as e:
            print(f"An error occurred: {e}")

    async def close(self):
        await self.session.close()

async def runbot(token, message_handler):
    client = AsyncTelegramClient(token)
    await client.listen_for_messages(message_handler)
    await client.close()
