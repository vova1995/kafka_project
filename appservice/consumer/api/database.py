"""
    Module for databases actions
"""
from datetime import datetime

from api.app import CASSANDRA_SESSION, KEY_SPACE, ZK
from api.models import Messages
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable
import asyncio
import aioredis
import logging

log = logging.getLogger()
log.setLevel('DEBUG')


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
            await conn.execute(Messages.insert().values(topic=topic, message=message))

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
    async def insert(cls, id, topic, message):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        try:
            session.execute_async("INSERT INTO messages (id, topic, message) VALUES (%s, %s, %s)", (id, topic, message)).result()
        except Exception as e:
            log.error(e)

    @classmethod
    async def select_count(cls):
        session = CASSANDRA_SESSION
        session.set_keyspace(KEY_SPACE)
        res = session.execute_async("SELECT COUNT(*) FROM messages").result()
        return res


class RedisDatabaseManager:
    """
    Class that manage data in redis
    """
    connection = None

    @classmethod
    async def connect(cls):
        RedisDatabaseManager.connection = await aioredis.create_redis('redis://redis:6379', loop=asyncio.get_event_loop())

    @classmethod
    async def close(cls):
        RedisDatabaseManager.connection.close()
        await RedisDatabaseManager.connection.wait_closed()

    @classmethod
    async def redisget(cls):
        result = await RedisDatabaseManager.connection.get('kafka')
        return result

    @classmethod
    async def redisset(cls, offset):
        await RedisDatabaseManager.connection.set('kafka', offset)


class ZookeeperDatabaseManager:
    """
    Class that manage data in zookeeper
    """

    @classmethod
    def setdata(cls, data):
        ZK.ensure_path("/my/offset")
        ZK.set("/my/offset", str(data).encode('utf-8'))
