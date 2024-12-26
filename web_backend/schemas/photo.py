from .message import Message


class PhotoUploaded(Message):
    filename: str
