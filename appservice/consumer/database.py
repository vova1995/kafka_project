"""
    Module for databases actions
"""
from .models import Messages, Message
from consumer import SESSION, CASSANDRA_SESSION, KEY_SPACE, REDIS, ZK
import logging
from datetime import datetime



class CreateTable:
    """
    Class that creates postgres model
    """
    def __init__(self):
        Messages.create_db()


class CreateCassandraTable:
    """
    Class that creates cassandra keyspace and table
    """
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
                id text,
                topic text,
                message text,
                PRIMARY KEY (id)
            )
            """)


class CreateTableCassandra2:
    """
    Class that creates cassandra table from model
    """
    def __init__(self):
        Message.create_db()


class PostgresDatabaseManager:
    """
    Class that manage data in postgres
    """
    @classmethod
    def session_commit(cls, data):
        session = SESSION()
        session.add(data)
        session.commit()
        session.close()


class CassandraDatabaseManager:
    """
    Class that manage data in cassandra
    """
    @classmethod
    def cassandra_query_insert(cls, id, topic, message):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        session.execute("INSERT INTO messages (id, topic, message) VALUES (%s, %s, %s)", (id, topic, message))

    @classmethod
    def cassandra_query_select(cls):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        res = session.execute("SELECT COUNT(*) FROM messages")
        return res


class RedisDatabaseManager:
    """
    Class that manage data in redis
    """
    @classmethod
    def redisset(cls, offset):
        REDIS.set('kafka', offset)


class CassandraDatabaseManager2:
    """
    Class that manage data in cassandra2
    """
    @classmethod
    def insert_data(cls, topic, message):
        msg = Message.create(topic=topic, created_at=datetime.now(), message=message)

    @classmethod
    def get_count(cls):
        return Message.objects.count()


class ZookeeperDatabaseManager:
    """
    Class that manage data in zookeeper
    """
    @classmethod
    def setdata(cls, data):
        ZK.ensure_path("/my/offset")
        ZK.set("/my/offset", str(data).encode('utf-8'))