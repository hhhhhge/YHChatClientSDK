import httpx
from typing import *

from message import MessageSegment, MessageType, add_message_record, query_message_record, delete_message_record


class Openapi:
    def __init__(self, token: str) -> None:
        self.client = httpx.Client(base_url="https://chat-go.jwzhd.com/open-apis/v1", params={"token": token})

    def _message_decode(self, message: MessageSegment):
        match message.type:
            case MessageType.text:
                return {"text": message.text}

            case MessageType.image:
                resp = self.client.post(
                    "/image/upload",
                    files={"image": bytes(message.image)}
                ).json()
                if resp["code"] == 1:
                    return {"imageKey": resp["data"]["imageKey"]}
                else:
                    raise ValueError(resp["msg"])

            case MessageType.video:
                resp = self.client.post(
                    "/video/upload",
                    files={"video": bytes(message.video)}
                ).json()
                if resp["code"] == 1:
                    return {"videoKey": resp["data"]["videoKey"]}
                else:
                    raise ValueError(resp["msg"])

            case MessageType.file:
                resp = self.client.post(
                    "/file/upload",
                    files={"file": bytes(message.file)}
                ).json()
                if resp["code"] == 1:
                    return {"fileKey": resp["data"]["fileKey"]}
                else:
                    raise ValueError(resp["msg"])

            case MessageType.markdown:
                return {"text": message.markdown}

            case MessageType.html:
                return {"text": message.html}

    def send_message(
            self,
            recv_type: str,
            recv_id: str,
            message: MessageSegment | List[MessageSegment],
            parent_id: str = None
    ):
        if isinstance(message, MessageSegment):
            message_list = [message]
        elif isinstance(message, list):
            message_list = message
        else:
            raise ValueError("content must be MessageSegment or List[MessageSegment]")

        return_list = []

        for message in message_list:
            resp = self.client.post(
                "/bot/send",
                json={
                    "recvType": recv_type,
                    "recvId": recv_id,
                    "parentId": parent_id,
                    "contentType": message.type.value,
                    "content": self._message_decode(message)
                }
            ).json()

            if resp["code"] == 1:
                message_record = resp["data"]["messageInfo"]
                add_message_record(message_record["msgId"], message_record["recvType"], message_record["recvId"])
                return_list.append(message_record)
            elif isinstance(message, MessageSegment):
                raise ValueError(resp["msg"])

        return return_list

    def edit_message(self, msg_id: str, message: MessageSegment, recv_type: str = None, recv_id: str = None):
        message_record = query_message_record(msg_id)
        return self.client.post(
            "/bot/edit",
            json={
                "msgId": msg_id,
                "recvType": recv_type or message_record.recv_type,
                "recvId":  recv_id or message_record.recv_id,
                "contentType": message.type.value,
                "content": self._message_decode(message)
            }
        ).json()

    def delete_message(self, msg_id: str, recv_type: str = None, recv_id: str = None):
        message_record = delete_message_record(msg_id)
        return self.client.post(
            "/bot/edit",
            json={
                "msgId": msg_id,
                "recvType": recv_type or message_record.recv_type,
                "recvId":  recv_id or message_record.recv_id,
            }
        ).json()

    def get_message(self, chat_type: str, chat_id: str, msg_id: str = None, before: int = 0, after: int = 0):
        return self.client.get(
            "/bot/messages",
            params={
                "chat-type": chat_type,
                "chat-id": chat_id,
                "msg-id": msg_id,
                "before": before,
                "after": after
            }
        ).json()
