import logging
from discord.message import Message
from discord.client import Client
import discord
from services.logger import logger
from .config import BotConfig as BOT_CFG
from .config import AppConfig as APP_CFG
from .config import PRIVATE_MESSAGE_PREFIX
from .responses import MessageHandler

intents = discord.Intents.default()
intents.message_content = True


class Bot:
    def __init__(self) -> None:
        self.client = Client(intents=intents)
        self.message_handler = MessageHandler()
        self.register_events()

    async def send_message(self, message: Message, is_private: bool):
        try:
            response = self.message_handler.make_response(message)
            if not response:
                return
            await message.author.send(response) if is_private else await message.channel.send(response)
            self.handle_app_debug_mode(f"Sent message: {response}")
        except Exception as e:
            logger.log_message(logging.ERROR, f"Error: {e}")
            return

    def register_events(self):
        @self.client.event
        async def on_ready():
            self.handle_app_debug_mode(f' {BOT_CFG.name} is now running!')

        @self.client.event
        async def on_message(message: Message):
            if message.author == self.client.user:
                return
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel.name) # type: ignore

            self.handle_app_debug_mode(f"{username} said: {user_message} in {channel}")

            if self.check_if_is_private_message(user_message):
                await self.send_message(message, True)
            else:
                await self.send_message(message, False)

    def check_if_is_private_message(self, message) -> bool:
        prefix = message[0]
        if any([letter in PRIVATE_MESSAGE_PREFIX for letter in prefix]):
            return True
        return False

    def handle_app_debug_mode(self, message):
        if APP_CFG.DEBUG:
            logger.log_message(logging.INFO, message)

    def run_bot(self):
        token = BOT_CFG.TOKEN
        self.client.run(token)
