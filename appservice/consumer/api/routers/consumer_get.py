"""
    Module for consumer routers
"""
from sanic import response
from api.app import APP
from common.database import CassandraDatabaseManager, PostgresDatabaseManager
from common.redis import RedisDatabaseManager
from common.zookeeper import ZookeeperDatabaseManager
from api.logger_conf import make_logger
from api.config import Configs


LOGGER = make_logger('logs/consumer_get', 'consumer_get')


@APP.route("/consumer_offset", methods=['GET'])
async def redis_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    if Configs['OFFSET_STORAGE'] == 'REDIS':
        offset = await RedisDatabaseManager.get('kafka')
    elif Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
        offset = await ZookeeperDatabaseManager.get('/offset')
    LOGGER.info(offset)
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_rows", methods=['GET'])
async def postgres_count(request):
    """
    Method that counts rows from postgres
    :param request:
    :return:
    """
    if Configs['DATA_STORAGE'] == 'POSTGRES':
        rows = await PostgresDatabaseManager.select_count()
    elif Configs['DATA_STORAGE'] == 'CASSANDRA':
        rows = await CassandraDatabaseManager.select_count()
    LOGGER.info(rows)
    return response.json({
        'rows': rows
    })
