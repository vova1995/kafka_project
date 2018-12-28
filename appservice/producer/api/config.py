"""
Configuration module for APP, MAIL
"""
import os

BASEDIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))


import os

docker = os.environ.get('DOCKER', None)


if not docker:
    Configs = {
        'KAFKA_ADDRESS': os.environ.get('KAFKA_ADDRESS') or 'localhost',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    }
else:
    Configs = {
        'KAFKA_ADDRESS': os.environ.get('KAFKA_ADDRESS') or 'kafka',
        'KAFKA_PORT': os.environ.get('KAFKA_PORT') or 9092,
    }