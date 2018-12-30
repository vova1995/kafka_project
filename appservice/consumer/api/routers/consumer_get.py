"""
    Module for consumer routers
"""
from sanic import response
from api.app import APP
from api.app import LOGGER
from api.config import Configs


@APP.route("/consumer_offset", methods=['GET'])
async def get_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    if Configs['OFFSET_STORAGE'] == 'REDIS':
        from common.redis import RedisDatabaseManager

        offset = await RedisDatabaseManager.get('kafka')
    else:
        from common.zookeeper import ZookeeperDatabaseManager

        offset = await ZookeeperDatabaseManager.get('/offset')
    LOGGER.info('Current offset: %s', offset)
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_rows", methods=['GET'])
async def rows_count(request):
    """
    Method that counts rows from postgres
    :param request:
    :return:
    """
    if Configs['DATA_STORAGE'] == 'POSTGRES':
        from common.database import PostgresDatabaseManager
        rows = await PostgresDatabaseManager.select_count()
    else:
        from common.database import CassandraDatabaseManager
        rows = await CassandraDatabaseManager.select_count()
    LOGGER.info(rows)
    return response.json({
        'rows': rows
    })
