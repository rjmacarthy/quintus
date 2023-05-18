from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from . import Base


class LocalModelConfig(Base):
    __tablename__ = "local_model_config"
    id = Column(Integer, primary_key=True)
    model_name_or_path = Column(String)
    ft_model_name_or_path = Column(String)
    temperature = Column(Integer)
    top_p = Column(Integer)
    top_k = Column(Integer)
    num_beams = Column(Integer)
    max_new_tokens = Column(Integer)
    openai_api_key = Column(String)
