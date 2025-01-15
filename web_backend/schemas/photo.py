from .message import Message


class PhotoUploaded(Message):
    photo_url: str
