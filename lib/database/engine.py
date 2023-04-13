import os
from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base

from database.schema import Base

PGPASSWORD = os.environ.get("PGPASSWORD") or "password"
PGUSER = os.environ.get("PGUSER") or "postgres"
PGDATABASE = os.environ.get("PGDATABASE") or "embeddings"
PGHOST = os.environ.get("PGHOST") or "localhost"
PGPORT = os.environ.get("PGPORT") or 5432


def get_uri(db_name):
    return f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{db_name}"


def get_engine(
    db_name: str = PGDATABASE,
):
    engine: Engine = create_engine(get_uri(db_name))

    if not database_exists(engine.url):
        create_database(engine.url)

    with engine.connect() as con:
        con.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        con.commit()

    Base.metadata.create_all(engine)

    return engine
