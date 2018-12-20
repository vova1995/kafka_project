from consumer import REDIS, APP
from sanic import response

@APP.route("/consumer", methods=['GET'])
def consumer_get_offset(request):
    offset = REDIS.get('kafka')
    return response.json({
        'offset': offset
    })
