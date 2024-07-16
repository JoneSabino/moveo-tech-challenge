from __future__ import annotations
from typing import List, Optional, Any
from pydantic import BaseModel


class Option(BaseModel):
    text: str
    label: str


class Response(BaseModel):
    type: str
    texts: List[str]
    options: Optional[List[Option]] = None


class ResponseModel(BaseModel):
    responses: Optional[List[Response]] = None
    output: Optional[Any] = None

def create_response(joke:str) -> ResponseModel:
    return ResponseModel(responses=[
        Response(type="text", texts=[joke])
    ])

def err_response(message: str) -> ResponseModel:
    return ResponseModel(responses=[], output={"error": message})