"""
    Module with main configs of project consumer
"""
from sanic import Sanic

APP = Sanic()


from .routers import (producer_send)
