from discord.message import Message
import random

from .config import ANSWER_WORDS, PRIVATE_MESSAGE_PREFIX


class MessageHandler:
    def __init__(self):
        self.interface = None
        self.commands = {
            'hello': self.hello,
            'roll': self.roll,
            'help': self.help,
        }

    def make_response(self, message: Message):
        if message.content[0] in PRIVATE_MESSAGE_PREFIX:
            message.content = message.content[1:]
        self.message = message
        return self.handle_response()

    def handle_response(self):
        message = self.message.content.lower()
        print(message.split(' '))

        if message.split(' ')[0] in self.commands.keys():
            return self.commands[message.split(' ')[0]]()

        for word in ANSWER_WORDS:
            if word in message:
                return f'You said {word}'

    def hello(self):
        user = self.message.author
        return f'Hello {user.mention}'

    def roll(self):
        message = self.message.content.lower()
        message = message.split(' ')
        if len(message) > 1 and message[1].isdigit():
            return str(random. randint(1, int(message[1])))

        return str(random. randint(1, 6))

    def help(self):
        return "This is a help message that you can modify."
