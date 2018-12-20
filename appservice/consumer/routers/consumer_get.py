from consumer import REDIS, APP, SESSION
from sanic import response
from consumer.models import Messages
from sqlalchemy import func
from consumer.database import DatabaseManager


@APP.route("/consumer", methods=['GET'])
async def consumer_get_offset(request):
    """
    Method that gets current offset from redis
    :param request:
    :return: offset
    """
    offset = REDIS.get('kafka')
    return response.json({
        'offset': offset
    })


@APP.route("/consumer_rows", methods=['GET'])
async def consumer_count(request):
    """

    :param request:
    :return:
    """
    session = SESSION()

    result = session.query(func.count(Messages.id)).scalar()
    return response.json({
        'rows': result
    })


@APP.route("/consumer_rows_cassandra", methods=['GET'])
async def consumer_count(request):
    """

    :param request:
    :return:
    """
    rows = DatabaseManager.cassandra_query_select()

    return response.json({
        'rows': rows
    })
