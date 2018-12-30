"""
Zookeeper manager module
"""
from api.logger_conf import make_logger
from api.config import Configs

import aiozk

LOGGER = make_logger('logs/database_logs', 'database_logs')


class ZookeeperDatabaseManager:
    """
    Class that manage data in zookeeper
    """
    _connection = None

    @classmethod
    async def connect(cls, path):
        """
        Method connects to zookeeper
        :param path:
        :return:
        """
        cls._connection = aiozk.ZKClient(f"{Configs['ZOOKEEPER_HOST']}:{Configs['ZOOKEEPER_PORT']}")
        await cls._connection.start()
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
        await cls._connection.set_data('offset', data.encode('utf-8'))

    @classmethod
    async def get(cls, path):
        """
        Method gets data from zk
        :param path:
        :return: result
        """
        result = await cls._connection.get_data('offset')
        return result
