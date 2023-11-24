import tiktoken

from .schemas.gpt_schemas import GPTModel


class GPTPromptShortener:
    def shorten_prompt(self, gpt_request: GPTModel) -> GPTModel:
        """
        Shortens the prompt if it is too long.
        """
        self.token_limit = self.get_token_limit(gpt_request.model)
        gpt_request = self.get_shorten_prompt(gpt_request)
        return gpt_request

    def get_shorten_prompt(self, request: GPTModel) -> GPTModel:
        message = request.messages[0]
        tokens = self.encode_tokens(message.content, request.model)

        if len(tokens) > self.token_limit:
            tokens = tokens[: self.token_limit - 150]
        message.content = self.decode_tokens(tokens, request.model)
        request.messages[0] = message
        return request

    def encode_tokens(self, text: str, model: str) -> list[int]:
        """
        Encode the text to tokens.
        """
        enc = tiktoken.encoding_for_model(model)
        tokens = enc.encode(text)
        return tokens

    def decode_tokens(self, tokens: list[int], model: str):
        """
        Decode the tokens to text.
        """
        enc = tiktoken.encoding_for_model(model)
        text = enc.decode(tokens)
        return text

    def get_token_limit(self, model) -> int:
        match model:
            case "gpt-3.5-turbo-16k": return 16384
            case "gpt-3.5-turbo-1106": return 16384
            case _: raise NotImplementedError
