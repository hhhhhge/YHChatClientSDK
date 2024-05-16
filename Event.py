from urllib import parse
from typing import *

from Message import MessageSegment
import inspect

on_message_func_list: List[Callable] = []


def message_convert(data):
    content_type = data["event"]["message"]["contentType"]
    content: Dict[str, (str | List[dict])] = data["event"]["message"]["content"]
    match content_type:
        case "text":
            data = {
                "type": "text",
                "data": {"text": content["text"]}
            }
        case "markdown":
            data = {
                "type": "markdown",
                "data": {"text": content["text"]}
            }
        case "image":
            data = {
                "type": "image",
                "data": {
                    "name": parse.urlparse(content["imageUrl"]).path[1:],
                    "url": content["imageUrl"]
                }
            }
    return data


class Event:
    def __init__(self, data):
        self.event_id = data["header"]["eventId"]
        self.event_time = data["header"]["eventTime"]
        self.event_type = data["header"]["eventType"]

        match self.event_type:
            case "message.receive.normal":
                self.chat_type = data["event"]["message"]["chatType"]
                self.chat_id = data["event"]["message"]["chatId"]
                self.message_id = data["event"]["message"]["msgId"]
                self.message_parent_id = data["event"]["message"]["parentId"]
                self.message = message_convert(data)
            case "message.receive.instruction":
                self.chat_type = data["event"]["message"]["chatType"]
                self.chat_id = data["event"]["message"]["chatId"]
                self.message_id = data["event"]["message"]["msgId"]
                self.message_parent_id = data["event"]["message"]["parentId"]
                self.message = message_convert(data)

            case "bot.followed":
                pass
            case "bot.unfollowed":
                pass

            case "group.join":
                pass
            case "group.leave":
                pass

            case "button.report.inline":
                pass

            case _:
                pass


def event_handle(data: dict):
    for func in on_message_func_list:
        signature = inspect.signature(func)

        if len(signature.parameters) == 0:
            func()
        elif len(signature.parameters) == 1:
            func(Event(data))
        else:
            print(f"on_message 处理时 {func.__name__} 参数数量错误")
