from aiokafka import AIOKafkaProducer
from api.app import APP
from sanic.response import json
from api.logger_conf import make_logger
from api.config import Configs
import json as j
import asyncio

LOGGER = make_logger('logs/producer_logs', 'producer_logs')


@APP.route("/producer", methods=['POST'])
async def producer(request):
    """
    Sanic producer that sends messages
    :param request:
    :return: json with message
    """
    data = request.json
    LOGGER.info(data)

    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=['kafka:9092'], loop=asyncio.get_event_loop(),
                                        value_serializer=lambda m: j.dumps(m).encode('utf-8'))
            break
        except Exception as e:
            LOGGER.info(e)
            await asyncio.sleep(10)
    try:
        await producer.start()
        await producer.send_and_wait(topic=data['topic'], value={data['key']: data['value']})
    except Exception as e:
        LOGGER.error("Producer send error" ,e)
    finally:
        await producer.stop()
    return json({"received": True, "message": request.json})
