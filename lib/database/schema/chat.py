from sqlalchemy import Column, Integer

from . import Base
from schema.message import Message


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
