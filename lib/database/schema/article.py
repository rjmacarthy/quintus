from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PostmanArticle(Base):
    __tablename__ = "postman_articles"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    html_url = Column(String)
    author_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    name = Column(String)
    title = Column(String)
    locale = Column(String)
    edited_at = Column(DateTime)
    body = Column(String)
