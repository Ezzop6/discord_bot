from discord.message import Message
import random
import discord

from .config import PRIVATE_MESSAGE_PREFIX, BotConfig
from services.gpt_interface import GPTInterface


class MessageHandler:
    def __init__(self):
        self.interface = GPTInterface()
        self.commands = {
            'roll': self.roll,
            'help': self.help,
            'restart': self.lost_memory,
            f'{BotConfig.name}': self.answer,
        }

    async def make_response(self, message: Message):
        if message.content[0] in PRIVATE_MESSAGE_PREFIX:
            message.content = message.content[1:]
        self.message = message
        return await self.handle_response()

    async def handle_response(self):
        message = self.message.content.lower()

        if message.split(' ')[0] in self.commands.keys():
            return await self.commands[message.split(' ')[0]]()

        elif self.message.channel.type == discord.ChannelType.private:
            return 'Private message'

    async def roll(self):
        message = self.message.content.lower()
        message = message.split(' ')
        if len(message) > 1 and message[1].isdigit():
            return str(random. randint(1, int(message[1])))

        return str(random. randint(1, 6))

    async def answer(self):
        answer = await self.interface.get_chat_response(self.message.content)
        return answer

    async def lost_memory(self):
        self.interface.lost_memory()
        return 'Bot memory has been lost.'

    async def help(self):
        return "This is a help message that you can modify."
