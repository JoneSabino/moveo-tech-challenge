from pydantic import BaseModel
from typing import List, Any


class IntentModel(BaseModel):
    intent: str
    confidence: float


class ContextModel(BaseModel):
    joke_language_value: str


class InputModel(BaseModel):
    text: str


class RequestModel(BaseModel):
    lang: str
    intents: List[IntentModel]
    context: ContextModel

    class Config:
        extra = "ignore"


def get_joke_language(payload: Any) -> str:
    model = RequestModel(**payload)
    if model.context and model.context.joke_language_value:
        return model.context.joke_language_value
    return "en"