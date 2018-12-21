from kafka import KafkaProducer
from kafka.errors import KafkaError
from producer.helper import getdata
from producer import APP
from sanic.response import json
import json as j
import logging
import asyncio


log = logging.getLogger()
log.setLevel('DEBUG')


@APP.route("/producer", methods=['POST'])
async def producer(request):
    data = request.json
    print(data)
    topic = data['topic']
    key = data['key']
    value = data['value']
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: j.dumps(m).encode('utf-8'))

    for _ in range(6):
        try:
            future = producer.send(topic=topic, value={key: value})
            getdata(future)
        except KafkaError as e:
            log.exception(e)
        await asyncio.sleep(1)


    return json({"received": True, "message": request.json})
