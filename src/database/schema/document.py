from sqlalchemy import Column, Integer, String
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column

from . import Base


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    doc_id = Column(String)
    doc_text = Column(String)
    doc_url = Column(String)
    doc_title = Column(String)
    embedding = mapped_column(Vector(768))
