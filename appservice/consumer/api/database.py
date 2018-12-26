"""
    Module for databases actions
"""
from datetime import datetime

from api.app import CASSANDRA_SESSION, KEY_SPACE, REDIS, ZK
from api.models import Messages, Message
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable
import asyncio
import logging


class PostgresDatabaseManager:
    """
    Class that manage data in postgres
    """

    @classmethod
    async def create_engine(cls):
        engine = await create_engine(user='appservice',
                                     database='appservice',
                                     host='postgres',
                                     password='appservice')
        return engine

    @classmethod
    async def create(cls):
        engine = await PostgresDatabaseManager.create_engine()
        async with engine.acquire() as conn:
            logging.critical('POSRTGTREEEDE')
            await conn.execute(CreateTable(Messages))

    @classmethod
    async def insert(cls, topic, message):
        engine = await PostgresDatabaseManager.create_engine()
        async with engine.acquire() as conn:
            await conn.execute(Messages.insert().values(topic, message))

    @classmethod
    async def select_count(cls):
        engine = await PostgresDatabaseManager.create_engine()
        async with engine.acquire() as conn:
            async with conn.execute(Messages.select()) as cur:
                return cur.rowcount


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
