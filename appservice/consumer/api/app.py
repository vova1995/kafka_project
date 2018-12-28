"""
    Module with main configs of project consumer
"""
from cassandra.cluster import Cluster
from sanic import Sanic
from .logger_conf import make_logger
import logging
from .config import Configs

APP = Sanic()

CLUSTER = Cluster([Configs['CASSANDRA_HOST']])

KEY_SPACE = 'messages'


CASSANDRA_SESSION = CLUSTER.connect()


from .routers import (consumer_get)


from api.database import PostgresDatabaseManager, CassandraDatabaseManager, RedisDatabaseManager,ZookeeperDatabaseManager

LOGGER = make_logger('logs/app_logs')


@APP.listener('before_server_start')
async def setup(app, loop):
    try:
        await PostgresDatabaseManager.create()
    except Exception as e:
        logging.critical(e)
        pass
    CassandraDatabaseManager.create_keyspace()
    CassandraDatabaseManager.create()
    await RedisDatabaseManager.connect()
    await ZookeeperDatabaseManager.connect()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from api.services import Consumer
    logging.critical('Server successfully started!')
    consumer = Consumer()
    await consumer.listener()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    await RedisDatabaseManager.close()
    await ZookeeperDatabaseManager.close()
