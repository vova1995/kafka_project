"""
Zookeeper manager module
"""
from api.app import LOGGER
from api.config import Configs

import aiozk


class ZookeeperDatabaseManager:
    """
    Class that manage data in zookeeper
    """
    _connection = None

    @classmethod
    async def connect(cls):
        """
        Method connects to zookeeper
        :param path:
        :return:
        """
        LOGGER.info(f'Create connection with zookeeper host %s and port %s', Configs['ZOOKEEPER_HOST'], Configs['ZOOKEEPER_PORT'])
        cls._connection = aiozk.ZKClient(f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}")
        await cls._connection.start()

    @classmethod
    async def ensure_or_create(cls, path):
        try:
            await cls._connection.ensure_path(path)
        except Exception as e:
            LOGGER.error('Ensure path for ZK', e)
            await cls._connection.create(path, data=b'null', ephemeral=True)

    @classmethod
    async def close(cls):
        """
        Method closes connection with zk
        :return:
        """
        await cls._connection.close()

    @classmethod
    async def set(cls, path, data):
        """
        Method sets data into zookeeper
        :param path:
        :param data:
        :return:
        """
        await cls._connection.set_data(path, data.encode('utf-8'))

    @classmethod
    async def get(cls, path):
        """
        Method gets data from zk
        :param path:
        :return: offset
        """
        return await cls._connection.get_data(path)
