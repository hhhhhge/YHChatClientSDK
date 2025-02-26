from pydantic import BaseModel, Field, model_validator
from concurrent.futures import ThreadPoolExecutor
from pyee.executor import ExecutorEventEmitter
from bottle import Bottle, Response, run, request

from message import MessageSegment, MessageType, add_message_record

thread_pool = ThreadPoolExecutor()
event_emitter = ExecutorEventEmitter(executor=thread_pool)

app = Bottle()


class EventHeader(BaseModel):
    event_id: str = Field(..., alias="eventId")
    event_time: int = Field(..., alias="eventTime")
    event_type: str = Field(..., alias="eventType")


class MessageEventSender(BaseModel):
    sender_id: str = Field(..., alias="senderId")
    sender_type: str = Field(..., alias="senderType")
    sender_user_level: str = Field(..., alias="senderUserLevel")
    sender_nickname: str = Field(..., alias="senderNickname")


class MessageEventChat(BaseModel):
    chat_id: str = Field(..., alias="chatId")
    chat_type: str = Field(..., alias="chatType")


class MessageEventMessage(BaseModel):
    msg_id: str = Field(..., alias="msgId")
    parent_id: str = Field(..., alias="parentId")
    send_time: int = Field(..., alias="sendTime")
    chat_id: str = Field(..., alias="chatId")
    chat_type: str = Field(..., alias="chatType")
    content_type: str = Field(..., alias="contentType")
    content: dict = Field(..., alias="content")
    message: MessageSegment = Field(None)
    command_id: int = Field(None, alias="commandId")
    command_name: str = Field(None, alias="commandName")

    @model_validator(mode="after")
    def after(self):
        self.message = MessageSegment(type=MessageType(self.content_type), **self.content)


class MessageEvent(BaseModel):
    sender: MessageEventSender = Field(..., alias="sender")
    chat: MessageEventChat = Field(..., alias="chat")
    message: MessageEventMessage = Field(..., alias="message")


@app.route("/")
def index():
    match request.json().get("header").get("eventType"):
        case "message.receive.normal":
            header = EventHeader(**request.json().get("header"))
            event = MessageEvent(**request.json().get("event"))
            add_message_record(event.message.msg_id, event.chat.chat_type, event.chat.chat_id)
            event_emitter.emit(
                "message.receive.normal",
                header,
                event
            )
        case "message.receive.instruction":
            header = EventHeader(**request.json().get("header"))
            event = MessageEvent(**request.json().get("event"))
            add_message_record(event.message.msg_id, event.chat.chat_type, event.chat.chat_id)
            event_emitter.emit(
                "message.receive.instruction",
                header,
                event
            )

    return Response(status=200)
