from sqlalchemy import Column, String, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from consumer import ENGINE


Base = declarative_base()

class Messages(Base):
    """
    Table Messages
    """
    __tablename__ = 'messages'

    id = Column('id', INTEGER, primary_key=True, autoincrement=True)
    topic = Column('topic', String, nullable=False, unique=False)
    message = Column('message', String, nullable=False, unique=False)

    def __init__(self, topic, message):
        self.topic = topic
        self.message = message

    @classmethod
    def create_db(cls):
        Base.metadata.create_all(bind=ENGINE)
