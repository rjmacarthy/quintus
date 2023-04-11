import os
from sqlalchemy import create_engine
from models import Base

password = os.environ.get("PGPASSWORD") or "password"
user = os.environ.get("PGUSER") or "postgres"
database = os.environ.get("PGDATABASE") or "embeddings"
host = os.environ.get("PGHOST") or "localhost"
port = os.environ.get("PGPORT") or 5432


def get_uri(db_name):
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def create_database(db_name: str):
    uri = get_uri(db_name)
    if engine.dialect.has_schema(engine, db_name):
        return
    engine = create_engine(uri)
    engine.execute(f"CREATE DATABASE {db_name}")


def get_engine(
    db_name: str = database,
):
    create_database(db_name)

    engine = create_engine(db_name)
    Base.metadata.create_all(engine)
    return engine