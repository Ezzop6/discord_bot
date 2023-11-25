from services.gpt_interface import GPTInterface
from services.schemas.gpt_schemas import GPTResponseSchema
interface = GPTInterface()


def make_response(message):
    return interface.answer(message)


prompt = ' kolik je hodin a rekni vtip'

content = make_response(prompt)

print(content)
