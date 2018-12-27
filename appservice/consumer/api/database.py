"""
    Module for databases actions
"""
from datetime import datetime

from api.app import CASSANDRA_SESSION, KEY_SPACE
from api.models import Messages
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable
from .logger_conf import make_logger
import asyncio
import aioredis
import aiozk
import logging

LOGGER = make_logger('logs/database_logs')


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
        LOGGER.info("creating keyspace...")
        session.execute("""
                        CREATE KEYSPACE IF NOT EXISTS %s
                        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                        """ % KEY_SPACE)

    @classmethod
    def create(cls):
        session = CASSANDRA_SESSION
        LOGGER.info("setting keyspace...")
        session.set_keyspace(KEY_SPACE)
        LOGGER.info("creating table...")
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
            LOGGER.error(e)

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
    connection = None

    @classmethod
    async def connect(cls):
        ZookeeperDatabaseManager.connection = aiozk.ZKClient('zookeeper:2181')
        await ZookeeperDatabaseManager.connection.start()
        try:
            await ZookeeperDatabaseManager.connection.ensure_path('/offset')
        except Exception as e:
            LOGGER.error('Ensure path for ZK', e)
            await ZookeeperDatabaseManager.connection.create('/offset', data=b'null', ephemeral=True)

    @classmethod
    async def close(cls):
        await RedisDatabaseManager.connection.close()

    @classmethod
    async def setdata(cls, data):
        await ZookeeperDatabaseManager.connection.set_data('offset', data.encode('utf-8'))

    @classmethod
    async def getdata(cls):
        result = await ZookeeperDatabaseManager.connection.get_data('offset')
        return result
