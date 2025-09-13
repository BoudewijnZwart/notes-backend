import factory
from sqlalchemy import orm

from tests.test_config import engine

Session = orm.scoped_session(orm.sessionmaker())
Session.configure(bind=engine)


class ModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Base factory for SQLAlchemy models."""

    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_session = Session
