from .models import Messages
from consumer import SESSION, CASSANDRA_SESSION, KEY_SPACE
import logging


class CreateTable:
    def __init__(self):
        Messages.create_db()


class CreateCassandraTable:
    def __init__(self):
        log = logging.getLogger()
        log.setLevel('DEBUG')
        session = CASSANDRA_SESSION
        log.info("creating keyspace...")
        session.execute("""
                CREATE KEYSPACE IF NOT EXISTS %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % KEY_SPACE)
        log.info("setting keyspace...")
        session.set_keyspace(KEY_SPACE)
        log.info("creating table...")
        session.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                thekey text,
                col1 text,
                col2 text,
                PRIMARY KEY (thekey, col1)
            )
            """)


class DatabaseManager:
    @classmethod
    def session_commit(cls, data):
        session = SESSION()
        session.add(data)
        session.commit()
        session.close()
