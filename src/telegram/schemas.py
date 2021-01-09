from typing import List, Optional

from pydantic import BaseModel, Field


class FromSchema(BaseModel):
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    language_code: str


class ChatSchema(BaseModel):
    id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    type: str


class Entities(BaseModel):
    offset: Optional[int]
    lenght: Optional[int]
    type: Optional[str]


class MessageSchema(BaseModel):
    message_id: int
    _from: Field(FromSchema, alias='from')
    chat: ChatSchema
    date: int
    text: Optional[str]
    entities: Optional[List[Entities]]


class TelegramWebHookSchema(BaseModel):
    update_id: int
    message: Optional[MessageSchema]
