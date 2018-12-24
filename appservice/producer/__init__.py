"""
    Module with main configs of project consumer
"""
from sanic import Sanic
from .config import Config

APP = Sanic()
APP.config.from_object(Config)


from .routers import (producer_send)
