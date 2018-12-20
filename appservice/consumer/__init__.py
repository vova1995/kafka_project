from sanic import Sanic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis
from .config import Config
from cassandra.cluster import Cluster




APP = Sanic()
APP.config.from_object(Config)

ENGINE = create_engine("postgresql://appservice:appservice@localhost:5432/appservice")
SESSION = sessionmaker(bind=ENGINE)

REDIS = redis.Redis(host=APP.config['REDIS_URL'], port=APP.config['REDIS_PORT'], db=0)

CLUSTER = Cluster(["localhost"])

KEY_SPACE = 'messages'
CASSANDRA_SESSION = CLUSTER.connect()

from .routers import (consumer_get)
