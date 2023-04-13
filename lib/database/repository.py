from sqlalchemy.orm import sessionmaker
from database.engine import get_engine
from sqlalchemy.sql import select


class Repository:
    def __init__(self, model_type, db_name="embeddings"):
        self.engine = get_engine(db_name=db_name)
        Session = sessionmaker(bind=self.engine)
        self.session = Session
        self.model_type = model_type

    def create(self, **kwargs):
        entity = self.model_type(**kwargs)
        with self.session() as session:
            session.add(entity)
            session.commit()
        return entity

    def get_by_id(self, id):
        with self.session(self.engine) as session:
            entity = session.query(self.model_type).get(id)
        return entity

    def get(self):
        with self.session() as session:
            entity = session.query(self.model_type).first()
        return entity

    def search(self, embedding):
        with self.session() as session:
            entities = session.scalars(
                select(self.model_type)
                .order_by(self.model_type.embedding.l2_distance(embedding))
                .limit(5)
            ).all()
        return entities

    def update(self, id, **kwargs):
        with self.session() as session:
            entity = session.query(self.model_type).get(id)
            for key, value in kwargs.items():
                setattr(entity, key, value)
            session.commit()
        return entity

    def delete(self, id):
        with self.session() as session:
            entity = session.query(self.model_type).get(id)
            session.delete(entity)
            session.commit()
        return entity

    def delete_all(self):
        with self.session() as session:
            session.query(self.model_type).delete()
            session.commit()
        return True
