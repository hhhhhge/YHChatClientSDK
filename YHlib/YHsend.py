import json
from typing import List, Optional
from loguru import logger

import httpx
from pydantic import BaseModel, Field


class Button(BaseModel):
    text: str = Field(..., description="按钮上的文字")
    actionType: int = Field(..., description="1: 跳转URL 2: 复制 3: 点击汇报")
    url: str = Field(None, description="当actionType为1时使用")
    value: str = Field(None, description="当actionType为2时，该值会复制到剪贴板 当actionType为3时，该值会发送给订阅端")


class Content(BaseModel):
    text: str = Field(None, description="消息正文")
    imageUrl: str = Field(None, description="图片URL")
    fileName: str = Field(None, description="文件名")
    fileUrl: str = Field(None, description="文件URL")
    buttons: Optional[List[List[Button]]] = Field(None, description="消息中包括button")


class Data(BaseModel):
    msgId: Optional[str] = Field(None, description="消息ID")
    recvId: str | List[str] = Field(..., description="接收消息对象ID 用户: userId 群: groupId")
    recvType: str = Field(..., description="接收对象类型 用户: user 群: group")
    contentType: str = Field(..., description="消息类型，取值如下 text,image,file,markdown")
    content: Content = Field(..., description="消息对象")
    before: Optional[int] = Field(None, description="指定消息ID前N条，默认0条")
    after: Optional[int] = Field(None, description="指定消息ID后N条，默认0条")


class Response(BaseModel):
    code: int = Field(..., description="响应代码")
    msg: str = Field(..., description="响应信息，包括异常信息")
    data: Optional[object] = Field(None, description="返回数据")


token = ""


class TokenEmptyError(Exception):
    pass


class YHClient:
    def __init__(self, token_: str = token):
        if token_ == "":
            raise TokenEmptyError("token不能为空")
        else:
            self.token = token_
        self.headers = {'Content-Type': 'application/json'}
        self.client = httpx.Client(base_url=f"https://chat-go.jwzhd.com/open-apis/v1/bot/", headers=self.headers,
                                   params={"token": f"{self.token}"})

    def send_msg(self, data: dict):
        Data(**data)
        logger.info(data)
        resp = self.client.post(url=f"/send", json=data)
        Response(**resp.json())

        code = resp.json()["code"]
        msg = resp.json()["msg"]
        if code == 1:
            data = resp.json()["data"]
        else:
            data = None
        return code, msg, data

    def batch_send_msg(self, data: dict):
        Data(**data)
        logger.debug(data)
        resp = self.client.post(url=f"/batch_send", json=data)
        Response(**resp.json())

        code = resp.json()["code"]
        msg = resp.json()["msg"]
        if code == 1:
            data = resp.json()["data"]
        else:
            data = None
        return code, msg, data

    def edit_msg(self, data: dict):
        Data(**data)
        logger.debug(data)
        resp = self.client.post(url=f"/edit", json=data)
        Response(**resp.json())

        code = resp.json()["code"]
        msg = resp.json()["msg"]
        if code == 1:
            data = resp.json()["data"]
        else:
            data = None
        return code, msg, data

    def query_msg(self, data: dict):
        Data(**data)
        logger.debug(data)
        params = {
            "chat-id": data["recvId"],
            "chat-type": data["recvType"],
            "message-id": data["msgId"],
            "before": data["before"],
            "after": data["after"],
        }
        resp = self.client.post(url=f"/messages", json=data, params=params)
        Response(**resp.json())

        code = resp.json()["code"]
        msg = resp.json()["msg"]
        if code == 1:
            data = resp.json()["data"]
        else:
            data = None
        return code, msg, data

    