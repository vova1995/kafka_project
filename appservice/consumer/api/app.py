"""
    Module with main configs of project consumer
"""
import time

from cassandra.cluster import Cluster
from sanic import Sanic
from .logger_conf import make_logger
from .config import Configs, CONSUMER_LOG_FILE_PATH

APP = Sanic()

CLUSTER = Cluster([Configs['CASSANDRA_HOST']])

KEY_SPACE = 'messages'

LOGGER = make_logger(CONSUMER_LOG_FILE_PATH, 'consumer_logger')


while True:
    time.sleep(25)
    CASSANDRA_SESSION = CLUSTER.connect()
    break



from .routers import consumer_get


from common.database import PostgresDatabaseManager, CassandraDatabaseManager
from common.zookeeper import ZookeeperDatabaseManager
from common.redis import RedisDatabaseManager


@APP.listener('before_server_start')
async def setup(app, loop):
    """
    Sanic before server start listener
    :param app:
    :param loop:
    :return:
    """
    LOGGER.info(Configs['DATA_STORAGE'])
    LOGGER.info(Configs['OFFSET_STORAGE'])
    LOGGER.info(Configs['OFFSET_STORAGE'] == 'REDIS')
    try:
        if Configs['DATA_STORAGE'] == 'POSTGRES':
            await PostgresDatabaseManager.create()
        if Configs['DATA_STORAGE'] == 'CASSANDRA':
            CassandraDatabaseManager.create_keyspace()
            await CassandraDatabaseManager.create()
    except Exception as e:
        LOGGER.error('Databases sql error %s', e)
    try:
        if Configs['OFFSET_STORAGE'] == 'REDIS':
            await RedisDatabaseManager.connect()
        if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
            await ZookeeperDatabaseManager.connect('/offset')
    except Exception as e:
        LOGGER.error('Databases no sql error %s', e)


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    """
    Sanic after server start listener
    :param app:
    :param loop:
    :return:
    """
    from api.services import Consumer
    await Consumer.listen()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    """
    Sanic after server stop listener
    :param app:
    :param loop:
    :return:
    """
    await RedisDatabaseManager.close()
    await ZookeeperDatabaseManager.close()
