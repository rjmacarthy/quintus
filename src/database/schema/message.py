from sqlalchemy import Column, Integer, String, ForeignKey

from . import Base


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    message = Column(String)
    time = Column(String)
    entity = Column(String)
