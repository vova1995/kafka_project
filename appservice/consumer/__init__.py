from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
from .config import Config
from cassandra.cluster import Cluster
from kazoo.client import KazooClient
from cassandra.cqlengine import connection





APP = Sanic()
APP.config.from_object(Config)

ENGINE = create_engine("postgresql://appservice:appservice@postgres:5432/appservice")
SESSION = sessionmaker(bind=ENGINE)

REDIS = redis.Redis(host=APP.config['REDIS_URL'], port=APP.config['REDIS_PORT'], db=0)

CLUSTER = Cluster(["cassandra"])

KEY_SPACE = 'messages'
# while True:
#     try:
#         CASSANDRA_SESSION = CLUSTER.connect()
#         break
#     except Exception as e:
#         print(e)
#         time.sleep(10)

CASSANDRA_SESSION = CLUSTER.connect()
ZK = KazooClient(hosts="zookeeper:2181")
connection.setup(['cassandra'], KEY_SPACE, protocol_version=3)

from .routers import (consumer_get)
