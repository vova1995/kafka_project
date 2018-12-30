"""
    Module with main configs of project consumer
"""
import time

from cassandra.cluster import Cluster
from sanic import Sanic
from .logger_conf import make_logger
from .config import Configs

APP = Sanic()

CLUSTER = Cluster([Configs['CASSANDRA_HOST']])

KEY_SPACE = 'messages'

while True:
    time.sleep(25)
    CASSANDRA_SESSION = CLUSTER.connect()
    break



from .routers import consumer_get


from common.database import PostgresDatabaseManager, CassandraDatabaseManager
from common.zookeeper import ZookeeperDatabaseManager
from common.redis import RedisDatabaseManager

LOGGER = make_logger('logs/app_logs', 'app_logs')


@APP.listener('before_server_start')
async def setup(app, loop):
    """
    Sanic before server start listener
    :param app:
    :param loop:
    :return:
    """
    try:
        await PostgresDatabaseManager.create()
    except Exception as e:
        LOGGER.info(e)
    CassandraDatabaseManager.create_keyspace()
    await CassandraDatabaseManager.create()
    await RedisDatabaseManager.connect()
    await ZookeeperDatabaseManager.connect('/offset')


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
