from pydantic import BaseModel
from typing import List


class ChatHistoryResponse(BaseModel):
    chat_history: List[List[str]]


class Query(BaseModel):
    text: str


class MessageResponse(BaseModel):
    message: str
