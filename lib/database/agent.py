from sqlalchemy import Column, Integer, String

from . import Base
from schema.message import Message


class Agent(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True)
    model = Column(String)
    description = Column(String)
