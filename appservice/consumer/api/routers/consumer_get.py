"""
    Module for consumer routers
"""
from sanic import response
from api.app import APP
from api.database import CassandraDatabaseManager, RedisDatabaseManager, PostgresDatabaseManager, ZookeeperDatabaseManager
from api.logger_conf import make_logger


LOGGER = make_logger('logs/consumer_get')


@APP.route("/consumer_redis_offset", methods=['GET'])
async def redis_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    offset = await RedisDatabaseManager.redisget()
    LOGGER.info(offset)
    return response.json({
        'offset': offset
    })

@APP.route("/consumer_zk_offset", methods=['GET'])
async def zk_offset(request):
    """
    Method that gets current offset from zookeeper
    :param request:
    :return: offset
    """
    offset = await ZookeeperDatabaseManager.getdata()
    LOGGER.info(offset)
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_postgres_rows", methods=['GET'])
async def postgres_count(request):
    """
    Method that counts rows from postgres
    :param request:
    :return:
    """
    rows = await PostgresDatabaseManager.select_count()
    LOGGER.info(rows)
    return response.json({
        'rows': rows
    })


@APP.route("/consumer_cassandra_rows", methods=['GET'])
async def cassandra_count(request):
    """
    Method that counts rows from cassandra 1 implementation
    :param request:
    :return:
    """
    rows = await CassandraDatabaseManager.select_count()
    LOGGER.info(rows)
    return response.json({
        'rows': rows
    })
