from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    messages = relationship("Message", backref="chat")
