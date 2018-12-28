"""
    Module for databases actions
"""
from api.app import CASSANDRA_SESSION, KEY_SPACE
from api.models import Messages
from aiopg.sa import create_engine
from sqlalchemy.sql.ddl import CreateTable
from api.logger_conf import make_logger
from api.config import Configs
import uuid


LOGGER = make_logger('logs/database_logs', 'database_logs')


class PostgresDatabaseManager:
    """
    Class that manage data in postgres
    """

    @classmethod
    async def create_engine(cls):
        engine = await create_engine(user=Configs['POSTGRES_USER'],
                                     database=Configs['POSTGRES_DATABASE'],
                                     host=Configs['POSTGRES_ADDRESS'],
                                     password=Configs['POSTGRES_PASSWORD'])
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

    _session = CASSANDRA_SESSION

    @classmethod
    def create_keyspace(cls):
        LOGGER.info("creating keyspace...")
        cls._session.execute("""
                        CREATE KEYSPACE IF NOT EXISTS %s
                        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                        """ % KEY_SPACE)

    @classmethod
    async def create(cls):
        LOGGER.info("setting keyspace...")
        cls._session.set_keyspace(KEY_SPACE)
        LOGGER.info("creating table...")
        try:
            cls._session.execute_async("""
                            CREATE TABLE IF NOT EXISTS messages (
                                id UUID,
                                topic text,
                                message text,
                            PRIMARY KEY (id)
                          )
                            """)
        except Exception as e:
            LOGGER.error(e)

    @classmethod
    async def insert(cls, id, topic, message):
        cls._session.set_keyspace(KEY_SPACE)
        try:
            cls._session.execute_async("INSERT INTO messages (id, topic, message) VALUES (%s, %s, %s)",
                                       (id, topic, message)).result()
        except Exception as e:
            LOGGER.error(e)

    @classmethod
    async def select_count(cls):
        cls._session.set_keyspace(KEY_SPACE)
        res = cls._session.execute_async("SELECT COUNT(*) FROM messages").result()
        return res
