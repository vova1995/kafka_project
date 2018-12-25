"""
    Module with main configs of project consumer
"""
from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
from .config import Config
from cassandra.cluster import Cluster
from kazoo.client import KazooClient
from cassandra.cqlengine import connection
import logging
from logger_conf import make_logger
from config import CONSUMER_LOG_FILE_PATH


APP = Sanic()
APP.config.from_object(Config)

ENGINE = create_engine("postgresql://appservice:appservice@postgres:5432/appservice")
SESSION = sessionmaker(bind=ENGINE)

REDIS = redis.Redis(host=APP.config['REDIS_URL'], port=APP.config['REDIS_PORT'], db=0)

CLUSTER = Cluster(["cassandra"])

KEY_SPACE = 'messages'


CASSANDRA_SESSION = CLUSTER.connect()
ZK = KazooClient(hosts="zookeeper:2181")
connection.setup(['cassandra'], KEY_SPACE, protocol_version=3)

LOGGER = make_logger(CONSUMER_LOG_FILE_PATH)


from .routers import (consumer_get)

from consumer.database import CreateTable, CreateCassandraTable, CreateTableCassandra2


@APP.listener('before_server_start')
async def setup(app, loop):
    CreateTable()
    CreateCassandraTable()
    CreateTableCassandra2()
    ZK.start()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from consumer.services import Consumer
    print('Server successfully started!')
    consumer = Consumer()
    await consumer.listener()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    ZK.stop()
