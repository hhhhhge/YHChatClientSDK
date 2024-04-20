from typing import Optional, List
from fastapi import FastAPI, Body
import uvicorn
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


class Message(BaseModel):
    msgId: str = Field(..., description="消息ID，全局唯一")
    parentId: str = Field(..., description="引用消息时的父消息ID")
    sendTime: int = Field(..., description="消息发送时间，毫秒13位时间戳")
    chatId: str = Field(...,
                        description="当前聊天的对象ID: 单聊消息 chatId即对方用户ID; 群聊消息 chatId即群ID; 机器人消息 chatId即机器人ID")
    chatType: str = Field(..., description="当前聊天的对象类型: group 群聊; bot 机器人")
    contentType: str = Field(...,
                             description="当前消息类型: text 文本消息; image 图片消息; markdown Markdown消息; file 文件消息")
    content: Content = Field(..., description="消息正文，注意为字符串类型")
    commandId: int = Field(..., description="指令ID，可用来区分用户发送的指令")
    commandName: str = Field(..., description="指令名称，可用来区分用户发送的指令")


class Chat(BaseModel):
    chatId: str = Field(..., description="聊天对象ID")
    chatType: str = Field(..., description="聊天对象类型，取值: bot, group")


class Sender(BaseModel):
    senderId: str = Field(..., description="发送者ID，给用户回复消息需要该字段")
    senderType: str = Field(..., description="发送者用户类型，取值：user")
    senderUserLevel: str = Field(..., description="发送者级别，取值：owner, administrator, member, unknown")
    senderNickname: str = Field(..., description="发送者昵称")


class Header(BaseModel):
    eventId: str = Field(..., description="事件ID，全局唯一")
    eventTime: int = Field(..., description="事件产生的时间，毫秒13位时间戳")
    eventType: str = Field(..., description="事件类型")


class Event(BaseModel):
    sender: Sender = Field(..., description="发送者的信息")
    chat: Chat = Field(..., description="聊天对象信息")
    message: Message = Field(..., description="消息内容")


class Data(BaseModel):
    version: str = Field(..., description="事件内容版本号")
    header: Header = Field(..., description="包括事件的基础信息")
    event: Event = Field(..., description="包括事件的内容。 注意：Event对象的结构会在不同的eventType下发生变化")


class ButtonData(BaseModel):
    msgId: str = Field(..., description="消息ID，全局唯一")
    recvId: str = Field(..., description="接收者ID，给用户回复消息需要该字段")
    recvType: str = Field(..., description="接收者类型，取值：bot, group")
    time: int = Field(..., description="事件产生的时间，毫秒13位时间戳")
    userId: str = Field(..., description="发送者ID，给用户回复消息需要该字段")
    value: str = Field(..., description="按钮值")


message_receive_normal_func = []
message_receive_instruction_func = []
bot_followed = []
bot_unfollowed = []
group_join = []
group_leave = []
button_report_inline = []


def message_receive_normal_event(func):
    message_receive_normal_func.append(func)
    return func


def message_receive_instruction_event(func):
    message_receive_instruction_func.append(func)
    return func


def bot_followed_event(func):
    bot_followed.append(func)
    return func


def bot_unfollowed_event(func):
    bot_unfollowed.append(func)
    return func


def group_join_event(func):
    group_join.append(func)
    return func


def group_leave_event(func):
    group_leave.append(func)
    return func


def button_report_inline_event(func):
    button_report_inline.append(func)
    return func


app = FastAPI()


def run_func(i, data):
    try:
        i(data)
    except TypeError:
        i()


@app.post("/")
def _(data=Body(...)):
    if data["header"]["eventType"] == "message.receive.normal":
        for i in message_receive_normal_func:
            run_func(i, data)
    elif data["header"]["eventType"] == "message.receive.instruction":
        for i in message_receive_instruction_func:
            run_func(i, data)
    elif data["header"]["eventType"] == "bot.followed":
        for i in bot_followed:
            run_func(i, data)
    elif data["header"]["eventType"] == "bot.unfollowed":
        for i in bot_unfollowed:
            run_func(i, data)
    elif data["header"]["eventType"] == "group.join":
        for i in group_join:
            run_func(i, data)
    elif data["header"]["eventType"] == "group.leave":
        for i in group_leave:
            run_func(i, data)
    elif data["header"]["eventType"] == "button.report.inline":
        for i in button_report_inline:
            run_func(i, data)


def run(port=8080):
    uvicorn.run(app, host='0.0.0.0', port=port)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=58080)
