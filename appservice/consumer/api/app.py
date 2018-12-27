"""
    Module with main configs of project consumer
"""
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from kazoo.client import KazooClient
from sanic import Sanic
from .config import Config, CONSUMER_LOG_FILE_PATH
from .logger_conf import make_logger
import redis
import logging

APP = Sanic()
APP.config.from_object(Config)

REDIS = redis.Redis(host=APP.config['REDIS_URL'], port=APP.config['REDIS_PORT'], db=0)

CLUSTER = Cluster(["cassandra"])

KEY_SPACE = 'messages'


CASSANDRA_SESSION = CLUSTER.connect()
ZK = KazooClient(hosts="zookeeper:2181")
connection.setup(['cassandra'], KEY_SPACE, protocol_version=3)

LOGGER = make_logger(CONSUMER_LOG_FILE_PATH)

from .routers import (consumer_get)


from api.database import PostgresDatabaseManager, CassandraDatabaseManager


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


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from api.services import Consumer
    logging.critical('Server successfully started!')
    consumer = Consumer()
    await consumer.listener()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    ZK.stop()
