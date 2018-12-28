from api.config import Configs
from api.logger_conf import make_logger
import aioredis
import asyncio

LOGGER = make_logger('logs/database_logs')


class RedisDatabaseManager:
    """
    Class that manage data in redis
    """
    _connection = None

    @classmethod
    async def connect(cls):
        cls._connection = await aioredis.create_redis(f"redis://{Configs['REDIS_HOST']}:{Configs['REDIS_PORT']}",
                                                      loop=asyncio.get_event_loop())

    @classmethod
    async def close(cls):
        cls._connection.close()
        await cls._connection.wait_closed()

    @classmethod
    async def redisget(cls, key):
        result = await cls._connection.get(key)
        return result

    @classmethod
    async def redisset(cls, key, offset):
        await cls._connection.set(key, offset)