from marshmallow_dataclass import dataclass, class_schema
from typing import List
from dataclasses import field


@dataclass
class Message:
    content: str
    role: str = "system"


@dataclass
class GPTModel:
    messages: List[Message]
    model: str = "gpt-3.5-turbo-16k"
    temperature: float = 0.6
    top_p: float = 0.4
    presence_penalty: float = 0.6
    n: int = 1


@dataclass
class ResponseFormat:
    type: str = "json_object"


@dataclass
class GPTTurboJson(GPTModel):
    model: str = "gpt-3.5-turbo-1106"
    # response_format: ResponseFormat = field(default_factory=ResponseFormat)


@dataclass
class GPTMessage:
    role: str = "system"
    content: str = "Sorry Something went wrong!"


@dataclass
class GPTChoices:
    index: int
    message: GPTMessage
    finish_reason: str


@dataclass
class GPTUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass
class GPTResponse:
    id: str
    object: str
    created: int
    model: str
    choices: list[GPTChoices]
    usage: GPTUsage
    system_fingerprint: str

    def get_message(self):
        message = self.choices[0].message.content
        return message


GPTResponseSchema = class_schema(GPTResponse)()
