from enum import Enum, StrEnum
from pydantic import BaseModel, Field, model_validator
from typing import *
from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///message.db")
Base = declarative_base()


class Message(Base):
    __tablename__ = "message"
    msg_id: int = Column(Integer, primary_key=True)
    recv_type: str = Column(String, nullable=False)
    recv_id: str = Column(String, nullable=False)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def add_message_record(msg_id: str, recv_type: str, recv_id: str):
    session = Session()
    message = Message(msg_id=int(msg_id, 16), recv_type=recv_type, recv_id=recv_id)
    session.add(message)
    session.commit()
    session.close()


def query_message_record(msg_id: str):
    session = Session()
    message = session.query(Message).filter_by(msg_id=int(msg_id, 16)).first()
    session.close()
    return message


def delete_message_record(msg_id: str):
    session = Session()
    message = session.query(Message).filter_by(msg_id=int(msg_id, 16)).first()
    session.delete(message)
    session.commit()
    session.close()
    return message


class MessageType(StrEnum):
    text = "text"
    image = "image"
    video = "video"
    file = "file"
    markdown = "markdown"
    html = "html"


class ButtonType(Enum):
    redirect = 1
    copy = 2
    callback = 3


class Button(BaseModel):
    text: str = Field(..., alias="text")
    action_type: ButtonType = Field(..., alias="actionType")


class MessageSegment(BaseModel):
    buttons: Optional[List[Button] | List[List[Button]]] = Field(None, alias="buttons")
    type: MessageType = Field(..., alias="type")
    text: Optional[str] = Field(None, alias="text")
    image: Optional[bytes] = Field(None, alias="image")
    video: Optional[bytes] = Field(None, alias="video")
    file: Optional[bytes] = Field(None, alias="file")
    markdown: Optional[str] = Field(None, alias="markdown")
    html: Optional[str] = Field(None, alias="html")
    reply: Optional[str] = Field(None, alias="reply")

    @model_validator(mode="after")
    def check_type(self):
        match self.type:
            case MessageType.text:
                if self.text is None:
                    raise ValueError("text is required when type is text")
            case MessageType.image:
                if self.image is None:
                    raise ValueError("image is required when type is image")
            case MessageType.video:
                if self.video is None:
                    raise ValueError("video is required when type is video")
            case MessageType.file:
                if self.file is None:
                    raise ValueError("file is required when type is file")
            case MessageType.markdown:
                if self.markdown is None:
                    raise ValueError("markdown is required when type is markdown")
            case MessageType.html:
                if self.html is None:
                    raise ValueError("html is required when type is html")


class MessageInfo(BaseModel):
    msg_id: str = Field(..., alias="msgId")
    recv_type: str = Field(..., alias="recvType")
    recv_id: str = Field(..., alias="recvId")
