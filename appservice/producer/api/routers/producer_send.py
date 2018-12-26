from aiokafka import AIOKafkaProducer
from api.app import APP
from sanic.response import json
import json as j
import asyncio
import logging


logging.basicConfig(filename='producer_logs.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@APP.route("/producer", methods=['POST'])
async def producer(request):
    """
    Sanic producer that sends messages
    :param request:
    :return: json with message
    """
    data = request.json
    logging.info(data)
    topic = data['topic']
    key = data['key']
    value = data['value']

    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=['kafka:9092'], loop=APP.loop,
                                        value_serializer=lambda m: j.dumps(m).encode('utf-8'))
            break
        except Exception as e:
            logging.info(e)
            await asyncio.sleep(10)
    await producer.start()
    try:
        await producer.send_and_wait(topic=topic, value={key: value})
    finally:
        await producer.stop()
    return json({"received": True, "message": request.json})
