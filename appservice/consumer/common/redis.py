"""
Module taht manages redis
"""
import asyncio
import aioredis

from api.config import Configs
from api.app import LOGGER


class RedisDatabaseManager:
    """
    Class that manage data in redis
    """
    _connection = None

    @classmethod
    async def connect(cls):
        """
        Method connects to redis
        :return:
        """
        while True:
            try:
                cls._connection = await aioredis.create_redis(f"redis://{Configs['REDIS_HOST']}:"
                                                              f"{Configs['REDIS_PORT']}",
                                                              loop=asyncio.get_event_loop())
                break
            except Exception as e:
                LOGGER.error('Issue with redis connection %s and try reconnect every 3 sec ', e)
                await asyncio.sleep(3)

    @classmethod
    async def close(cls):
        """
        Method closes connection with redis
        :return:
        """
        cls._connection.close()
        await cls._connection.wait_closed()

    @classmethod
    async def get(cls, key):
        """
        Method gets data from redis
        :param key:
        :return: offset
        """
        return await cls._connection.get(key)

    @classmethod
    async def set(cls, key, offset):
        """
        Method sets data into redis
        :param key:
        :param offset:
        :return:
        """
        await cls._connection.set(key, offset)
