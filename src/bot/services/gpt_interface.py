import json
from dataclasses import asdict
from pathlib import Path
import logging

from .connection import HTTPSConnectionClient
from .services_config import services_config as config
from .gpt_prompt_shortener import GPTPromptShortener
from .logger import logger

from .schemas.gpt_schemas import (
    GPTModel,
    GPTTurboJson,
    Message,
    GPTMessage,
    GPTResponseSchema,
)


class GPTInterface:
    def __init__(self) -> None:
        self.prompts: dict[str, str] = {}
        self.prompt_folder = Path(__file__).parent / "gpt_prompts"
        self.prompt_shortener = GPTPromptShortener()
        self.load_prompts()

        self.api_endpoint = "/v1/chat/completions"
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

    def send_request_to_gpt(self, base_prompt: str) -> GPTMessage:
        """
        Sends a request to the OpenAI API and returns the response.
        """
        request_body = GPTTurboJson(
            messages=[Message(content=f"{base_prompt}")]
        )
        request_body = self.set_max_prompt_length(request_body)

        request = json.dumps(asdict(request_body))

        with HTTPSConnectionClient("api.openai.com") as conn:
            try:
                conn.request("POST", self.api_endpoint, request, self.headers)
                response = conn.getresponse()
                data = response.read().decode("utf-8")
                data = json.loads(data)
                gpt_response = GPTResponseSchema.load(data)
                logger.log_message(logging.INFO, f"Response: {gpt_response}")
                return gpt_response.get_message()
            except Exception as e:
                return GPTMessage()

    def testing_prompt(self, prompt_content: str):
        base_prompt = self.prompts.get("question", "")
        base_prompt = base_prompt.replace("<question>", prompt_content)
        response = self.send_request_to_gpt(base_prompt)
        return response
