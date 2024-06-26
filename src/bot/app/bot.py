import tracemalloc
import logging
from discord.message import Message
from discord.client import Client
import discord
import queue
import asyncio

from services.logger import logger
from .config import BotConfig as BOT_CFG
from .config import PRIVATE_MESSAGE_PREFIX
from .responses import MessageHandler

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

tracemalloc.start()


class DiscordBot:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DiscordBot, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not hasattr(self, '_initialized'):
            self._initialized = True
        self.message_queue = queue.Queue()
        self.client = Client(intents=intents)
        self.message_handler = MessageHandler()
        self.register_events()

    async def send_message(self, message: Message, is_private: bool):
        try:
            response = await self.message_handler.make_response(message)
            if not response:
                return
            await message.author.send(response) if is_private else await message.channel.send(response)
            await self.handle_app_debug_mode(f"Sent message: {response}")
        except Exception as e:
            await logger.log_message(logging.ERROR, f"Error: {e}")
            return

    def register_events(self):
        @self.client.event
        async def on_ready():
            asyncio.create_task(self.process_queue_items())
            # await self.send_message_to_user(BOT_CFG.BOT_ID, f'{BOT_CFG.name} is now running!')
            await self.send_message_to_user(BOT_CFG.OWNER_ID, f'{BOT_CFG.name} is now running!')

        @self.client.event
        async def on_message(message: Message):
            try:
                if message.author == self.client.user:
                    return

                if message.content == 'restart':
                    await self.restart_bot_memory()

                await self.handle_app_debug_mode(message)

                if self.check_if_is_private_message(message):
                    # message.content = f'{BOT_NAME} {message.content}'
                    await self.send_message(message, True)
                else:
                    await self.send_message(message, False)
            except Exception as e:
                await logger.log_message(logging.ERROR, f"Error: {e}")
                return

    async def send_message_to_user(self, user_id: int, message: str):
        try:
            user = await self.client.fetch_user(user_id)
            if user:
                await user.send(message)
            else:
                await logger.log_message(logging.INFO, f"User {user_id} not found")
        except Exception as e:
            await logger.log_message(logging.ERROR, f"Error sending message to user {user_id}: {e}")

    async def handle_external_request(self, data):
        if data['message'] and type(data['message']) == str:
            await self.send_message_to_user(BOT_CFG.OWNER_ID, data['message'])

    async def process_queue_items(self):
        while True:
            request = await asyncio.to_thread(self.message_queue.get)
            if request:
                await logger.log_message(logging.INFO, f"Received message from queue: {request}")
                await self.handle_external_request(request)

    def check_if_is_private_message(self, message) -> bool:
        user_message = str(message.content)
        prefix = user_message[0]

        if any([letter in PRIVATE_MESSAGE_PREFIX for letter in prefix]):
            return True
        if message.channel.type == discord.ChannelType.private:
            return True
        return False

    async def handle_app_debug_mode(self, message):
        # if APP_CFG.DEBUG:
        #     await logger.log_message(logging.DEBUG, message)
        pass

    async def restart_bot_memory(self):
        await self.message_handler.lost_memory()
        await logger.log_message(logging.INFO, "Restarting bot...")

    def run_bot(self):
        token = BOT_CFG.TOKEN
        self.client.run(token)
