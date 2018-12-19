from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from sanic import Sanic

import redis
from .config import Config


app = Sanic()
APP = Flask(__name__)
APP.config.from_object(Config)

DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB, directory=APP.config['MIGRATION_DIR'])
MANAGER = Manager(APP)
MANAGER.add_command('DB', MigrateCommand)

REDIS = redis.Redis(host=APP.config['REDIS_URL'], port=APP.config['REDIS_PORT'], db=0)



from .routers import (consumer_get)
