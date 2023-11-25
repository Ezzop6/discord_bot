import tiktoken

from .services_config import services_config as config
from .project_paths import ProjectFolders
from .schemas.gpt_schemas import (
    GPTModel,
    GPTTurbo,
    GPTTurboJson,
)


class GPTPromptManager:
    def __init__(self) -> None:
        self.prompts: dict[str, str] = {}
        self.prompt_folder = ProjectFolders.bot_prompts
        self.load_prompts()

    def load_prompts(self) -> None:
        for file in self.prompt_folder.iterdir():
            if file.name.endswith(".txt"):
                file_name = file.name.split(".")[0]
                with open(file, "r") as f:
                    self.prompts[file_name] = f.read()

    def get_max_prompt_length(self, request: GPTModel, strip_end: bool = True) -> GPTModel:
        """
        Shortens the prompt if it is too long.
        Args: Side of the prompt to strip from.
        """
        message = request.messages[0]
        tokens = self.encode_tokens(message.content, request)
        token_limit = self.get_token_limit(request)

        if len(tokens) > token_limit:
            if strip_end:
                tokens = tokens[: token_limit - 150]
            else:
                token_count = len(tokens)
                tokens = tokens[abs(token_limit - token_count) + 150:]

        message.content = self.decode_tokens(tokens, request)
        request.messages[0] = message
        return request

    def encode_tokens(self, text: str, gpt: GPTModel) -> list[int]:
        """
        Encode the text to tokens.
        """
        enc = tiktoken.encoding_for_model(gpt.model)
        tokens = enc.encode(text)
        return tokens

    def decode_tokens(self, tokens: list[int], gpt: GPTModel) -> str:
        """
        Decode the tokens to text.
        """
        enc = tiktoken.encoding_for_model(gpt.model)
        text = enc.decode(tokens)
        return text

    def get_token_limit(self, gpt: GPTModel) -> int:
        match gpt.model:
            case 'gpt-3.5-turbo-16k': return 16384
            case 'gpt-3.5-turbo-1106': return 16384
            case _: raise NotImplementedError
