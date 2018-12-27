"""
    Module with main configs of project consumer
"""
from cassandra.cluster import Cluster
from kazoo.client import KazooClient
from sanic import Sanic
from .config import Config, CONSUMER_LOG_FILE_PATH
from .logger_conf import make_logger
import logging

APP = Sanic()
APP.config.from_object(Config)

CLUSTER = Cluster(["cassandra"])

KEY_SPACE = 'messages'


CASSANDRA_SESSION = CLUSTER.connect()
ZK = KazooClient(hosts="zookeeper:2181")

LOGGER = make_logger(CONSUMER_LOG_FILE_PATH)

from .routers import (consumer_get)


from api.database import PostgresDatabaseManager, CassandraDatabaseManager, RedisDatabaseManager


@APP.listener('before_server_start')
async def setup(app, loop):
    try:
        await PostgresDatabaseManager.create()
    except Exception as e:
        logging.critical(e)
        pass
    CassandraDatabaseManager.create_keyspace()
    CassandraDatabaseManager.create()
    ZK.start()
    await RedisDatabaseManager.connect()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from api.services import Consumer
    logging.critical('Server successfully started!')
    consumer = Consumer()
    await consumer.listener()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    ZK.stop()
    RedisDatabaseManager.close()
