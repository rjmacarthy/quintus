from sqlalchemy import Column, Integer, String
from . import Base


class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class OpenAIProvider(Provider):
    __tablename__ = "openai_providers"
    model_engine = Column(String)
