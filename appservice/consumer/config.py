"""
Configuration module for APP, MAIL
"""
import os

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


IS_IN_DOCKER = os.environ.get('DOCKER', False)


class Config:
    """
    Configuration class to configure APP from object
    """
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "postgresql://appservice:appservice@localhost:5432/appservice"


    MIGRATION_DIR = os.path.join(BASEDIR, 'migrations')

    REDIS_PORT = 6379

    if IS_IN_DOCKER:
        REDIS_URL = 'appserive_redis'
    else:
        REDIS_URL = 'localhost'