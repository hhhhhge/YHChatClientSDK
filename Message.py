import uuid
from typing import *


class MessageSegment:
    @staticmethod
    def text(text: str, *, buttons: List[List[dict] | dict] = None):
        if not text or text.isspace():
            raise ValueError("text cannot be empty")
        message = {"contentType": "text", "content": {"text": text}}
        if buttons is not None:
            message["content"]["buttons"] = buttons
        return message

    @staticmethod
    def markdown(text: str, *, buttons: List[List[dict] | dict] = None):
        if not text or text.isspace():
            raise ValueError("text cannot be empty")
        message = {"contentType": "markdown", "content": {"text": text, "buttons": buttons}}
        if buttons is not None:
            message["content"]["buttons"] = buttons
        return message

    @staticmethod
    def image(*, fileName: str = None, fileUrl: str, buttons: List[List[dict] | dict] = None):
        if not fileUrl or fileUrl.isspace():
            raise ValueError("fileUrl cannot be empty")
        message = {"contentType": "image", "content": {"imageUrl": fileUrl, "buttons": buttons}}
        if buttons is not None:
            message["content"]["buttons"] = buttons
        return message

    @staticmethod
    def file(*, fileName: str = uuid.uuid4(), fileUrl: str, buttons: List[List[dict] | dict] = None):
        if not fileUrl or fileUrl.isspace():
            raise ValueError("fileUrl cannot be empty")
        message = {"contentType": "file", "content": {"fileName": fileName, "fileUrl": fileUrl, "buttons": buttons}}
        if buttons is not None:
            message["content"]["buttons"] = buttons
        return message

    @staticmethod
    def button(*, text: str, actionType: int, url: str = "", value: str = ""):
        if actionType == 1:
            if not url or url.isspace():
                raise ValueError("url cannot be empty")
        elif actionType == (2 or 3):
            if not value or value.isspace():
                raise ValueError("value cannot be empty")
        return {"actionType": actionType, "content": {"text": text, "url": url, "value": value}}
