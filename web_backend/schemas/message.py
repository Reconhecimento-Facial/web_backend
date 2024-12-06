from pydantic import BaseModel


class Message(BaseModel):
    message: str


class HTTPExceptionResponse(BaseModel):
    detail: str
