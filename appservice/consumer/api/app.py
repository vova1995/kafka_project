"""
    Module with main configs of project consumer
"""
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from kazoo.client import KazooClient
from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import redis
from .config import Config

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

from .routers import (consumer_get)


from api.database import PostgresDatabaseManager, CassandraDatabaseManager, CassandraDatabaseManager2


@APP.listener('before_server_start')
async def setup(app, loop):
    PostgresDatabaseManager.create()
    CassandraDatabaseManager.create_keyspace()
    CassandraDatabaseManager.create()
    CassandraDatabaseManager2.create()
    ZK.start()


@APP.listener('after_server_start')
async def notify_server_started(app, loop):
    from api.services import Consumer
    print('Server successfully started!')
    consumer = Consumer()
    await consumer.listener()


@APP.listener('after_server_stop')
async def close_db(app, loop):
    ZK.stop()
