import os
from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base

from database.schema import Base

PGPASSWORD = "password"
PGUSER = "postgres"
PGDATABASE = "embeddings"
PGHOST = "localhost"
PGPORT = 5432


def get_uri():
    return f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"


def get_engine():
    engine: Engine = create_engine(get_uri())

    if not database_exists(engine.url):
        create_database(engine.url)

    with engine.connect() as con:
        con.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        con.commit()

    Base.metadata.create_all(engine)

    return engine
