import json
from dataclasses import asdict
from pathlib import Path
import logging
import aiohttp

from .schemas.gpt_schemas import (
    GPTModel,
    GPTTurboJson,
    Message,
    GPTMessage,
    GPTResponseSchema,
)
from .gpt_prompt_shortener import GPTPromptShortener
from .logger import logger
from .services_config import services_config as config


class GPTInterface:
    def __init__(self) -> None:
        self.prompts: dict[str, str] = {}
        self.prompt_folder = Path(__file__).parent / "gpt_prompts"
        self.prompt_shortener = GPTPromptShortener()
        self.load_prompts()

        self.api_endpoint = "https://api.openai.com/v1/chat/completions"  # Upravil jsem endpoint, aby obsahoval celou URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.OPEN_AI_API_KEY}"
        }

    def load_prompts(self) -> None:
        for file in self.prompt_folder.iterdir():
            if file.name.endswith(".txt"):
                file_name = file.name.split(".")[0]
                with open(file, "r") as f:
                    self.prompts[file_name] = f.read()

    def set_max_prompt_length(self, request: GPTModel) -> GPTModel:
        request = self.prompt_shortener.shorten_prompt(request)
        return request

    async def send_request_to_gpt(self, base_prompt: str) -> GPTMessage:
        request_body = GPTTurboJson(
            messages=[Message(content=f"{base_prompt}")]
        )
        request_body = self.set_max_prompt_length(request_body)

        request = json.dumps(asdict(request_body))

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_endpoint, data=request, headers=self.headers) as response:
                    data = await response.text()
                    data = json.loads(data)
                    gpt_response = GPTResponseSchema.load(data)
                    return gpt_response.get_message()
            except Exception as e:
                await logger.log_message(logging.ERROR, f"Error: {e}")
                return GPTMessage()

    async def answer(self, prompt_content: str, prompt_name: str) -> GPTMessage:
        base_prompt = self.prompts.get(prompt_name, None)

        if not base_prompt:
            raise Exception(f"Prompt {prompt_name} not found!")

        base_prompt = base_prompt.replace(f"<{prompt_name}>", prompt_content)
        await logger.log_message(logging.INFO, f"Sending prompt: {base_prompt}")
        response = await self.send_request_to_gpt(base_prompt)
        return response
