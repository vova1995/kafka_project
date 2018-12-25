"""
    Module for databases actions
"""
import logging
from datetime import datetime

from api.app import SESSION, CASSANDRA_SESSION, KEY_SPACE, REDIS, ZK
from api.models import Messages, Message


class PostgresDatabaseManager:
    """
    Class that manage data in postgres
    """

    @classmethod
    def create(cls):
        Messages.create_db()

    @classmethod
    def insert(cls, topic, message):
        session = SESSION()
        msg = Messages(topic, message)
        session.add(msg)
        session.commit()
        session.close()


class CassandraDatabaseManager:
    """
    Class that manage data in cassandra
    """
    @classmethod
    def create_keyspace(cls):
        log = logging.getLogger()
        log.setLevel('DEBUG')
        session = CASSANDRA_SESSION
        log.info("creating keyspace...")
        session.execute("""
                        CREATE KEYSPACE IF NOT EXISTS %s
                        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                        """ % KEY_SPACE)

    @classmethod
    def create(cls):
        session = CASSANDRA_SESSION
        log = logging.getLogger()
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

    @classmethod
    def insert(cls, id, topic, message):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        session.execute("INSERT INTO messages (id, topic, message) VALUES (%s, %s, %s)", (id, topic, message))

    @classmethod
    def select_count(cls):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        res = session.execute("SELECT COUNT(*) FROM messages")
        return res


class CassandraDatabaseManager2:
    """
    Class that manages data in cassandra2
    """

    @classmethod
    def create(cls):
        Message.create_db()

    @classmethod
    def insert(cls, topic, message):
        msg = Message.create(topic=topic, created_at=datetime.now(), message=message)

    @classmethod
    def get_count(cls):
        return Message.objects.count()


class RedisDatabaseManager:
    """
    Class that manage data in redis
    """
    @classmethod
    def redisget(cls):
        result = REDIS.get('kafka')
        return result

    @classmethod
    def redisset(cls, offset):
        REDIS.set('kafka', offset)


class ZookeeperDatabaseManager:
    """
    Class that manage data in zookeeper
    """
    @classmethod
    def setdata(cls, data):
        ZK.ensure_path("/my/offset")
        ZK.set("/my/offset", str(data).encode('utf-8'))