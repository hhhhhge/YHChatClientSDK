from typing import *
from Message import MessageSegment
import httpx

token = ""
client = httpx.Client(base_url="https://chat-go.jwzhd.com/open-apis/v1/bot",
                      headers={"Content-Type": "application/json; charset=utf-8"})


def send_message(*, recv_type, recv_id, message: dict):
    global client
    data = {"recvType": recv_type, "recvId": recv_id, **message}
    data = client.post("/send", params={"token": token}, json=data).json()
    if data["code"] != 1:
        raise ValueError(data["msg"])
    else:
        return data["data"]
