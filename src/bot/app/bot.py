import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import tracemalloc
import logging
from discord.message import Message
from discord.client import Client
import discord
from services.logger import logger
from .config import BotConfig as BOT_CFG
from .config import PRIVATE_MESSAGE_PREFIX
from .responses import MessageHandler

intents = discord.Intents.default()
intents.message_content = True

tracemalloc.start()


class Bot:
    def __init__(self) -> None:
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
            await self.handle_app_debug_mode(f' {BOT_CFG.name} is now running!')

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
