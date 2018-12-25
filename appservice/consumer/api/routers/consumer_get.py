"""
    Module for consumer routers
"""
from api.logger_conf import logger as logging

from sanic import response
from sqlalchemy import func

from api.app import APP, SESSION, ZK
from api.database import CassandraDatabaseManager, CassandraDatabaseManager2, RedisDatabaseManager
from api.models import Messages
import logging


logging.basicConfig(filename='consumer_logs.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@APP.route("/consumer_redis_offset", methods=['GET'])
async def consumer_get_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    offset = RedisDatabaseManager.redisget()
    logging.info(offset)
    return response.json({
        'offset': offset
    })

@APP.route("/consumer_zk_offset", methods=['GET'])
async def consumer_get_offset(request):
    """
    Method that gets current offset from zookeeper
    :param request:
    :return: offset
    """
    offset, stat = ZK.get("my/offset")
    logging.info(offset)
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_postgres_rows", methods=['GET'])
async def consumer_count(request):
    """
    Method that counts rows from postgres
    :param request:
    :return:
    """
    session = SESSION()

    result = session.query(func.count(Messages.id)).scalar()
    logging.info(result)
    return response.json({
        'rows': result
    })


@APP.route("/consumer_cassandra_rows", methods=['GET'])
async def consumer_count(request):
    """
    Method that counts rows from cassandra 1 implementation
    :param request:
    :return:
    """
    rows = CassandraDatabaseManager.select_count()
    logging.info(rows)
    return response.json({
        'rows': rows
    })

@APP.route("/consumer_cassandra2_rows", methods=['GET'])
async def consumer_count(request):
    """
    Method that counts rows from cassandra 2 implementation
    :param request:
    :return:
    """
    rows = CassandraDatabaseManager2.get_count()
    logging.info(rows)
    return response.json({
        'rows': rows
    })
