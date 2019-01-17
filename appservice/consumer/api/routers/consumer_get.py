"""
    Module for consumer routers
"""
from sanic import response
from api.app import APP, LOGGER
from api.config import Configs


@APP.route("/consumer_offset", methods=['GET'])
async def get_offset(request):
    """
    Method that gets current offset from redis or zookeeper
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
    Method that counts rows from postgres or cassandra
    :param request:
    :return: rows
    """

    from common.database import database
    rows = await database.select_count()
    LOGGER.info(rows)
    return response.json({
        'rows': rows
    })
