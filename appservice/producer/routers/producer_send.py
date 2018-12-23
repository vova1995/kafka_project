from kafka import KafkaProducer
from producer.helper import getdata
from producer import APP
from sanic.response import json
import json as j
import logging
import asyncio

logging.basicConfig(filename='producer_logs.txt' ,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@APP.route("/producer", methods=['POST'])
async def producer(request):
    data = request.json
    logging.info(data)
    topic = data['topic']
    key = data['key']
    value = data['value']
    while True:
        try:
            producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                 value_serializer=lambda m: j.dumps(m).encode('utf-8'))
            break
        except Exception as e:
            logging.info(e)
            await asyncio.sleep(10)
    for _ in range(6):
        future = producer.send(topic=topic, value={key: value})
        getdata(future)

    return json({"received": True, "message": request.json})
