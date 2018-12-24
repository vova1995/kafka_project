"""
    Module for consumer routers
"""
from consumer import REDIS, APP, SESSION, ZK
from sanic import response
from consumer.models import Messages
from sqlalchemy import func
from consumer.database import CassandraDatabaseManager, CassandraDatabaseManager2
import logging

logging.basicConfig(filename='consumer_logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



@APP.route("/consumer", methods=['GET'])
async def consumer_get_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    offset = REDIS.get('kafka')
    logging.info(offset)
    return response.json({
        'offset': offset
    })

@APP.route("/consumer_offset", methods=['GET'])
async def consumer_get_offset(request):
    """
    Method that gets current offset from zookeeper
    :param request:
    :return: offset
    """
    ZK.start()
    offset, stat = ZK.get("my/offset")
    logging.info(offset)
    ZK.stop()
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_rows", methods=['GET'])
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


@APP.route("/consumer_rows_cassandra", methods=['GET'])
async def consumer_count(request):
    """
    Method that counts rows from cassandra 1 implementation
    :param request:
    :return:
    """
    rows = CassandraDatabaseManager.cassandra_query_select()
    logging.info(rows)
    return response.json({
        'rows': rows
    })

@APP.route("/consumer_rows_cassandra2", methods=['GET'])
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
