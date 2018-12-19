import json as j
from consumer.models import Message
from consumer import app, REDIS, APP
from sanic import response

@app.route("/consumer", methods=['GET'])
def consumer_get_offset(request):
    offset = REDIS.get('kafka')
    return response.json({
        'offset': offset
    })

@APP.route("/consumer_count", methods=['GET'])
def consumer_get_count():
    id_m = 1
    message = Message.query.filter(Message.id == id_m).first()
    # for _ in messages:
    #     count +=1
    return j.dumps({
        'status': 'success',
        'message': message.value
    }), 200
