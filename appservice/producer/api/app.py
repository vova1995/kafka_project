"""
    Module with main configs of project consumer
"""
from sanic import Sanic
from .logger_conf import make_logger
from .config import PRODUCER_LOG_FILE_PATH

APP = Sanic()

LOGGER = make_logger(PRODUCER_LOG_FILE_PATH, 'producer_logger')

from .routers import (producer_send)
